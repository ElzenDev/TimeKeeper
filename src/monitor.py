import psutil, time, os
from datetime import datetime
import logging

"""
Main App Monitor logic
"""

class AppMonitor:
    def __init__(self, check_interval: int = 60): ## Initialize with a default check interval of a minute
        self.is_running = False
        self.check_interval = check_interval
        
   
    ## Get a list of all the machines active processes
    def get_running_apps(self):
        
        apps = []
        for process in psutil.process_iter(['pid', 'username', 'name', 'create_time', 'exe', 'status']):
            try:  
                # Filter user apps
                if self.app_filter(process): 
                    apps.append({
                        'pid': process.info['pid'],
                        'name': process.info['name'],
                        'user': process.info['username'],
                        'start_time': process.info['create_time'],
                        'usage_time': int(time.time() - process.info['create_time']), # Calculate usage time in seconds
                        'executable_path': process.info['exe'],
                        'status': process.info['status']
                    })                          
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): # Handle processes that may have ended or are inaccessible
                ...
            
        return apps
    
    def apps_sorter(self, apps:list) -> list:
        # create an annonymous function that takes x as an parameter and returns the usage time as an integer
        # Sort apps by usage time, longest first
        return apps.sort(key=lambda x: int(x.get('usage_time')), reverse=True)
    
    ## A simple function to filter out system processes
    def app_filter(self,process:dict) -> bool:
        process_name = process.info['name']
        user_name = process.info['username']
        exe = process.info['exe']
        
        
        # A list of common system processes to ignore
        system_processes = ['System', 'System Idle Process', 'Registry', 'smss.exe', 'csrss.exe', 'wininit.exe',
                      'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe',
                      'spoolsv.exe', 'taskhostw.exe', 'dwm.exe' ,'SearchUI.exe',
                       'RuntimeBroker.exe', 'sihost.exe', 'ctfmon.exe', 'conhost.exe',
                       'ApplicationFrameHost.exe0','winlogon.exe', 'fontdrvhost.exe', 'WmiPrvSE.exe', 'SecurityHealthService.exe'
                       , 'sppsvc.exe', 'audiodg.exe', 'SystemSettings.exe']
        
        
        ## Filter out system processes in the list, processes with very short names and processes running under system accounts
        if process_name in system_processes or len(process_name) <3 or 'service' in process_name.lower() or user_name in ['SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE', None]:
            return False
        
        # Filter out processes running from Windows directories
        if exe and ('Windows' in exe or 'System32' in exe or 'SysWOW64' in exe or 'EdgeWebView' in exe):
            return False
        ## Temporary files and local system files  
        if  exe and ('temp' in exe.lower() or 'local' in exe.lower()):
            return False      
        
       ## Check if the process has a parent or children processes
        process_parent = process.parent()
        process_children = process.children()
        ## We assume parent processes are apps, children are not
        if process_children:
            return True 
        if process_parent:
            return False
        
        # Filter processes that aren't in typical directories for user-installed apps
        current_user = os.getenv('USERNAME', '').lower()
        if  current_user in user_name:
            if exe and ('appdata' in exe.lower() or 'users' in exe.lower() or 'Program Files' in exe or 'Program Files (x86)' in exe): ## or exe.startswith('C:\\Program Files') or exe.startswith('C:\\Program Files (x86)')
                return True
            else: ## Backgorund processes
                return False
                
        
        ## If nothing matches, we assume it's an app
        
        # To-do : Modify this function or create another to return the types of the apps
        # As for now, True = App, False = Not an App
        # However, I woukd like to return types like 'System App', 'Background Process', 'User App' etc.
        # This will help in better categorization and reporting of the apps
        # Then we can filter based on type in the main logic


        return True
        
        
    
    def start_monitoring(self):
        print("Starting system monitor...")
        try:
            self.is_running = True
            while self.is_running:
                self.process_apps()
                time.sleep(self.check_interval) ## Waits for the next check interval to run again
        except KeyboardInterrupt:
            print("Monitoring interrupted by user.")
        finally:
            self.stop_monitoring()
    
    def process_apps(self):
        active_apps = self.get_running_apps()
        
        print(f"found {len(active_apps)} apps running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
       
        self.apps_sorter(active_apps) # Sort apps by usage time

        # Print details of the first n active apps
        for app in active_apps[:50]:  
           # format usage time as Hours:Minutes:Seconds
            usage_time_str = f"{app['usage_time']//3600}h:{(app['usage_time']%3600)//60}m:{app['usage_time']%60}s" 
            app_info = f"{app['name']} (PID: {app['pid']}, STATUS: {app['status']}, Usage_time: {usage_time_str}, PATH: {app['executable_path']})"
            
            # Highlight the top active app
            if app in active_apps[:1]:
                print(f"*** TOP Active APP: {app_info} ***")
                
            else:
                # Print app details normally
                print(app_info)
            
            

        # Add Database logic here, in the future

    def stop_monitoring(self):
        self.is_running = False
        print("Stopping system monitor...")

def main():
    print("Starting TimeKeeper..")
    print("Press Ctrl+C to stop")

    monitor = AppMonitor(check_interval=30)
    monitor.start_monitoring()

if __name__ == "__main__":
        main()