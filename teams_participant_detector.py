import psutil
import time
import threading
import requests
import json
import re
import os
from datetime import datetime
try:
    import win32gui
    import win32process
    import win32api
    import win32con
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False

class TeamsParticipantDetector:
    def __init__(self):
        self.participants = {}
        self.meeting_id = None
        self.meeting_title = None
        self.detection_callback = None
        self.participant_callback = None
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Teams API endpoints (when available)
        self.teams_api_base = "https://graph.microsoft.com/v1.0"
        self.access_token = None
        
        # Alternative detection methods
        self.window_detection_enabled = True
        self.process_detection_enabled = True
        self.network_detection_enabled = True
        
        print("Teams Participant Detector initialized")
    
    def set_callbacks(self, detection_callback=None, participant_callback=None):
        """Set callback functions for Teams and participant detection"""
        self.detection_callback = detection_callback
        self.participant_callback = participant_callback
    
    def detect_teams_participants_via_api(self):
        """Detect participants using Microsoft Graph API (requires authentication)"""
        if not self.access_token:
            return {}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            # Get online meetings
            response = requests.get(
                f"{self.teams_api_base}/me/onlineMeetings",
                headers=headers
            )
            
            if response.status_code == 200:
                meetings = response.json().get('value', [])
                for meeting in meetings:
                    if meeting.get('state') == 'active':
                        meeting_id = meeting.get('id')
                        participants = self.get_meeting_participants(meeting_id, headers)
                        return participants
            
            return {}
            
        except Exception as e:
            print(f"API participant detection error: {e}")
            return {}
    
    def get_meeting_participants(self, meeting_id, headers):
        """Get participants for a specific meeting"""
        try:
            response = requests.get(
                f"{self.teams_api_base}/me/onlineMeetings/{meeting_id}/participants",
                headers=headers
            )
            
            if response.status_code == 200:
                participants_data = response.json().get('value', [])
                participants = {}
                
                for participant in participants_data:
                    name = participant.get('displayName', 'Unknown')
                    email = participant.get('email', '')
                    role = participant.get('role', 'attendee')
                    
                    participants[name] = {
                        'email': email,
                        'role': role,
                        'detection_method': 'api',
                        'confidence': 'high'
                    }
                
                return participants
            
            return {}
            
        except Exception as e:
            print(f"Meeting participants API error: {e}")
            return {}
    
    def detect_participants_via_window_analysis(self):
        """Detect participants by analyzing Teams window content"""
        if not WINDOWS_AVAILABLE or not self.window_detection_enabled:
            return {}
        
        try:
            participants = {}
            teams_windows = self.find_teams_windows()
            
            for window_info in teams_windows:
                hwnd = window_info['hwnd']
                title = window_info['title']
                
                # Extract meeting info from window title
                meeting_info = self.parse_meeting_title(title)
                if meeting_info:
                    self.meeting_title = meeting_info.get('title')
                    self.meeting_id = meeting_info.get('id')
                
                # Try to get participant names from window content
                # This is limited due to security restrictions
                window_participants = self.extract_participants_from_window(hwnd)
                participants.update(window_participants)
            
            return participants
            
        except Exception as e:
            print(f"Window analysis error: {e}")
            return {}
    
    def find_teams_windows(self):
        """Find all Teams-related windows"""
        teams_windows = []
        
        def enum_windows_proc(hwnd, results):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    
                    # Look for Teams meeting windows
                    if window_text and any(keyword in window_text.lower() for keyword in 
                                         ['microsoft teams', 'teams meeting', 'meeting with']):
                        results.append({
                            'hwnd': hwnd,
                            'title': window_text,
                            'class': class_name
                        })
            except:
                pass
        
        try:
            win32gui.EnumWindows(enum_windows_proc, teams_windows)
        except:
            pass
        
        return teams_windows
    
    def parse_meeting_title(self, title):
        """Extract meeting information from window title"""
        try:
            # Common Teams window title patterns
            patterns = [
                r"Microsoft Teams - (.+)",
                r"Meeting with (.+) \| Microsoft Teams",
                r"(.+) \| Microsoft Teams",
                r"Teams Meeting - (.+)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, title, re.IGNORECASE)
                if match:
                    meeting_title = match.group(1).strip()
                    
                    # Try to extract participant names from title
                    if " and " in meeting_title or "," in meeting_title:
                        # Multiple participants in title
                        participants = re.split(r'[,&]|\sand\s', meeting_title)
                        return {
                            'title': meeting_title,
                            'participants': [p.strip() for p in participants if p.strip()],
                            'id': self.generate_meeting_id(meeting_title)
                        }
                    else:
                        return {
                            'title': meeting_title,
                            'participants': [meeting_title] if meeting_title else [],
                            'id': self.generate_meeting_id(meeting_title)
                        }
            
            return None
            
        except Exception as e:
            print(f"Title parsing error: {e}")
            return None
    
    def generate_meeting_id(self, title):
        """Generate a consistent meeting ID from title"""
        import hashlib
        return hashlib.md5(title.encode()).hexdigest()[:8]
    
    def extract_participants_from_window(self, hwnd):
        """Try to extract participant information from window content"""
        participants = {}
        
        try:
            # This is limited due to security restrictions in modern Windows
            # Most reliable method is title parsing and process detection
            
            # Get window process info
            _, process_id = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(process_id)
            
            # Check command line arguments for participant info
            cmdline = process.cmdline()
            for arg in cmdline:
                if '@' in arg and '.' in arg:  # Potential email
                    email = arg.strip()
                    name = email.split('@')[0].replace('.', ' ').title()
                    participants[name] = {
                        'email': email,
                        'detection_method': 'process_cmdline',
                        'confidence': 'medium'
                    }
            
        except Exception as e:
            print(f"Window content extraction error: {e}")
        
        return participants
    
    def detect_participants_via_network_analysis(self):
        """Detect participants by analyzing network connections"""
        if not self.network_detection_enabled:
            return {}
        
        try:
            participants = {}
            teams_processes = self.get_teams_processes()
            
            for proc in teams_processes:
                try:
                    # Get network connections for Teams processes
                    connections = proc.connections(kind='inet')
                    
                    for conn in connections:
                        if conn.status == 'ESTABLISHED':
                            # Analyze remote addresses for Teams-related endpoints
                            remote_ip = conn.raddr.ip if conn.raddr else None
                            if remote_ip and self.is_teams_endpoint(remote_ip):
                                # This would require more sophisticated analysis
                                # to extract participant info from network data
                                pass
                    
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    continue
            
            return participants
            
        except Exception as e:
            print(f"Network analysis error: {e}")
            return {}
    
    def get_teams_processes(self):
        """Get all Teams-related processes"""
        teams_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                process_name = proc.info['name'].lower()
                if any(teams_name in process_name for teams_name in 
                      ['teams', 'msteams', 'microsoft teams']):
                    teams_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        return teams_processes
    
    def is_teams_endpoint(self, ip):
        """Check if IP address is a Teams-related endpoint"""
        # Microsoft Teams uses various Azure/Office 365 endpoints
        teams_ip_ranges = [
            '13.107.',  # Microsoft services
            '52.112.',  # Teams media
            '52.120.',  # Teams signaling
            '20.190.',  # Azure
        ]
        
        return any(ip.startswith(prefix) for prefix in teams_ip_ranges)
    
    def detect_participants_comprehensive(self):
        """Comprehensive participant detection using all available methods"""
        all_participants = {}
        
        # Method 1: API detection (most reliable, requires auth)
        api_participants = self.detect_teams_participants_via_api()
        all_participants.update(api_participants)
        
        # Method 2: Window analysis (moderately reliable)
        window_participants = self.detect_participants_via_window_analysis()
        all_participants.update(window_participants)
        
        # Method 3: Network analysis (least reliable, supplementary)
        network_participants = self.detect_participants_via_network_analysis()
        all_participants.update(network_participants)
        
        # Method 4: Smart name extraction from known patterns
        pattern_participants = self.detect_participants_via_patterns()
        all_participants.update(pattern_participants)
        
        return all_participants
    
    def detect_participants_via_patterns(self):
        """Detect participants using common naming patterns and heuristics"""
        participants = {}
        
        # If we have a meeting title, try to extract names
        if self.meeting_title:
            # Common patterns for meeting titles with names
            patterns = [
                r'(?:meeting|call|chat)\s+with\s+([^|]+)',
                r'([A-Z][a-z]+\s+[A-Z][a-z]+)',  # First Last name pattern
                r'([a-zA-Z.]+@[a-zA-Z.]+)',      # Email pattern
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, self.meeting_title, re.IGNORECASE)
                for match in matches:
                    name = match.strip()
                    if len(name) > 2 and name not in participants:
                        participants[name] = {
                            'detection_method': 'title_pattern',
                            'confidence': 'medium',
                            'source': 'meeting_title'
                        }
        
        return participants
    
    def start_monitoring(self, check_interval=10):
        """Start monitoring for Teams participants"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, 
            args=(check_interval,)
        )
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print(f"Teams participant monitoring started (interval: {check_interval}s)")
    
    def _monitoring_loop(self, check_interval):
        """Main monitoring loop for participant detection"""
        last_participants = {}
        
        while self.is_monitoring:
            try:
                # Detect current participants
                current_participants = self.detect_participants_comprehensive()
                
                # Check for changes
                if current_participants != last_participants:
                    self.participants = current_participants
                    
                    # Notify about participant changes
                    if self.participant_callback:
                        self.participant_callback(current_participants)
                    
                    if current_participants:
                        participant_names = list(current_participants.keys())
                        print(f"🎭 Participants detected: {', '.join(participant_names)}")
                        
                        # Also notify about Teams meeting status
                        if self.detection_callback:
                            meeting_active = len(current_participants) > 0
                            reason = f"Active meeting with {len(current_participants)} participants"
                            self.detection_callback(meeting_active, reason)
                    
                    last_participants = current_participants.copy()
                
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"Participant monitoring error: {e}")
                time.sleep(check_interval)
    
    def stop_monitoring(self):
        """Stop participant monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("Teams participant monitoring stopped")
    
    def get_participants(self):
        """Get current list of detected participants"""
        return self.participants.copy()
    
    def get_participant_by_voice_match(self, voice_characteristics):
        """Match voice characteristics to known participants"""
        # This would use advanced matching algorithms
        # For now, return the most likely match based on simple heuristics
        
        if not self.participants:
            return None
        
        # Simple matching based on voice type and participant list
        participant_names = list(self.participants.keys())
        
        # If voice characteristics suggest gender, try to match
        voice_type = voice_characteristics.get('voice_type', '').lower()
        
        if 'female' in voice_type or 'high' in voice_type:
            # Look for likely female names
            female_patterns = ['ana', 'maria', 'elena', 'sara', 'linda']
            for name in participant_names:
                if any(pattern in name.lower() for pattern in female_patterns):
                    return name
        
        elif 'male' in voice_type or 'low' in voice_type:
            # Look for likely male names
            male_patterns = ['john', 'david', 'michael', 'robert', 'mark']
            for name in participant_names:
                if any(pattern in name.lower() for pattern in male_patterns):
                    return name
        
        # If no gender-based match, return first participant
        return participant_names[0] if participant_names else None
    
    def map_speaker_to_participant(self, speaker_id, voice_characteristics):
        """Map detected speaker to actual participant name"""
        if not self.participants:
            return speaker_id
        
        # Try to match based on voice characteristics
        matched_participant = self.get_participant_by_voice_match(voice_characteristics)
        
        if matched_participant:
            return matched_participant
        
        # Fallback: map speakers to participants in order
        participant_names = list(self.participants.keys())
        
        try:
            # Extract speaker number from speaker_id (e.g., "Speaker 1" -> 0)
            speaker_number = int(re.search(r'(\d+)', speaker_id).group(1)) - 1
            if 0 <= speaker_number < len(participant_names):
                return participant_names[speaker_number]
        except (AttributeError, ValueError, IndexError):
            pass
        
        # If all else fails, return original speaker_id
        return speaker_id
    
    def get_meeting_info(self):
        """Get current meeting information"""
        return {
            'meeting_id': self.meeting_id,
            'meeting_title': self.meeting_title,
            'participant_count': len(self.participants),
            'participants': self.participants,
            'detection_methods': list(set(
                p.get('detection_method', 'unknown') 
                for p in self.participants.values()
            ))
        }
    
    def set_teams_api_token(self, access_token):
        """Set Microsoft Graph API access token for enhanced participant detection"""
        self.access_token = access_token
        print("Teams API token configured for enhanced participant detection")
    
    def configure_detection_methods(self, **kwargs):
        """Configure which detection methods to use"""
        if 'window_detection' in kwargs:
            self.window_detection_enabled = kwargs['window_detection']
        if 'process_detection' in kwargs:
            self.process_detection_enabled = kwargs['process_detection']
        if 'network_detection' in kwargs:
            self.network_detection_enabled = kwargs['network_detection']
        
        print("Participant detection methods configured")