#!/usr/bin/env python3
"""
Working Albanian Teams Transcriber
Uses OpenAI Whisper instead of problematic Albanian ASR
"""

import threading
import time
import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import numpy as np

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

class WorkingAlbanianTranscriber:
    def __init__(self):
        print("🎭 Starting Albanian Teams Transcriber...")
        
        # Initialize UI first
        self.ui = LiveTranscriptUI()
        
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
        """Main transcription loop"""
        audio_buffer = []
        
        while self.is_recording:
            try:
                # Read audio data
                if self.audio_stream:
                    data = self.audio_stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_buffer.append(data)
                
                # Process every 3 seconds of audio
                if len(audio_buffer) >= (self.sample_rate * 3) // self.chunk_size:
                    self.process_audio_buffer(audio_buffer)
                    audio_buffer = []
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"⚠ Transcription error: {e}")
                time.sleep(1)
    
    def process_audio_buffer(self, audio_buffer):
        """Process accumulated audio buffer"""
        try:
            # Convert audio buffer to numpy array
            audio_data = b''.join(audio_buffer)
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Transcribe with available method
            text = self.transcribe_audio(audio_np)
            
            if text and text.strip():
                print(f"🎯 Transcribed: {text}")
                self.ui.add_transcript_entry("Speaker", text, datetime.now())
                
        except Exception as e:
            print(f"⚠ Audio processing error: {e}")
    
    def transcribe_audio(self, audio_data):
        """Transcribe audio using available method"""
        try:
            if self.whisper_model is not None:
                # Use Whisper for transcription
                result = self.whisper_model.transcribe(audio_data, language='sq')  # 'sq' for Albanian
                return result['text'].strip()
            else:
                # Fallback to basic speech recognition
                return self.fallback_transcription(audio_data)
                
        except Exception as e:
            print(f"⚠ Transcription error: {e}")
            return ""
    
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