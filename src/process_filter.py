import psutil
import os
import win32gui, win32process, win32con

from typing import List, Dict, Any

class ProcessFilter:
    def __init__(self):
        self.system_processes = ['System', 'System Idle Process', 'Registry', 'smss.exe', 'csrss.exe', 'wininit.exe',
                    'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe',
                    'spoolsv.exe', 'taskhostw.exe', 'dwm.exe' ,'SearchUI.exe',
                    'RuntimeBroker.exe', 'sihost.exe', 'ctfmon.exe', 'conhost.exe',
                    'ApplicationFrameHost.exe0','winlogon.exe', 'fontdrvhost.exe', 'WmiPrvSE.exe', 'SecurityHealthService.exe'
                    ,'sppsvc.exe', 'audiodg.exe', 'SystemSettings.exe', 'esrv.exe']
    
    def has_window(self, pid: int) -> bool:
        """
        Check if a procces has a window based on it's PID.
        Receives an Integer (PID) and returns a boolean (has_window)

        pid: int
        """
        has_window: bool = False
        try:
            def callback(hwnd, lparam):
                nonlocal has_window
                # check if window is enabled
                if win32gui.IsWindowEnabled(hwnd):
                    try:
                        lparam, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                        # Check if is the main window
                        if found_pid == pid:
                            if (win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & win32con.WS_CAPTION and win32gui.GetWindowTextLength(hwnd) > 0):
                                has_window = True
                                return False
                    except:
                        pass
                return True
                
            win32gui.EnumWindows(callback, 0)
            return has_window
        
        except Exception as e:
            print(f"Error enumerating windows: {e}")

    

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