#!/usr/bin/env python3
"""
Albanian Teams Transcriber
Real-time transcription app for Microsoft Teams meetings in Albanian language
"""

import threading
import time
import sys
from datetime import datetime

from audio_capture import TeamsAudioCapture
from albanian_transcriber import AlbanianRealTimeTranscriber
from teams_detector import TeamsDetector
from speaker_identifier import SpeakerIdentifier
from live_transcript_ui import LiveTranscriptUI

class AlbanianTeamsTranscriber:
    def __init__(self):
        print("Initializing Albanian Teams Transcriber...")
        
        # Initialize components
        self.audio_capture = TeamsAudioCapture()
        self.transcriber = AlbanianRealTimeTranscriber()
        self.speaker_identifier = SpeakerIdentifier()
        self.teams_detector = TeamsDetector()
        self.ui = LiveTranscriptUI()
        
        # State management
        self.is_running = False
        self.is_transcribing = False
        
        # Setup callbacks
        self.setup_callbacks()
        
        print("Albanian Teams Transcriber initialized successfully!")
    
    def setup_callbacks(self):
        """Setup callbacks between components"""
        # UI callbacks
        self.ui.set_callbacks(
            start_callback=self.start_transcription,
            stop_callback=self.stop_transcription
        )
        
        # Teams detection callback
        self.teams_detector.set_detection_callback(self.on_teams_detection)
        
        # Transcription callback
        self.transcriber.set_transcription_callback(self.on_transcription_result)
    
    def on_teams_detection(self, is_meeting, reason):
        """Handle Teams meeting detection"""
        self.ui.update_teams_status(is_meeting, reason)
        
        if is_meeting and not self.is_transcribing:
            print(f"Teams meeting detected: {reason}")
            # Auto-start transcription if not already running
            threading.Thread(target=self.start_transcription, daemon=True).start()
        elif not is_meeting and self.is_transcribing:
            print("Teams meeting ended")
            # Optionally auto-stop transcription
            # self.stop_transcription()
    
    def on_transcription_result(self, text, timestamp):
        """Handle transcription results"""
        if not text.strip():
            return
        
        # Get current speaker (if any)
        current_speaker = self.speaker_identifier.get_current_speaker()
        
        # Update UI
        self.ui.update_transcript(current_speaker, text, timestamp)
        
        # Print to console for debugging
        print(f"[{timestamp}] {current_speaker or 'Unknown'}: {text}")
    
    def start_transcription(self):
        """Start the transcription process"""
        if self.is_transcribing:
            print("Transcription already running")
            return
        
        try:
            print("Starting transcription...")
            self.is_transcribing = True
            
            # Start audio capture
            self.audio_capture.start_capture()
            
            # Start transcription processing
            self.transcriber.start_real_time_transcription(self.audio_capture.audio_queue)
            
            # Start speaker identification processing
            threading.Thread(
                target=self.process_speaker_identification,
                daemon=True
            ).start()
            
            print("Transcription started successfully!")
            
        except Exception as e:
            print(f"Error starting transcription: {e}")
            self.is_transcribing = False
    
    def stop_transcription(self):
        """Stop the transcription process"""
        if not self.is_transcribing:
            print("Transcription not running")
            return
        
        try:
            print("Stopping transcription...")
            self.is_transcribing = False
            
            # Stop audio capture
            self.audio_capture.stop_capture()
            
            print("Transcription stopped successfully!")
            
        except Exception as e:
            print(f"Error stopping transcription: {e}")
    
    def process_speaker_identification(self):
        """Process audio for speaker identification"""
        while self.is_transcribing:
            try:
                # Get audio chunk
                audio_chunk = self.audio_capture.get_audio_chunk(timeout=1)
                
                if audio_chunk:
                    # Identify speaker
                    self.speaker_identifier.identify_speaker(audio_chunk)
                    
            except Exception as e:
                print(f"Speaker identification error: {e}")
                time.sleep(0.1)
    
    def run_auto_mode(self):
        """Run in automatic mode - wait for Teams and start transcription"""
        print("Running in automatic mode...")
        print("Waiting for Microsoft Teams meeting...")
        
        # Start Teams monitoring
        self.teams_detector.start_monitoring(check_interval=5)
        
        # Start UI
        self.ui.run()
    
    def run_manual_mode(self):
        """Run in manual mode - user controls transcription"""
        print("Running in manual mode...")
        print("Use the UI to start/stop transcription manually")
        
        # Start Teams monitoring (for status display)
        self.teams_detector.start_monitoring(check_interval=10)
        
        # Start UI
        self.ui.run()
    
    def run(self, auto_mode=True):
        """Main run method"""
        self.is_running = True
        
        try:
            if auto_mode:
                self.run_auto_mode()
            else:
                self.run_manual_mode()
                
        except KeyboardInterrupt:
            print("\nShutting down...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        print("Cleaning up...")
        
        self.is_running = False
        self.is_transcribing = False
        
        # Stop components
        try:
            self.audio_capture.stop_capture()
            self.teams_detector.stop_monitoring()
            self.ui.destroy()
        except:
            pass
        
        print("Cleanup completed")

def print_usage():
    """Print usage information"""
    print("Albanian Teams Transcriber")
    print("=" * 40)
    print("Usage:")
    print("  python main.py [mode]")
    print("")
    print("Modes:")
    print("  auto   - Automatically start transcription when Teams meeting detected (default)")
    print("  manual - Manual control via UI")
    print("")
    print("Features:")
    print("  ✓ Real-time Albanian speech transcription")
    print("  ✓ Automatic Teams meeting detection")
    print("  ✓ Speaker identification and diarization")
    print("  ✓ Live transcript display")
    print("  ✓ Export to multiple formats (TXT, JSON, DOCX)")
    print("  ✓ Auto-save functionality")
    print("")
    print("Requirements:")
    print("  - Microsoft Teams")
    print("  - System audio access")
    print("  - Albanian ASR model (see setup instructions)")

def main():
    """Main entry point"""
    # Parse command line arguments
    auto_mode = True
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "manual":
            auto_mode = False
        elif mode == "help" or mode == "-h" or mode == "--help":
            print_usage()
            return
        elif mode != "auto":
            print(f"Unknown mode: {mode}")
            print_usage()
            return
    
    try:
        # Create and run transcriber
        transcriber = AlbanianTeamsTranscriber()
        transcriber.run(auto_mode=auto_mode)
        
    except KeyboardInterrupt:
        print("\nApplication closed by user")
        sys.exit(0)
    except ImportError as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
        error_msg = f"""
Missing Required Module: {missing_module}

To fix this, please run:
pip install -r requirements.txt

Or install the specific module:
pip install {missing_module}

Would you like to open the setup guide?
"""
        
        result = messagebox.askyesno("Missing Dependencies", error_msg)
        if result:
            try:
                import webbrowser
                webbrowser.open("https://python.org")
            except:
                pass
        
        sys.exit(1)
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        
        try:
            root = tk.Tk()
            root.withdraw()
            
            error_msg = f"""
Albanian Teams Transcriber Error

{str(e)}

This might be due to:
• Missing audio drivers
• Teams not running
• Permission issues
• Missing dependencies

Check the console output for more details.
"""
            messagebox.showerror("Application Error", error_msg)
        except:
            print(f"Fatal error: {e}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()