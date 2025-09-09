import os
from datetime import datetime
from typing import List, Dict, Any
class ProcessRenderer:
    # Responsible for rendering processes to the terminal.
    def __init__(self):
        self.header_format = "{:<8} {:<25} {:<10} {:<15}"
        self.row_format = "{:<8} {:<25} {:<10.2} {:<15.2}"

    def clear_screen(self):
        # Clear the terminal screen
        os.system('cls' if os.name== 'nt' else 'clear')

    def render_processes(self, processes: List[Dict[str, Any]]):
        # Render the list

        self.clear_screen() # Clear Screen 

        print(f"found {len(processes)} apps running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        # Print Header
        print(self.header_format.format("PID", "Name", "User", "Usage Time"))
        print("-" * 60)

        
        for app in processes[:50]:
            # format usage time as Hours:Minutes:Seconds
            running_time_str = f"{app['running_time']//3600}h:{(app['running_time']%3600)//60}m:{app['running_time']%60}s" 
            
            # Print Rows
            print(self.row_format.format(
                app['pid'],
                app['name'],
                app['username'],
                running_time_str
            ))
    
                
            
        