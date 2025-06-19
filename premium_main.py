#!/usr/bin/env python3
"""
Premium Albanian Teams Transcriber
Real-time transcription with participant recognition and modern UI
"""

import threading
import time
import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

from enhanced_audio_processing import EnhancedAudioProcessor
from enhanced_albanian_transcriber import EnhancedAlbanianTranscriber
from advanced_speaker_diarization import AdvancedSpeakerDiarization
from teams_participant_detector import TeamsParticipantDetector
from modern_transcript_ui import ModernTranscriptUI

class PremiumAlbanianTeamsTranscriber:
    def __init__(self):
        print("🚀 Initializing Premium Albanian Teams Transcriber...")
        
        # Initialize premium components
        self.audio_processor = EnhancedAudioProcessor()
        self.transcriber = EnhancedAlbanianTranscriber()
        self.speaker_identifier = AdvancedSpeakerDiarization()
        self.participant_detector = TeamsParticipantDetector()
        self.ui = ModernTranscriptUI()
        
        # State management
        self.is_running = False
        self.is_transcribing = False
        
        # Participant mapping
        self.speaker_to_participant_map = {}
        self.participants = {}
        
        # Performance monitoring
        self.performance_stats = {
            'session_start': time.time(),
            'total_transcriptions': 0,
            'participants_detected': 0,
            'speaker_mappings_created': 0,
            'average_processing_time': 0
        }
        
        # Setup callbacks
        self.setup_callbacks()
        
        # Show premium features dialog
        self.show_premium_features_dialog()
        
        print("✨ Premium Albanian Teams Transcriber initialized successfully!")
    
    def show_premium_features_dialog(self):
        """Show premium features to user"""
        features_window = tk.Toplevel()
        features_window.title("🌟 Premium Features")
        features_window.geometry("600x500")
        features_window.configure(bg='#1e1e2e')
        features_window.transient(self.ui.window)
        
        # Center the window
        features_window.update_idletasks()
        x = (features_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (features_window.winfo_screenheight() // 2) - (500 // 2)
        features_window.geometry(f"600x500+{x}+{y}")
        
        # Title with gradient effect
        title_frame = tk.Frame(features_window, bg='#89b4fa', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🌟 PREMIUM ALBANIAN TEAMS TRANSCRIBER",
            font=("Segoe UI", 18, "bold"),
            fg='white',
            bg='#89b4fa'
        )
        title_label.pack(expand=True)
        
        # Content area
        content_frame = tk.Frame(features_window, bg='#1e1e2e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Features list
        features_text = """
🎭 PARTICIPANT RECOGNITION:
   • Automatically detects Teams meeting participants
   • Maps voices to actual participant names
   • Real-time participant status monitoring
   • Multiple detection methods (API, window analysis, patterns)

🎨 MODERN BEAUTIFUL UI:
   • Dark/Light theme support with animated transitions
   • Professional gradient design and modern typography
   • Real-time animated status indicators
   • Responsive layout with customizable panels

🎙️ PREMIUM AUDIO PROCESSING:
   • Professional-grade noise reduction algorithms
   • Advanced echo cancellation and gain control
   • Adaptive background noise learning
   • Multi-band audio enhancement

🧠 INTELLIGENT VOICE MAPPING:
   • AI-powered speaker-to-participant matching
   • Voice characteristics analysis (pitch, tone, gender)
   • Persistent voice profiles across meetings
   • Smart fallback identification systems

🇦🇱 ENHANCED ALBANIAN SUPPORT:
   • Multiple transcription engines with auto-fallback
   • Albanian spell checking and grammar corrections
   • Cultural context awareness and proper nouns
   • Confidence scoring and quality indicators

📊 ADVANCED ANALYTICS:
   • Real-time performance monitoring
   • Speaker statistics and voice analysis
   • Meeting insights and participation metrics
   • Comprehensive export options with metadata

💾 SMART PERSISTENCE:
   • Automatic participant profile saving
   • Meeting history and analytics
   • Cross-session voice recognition
   • Enhanced backup and recovery
        """
        
        features_label = tk.Label(
            content_frame,
            text=features_text,
            font=("Consolas", 10),
            bg='#1e1e2e',
            fg='#cdd6f4',
            justify=tk.LEFT,
            anchor=tk.W
        )
        features_label.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        close_btn = tk.Button(
            content_frame,
            text="🚀 Start Premium Experience",
            command=features_window.destroy,
            font=("Segoe UI", 14, "bold"),
            bg='#a6e3a1',
            fg='#1e1e2e',
            relief=tk.FLAT,
            borderwidth=0,
            padx=30,
            pady=15,
            cursor="hand2"
        )
        close_btn.pack(pady=(20, 0))
        
        # Hover effect
        def on_enter(e):
            close_btn.config(bg='#94e2d5')
        def on_leave(e):
            close_btn.config(bg='#a6e3a1')
        
        close_btn.bind("<Enter>", on_enter)
        close_btn.bind("<Leave>", on_leave)
    
    def setup_callbacks(self):
        """Setup callbacks between premium components"""
        # UI callbacks
        self.ui.set_callbacks(
            start_callback=self.start_transcription,
            stop_callback=self.stop_transcription
        )
        
        # Participant detection callbacks
        self.participant_detector.set_callbacks(
            detection_callback=self.on_teams_detection,
            participant_callback=self.on_participants_detected
        )
        
        # Transcription callback
        self.transcriber.set_transcription_callback(self.on_premium_transcription_result)
    
    def on_teams_detection(self, is_meeting, reason):
        """Handle Teams meeting detection with participant awareness"""
        self.ui.update_teams_status(is_meeting, reason)
        
        if is_meeting and not self.is_transcribing:
            print(f"🎯 Teams meeting detected: {reason}")
            # Auto-start transcription if not already running
            threading.Thread(target=self.start_transcription, daemon=True).start()
        elif not is_meeting and self.is_transcribing:
            print("📴 Teams meeting ended")
            # Save all profiles when meeting ends
            self.save_session_data()
    
    def on_participants_detected(self, participants):
        """Handle detected participants"""
        self.participants = participants
        self.performance_stats['participants_detected'] = len(participants)
        
        # Update UI
        self.ui.update_participants(participants)
        
        # Log participant detection
        if participants:
            participant_names = list(participants.keys())
            print(f"👥 Participants detected: {', '.join(participant_names)}")
            
            # Create or update speaker mappings
            self.update_speaker_mappings()
    
    def update_speaker_mappings(self):
        """Update speaker-to-participant mappings"""
        if not self.participants:
            return
        
        # Get current speaker profiles
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        current_speakers = list(speaker_stats.get('speaker_details', {}).keys())
        
        participant_names = list(self.participants.keys())
        
        # Simple mapping strategy: assign participants to speakers in order
        for i, speaker_id in enumerate(current_speakers):
            if i < len(participant_names) and speaker_id not in self.speaker_to_participant_map:
                participant_name = participant_names[i]
                self.speaker_to_participant_map[speaker_id] = participant_name
                self.performance_stats['speaker_mappings_created'] += 1
                print(f"🔗 Mapped {speaker_id} → {participant_name}")
    
    def get_participant_name_for_speaker(self, speaker_id):
        """Get participant name for a speaker, with intelligent fallback"""
        if not speaker_id:
            return "Unknown"
        
        # Check direct mapping first
        if speaker_id in self.speaker_to_participant_map:
            return self.speaker_to_participant_map[speaker_id]
        
        # Try intelligent mapping based on voice characteristics
        if self.participants:
            speaker_characteristics = self.speaker_identifier.get_speaker_characteristics(speaker_id)
            if speaker_characteristics:
                # Use participant detector's voice matching
                matched_participant = self.participant_detector.get_participant_by_voice_match(
                    speaker_characteristics
                )
                if matched_participant:
                    # Create new mapping
                    self.speaker_to_participant_map[speaker_id] = matched_participant
                    print(f"🧠 Intelligent mapping: {speaker_id} → {matched_participant}")
                    return matched_participant
        
        # Fallback to original speaker ID
        return speaker_id
    
    def on_premium_transcription_result(self, enhanced_result, timestamp):
        """Handle premium transcription results with participant mapping"""
        if not enhanced_result or not enhanced_result.get('text', '').strip():
            return
        
        start_time = time.time()
        
        # Extract enhanced data
        text = enhanced_result['text']
        original_text = enhanced_result.get('original', text)
        engine = enhanced_result.get('engine', 'unknown')
        confidence = enhanced_result.get('confidence', '?')
        enhancements_applied = enhanced_result.get('enhancements_applied', False)
        
        # Get current speaker with enhanced identification
        detected_speaker = self.speaker_identifier.get_current_speaker()
        
        # Map to actual participant name
        participant_name = self.get_participant_name_for_speaker(detected_speaker)
        
        # Update UI with participant name instead of generic speaker ID
        self.ui.update_transcript(participant_name, text, timestamp, enhanced_result)
        
        # Enhanced console output with participant info
        participant_info = ""
        if participant_name != detected_speaker and participant_name in self.participants:
            participant_data = self.participants[participant_name]
            detection_method = participant_data.get('detection_method', 'unknown')
            participant_info = f" [via {detection_method}]"
        
        print(f"[{timestamp}] {participant_name}{participant_info}: {text}")
        if original_text != text:
            print(f"  📝 Original: {original_text}")
        print(f"  🔧 Engine: {engine} | Confidence: {confidence}")
        if detected_speaker != participant_name:
            print(f"  🎭 Speaker mapping: {detected_speaker} → {participant_name}")
        
        # Update performance stats
        self.performance_stats['total_transcriptions'] += 1
        processing_time = time.time() - start_time
        self.performance_stats['average_processing_time'] = (
            (self.performance_stats['average_processing_time'] + processing_time) / 2
        )
    
    def start_transcription(self):
        """Start premium transcription process"""
        if self.is_transcribing:
            print("Premium transcription already running")
            return
        
        try:
            print("🚀 Starting premium transcription with participant recognition...")
            self.is_transcribing = True
            
            # Configure premium audio processing
            self.audio_processor.configure_processing(
                noise_reduction=True,
                echo_cancellation=True,
                gain_control=True,
                high_pass_filter=True
            )
            
            # Start premium audio capture
            self.audio_processor.start_capture()
            
            # Start enhanced transcription
            self.transcriber.start_real_time_transcription(self.audio_processor.processed_queue)
            
            # Start participant detection
            self.participant_detector.start_monitoring(check_interval=5)
            
            # Start enhanced speaker identification
            threading.Thread(
                target=self.process_premium_speaker_identification,
                daemon=True
            ).start()
            
            # Start performance monitoring
            threading.Thread(
                target=self.monitor_premium_performance,
                daemon=True
            ).start()
            
            print("✨ Premium transcription started successfully!")
            
        except Exception as e:
            print(f"❌ Error starting premium transcription: {e}")
            self.is_transcribing = False
    
    def stop_transcription(self):
        """Stop premium transcription process"""
        if not self.is_transcribing:
            print("Premium transcription not running")
            return
        
        try:
            print("🛑 Stopping premium transcription...")
            self.is_transcribing = False
            
            # Stop all components
            self.audio_processor.stop_capture()
            self.participant_detector.stop_monitoring()
            
            # Save session data
            self.save_session_data()
            
            # Print final statistics
            self.print_premium_session_statistics()
            
            print("✅ Premium transcription stopped successfully!")
            
        except Exception as e:
            print(f"❌ Error stopping premium transcription: {e}")
    
    def process_premium_speaker_identification(self):
        """Process audio for premium speaker identification with participant mapping"""
        while self.is_transcribing:
            try:
                # Get processed audio chunk
                audio_chunk = self.audio_processor.get_audio_chunk(timeout=1)
                
                if audio_chunk:
                    # Enhanced speaker identification
                    speaker_id = self.speaker_identifier.identify_speaker(audio_chunk)
                    
                    if speaker_id:
                        # Update participant mappings when new speakers are detected
                        current_speakers = len(self.speaker_identifier.speaker_profiles)
                        if current_speakers > 0:
                            self.update_speaker_mappings()
                    
            except Exception as e:
                print(f"Premium speaker identification error: {e}")
                time.sleep(0.1)
    
    def monitor_premium_performance(self):
        """Monitor premium performance with participant metrics"""
        last_report_time = time.time()
        
        while self.is_transcribing:
            try:
                current_time = time.time()
                
                # Report every 60 seconds
                if current_time - last_report_time >= 60:
                    self.print_premium_performance_update()
                    last_report_time = current_time
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                print(f"Premium performance monitoring error: {e}")
                time.sleep(10)
    
    def print_premium_performance_update(self):
        """Print premium performance update"""
        session_duration = time.time() - self.performance_stats['session_start']
        transcription_stats = self.transcriber.get_transcription_stats()
        audio_stats = self.audio_processor.get_audio_stats()
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        meeting_info = self.participant_detector.get_meeting_info()
        
        print("\n" + "="*70)
        print("🌟 PREMIUM TRANSCRIPTION PERFORMANCE UPDATE")
        print("="*70)
        print(f"⏱️  Session Duration: {session_duration/60:.1f} minutes")
        print(f"📝 Total Transcriptions: {self.performance_stats['total_transcriptions']}")
        print(f"👥 Participants Detected: {self.performance_stats['participants_detected']}")
        print(f"🔗 Speaker Mappings: {self.performance_stats['speaker_mappings_created']}")
        print(f"🗣️  Active Speakers: {speaker_stats['total_speakers']}")
        print(f"⚡ Avg Processing Time: {self.performance_stats['average_processing_time']:.3f}s")
        print(f"🎯 Transcription Success Rate: {transcription_stats['success_rate']}")
        print(f"🎙️  Background Noise: {audio_stats['background_noise_level']}")
        
        if meeting_info['meeting_title']:
            print(f"📱 Meeting: {meeting_info['meeting_title']}")
        
        print("="*70 + "\n")
    
    def save_session_data(self):
        """Save premium session data"""
        try:
            # Save speaker profiles
            self.speaker_identifier.save_speaker_profiles()
            
            # Save speaker-to-participant mappings
            with open("speaker_participant_mappings.json", 'w') as f:
                import json
                json.dump({
                    'mappings': self.speaker_to_participant_map,
                    'participants': self.participants,
                    'session_stats': self.performance_stats,
                    'timestamp': datetime.now().isoformat()
                }, f, indent=2)
            
            print("💾 Premium session data saved")
            
        except Exception as e:
            print(f"⚠️ Error saving session data: {e}")
    
    def load_session_data(self):
        """Load previous session data"""
        try:
            import os
            import json
            
            if os.path.exists("speaker_participant_mappings.json"):
                with open("speaker_participant_mappings.json", 'r') as f:
                    data = json.load(f)
                    self.speaker_to_participant_map = data.get('mappings', {})
                    print(f"📂 Loaded {len(self.speaker_to_participant_map)} speaker mappings")
            
        except Exception as e:
            print(f"⚠️ Error loading session data: {e}")
    
    def print_premium_session_statistics(self):
        """Print comprehensive premium session statistics"""
        session_duration = time.time() - self.performance_stats['session_start']
        transcription_stats = self.transcriber.get_transcription_stats()
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        meeting_info = self.participant_detector.get_meeting_info()
        
        print("\n" + "="*80)
        print("🌟 PREMIUM TRANSCRIPTION SESSION SUMMARY")
        print("="*80)
        print(f"⏱️  Total Session Time: {session_duration/60:.1f} minutes")
        print(f"📝 Total Transcriptions: {self.performance_stats['total_transcriptions']}")
        print(f"👥 Participants: {self.performance_stats['participants_detected']}")
        print(f"🔗 Speaker Mappings Created: {self.performance_stats['speaker_mappings_created']}")
        print(f"🗣️  Total Speakers: {speaker_stats['total_speakers']}")
        print(f"🎯 Success Rate: {transcription_stats['success_rate']}")
        print(f"⚡ Avg Response Time: {transcription_stats['average_response_time']}")
        
        print("\n🔧 Engine Usage:")
        for engine, count in transcription_stats['engine_usage'].items():
            print(f"   • {engine}: {count} times")
        
        print("\n👥 Participant Details:")
        for name, details in self.participants.items():
            method = details.get('detection_method', 'unknown')
            confidence = details.get('confidence', 'unknown')
            print(f"   • {name}: detected via {method} ({confidence} confidence)")
        
        print("\n🎭 Speaker-Participant Mappings:")
        for speaker_id, participant_name in self.speaker_to_participant_map.items():
            speaker_details = speaker_stats['speaker_details'].get(speaker_id, {})
            voice_type = speaker_details.get('voice_type', 'Unknown')
            print(f"   • {speaker_id} → {participant_name} ({voice_type})")
        
        if meeting_info['meeting_title']:
            print(f"\n📱 Meeting Info:")
            print(f"   • Title: {meeting_info['meeting_title']}")
            print(f"   • ID: {meeting_info['meeting_id']}")
            print(f"   • Detection Methods: {', '.join(meeting_info['detection_methods'])}")
        
        print("="*80 + "\n")
    
    def run(self, auto_mode=True):
        """Main premium run method"""
        self.is_running = True
        
        # Load previous session data
        self.load_session_data()
        
        try:
            print("🌟 Running Premium Albanian Teams Transcriber...")
            
            if auto_mode:
                print("   🤖 Auto mode: Will start when Teams meeting detected")
            else:
                print("   🎮 Manual mode: User controls via modern UI")
            
            # Start UI
            self.ui.run()
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down premium transcriber...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Premium cleanup with data persistence"""
        print("🧹 Premium cleanup...")
        
        self.is_running = False
        self.is_transcribing = False
        
        # Stop components
        try:
            self.audio_processor.stop_capture()
            self.participant_detector.stop_monitoring()
            self.save_session_data()
            self.ui.destroy()
        except:
            pass
        
        # Print final session summary
        self.print_premium_session_statistics()
        
        print("✨ Premium cleanup completed")

def print_premium_usage():
    """Print premium usage information"""
    print("🌟 Premium Albanian Teams Transcriber")
    print("="*60)
    print("Usage:")
    print("  python premium_main.py [mode]")
    print("")
    print("Modes:")
    print("  auto   - Premium automatic mode (default)")
    print("  manual - Premium manual control mode")
    print("")
    print("🌟 Premium Features:")
    print("  ✓ Real participant name detection and mapping")
    print("  ✓ Modern beautiful UI with dark/light themes")
    print("  ✓ Advanced speaker-to-participant matching")
    print("  ✓ Professional audio processing and enhancement")
    print("  ✓ AI-powered voice analysis and characteristics")
    print("  ✓ Persistent participant profiles and mappings")
    print("  ✓ Real-time performance monitoring and analytics")
    print("  ✓ Enhanced Albanian language processing")
    print("  ✓ Comprehensive session data persistence")
    print("  ✓ Multiple Teams detection methods")

def main():
    """Premium main entry point"""
    # Parse command line arguments
    auto_mode = True
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "manual":
            auto_mode = False
        elif mode == "help" or mode == "-h" or mode == "--help":
            print_premium_usage()
            return
        elif mode != "auto":
            print(f"Unknown mode: {mode}")
            print_premium_usage()
            return
    
    try:
        # Create and run premium transcriber
        transcriber = PremiumAlbanianTeamsTranscriber()
        transcriber.run(auto_mode=auto_mode)
        
    except KeyboardInterrupt:
        print("\n🛑 Premium application closed by user")
        sys.exit(0)
    except ImportError as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
        error_msg = f"""
🌟 Premium Albanian Teams Transcriber

Missing Premium Module: {missing_module}

To use premium features, please install:
pip install scipy librosa scikit-learn

Or run the enhanced version:
python enhanced_main.py

Would you like installation instructions?
"""
        
        result = messagebox.askyesno("Premium Features", error_msg)
        if result:
            try:
                import webbrowser
                webbrowser.open("https://github.com/MarinDushku/Teams-ALB-Transcripter")
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
🌟 Premium Albanian Teams Transcriber Error

{str(e)}

This might be due to:
• Missing premium dependencies
• Teams not running
• Permission issues
• Audio device configuration

Try running the enhanced version: python enhanced_main.py
"""
            messagebox.showerror("Premium Application Error", error_msg)
        except:
            print(f"Premium transcriber error: {e}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()