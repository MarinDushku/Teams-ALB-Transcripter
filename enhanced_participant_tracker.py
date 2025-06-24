#!/usr/bin/env python3
"""
Enhanced Teams Participant Tracker
Advanced participant detection using multiple methods
"""

import time
import threading
import re
import json
from datetime import datetime
from collections import defaultdict

# Multiple detection methods
try:
    import psutil
    import win32gui
    import win32process
    import win32api
    import win32con
    WINDOWS_API_AVAILABLE = True
except ImportError:
    WINDOWS_API_AVAILABLE = False

try:
    import pygetwindow as gw
    import pyautogui
    import cv2
    import numpy as np
    from PIL import Image
    import pytesseract
    SCREEN_CAPTURE_AVAILABLE = True
except ImportError:
    SCREEN_CAPTURE_AVAILABLE = False

class EnhancedParticipantTracker:
    def __init__(self):
        self.participants = {}
        self.active_speakers = {}
        self.monitoring = False
        self.teams_process = None
        self.teams_windows = []
        
        # Detection methods
        self.detection_methods = {
            'window_api': self.detect_via_windows_api,
            'screen_ocr': self.detect_via_screen_ocr,
            'process_monitor': self.detect_via_process_monitor
        }
        
        # Callbacks
        self.participant_callbacks = []
        self.speaker_callbacks = []
        
        # Settings
        self.check_interval = 1.0  # More frequent checking
        self.confidence_threshold = 0.7
        
        print("🔍 Enhanced Participant Tracker initialized")
        self.check_capabilities()
    
    def check_capabilities(self):
        """Check available detection methods"""
        methods = []
        if WINDOWS_API_AVAILABLE:
            methods.append("Windows API")
        if SCREEN_CAPTURE_AVAILABLE:
            methods.append("Screen OCR")
        
        print(f"🔧 Available methods: {', '.join(methods) if methods else 'None'}")
        
        if not methods:
            print("⚠ No detection methods available")
            print("  Install: pip install pywin32 pygetwindow pyautogui opencv-python pytesseract")
    
    def add_participant_callback(self, callback):
        """Add callback for participant events"""
        self.participant_callbacks.append(callback)
    
    def add_speaker_callback(self, callback):
        """Add callback for speaker events"""
        self.speaker_callbacks.append(callback)
    
    def notify_participant_callbacks(self, event_type, participant, details=None):
        """Notify participant event callbacks"""
        for callback in self.participant_callbacks:
            try:
                callback(event_type, participant, details)
            except Exception as e:
                print(f"⚠ Participant callback error: {e}")
    
    def notify_speaker_callbacks(self, speaker, is_speaking, details=None):
        """Notify speaker event callbacks"""
        for callback in self.speaker_callbacks:
            try:
                callback(speaker, is_speaking, details)
            except Exception as e:
                print(f"⚠ Speaker callback error: {e}")
    
    def find_teams_processes(self):
        """Find Teams processes and windows"""
        teams_processes = []
        teams_windows = []
        
        try:
            # Find Teams processes
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if 'teams' in proc.info['name'].lower():
                        teams_processes.append(proc)
                except:
                    continue
            
            # Find Teams windows
            if WINDOWS_API_AVAILABLE:
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_text = win32gui.GetWindowText(hwnd)
                        if 'teams' in window_text.lower():
                            windows.append({
                                'hwnd': hwnd,
                                'title': window_text,
                                'rect': win32gui.GetWindowRect(hwnd)
                            })
                
                win32gui.EnumWindows(enum_windows_callback, teams_windows)
        
        except Exception as e:
            print(f"⚠ Process detection error: {e}")
        
        self.teams_process = teams_processes
        self.teams_windows = teams_windows
        return len(teams_processes) > 0, len(teams_windows) > 0
    
    def detect_via_windows_api(self):
        """Detect participants using Windows API"""
        participants = {}
        
        try:
            if not WINDOWS_API_AVAILABLE:
                return participants
            
            # Get Teams window information
            for window in self.teams_windows:
                hwnd = window['hwnd']
                
                # Try to get accessibility information
                # This would require additional Windows accessibility APIs
                # For now, we'll focus on window title analysis
                title = window['title']
                
                # Extract meeting info from window title
                if 'meeting' in title.lower() or 'call' in title.lower():
                    # Parse title for participant info
                    # Teams often shows participant count in title
                    participant_match = re.search(r'(\d+)\s*participant', title, re.IGNORECASE)
                    if participant_match:
                        count = int(participant_match.group(1))
                        participants['_meeting_info'] = {
                            'participant_count': count,
                            'title': title,
                            'method': 'windows_api'
                        }
        
        except Exception as e:
            print(f"⚠ Windows API detection error: {e}")
        
        return participants
    
    def detect_via_screen_ocr(self):
        """Detect participants using screen OCR"""
        participants = {}
        
        try:
            if not SCREEN_CAPTURE_AVAILABLE:
                return participants
            
            # Find Teams window
            teams_window = None
            for window in gw.getAllWindows():
                if 'teams' in window.title.lower() and window.visible:
                    teams_window = window
                    break
            
            if not teams_window:
                return participants
            
            # Screenshot participant area
            left = teams_window.left + int(teams_window.width * 0.7)  # Right side
            top = teams_window.top + 100
            width = teams_window.width - int(teams_window.width * 0.7)
            height = teams_window.height - 200
            
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            
            # OCR processing
            gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            text = pytesseract.image_to_string(gray, config='--psm 6')
            
            # Extract names
            names = self.extract_participant_names(text)
            
            for name in names:
                participants[name] = {
                    'status': 'active',
                    'method': 'screen_ocr',
                    'confidence': 0.8,
                    'detected_at': datetime.now()
                }
        
        except Exception as e:
            print(f"⚠ Screen OCR detection error: {e}")
        
        return participants
    
    def detect_via_process_monitor(self):
        """Detect participants by monitoring Teams process activity"""
        participants = {}
        
        try:
            # Monitor Teams process network connections
            # This could indicate participant activity
            for proc in self.teams_process:
                try:
                    connections = proc.connections()
                    
                    # Count active connections (rough indicator of participants)
                    active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
                    
                    if active_connections > 0:
                        participants['_connection_info'] = {
                            'active_connections': active_connections,
                            'method': 'process_monitor',
                            'confidence': 0.5
                        }
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        
        except Exception as e:
            print(f"⚠ Process monitor error: {e}")
        
        return participants
    
    def extract_participant_names(self, text):
        """Extract participant names from OCR text"""
        names = []
        lines = text.split('\n')
        
        # Common patterns for participant names
        name_patterns = [
            r'^[A-Z][a-z]+ [A-Z][a-z]+$',  # First Last
            r'^[A-Z][a-z]+ [A-Z]\.$',       # First L.
            r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+$',  # First Middle Last
        ]
        
        for line in lines:
            line = line.strip()
            if len(line) < 3 or len(line) > 50:
                continue
            
            # Skip UI elements
            skip_words = ['participants', 'mute', 'camera', 'share', 'chat', 'more', 
                         'leave', 'end', 'call', 'meeting', 'video', 'audio']
            if any(word in line.lower() for word in skip_words):
                continue
            
            # Check if line matches name pattern
            for pattern in name_patterns:
                if re.match(pattern, line):
                    # Clean the name
                    clean_name = re.sub(r'[^a-zA-Z\s\.]', '', line).strip()
                    if clean_name and len(clean_name.split()) <= 4:
                        names.append(clean_name)
                        break
        
        return list(set(names))  # Remove duplicates
    
    def detect_active_speakers(self):
        """Detect who is currently speaking"""
        speakers = {}
        
        try:
            # Use multiple methods to detect active speakers
            
            # Method 1: Screen analysis for visual indicators
            if SCREEN_CAPTURE_AVAILABLE:
                speakers.update(self.detect_speakers_visual())
            
            # Method 2: Audio level analysis (if available)
            # This would require integration with audio capture
            
            # Method 3: Window title analysis
            for window in self.teams_windows:
                title = window['title']
                if 'speaking' in title.lower() or 'unmuted' in title.lower():
                    speakers['_speaking_indicator'] = {
                        'active': True,
                        'method': 'window_title'
                    }
        
        except Exception as e:
            print(f"⚠ Speaker detection error: {e}")
        
        return speakers
    
    def detect_speakers_visual(self):
        """Detect speakers using visual cues"""
        speakers = {}
        
        try:
            # Find Teams window
            teams_window = None
            for window in gw.getAllWindows():
                if 'teams' in window.title.lower() and window.visible:
                    teams_window = window
                    break
            
            if not teams_window:
                return speakers
            
            # Screenshot main video area
            screenshot = pyautogui.screenshot(region=(
                teams_window.left + 50,
                teams_window.top + 100,
                teams_window.width - 100,
                teams_window.height - 200
            ))
            
            # Convert to OpenCV format
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Look for speaking indicators (green borders, waveforms)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Green color range (speaking indicator)
            lower_green = np.array([40, 50, 50])
            upper_green = np.array([80, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            
            # Count green pixels (speaking indicators)
            green_pixels = cv2.countNonZero(green_mask)
            
            if green_pixels > 1000:  # Threshold for speaking indicator
                speakers['visual_speaker'] = {
                    'active': True,
                    'confidence': min(green_pixels / 10000, 1.0),
                    'method': 'visual_detection'
                }
        
        except Exception as e:
            print(f"⚠ Visual speaker detection error: {e}")
        
        return speakers
    
    def update_participants(self, detected_participants):
        """Update participant list with change detection"""
        current_time = datetime.now()
        changes = []
        
        # Process detected participants
        for name, info in detected_participants.items():
            if name.startswith('_'):  # Skip metadata
                continue
            
            if name not in self.participants:
                # New participant joined
                self.participants[name] = {
                    'joined_at': current_time,
                    'status': 'active',
                    'last_seen': current_time,
                    'speaking_time': 0,
                    'detection_method': info.get('method', 'unknown'),
                    'confidence': info.get('confidence', 0.5)
                }
                changes.append(('join', name, info))
                print(f"✅ {name} joined (via {info.get('method', 'unknown')})")
                self.notify_participant_callbacks('join', name, info)
            else:
                # Update existing participant
                self.participants[name]['last_seen'] = current_time
                self.participants[name]['status'] = 'active'
        
        # Check for participants who left
        for name, info in self.participants.items():
            if info['status'] == 'active':
                time_since_seen = (current_time - info['last_seen']).total_seconds()
                if time_since_seen > 15:  # 15 second threshold
                    info['status'] = 'left'
                    info['left_at'] = current_time
                    changes.append(('leave', name, info))
                    print(f"❌ {name} left the meeting")
                    self.notify_participant_callbacks('leave', name, info)
        
        return changes
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        print("🔍 Starting enhanced participant monitoring...")
        
        while self.monitoring:
            try:
                # Find Teams processes and windows
                has_process, has_window = self.find_teams_processes()
                
                if not (has_process or has_window):
                    print("⚠ Teams not detected - waiting...")
                    time.sleep(5)
                    continue
                
                # Run all detection methods
                all_participants = {}
                
                for method_name, method_func in self.detection_methods.items():
                    try:
                        participants = method_func()
                        all_participants.update(participants)
                    except Exception as e:
                        print(f"⚠ {method_name} failed: {e}")
                
                # Update participant list
                if all_participants:
                    changes = self.update_participants(all_participants)
                
                # Detect active speakers
                speakers = self.detect_active_speakers()
                for speaker, info in speakers.items():
                    if not speaker.startswith('_'):
                        self.notify_speaker_callbacks(speaker, info.get('active', False), info)
                
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"⚠ Monitoring loop error: {e}")
                time.sleep(5)
        
        print("⏹️ Enhanced monitoring stopped")
    
    def start_monitoring(self):
        """Start enhanced monitoring"""
        if self.monitoring:
            return True
        
        # Check if Teams is running
        has_process, has_window = self.find_teams_processes()
        if not (has_process or has_window):
            print("❌ Teams not detected - please open Teams")
            return False
        
        print(f"✅ Teams detected: {len(self.teams_process)} processes, {len(self.teams_windows)} windows")
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        return True
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=3)
    
    def get_active_participants(self):
        """Get currently active participants"""
        return {name: info for name, info in self.participants.items() 
                if info['status'] == 'active'}
    
    def get_session_summary(self):
        """Get session summary"""
        total_participants = len(self.participants)
        active_participants = len(self.get_active_participants())
        
        return {
            'total_participants': total_participants,
            'active_participants': active_participants,
            'participants': self.participants
        }

# Test function
if __name__ == "__main__":
    tracker = EnhancedParticipantTracker()
    
    def on_participant_change(event_type, participant, details):
        print(f"🎯 {event_type.upper()}: {participant}")
    
    def on_speaker_change(speaker, is_speaking, details):
        if is_speaking:
            print(f"🎤 {speaker} is speaking")
    
    tracker.add_participant_callback(on_participant_change)
    tracker.add_speaker_callback(on_speaker_change)
    
    if tracker.start_monitoring():
        try:
            print("Monitoring for 30 seconds...")
            time.sleep(30)
        except KeyboardInterrupt:
            pass
        finally:
            tracker.stop_monitoring()
            summary = tracker.get_session_summary()
            print(f"\n📊 Session Summary: {summary}")