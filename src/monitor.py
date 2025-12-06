import time, os, sys
import logging
from typing import Optional

# Import the classes for data injection
from process_collector import ProcessCollector
from database import Database
from process_categorizer import ProcessCategorizer
from process_enricher import ProcessEnricher
from process_filter import ProcessFilter
from process_sorter import ProcessSorter
from process_renderer import ProcessRenderer


script_dir = os.path.dirname(__file__)
log_path = os.path.join(os.path.dirname(script_dir), "docs" ,"monitor.log") 
logging.basicConfig(filename= f"{log_path}", level=logging.INFO, format='%(asctime)s - %(message)s')

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
    
    print("Starting TimeKeeper..")
    print("Press Ctrl+C to stop")

    monitor = ProcessesMonitor()
    if len(sys.argv) < 2:
        print("Usage: python process_tracker.py [track|Report|]")
        return
    
    command = sys.argv[1].lower()
    if command == "track":
        monitor.track()
        return
    elif command == "report":
        monitor.report()
    elif command != "report":
        print("Unknown command. Use 'track' to start monitoring or 'report' to print the data.")
        return
   

if __name__ == "__main__":
        main()