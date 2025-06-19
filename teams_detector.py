import psutil
import time
import threading
try:
    import win32gui
    import win32process
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False

class TeamsDetector:
    def __init__(self):
        self.detection_callback = None
        self.is_monitoring = False
        self.monitor_thread = None
        
    def set_detection_callback(self, callback):
        """Set callback function when Teams meeting is detected"""
        self.detection_callback = callback
    
    def detect_teams_process(self):
        """Check if Teams process is running"""
        teams_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                process_name = proc.info['name'].lower()
                if any(teams_name in process_name for teams_name in 
                      ['teams', 'msteams', 'microsoft teams']):
                    teams_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        return teams_processes
    
    def detect_teams_window(self):
        """Check for Teams meeting window (Windows only)"""
        if not WINDOWS_AVAILABLE:
            return False
            
        teams_windows = []
        
        def enum_windows_proc(hwnd, results):
            try:
                window_text = win32gui.GetWindowText(hwnd)
                if window_text and any(keyword in window_text.lower() for keyword in 
                                     ['teams', 'meeting', 'microsoft teams']):
                    results.append({
                        'hwnd': hwnd,
                        'title': window_text
                    })
            except:
                pass
                
        try:
            win32gui.EnumWindows(enum_windows_proc, teams_windows)
            return len(teams_windows) > 0
        except:
            return False
    
    def detect_teams_meeting(self):
        """Comprehensive Teams meeting detection"""
        # Method 1: Check if Teams process is running
        teams_processes = self.detect_teams_process()
        if not teams_processes:
            return False, "Teams not running"
        
        # Method 2: Check for Teams meeting window (Windows only)
        if WINDOWS_AVAILABLE:
            has_meeting_window = self.detect_teams_window()
            if has_meeting_window:
                return True, "Teams meeting window detected"
        
        # Method 3: Check for multiple Teams processes (often indicates active meeting)
        if len(teams_processes) > 1:
            return True, "Multiple Teams processes detected"
        
        # Method 4: Check for high CPU usage by Teams (indicates active meeting)
        for proc_info in teams_processes:
            try:
                proc = psutil.Process(proc_info['pid'])
                cpu_percent = proc.cpu_percent(interval=1)
                if cpu_percent > 10:  # Teams using significant CPU
                    return True, f"Teams high CPU usage: {cpu_percent}%"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return False, "Teams running but no meeting detected"
    
    def start_monitoring(self, check_interval=5):
        """Start monitoring for Teams meetings"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(check_interval,))
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print(f"Started Teams monitoring (checking every {check_interval} seconds)")
    
    def _monitor_loop(self, check_interval):
        """Main monitoring loop"""
        previous_meeting_state = False
        
        while self.is_monitoring:
            try:
                is_meeting, reason = self.detect_teams_meeting()
                
                # Only trigger callback on state change
                if is_meeting != previous_meeting_state:
                    if self.detection_callback:
                        self.detection_callback(is_meeting, reason)
                    
                    if is_meeting:
                        print(f"Teams meeting detected: {reason}")
                    else:
                        print("Teams meeting ended")
                        
                    previous_meeting_state = is_meeting
                
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(check_interval)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        print("Stopped Teams monitoring")
    
    def auto_start_transcription(self):
        """Block until Teams meeting is detected"""
        print("Waiting for Teams meeting...")
        
        while True:
            is_meeting, reason = self.detect_teams_meeting()
            if is_meeting:
                print(f"Teams meeting detected! {reason}")
                return True
            time.sleep(5)  # Check every 5 seconds