import psutil
import time
from datetime import datetime

"""
Main App Monitor logic
"""

class AppMonitor:
    def __init__(self, check_interval: int = 60): ## Initialize with a default check interval of a minute
        self.is_running = False
        
   

    def get_running_apps(self):
        ## Get a list of all the machines active processes
        apps = []
        for process in psutil.process_iter(['pid', 'username', 'name', 'create_time']):
            try:  
                if self.is_process_an_user_app(process.info['name'], process.info['username']): # Filter user apps
                    apps.append({
                        'pid': process.info['pid'],
                        'name': process.info['name'],
                        'user': process.info['username'],
                        'start_time': process.info['create_time']
                    })                          
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): # Handle processes that may have ended or are inaccessible
                pass
        return apps
    
    def is_process_an_user_app(self, process_name: str, user_name:str) -> bool:
        ## A simple filter to determine if a process is a user app

        # A list of common system processes to ignore
        system_processes = ['System', 'Registry', 'smss.exe', 'csrss.exe', 'wininit.exe',
                       'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe',
                       'spoolsv.exe', 'taskhostw.exe', 'dwm.exe' ,'SearchUI.exe',
                       'RuntimeBroker.exe', 'sihost.exe', 'ctfmon.exe', 'conhost.exe',
                       'ApplicationFrameHost.exe0','winlogon.exe', 'fontdrvhost.exe', 'WmiPrvSE.exe', 'SecurityHealthService.exe'
                       , 'sppsvc.exe', 'audiodg.exe', 'SystemSettings.exe']
        
        ## Filter out system processes and very short names
        if process_name in system_processes:
            return False
        elif len(process_name) <3:
                return False
        ## Filter out processes running under system accounts
        if user_name in ['SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE', None]:
            return False
        return True
    
    def start_monitoring(self):
        print("Starting system monitor...")
        try:
            self.is_running = True
            while self.is_running:
                self.process_apps()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("Monitoring interrupted by user.")
        finally:
            self.stop_monitoring()
    
    def process_apps(self):
        active_apps = self.get_running_apps()
        
        print(f"found {len(active_apps)} apps running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        for app in active_apps[:20]:  # Limit output to first 20 apps
            usage_time = time.time() - app['start_time']# Calculate usage time
            usage_time = int(usage_time) # Convert to integer seconds
            usage_time = f"{usage_time//3600}h:{(usage_time%3600)//60}m:{usage_time%60}s" # Format as H:M:S
            app_info = f"{app['name']} (PID: {app['pid']}, User: {app['user']}, Usage_time: {usage_time})"
            print(app_info)

        # Add Database logging here in the future

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