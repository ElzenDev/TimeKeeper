import threading
import time 

class TrackerThread(threading.Thread):
    def __init__(self, monitor, interval:int = 2):
        super().__init__(daemon=True) 
        self.monitor = monitor
        self.interval = interval
        self._stop_event = threading.Event()
    
    def run(self):
        while not self._stop_event.is_set():
            self.monitor.track()  
            self._stop_event.wait(self.interval) 
    
    def stop(self):
        self._stop_event.set()