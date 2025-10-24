import win32gui, win32process, win32con
from typing import List, Dict, Any
class WindowChecker:
    def __init__(self, target_pid: int):
        self.target_pid = target_pid
        self.found_window = False
        self.window_handle = None
        self.window_title = None

    def check_window(self, hwnd, _):
        """Check if window belongs to target process and has the right characteristics"""
        # If we already found a window, skip further enumeration
        if self.found_window:
            return True

        # Skip invisible windows
        if not win32gui.IsWindowVisible(hwnd):
            return True

        try:
            _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
            if window_pid != self.target_pid:
                return True
            
            window_title = win32gui.GetWindowText(hwnd)
            if not window_title:
                return True
            
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            
            if style:
                self.found_window = True
                self.window_handle = hwnd
                self.window_title = window_title
                print(f"Found window for PID {self.target_pid}: {window_title}")
                # Continue enumeration instead of stopping
                return True

        except Exception:
            # Silently continue on any error
            pass
        
        return True

    def get_result(self):
        """Get the final result of the window check"""
        if self.found_window:
            print(f"Final result: Found window. Handle: {self.window_handle}, Title: {self.window_title}")
        else:
            print("Final result: No matching window found")
        return self.found_window
    
    def get_window_title(self):
        """Get the title of the found window, if any"""
        return self.window_title if self.found_window else None