import psutil, os
from typing import List, Dict, Any

class ProcessFilter:
    def __init__(self):
        self.system_processes = ['System', 'System Idle Process', 'Registry', 'smss.exe', 'csrss.exe', 'wininit.exe',
                    'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe',
                    'spoolsv.exe', 'taskhostw.exe', 'dwm.exe' ,'SearchUI.exe',
                    'RuntimeBroker.exe', 'sihost.exe', 'ctfmon.exe', 'conhost.exe',
                    'ApplicationFrameHost.exe0','winlogon.exe', 'fontdrvhost.exe', 'WmiPrvSE.exe', 'SecurityHealthService.exe'
                    ,'sppsvc.exe', 'audiodg.exe', 'SystemSettings.exe', 'esrv.exe']
    
    def filter_for_apps(self, processes:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        apps_list = []

        # Start analyzing the processes in the given processes's list
        for proc in processes:
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
                
                # Check if the process has a parent or children processes
                process_parent = psutil.Process(pid).parent()
                if process_parent:
                    print("Process Parent:", process_parent.name())
                    process_category = 'background_process'
                    continue

                process_children = psutil.Process(pid).children()
                if process_children:
                    print(f"User App Found: {process_name} by {user_name} at {exe}")
                    process_category = 'user_app'

            # Append the process to proceeses's list if it is classified as an app
            if process_category == 'user_app': apps_list.append(proc)
        return apps_list