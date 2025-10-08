import time, os
import logging
import threading
from typing import Optional

# Import the classes for data injection
from process_collector import ProcessCollector
from database import Database
from process_categorizer import ProcessCategorizer
from process_enricher import ProcessEnricher
from process_filter import ProcessFilter
from process_sorter import ProcessSorter
from process_renderer import ProcessRenderer


class ProcessesMonitor:

    """
    Main App Monitor logic
    """

    def __init__(self, check_interval: int = 60): ## Initialize with a default check interval of a minute
        self.is_running = False
        self.check_interval = check_interval

        # Data Injection
        self.collector = ProcessCollector()
        self.categorizer = ProcessCategorizer()
        self.database = Database()
        self.enricher = ProcessEnricher(self.database)
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
            
            ##  Background Thread--------------------------
            # Get all the running Processes
            processes = self.collector.get_running_processes()
            self.categorizer.categorize(processes)
            
            #Sync Processes with the database
            self.database.sync_processes(processes)
            
            ## ----------------------------


            # Adds the today's running time for processes
            enriched_processes = self.enricher.add_running_time(processes)
            
            # Filter out Background Processes and System Processes
            filtered_processes = self.filter.filter_for_apps(enriched_processes)
            
            #Sort Processes
            sorted_processes = self.sorter.sort_by_running_time(filtered_processes,True)

            # Render the processes sorted by how long they've been running
            self.renderer.render_processes(sorted_processes)

            time.sleep(self.check_interval)
        

def main():
    print("Starting TimeKeeper..")
    print("Press Ctrl+C to stop")

    monitor = ProcessesMonitor(check_interval=30)
    monitor.start_monitoring()

if __name__ == "__main__":
        main()