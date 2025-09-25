from typing import List, Dict, Any

class ProcessFilter:

    def filter_for_apps(self, processes:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        apps = []
        for proc in processes:
<<<<<<< HEAD
            process_category ='Unknow'
            process_name     = proc['name']
            user_name        = proc['username']
            exe              = proc['path']
            pid              = proc['pid']

            ## Filter out system processes in the list, processes with very short names and processes running under system accounts
            if process_name in self.system_processes or len(process_name) <3 or 'service' in process_name.lower() or user_name in ['SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE', None]:
                process_category = 'system_process'
                continue
            
            # Filter out processes running from system directories
            if exe and ('Windows' in exe or 'System32' in exe or 'SysWOW64' in exe or 'EdgeWebView' in exe):
                process_category = 'windows_process'
                continue

            # Filter processes that aren't in typical directories for user-installed apps
            current_user = os.getenv('USERNAME', '').lower()
            if user_name and (current_user in user_name or exe and ('appdata' in exe.lower() or 'users' in exe.lower() or 'Program Files' in exe or 'Program Files (x86)' in exe)):
                process_category = 'user_app'
                
                
            #Filter out processes with parents ( child processes )               
            if psutil.Process(pid).parent() == False or self.has_window(pid) :
                # Checks for windows
                process_category = 'user_app'
                print(f"User App Found: {process_name} at {exe}")
                process_category = "user_app"
                    
            else:
                process_category = 'background_process'
                continue
           
            # Append the process to proceeses's list if it is classified as an app
            if 'processs' not in process_category: apps_list.append(proc)
        return apps_list
=======
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
>>>>>>> 8f0fe34e5a4e98b2fe90bae58ef822c1035ce140
