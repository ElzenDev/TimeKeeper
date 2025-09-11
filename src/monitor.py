import time, os
import logging

"""
Main App Monitor logic
"""

# Import the classes
from process_collector import ProcessCollector
from process_filter import ProcessFilter
from process_sorter import ProcessSorter
from process_renderer import ProcessRenderer

class ProcessesMonitor:
    def __init__(self, check_interval: int = 60): ## Initialize with a default check interval of a minute
        self.is_running = False
        self.check_interval = check_interval

        # Data Injection
        self.collector = ProcessCollector()
        self.filter = ProcessFilter()
        self.sorter = ProcessSorter()
        self.renderer = ProcessRenderer()
        
    def start_monitoring(self):
        print("Starting system monitor...")
        try:
            self.is_running = True
            while self.is_running:

                self.monitoring_loop() ## Start Running
                
                time.sleep(self.check_interval) ## Waits for the next check interval to run again
        except KeyboardInterrupt:
            print("Monitoring interrupted by user.")
        finally:
            self.stop_monitoring()

    def stop_monitoring(self):
        self.is_running = False
        print("Stopping system monitor...")

    def monitoring_loop(self):
        while self.is_running:

            # Get all the running Processes
            processes = self.collector.get_running_processes()

            #Sync Processes with the database

            # Filter out Background Processes and System Processes
            filtered_processes = self.filter.filter_for_apps(processes)
            
            #Sort Processes
            sorted_processes = self.sorter.sort_by_running_time(filtered_processes,True)

            # Render the processes sorted by how long they've been running
            self.renderer.render_processes(sorted_processes)

            time.sleep(self.check_interval)
        

def main():
    print("ITS TIMEKEEPER TIME \n WHAT DO YOU WANT TO DO")
    order: str = input("\n [1] - Run TimeKeeper\n : ")
    if order == "1":
        print("Starting TimeKeeper..")
        print("Press Ctrl+C to stop")

        monitor = ProcessesMonitor(check_interval=30)
        monitor.start_monitoring()
    else: 
        os.system('cls' if os.name == 'nt' else 'clear')
        main()

if __name__ == "__main__":
        main()