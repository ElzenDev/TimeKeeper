from typing import List, Dict, Any
from database import Database


class ProcessEnricher():
    """ Responsable for Enriching current processes with more/better data"""

    def __init__(self, database: Database):
        self.database = database

    def add_running_time(self, processes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """ Add the running time from database to each process """

        today_stats = self.database.get_today_running_time()
        weekly_stats = self.database.get_week_running_time()
        monthly_stats = self.database.get_month_running_time()
        

        today_lookup = {stat['name']: stat['total_seconds'] for stat in today_stats}
        week_lookup = {stat['name']: stat['total_seconds'] for stat in weekly_stats}
        month_lookup = {stat['name'] : stat['total_seconds'] for stat in monthly_stats}

         
        print(f"Collected {len(processes)} processes from the system.")
        enriched_processes = []
        for proc in processes:
            name = proc['name']

            proc['today_running_time'] = today_lookup.get(name, 0.0)
            proc['week_running_time'] = week_lookup.get(name, 0.0)
            proc['month_running_time'] = month_lookup.get(name, 0.0)            
            enriched_processes.append(proc)
            
        return enriched_processes