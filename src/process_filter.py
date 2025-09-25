from typing import List, Dict, Any

class ProcessFilter:

    def filter_for_apps(self, processes:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        apps = []
        for proc in processes:
            if proc['category'] == 'user_app': apps.append(proc)
        return apps
    
    def filter_for_system_processes(self, processes:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        system_processes = []
        for proc in processes:
            if proc['category'] == 'system_process' : system_processes.append(proc)
        return system_processes
    
    def filter_for_background_processes(self, processes:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        background_processes = []
        for proc in processes:
            if proc['category'] == 'background_process' : background_processes.append(proc)
        return background_processes