import os
from datetime import datetime
from typing import List, Dict, Any
class ProcessRenderer:
    """Responsable for rendering processes on the terminal"""
    def __init__(self):
        self.header_format = "{:<8} | {:<15} | {:<15} | {:<15}| {:<15}| {:<15}"
        self.row_format = "{:<8} | {:<15} | {:<18} | {:<18}| {:<18}| {:<15}"

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render_processes(self, processes: List[Dict[str, Any]]):
        """
        Renders processes on a table format 
        """

        self.clear_screen()
        # Just to make sure  :) xd
        self.clear_screen()

        


        print(f"found {len(processes)} apps running  [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
        print("-" * 120)
        # Print Header
        print(self.header_format.format("PID", "Name", "TODAY_RUNNING_TIME", "WEEK_RUNNING_TIME","MONTH_RUNNING_TIME"," User"))
        print("-" * 120)

        
        for app in processes[:50]:
            # format usage time for better showcase
            
            today_running_time_str = f"{app['today_running_time']//3600}h:{(app['today_running_time']%3600)//60}m:{app['today_running_time']%60}s"
            week_running_time_str = f"{app['week_running_time']//3600}h:{(app['week_running_time']%3600)//60}m:{app['week_running_time']%60}s"
            month_running_time_str = f"{app['month_running_time']//3600}h:{(app['month_running_time']%3600)//60}m:{app['month_running_time']%60}s"


            username:str = app['username']
            name:str = app['name']
            
            if username.split('\\'):
                reduced_username = username.split('\\')[1]
            
            if name.split('.'):
                name = name.split('.')[0]
            if name.split(" - ", 1):
                name = name.split("-")[0]
            
            print(self.row_format.format(
                app['pid'],
                name,
                today_running_time_str,
                week_running_time_str,
                month_running_time_str,
                reduced_username if reduced_username else username
            ))
    
                
            
        