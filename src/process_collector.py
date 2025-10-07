import psutil
from typing import List, Dict, Any
class ProcessCollector:
    def get_running_processes(self) -> List[Dict[str, Any]]:
        processes: List = []

        # Gets all the running processes and append them to the processes's list with selected paramaters
        for proc in psutil.process_iter(['pid', 'username', 'name', 'create_time', 'exe', 'cpu_percent', 'memory_info']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'username': proc.info['username'],
                    'create_time': proc.info['create_time'],
                    'category': '',
                    'path': proc.info['exe'],
                    'cpu_usage': proc.info['cpu_percent'],
                    'memory_info': proc.info['memory_info']
                })

            except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess): # Handle processes that may have ended or are inaccessible
                continue
            
        return processes