from typing import List, Dict, Any
import win32gui, win32process, win32con, psutil, os

class ProcessCategorizer:
    def __init__(self):
        self.system_processes = ['System', 'System Idle Process', 'Registry', 'smss.exe', 'csrss.exe', 'wininit.exe',
                    'services.exe', 'lsass.exe', 'svchost.exe', 'explorer.exe',
                    'spoolsv.exe', 'taskhostw.exe', 'dwm.exe' ,'SearchUI.exe',
                    'RuntimeBroker.exe', 'sihost.exe', 'ctfmon.exe', 'conhost.exe',
                    'ApplicationFrameHost.exe0','winlogon.exe', 'fontdrvhost.exe', 'WmiPrvSE.exe', 'SecurityHealthService.exe'
                    ,'sppsvc.exe', 'audiodg.exe', 'SystemSettings.exe', 'esrv.exe']
    
    def has_window(self, pid: int) -> bool:
        """
        Check if a procces has a window and if it is the main one.
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
                        if found_pid == pid and (win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE) & win32con.WS_CAPTION and win32gui.GetWindowTextLength(hwnd) > 0):
                            has_window = True
                            return False
                    except:
                        pass
                return True
                
            win32gui.EnumWindows(callback, 0)
            return has_window
        
        except Exception as e:
            print(f"Error enumerating windows: {e}")

    def categorize(self, processes: List[Dict[str, Any]]) -> None:
        
        for proc in processes:
            process_name     = proc['name']
            user_name        = proc['username']
            exe              = proc['path']
            pid              = proc['pid']

            if process_name in self.system_processes or len(process_name) <3 or 'service' in process_name.lower() or user_name in ['SYSTEM', 'LOCAL SERVICE', 'NETWORK SERVICE', None]:
                proc['category'] = 'system_process'
                continue
            
            # Filter out processes running from system directories
            if exe and ('Windows' in exe or 'System32' in exe or 'SysWOW64' in exe or 'EdgeWebView' in exe):
                proc['category'] = 'system_process'
                continue

            # Filter processes that aren't in typical directories for user-installed apps
            current_user = os.getenv('USERNAME', '').lower()
            if user_name and (current_user in user_name or exe and ('appdata' in exe.lower() or 'users' in exe.lower() or 'Program Files' in exe or 'Program Files (x86)' in exe)):
                proc['category'] = 'user_app'


            #Filter Processes without a window and those with parent processes and no children ones (child processes that are not parent one as well)  
            if self.has_window(pid) == False or (psutil.Process(pid).parent() and psutil.Process(pid).children == False):
                proc['category'] = 'background_process'
                continue
            else:
                # print(f"User App Found: {process_name} at {exe}")
                proc['category'] = 'user_app'

