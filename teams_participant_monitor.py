#!/usr/bin/env python3
"""
Teams Participant Monitor
Detects participants, joins/leaves, and active speakers from Teams UI
"""

import time
import threading
import re
from datetime import datetime
import json

# Windows-specific imports
try:
    import pygetwindow as gw
    import pyautogui
    import cv2
    import numpy as np
    from PIL import Image
    import pytesseract
    SCREEN_AVAILABLE = True
except ImportError:
    SCREEN_AVAILABLE = False

try:
    import psutil
    PROCESS_AVAILABLE = True
except ImportError:
    PROCESS_AVAILABLE = False

class TeamsParticipantMonitor:
    def __init__(self):
        self.participants = {}
        self.active_speakers = set()
        self.teams_window = None
        self.monitoring = False
        self.last_screenshot = None
        self.participant_callbacks = []
        
        # Detection settings
        self.check_interval = 2.0  # seconds
        self.screenshot_region = None
        
        print("🔍 Teams Participant Monitor initialized")
        if not SCREEN_AVAILABLE:
            print("⚠ Screen capture not available - install: pip install pygetwindow pyautogui opencv-python pillow pytesseract")
        
    def add_participant_callback(self, callback):
        """Add callback for participant changes"""
        self.participant_callbacks.append(callback)
        
    def notify_callbacks(self, event_type, participant_name, details=None):
        """Notify all callbacks of participant events"""
        for callback in self.participant_callbacks:
            try:
                callback(event_type, participant_name, details)
            except Exception as e:
                print(f"⚠ Callback error: {e}")
    
    def find_teams_window(self):
        """Find and focus Teams window"""
        try:
            # Look for Teams windows
            teams_windows = []
            for window in gw.getAllWindows():
                title = window.title.lower()
                if ('teams' in title or 'microsoft teams' in title) and window.visible:
                    teams_windows.append(window)
            
            if not teams_windows:
                return None
                
            # Prefer meeting windows
            for window in teams_windows:
                if any(keyword in window.title.lower() for keyword in ['meeting', 'call', 'conference']):
                    self.teams_window = window
                    return window
            
            # Fallback to first Teams window
            self.teams_window = teams_windows[0]
            return teams_windows[0]
            
        except Exception as e:
            print(f"⚠ Error finding Teams window: {e}")
            return None
    
    def get_participant_area_screenshot(self):
        """Take screenshot of participant area"""
        try:
            if not self.teams_window:
                if not self.find_teams_window():
                    return None
            
            # Get Teams window position and size
            left, top, width, height = self.teams_window.left, self.teams_window.top, self.teams_window.width, self.teams_window.height
            
            # Participant area is typically on the right side or bottom
            # Try right side first (most common layout)
            participant_left = left + int(width * 0.75)  # Right 25% of window
            participant_top = top + 100  # Skip title bar
            participant_width = width - int(width * 0.75)
            participant_height = height - 200  # Skip title and controls
            
            # Take screenshot of participant area
            screenshot = pyautogui.screenshot(region=(participant_left, participant_top, participant_width, participant_height))
            
            return np.array(screenshot)
            
        except Exception as e:
            print(f"⚠ Screenshot error: {e}")
            return None
    
    def detect_participants_from_screenshot(self, screenshot):
        """Extract participant names from screenshot using OCR"""
        try:
            # Convert to PIL Image for OCR
            if isinstance(screenshot, np.ndarray):
                image = Image.fromarray(screenshot)
            else:
                image = screenshot
            
            # Preprocess image for better OCR
            # Convert to grayscale
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Increase contrast
            gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
            
            # Use OCR to extract text
            text = pytesseract.image_to_string(gray, config='--psm 6')
            
            # Extract potential names
            participants = self.extract_names_from_text(text)
            
            return participants
            
        except Exception as e:
            print(f"⚠ OCR error: {e}")
            return []
    
    def extract_names_from_text(self, text):
        """Extract participant names from OCR text"""
        participants = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Skip common UI elements
            if any(skip in line.lower() for skip in ['participants', 'mute', 'camera', 'share', 'chat', 'more', 'leave', 'end']):
                continue
            
            # Look for name patterns
            # Names are usually 2-4 words, with first letter capitalized
            if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', line) or re.match(r'^[A-Z][a-z]+ [A-Z]\.$', line):
                # Clean the name
                name = re.sub(r'[^a-zA-Z\s\.]', '', line).strip()
                if len(name) > 2 and len(name.split()) <= 4:
                    participants.append(name)
        
        return participants
    
    def detect_active_speakers(self, screenshot):
        """Detect who is currently speaking from visual cues"""
        try:
            # Look for visual indicators of active speakers
            # Teams shows green border, waveform, or speaking indicator
            
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(screenshot, cv2.COLOR_RGB2HSV)
            
            # Look for green indicators (speaking)
            lower_green = np.array([40, 50, 50])
            upper_green = np.array([80, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Look for blue indicators (active)
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
            
            # Combine masks
            speaking_mask = cv2.bitwise_or(green_mask, blue_mask)
            
            # Find contours (speaking indicators)
            contours, _ = cv2.findContours(speaking_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Return number of active speakers detected
            active_count = len([c for c in contours if cv2.contourArea(c) > 100])
            
            return active_count > 0
            
        except Exception as e:
            print(f"⚠ Speaker detection error: {e}")
            return False
    
    def update_participants(self, new_participants):
        """Update participant list and detect changes"""
        current_time = datetime.now()
        
        # Detect new participants (joins)
        for participant in new_participants:
            if participant not in self.participants:
                self.participants[participant] = {
                    'joined_at': current_time,
                    'status': 'active',
                    'speaking_time': 0,
                    'last_seen': current_time
                }
                print(f"✅ {participant} joined the meeting")
                self.notify_callbacks('join', participant, {'timestamp': current_time})
        
        # Update existing participants
        for participant in new_participants:
            if participant in self.participants:
                self.participants[participant]['last_seen'] = current_time
                self.participants[participant]['status'] = 'active'
        
        # Detect participants who left (not seen recently)
        left_participants = []
        for participant, info in self.participants.items():
            time_since_seen = (current_time - info['last_seen']).total_seconds()
            if time_since_seen > 10 and info['status'] == 'active':  # 10 seconds threshold
                info['status'] = 'left'
                info['left_at'] = current_time
                left_participants.append(participant)
                print(f"❌ {participant} left the meeting")
                self.notify_callbacks('leave', participant, {'timestamp': current_time})
        
        return len(new_participants), len(left_participants)
    
    def monitor_loop(self):
        """Main monitoring loop"""
        print("🔍 Starting Teams participant monitoring...")
        
        while self.monitoring:
            try:
                # Take screenshot of participant area
                screenshot = self.get_participant_area_screenshot()
                
                if screenshot is not None:
                    # Detect participants
                    participants = self.detect_participants_from_screenshot(screenshot)
                    
                    # Detect active speakers
                    has_active_speaker = self.detect_active_speakers(screenshot)
                    
                    # Update participant list
                    if participants:
                        active_count, left_count = self.update_participants(participants)
                        
                        if has_active_speaker:
                            print(f"🎤 Someone is speaking ({len(participants)} participants)")
                            self.notify_callbacks('speaking', 'unknown', {'active': True})
                    
                    # Store screenshot for debugging
                    self.last_screenshot = screenshot
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"⚠ Monitoring error: {e}")
                time.sleep(5)  # Wait longer on error
        
        print("⏹️ Teams monitoring stopped")
    
    def start_monitoring(self):
        """Start participant monitoring"""
        if not SCREEN_AVAILABLE:
            print("❌ Cannot start monitoring - missing dependencies")
            return False
        
        if self.monitoring:
            print("⚠ Monitoring already started")
            return True
        
        # Find Teams window
        if not self.find_teams_window():
            print("❌ Teams window not found - please open Teams meeting")
            return False
        
        print(f"✅ Found Teams window: {self.teams_window.title}")
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        return True
    
    def stop_monitoring(self):
        """Stop participant monitoring"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=2)
        
        print("⏹️ Participant monitoring stopped")
    
    def get_current_participants(self):
        """Get current active participants"""
        active_participants = {
            name: info for name, info in self.participants.items() 
            if info['status'] == 'active'
        }
        return active_participants
    
    def export_session_log(self, filename):
        """Export participant session log"""
        log_data = {
            'session_start': datetime.now().isoformat(),
            'participants': {},
            'total_participants': len(self.participants)
        }
        
        for name, info in self.participants.items():
            log_data['participants'][name] = {
                'joined_at': info['joined_at'].isoformat(),
                'left_at': info.get('left_at', '').isoformat() if info.get('left_at') else None,
                'status': info['status'],
                'duration': str(datetime.now() - info['joined_at'])
            }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Session log exported to {filename}")

# Test function
def test_monitor():
    """Test the participant monitor"""
    monitor = TeamsParticipantMonitor()
    
    def on_participant_event(event_type, participant, details):
        print(f"🎯 Event: {event_type} - {participant} - {details}")
    
    monitor.add_participant_callback(on_participant_event)
    
    if monitor.start_monitoring():
        try:
            print("Monitoring for 60 seconds... (Ctrl+C to stop)")
            time.sleep(60)
        except KeyboardInterrupt:
            pass
        finally:
            monitor.stop_monitoring()
            
            # Show results
            participants = monitor.get_current_participants()
            print(f"\n📊 Session Summary:")
            print(f"Total participants detected: {len(monitor.participants)}")
            print(f"Currently active: {len(participants)}")
            
            for name, info in monitor.participants.items():
                print(f"  👤 {name} - {info['status']} (joined: {info['joined_at'].strftime('%H:%M:%S')})")

if __name__ == "__main__":
    test_monitor()