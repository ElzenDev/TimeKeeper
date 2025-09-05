import psutil
import time
from datetime import datetime

def get_active_processes():
    ## Get a list of all the machines active processes
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            processes.append(process.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes
def main():
    print("Starting system monitor...")
    while True:
        active_apps = get_active_processes()
        ## Print the first 5 active apps
        print(f"found {len(active_apps)} at {datetime.now()}: active apps: {active_apps[1:5]}") 
        time.sleep(60) ## Make it monitor once every minute so the system doesn't get overloaded
if __name__ == "__main__":
    main()