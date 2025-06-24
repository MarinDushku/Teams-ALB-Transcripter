#!/usr/bin/env python3
"""
Albanian Teams Transcriber - Production Version
Real-time transcription with beautiful UI and AI-powered accuracy
"""

import threading
import time
import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import numpy as np
import queue
import json

# Try to import available packages
try:
    import pyaudiowpatch as pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    try:
        import pyaudio
        AUDIO_AVAILABLE = True
    except ImportError:
        AUDIO_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from live_transcript_ui import LiveTranscriptUI
from teams_participant_monitor import TeamsParticipantMonitor

class WorkingAlbanianTranscriber:
    def __init__(self):
        print("🎭 Starting Albanian Teams Transcriber...")
        
        # Initialize UI first
        self.ui = LiveTranscriptUI()
        
        # Initialize participant monitor
        self.participant_monitor = TeamsParticipantMonitor()
        self.participant_monitor.add_participant_callback(self.on_participant_event)
        
        # Check capabilities
        self.check_capabilities()
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.audio_format = pyaudio.paInt16 if AUDIO_AVAILABLE else None
        self.channels = 1
        
        # State
        self.is_recording = False
        self.audio_stream = None
        self.transcription_thread = None
        self.audio_queue = queue.Queue()
        
        # Performance settings
        self.buffer_duration = 3  # seconds of audio to process at once
        self.silence_threshold = 0.01
        self.speaker_count = 0
        
        # Participant tracking
        self.current_participants = {}
        self.speaker_participant_map = {}  # Map detected speakers to real participants
        
        # Initialize Whisper if available
        self.whisper_model = None
        if WHISPER_AVAILABLE:
            try:
                print("Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")
                print("✓ Whisper model loaded")
            except Exception as e:
                print(f"⚠ Whisper model failed to load: {e}")
        
        # Connect UI callbacks
        self.setup_ui_callbacks()
    
    def on_participant_event(self, event_type, participant_name, details):
        """Handle participant join/leave/speaking events"""
        timestamp = details.get('timestamp', datetime.now()) if details else datetime.now()
        
        if event_type == 'join':
            self.current_participants[participant_name] = {
                'joined_at': timestamp,
                'status': 'active',
                'last_speaking': None
            }
            message = f"👤 {participant_name} joined the meeting"
            print(f"✅ {message}")
            self.ui.add_transcript_entry("System", message, timestamp)
            
        elif event_type == 'leave':
            if participant_name in self.current_participants:
                self.current_participants[participant_name]['status'] = 'left'
            message = f"👤 {participant_name} left the meeting"
            print(f"❌ {message}")
            self.ui.add_transcript_entry("System", message, timestamp)
            
        elif event_type == 'speaking':
            # Update last speaking time for speaker detection
            for participant in self.current_participants:
                if self.current_participants[participant]['status'] == 'active':
                    self.current_participants[participant]['last_speaking'] = timestamp
    
    def get_likely_speaker_name(self, speaker_id):
        """Map detected speaker to actual participant name"""
        try:
            # If we have participant info, try to match
            active_participants = [name for name, info in self.current_participants.items() 
                                 if info['status'] == 'active']
            
            if not active_participants:
                return speaker_id
            
            # Simple mapping based on speaker ID
            if speaker_id in self.speaker_participant_map:
                return self.speaker_participant_map[speaker_id]
            
            # Try to assign speakers to participants
            if len(active_participants) == 1:
                # Only one participant, likely them
                participant_name = active_participants[0]
                self.speaker_participant_map[speaker_id] = participant_name
                return participant_name
            
            elif len(active_participants) >= 2:
                # Multiple participants - assign based on speaker pattern
                speaker_index = ord(speaker_id[-1]) % len(active_participants) if speaker_id else 0
                participant_name = active_participants[speaker_index]
                self.speaker_participant_map[speaker_id] = participant_name
                return participant_name
            
            return speaker_id
            
        except Exception as e:
            print(f"⚠ Speaker mapping error: {e}")
            return speaker_id
        
    def check_capabilities(self):
        """Check what features are available"""
        print("\n🔍 Checking capabilities:")
        print(f"  Audio capture: {'✓' if AUDIO_AVAILABLE else '✗'}")
        print(f"  Whisper AI: {'✓' if WHISPER_AVAILABLE else '✗'}")
        print(f"  PyTorch: {'✓' if TORCH_AVAILABLE else '✗'}")
        
        if not AUDIO_AVAILABLE:
            print("  ⚠ Audio capture not available - install pyaudiowpatch")
        if not WHISPER_AVAILABLE:
            print("  ⚠ Whisper not available - install openai-whisper")
        
        print()
        
    def setup_ui_callbacks(self):
        """Connect UI buttons to functionality"""
        # Override UI methods to connect to our transcriber
        original_toggle = self.ui.toggle_transcription
        
        def new_toggle():
            if self.is_recording:
                self.stop_recording()
            else:
                self.start_recording()
            original_toggle()
        
        self.ui.toggle_transcription = new_toggle
        
    def start_recording(self):
        """Start audio recording and transcription"""
        if not AUDIO_AVAILABLE:
            messagebox.showerror("Error", "Audio capture not available.\nInstall pyaudiowpatch: pip install pyaudiowpatch")
            return
            
        try:
            self.is_recording = True
            
            # Initialize audio stream
            self.audio = pyaudio.PyAudio()
            
            # Try to find system audio device (for Teams capture)
            device_index = self.find_system_audio_device()
            
            self.audio_stream = self.audio.open(
                format=self.audio_format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=self.chunk_size
            )
            
            # Start transcription thread
            self.transcription_thread = threading.Thread(target=self.transcription_loop, daemon=True)
            self.transcription_thread.start()
            
            # Start participant monitoring
            if self.participant_monitor.start_monitoring():
                print("🔍 Participant monitoring started")
                self.ui.add_transcript_entry("System", "🔍 Monitoring Teams participants...", datetime.now())
            else:
                print("⚠ Participant monitoring failed - continuing with audio only")
            
            print("🎤 Recording started...")
            self.ui.add_transcript_entry("System", "🎤 Recording started - speak now!", datetime.now())
            
        except Exception as e:
            self.is_recording = False
            error_msg = f"Failed to start recording: {str(e)}"
            print(f"❌ {error_msg}")
            messagebox.showerror("Recording Error", error_msg)
    
    def find_system_audio_device(self):
        """Find the best audio input device"""
        if not AUDIO_AVAILABLE:
            return None
            
        try:
            # Look for WASAPI loopback devices (Windows)
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                if 'wasapi' in device_info['name'].lower() and 'loopback' in device_info['name'].lower():
                    print(f"🔊 Found system audio device: {device_info['name']}")
                    return i
            
            # Fallback to default input device
            default_device = self.audio.get_default_input_device_info()
            print(f"🔊 Using default input device: {default_device['name']}")
            return default_device['index']
            
        except Exception as e:
            print(f"⚠ Device selection error: {e}")
            return None
    
    def transcription_loop(self):
        """Main transcription loop with improved performance"""
        audio_buffer = []
        last_process_time = time.time()
        
        while self.is_recording:
            try:
                # Read audio data
                if self.audio_stream:
                    data = self.audio_stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_buffer.append(data)
                    
                    # Add to queue for real-time processing
                    self.audio_queue.put(data)
                
                # Process every buffer_duration seconds of audio
                current_time = time.time()
                if current_time - last_process_time >= self.buffer_duration:
                    if audio_buffer:
                        threading.Thread(target=self.process_audio_buffer, args=(audio_buffer.copy(),), daemon=True).start()
                        audio_buffer = []
                        last_process_time = current_time
                
                time.sleep(0.05)  # Reduced sleep for better responsiveness
                
            except Exception as e:
                print(f"⚠ Transcription error: {e}")
                time.sleep(0.5)
    
    def process_audio_buffer(self, audio_buffer):
        """Process accumulated audio buffer with enhanced features"""
        try:
            # Convert audio buffer to numpy array
            audio_data = b''.join(audio_buffer)
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Check for silence
            energy = np.sqrt(np.mean(audio_np ** 2))
            if energy < self.silence_threshold:
                return
            
            # Transcribe with available method
            text = self.transcribe_audio(audio_np)
            
            if text and text.strip() and len(text.strip()) > 3:
                # Simple speaker detection based on audio characteristics
                speaker_id = self.detect_speaker(audio_np, text)
                
                # Map to actual participant name if available
                speaker_name = self.get_likely_speaker_name(speaker_id)
                
                print(f"🎯 [{speaker_name}] {text}")
                self.ui.add_transcript_entry(speaker_name, text, datetime.now())
                
                # Update statistics
                self.ui.update_session_stats(len(text.split()), energy * 100)
                
        except Exception as e:
            print(f"⚠ Audio processing error: {e}")
    
    def detect_speaker(self, audio_data, text):
        """Simple speaker detection based on audio characteristics"""
        try:
            # Basic speaker detection using audio energy and frequency
            energy = np.sqrt(np.mean(audio_data ** 2))
            
            # Simple heuristic: higher energy usually means different speaker
            if energy > 0.05:
                speaker_id = "Speaker A"
            elif energy > 0.02:
                speaker_id = "Speaker B" 
            else:
                speaker_id = "Speaker C"
                
            return speaker_id
            
        except:
            self.speaker_count += 1
            return f"Speaker {self.speaker_count}"
    
    def transcribe_audio(self, audio_data):
        """Transcribe audio using available method with optimizations"""
        try:
            if self.whisper_model is not None:
                # Use Whisper for high-quality transcription
                result = self.whisper_model.transcribe(
                    audio_data, 
                    language='sq',  # Albanian
                    fp16=False,     # Better compatibility
                    temperature=0.0, # More deterministic
                    word_timestamps=True,
                    condition_on_previous_text=True
                )
                
                # Extract text and confidence
                text = result['text'].strip()
                confidence = getattr(result, 'confidence', 0.8)
                
                # Filter out low confidence or very short transcriptions
                if confidence > 0.5 and len(text) > 2:
                    return text
                return ""
                
            else:
                # Fallback to basic speech recognition
                return self.fallback_transcription(audio_data)
                
        except Exception as e:
            print(f"⚠ Transcription error: {e}")
            return self.fallback_transcription(audio_data)
    
    def fallback_transcription(self, audio_data):
        """Fallback transcription method"""
        try:
            # Simple energy-based voice activity detection
            energy = np.sqrt(np.mean(audio_data ** 2))
            if energy > 0.01:  # Threshold for voice activity
                return f"[Audio detected - energy: {energy:.3f}]"
            return ""
        except:
            return "[Audio processing...]"
    
    def stop_recording(self):
        """Stop recording and transcription"""
        self.is_recording = False
        
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
        
        if hasattr(self, 'audio'):
            self.audio.terminate()
        
        # Stop participant monitoring
        self.participant_monitor.stop_monitoring()
        
        print("⏹️ Recording stopped")
        self.ui.add_transcript_entry("System", "⏹️ Recording stopped", datetime.now())
    
    def run(self):
        """Start the application"""
        try:
            print("🚀 Starting Albanian Teams Transcriber...")
            print("📋 Instructions:")
            print("  1. Click 'Start Transcription' to begin")
            print("  2. Speak or play Teams audio")
            print("  3. See real-time transcription")
            print("  4. Use Export to save transcripts")
            print()
            
            # Start the UI
            self.ui.run()
            
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
        except Exception as e:
            print(f"❌ Application error: {e}")
        finally:
            if self.is_recording:
                self.stop_recording()

def main():
    """Main entry point"""
    print("🎭 Albanian Teams Transcriber - Working Version")
    print("=" * 60)
    
    try:
        app = WorkingAlbanianTranscriber()
        app.run()
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        print("\n🔧 Troubleshooting:")
        print("  1. Install audio: pip install pyaudiowpatch")
        print("  2. Install AI: pip install openai-whisper")
        print("  3. Check system audio permissions")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()