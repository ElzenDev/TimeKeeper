import time, os, sys, signal
import logging
from typing import Optional

import subprocess

# Import the classes for data injection
from process_collector import ProcessCollector
from database import Database
from process_categorizer import ProcessCategorizer
from process_enricher import ProcessEnricher
from process_filter import ProcessFilter
from process_sorter import ProcessSorter
from process_renderer import ProcessRenderer

from tracker_thread import TrackerThread


BASE_DIR = os.path.dirname(__file__)
VENV_PYTHON = os.path.join(sys.prefix, "Scripts", "python.exe") 
PYTHON_EXE = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable
print(f"Python exe: {PYTHON_EXE} \n Sys exe: {sys.executable}")
PID_FILE = os.path.join(BASE_DIR, "..", "data", "tracker.pid")
STOP_FLAG = os.path.join(BASE_DIR, "..", "data", "stop.flag")
LOG_FILE = os.path.join(BASE_DIR, "..", "data", "tracker.log")

LOGGING_PATH = os.path.join(os.path.dirname(BASE_DIR), "data" ,"monitor.log") 
logging.basicConfig(filename= f"{LOGGING_PATH}", level=logging.INFO, format='%(asctime)s - %(message)s')

class ProcessesMonitor:

    """
    Main App Monitor logic
    """

    def __init__(self): ## No chceck_interval
        self.is_running = False

        # Data Injection
        self.collector = ProcessCollector()
        self.categorizer = ProcessCategorizer()
        self.database = Database()
        self.enricher = ProcessEnricher(self.database)
        self.filter = ProcessFilter()
        self.sorter = ProcessSorter()
        self.renderer = ProcessRenderer()

    


    def track(self):
        
        logging.info("Track Started")
        ##  Background part--------------------------
        # Get all the running Processes
        try:
            processes = self.collector.get_running_processes()
            self.categorizer.categorize(processes)
            logging.info(f"Collected {len(processes)} processes from the system.")
            #Sync Processes with the database
            self.database.sync_processes(processes)
            logging.info("Database synced with current processes.")
        except Exception as e:
            logging.error(f"Error: {e}")    
        ## ----------------------------

    def report(self):
        # Get all the running Processes
        processes = self.collector.get_running_processes()
        self.categorizer.categorize(processes)
        print(f"Collected {len(processes)} processes from the system.")
        # Adds today's running time for processes
        enriched_processes = self.enricher.add_running_time(processes)
        
        # Filter out Background Processes and System Processes
        filtered_processes = self.filter.filter_for_apps(enriched_processes)
        
        # Sort Processes
        sorted_processes = self.sorter.sort_by_running_time(filtered_processes,True)

        # Render the processes sorted by how long they've been running
        self.renderer.render_processes(sorted_processes)


def main():

    def is_running(pid:int) -> bool:
        try:
            output = subprocess.check_output(
            ["tasklist", "/FI", f"PID eq {pid}"], text=True
            )
            return str(pid) in output
        except subprocess.CalledProcessError:
            return False
        
    def start_tracker():
        if os.path.exists(PID_FILE):
            with open(PID_FILE) as f:
                pid = int(f.read().strip())
            if is_running(pid):
                print(f"Tracker already running (PID {pid}).")
                return
            os.remove(PID_FILE)

        proc = subprocess.Popen(
            [PYTHON_EXE,"-u", __file__, "_run"],
            cwd=BASE_DIR,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=open(LOG_FILE, "a"),
            stderr=subprocess.STDOUT,
            stdin=subprocess.DEVNULL,
            close_fds=True,
        )

    def stop_tracker():
        if not os.path.exists(PID_FILE):
            print("Tracker not running")
            return
        with open(STOP_FLAG, "w") as f:
            f.write("stop")
            print("Stop signal sent. Tracker will exit within a few seconds.")

    def run_tracker_loop():
        print("Starting tracker loop, PID:", os.getpid())
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
            print(f"Tracker actually running with PID {os.getpid()}")
        
        if os.path.exists(STOP_FLAG):
            os.remove(STOP_FLAG)
        
        try:
            while True:
                if os.path.exists(STOP_FLAG):
                    print("Stop flag detected, shutting down cleanly.")
                    break
                monitor.track()
                time.sleep(2)
        finally:
            os.remove(STOP_FLAG) if os.path.exists(STOP_FLAG) else None
            os.remove(PID_FILE) if os.path.exists(PID_FILE) else None

    print("Starting TimeKeeper..")
    print("Press Ctrl+C to stop")

    monitor = ProcessesMonitor()
    if len(sys.argv) < 2:
        print("Usage: python monitor.py [Start|Stop|Report")
        return
    
    command = sys.argv[1].lower()
    if command == "start":
        start_tracker()
    elif command == "stop":
        stop_tracker()
    elif command == "_run":
        run_tracker_loop()
    elif command == "report":
        monitor.report()
    elif command != "report":
        print("Unknown command. Use 'Start' to start monitoring, 'Stop' to stop monitoring or 'report' to print the data.")
        return
   

if __name__ == "__main__":
        main()