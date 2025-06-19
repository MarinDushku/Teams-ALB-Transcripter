#!/usr/bin/env python3
"""
Enhanced Albanian Teams Transcriber
Real-time transcription app with advanced capabilities
"""

import threading
import time
import sys
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

from enhanced_audio_processing import EnhancedAudioProcessor
from enhanced_albanian_transcriber import EnhancedAlbanianTranscriber
from advanced_speaker_diarization import AdvancedSpeakerDiarization
from teams_detector import TeamsDetector
from live_transcript_ui import LiveTranscriptUI

class EnhancedAlbanianTeamsTranscriber:
    def __init__(self):
        print("Initializing Enhanced Albanian Teams Transcriber...")
        
        # Initialize enhanced components
        self.audio_processor = EnhancedAudioProcessor()
        self.transcriber = EnhancedAlbanianTranscriber()
        self.speaker_identifier = AdvancedSpeakerDiarization()
        self.teams_detector = TeamsDetector()
        self.ui = LiveTranscriptUI()
        
        # State management
        self.is_running = False
        self.is_transcribing = False
        
        # Performance monitoring
        self.performance_stats = {
            'session_start': time.time(),
            'total_transcriptions': 0,
            'total_speakers_detected': 0,
            'average_processing_time': 0
        }
        
        # Setup callbacks
        self.setup_callbacks()
        
        # Show capabilities dialog
        self.show_capabilities_dialog()
        
        print("Enhanced Albanian Teams Transcriber initialized successfully!")
    
    def show_capabilities_dialog(self):
        """Show enhanced capabilities to user"""
        capabilities_window = tk.Toplevel()
        capabilities_window.title("Enhanced Features")
        capabilities_window.geometry("500x400")
        capabilities_window.configure(bg='white')
        
        # Title
        title_label = tk.Label(
            capabilities_window,
            text="🚀 Enhanced Albanian Teams Transcriber",
            font=("Arial", 16, "bold"),
            bg='white',
            fg='#2196F3'
        )
        title_label.pack(pady=10)
        
        # Features list
        features_text = """
✨ ENHANCED FEATURES ACTIVE ✨

🎙️ ADVANCED AUDIO PROCESSING:
   • Intelligent noise reduction
   • Echo cancellation
   • Automatic gain control
   • High-pass filtering for clarity

🗣️ SUPERIOR SPEAKER IDENTIFICATION:
   • Voice embeddings and clustering
   • Pitch and spectral analysis
   • Persistent speaker profiles
   • Voice type classification

🇦🇱 ENHANCED ALBANIAN TRANSCRIPTION:
   • Multiple transcription engines
   • Automatic fallback systems
   • Albanian spell checking
   • Grammar corrections
   • Confidence indicators

📊 INTELLIGENT PROCESSING:
   • Real-time performance monitoring
   • Adaptive audio sensitivity
   • Background noise learning
   • Processing statistics

💾 SMART PERSISTENCE:
   • Speaker profile memory
   • Performance tracking
   • Enhanced export options
        """
        
        features_label = tk.Label(
            capabilities_window,
            text=features_text,
            font=("Arial", 10),
            bg='white',
            justify=tk.LEFT,
            anchor=tk.W
        )
        features_label.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Close button
        close_btn = tk.Button(
            capabilities_window,
            text="Start Enhanced Transcription",
            command=capabilities_window.destroy,
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='white'
        )
        close_btn.pack(pady=10)
    
    def setup_callbacks(self):
        """Setup callbacks between enhanced components"""
        # UI callbacks
        self.ui.set_callbacks(
            start_callback=self.start_transcription,
            stop_callback=self.stop_transcription
        )
        
        # Teams detection callback
        self.teams_detector.set_detection_callback(self.on_teams_detection)
        
        # Transcription callback
        self.transcriber.set_transcription_callback(self.on_enhanced_transcription_result)
    
    def on_teams_detection(self, is_meeting, reason):
        """Handle Teams meeting detection with enhanced logging"""
        self.ui.update_teams_status(is_meeting, reason)
        
        if is_meeting and not self.is_transcribing:
            print(f"🎯 Teams meeting detected: {reason}")
            # Auto-start transcription if not already running
            threading.Thread(target=self.start_transcription, daemon=True).start()
        elif not is_meeting and self.is_transcribing:
            print("📴 Teams meeting ended")
            # Save speaker profiles when meeting ends
            self.speaker_identifier.save_speaker_profiles()
    
    def on_enhanced_transcription_result(self, enhanced_result, timestamp):
        """Handle enhanced transcription results"""
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
        current_speaker = self.speaker_identifier.get_current_speaker()
        
        # Create enhanced display text
        display_text = text
        if enhancements_applied:
            display_text += f" ✨"  # Indicator for enhanced text
        
        # Add confidence and engine info for debugging
        if confidence and confidence != '?':
            display_text += f" ({confidence})"
        
        # Update UI with enhanced information
        self.ui.update_transcript(current_speaker, display_text, timestamp)
        
        # Enhanced console output
        speaker_info = ""
        if current_speaker:
            characteristics = self.speaker_identifier.get_speaker_characteristics(current_speaker)
            if characteristics:
                voice_type = characteristics.get('voice_type', 'Unknown')
                speaker_info = f" [{voice_type}]"
        
        print(f"[{timestamp}] {current_speaker or 'Unknown'}{speaker_info}: {text}")
        if original_text != text:
            print(f"  📝 Original: {original_text}")
        print(f"  🔧 Engine: {engine} | Confidence: {confidence}")
        
        # Update performance stats
        self.performance_stats['total_transcriptions'] += 1
        processing_time = time.time() - start_time
        self.performance_stats['average_processing_time'] = (
            (self.performance_stats['average_processing_time'] + processing_time) / 2
        )
    
    def start_transcription(self):
        """Start enhanced transcription process"""
        if self.is_transcribing:
            print("Enhanced transcription already running")
            return
        
        try:
            print("🚀 Starting enhanced transcription...")
            self.is_transcribing = True
            
            # Configure audio processing
            self.audio_processor.configure_processing(
                noise_reduction=True,
                echo_cancellation=True,
                gain_control=True,
                high_pass_filter=True
            )
            
            # Start enhanced audio capture
            self.audio_processor.start_capture()
            
            # Start enhanced transcription processing
            self.transcriber.start_real_time_transcription(self.audio_processor.processed_queue)
            
            # Start enhanced speaker identification
            threading.Thread(
                target=self.process_enhanced_speaker_identification,
                daemon=True
            ).start()
            
            # Start performance monitoring
            threading.Thread(
                target=self.monitor_performance,
                daemon=True
            ).start()
            
            print("✅ Enhanced transcription started successfully!")
            
        except Exception as e:
            print(f"❌ Error starting enhanced transcription: {e}")
            self.is_transcribing = False
    
    def stop_transcription(self):
        """Stop enhanced transcription process"""
        if not self.is_transcribing:
            print("Enhanced transcription not running")
            return
        
        try:
            print("🛑 Stopping enhanced transcription...")
            self.is_transcribing = False
            
            # Stop enhanced audio processing
            self.audio_processor.stop_capture()
            
            # Save speaker profiles
            self.speaker_identifier.save_speaker_profiles()
            
            # Print final statistics
            self.print_session_statistics()
            
            print("✅ Enhanced transcription stopped successfully!")
            
        except Exception as e:
            print(f"❌ Error stopping enhanced transcription: {e}")
    
    def process_enhanced_speaker_identification(self):
        """Process audio for enhanced speaker identification"""
        while self.is_transcribing:
            try:
                # Get processed audio chunk
                audio_chunk = self.audio_processor.get_audio_chunk(timeout=1)
                
                if audio_chunk:
                    # Enhanced speaker identification
                    speaker_id = self.speaker_identifier.identify_speaker(audio_chunk)
                    
                    if speaker_id:
                        # Update speaker count
                        current_speakers = len(self.speaker_identifier.speaker_profiles)
                        if current_speakers > self.performance_stats['total_speakers_detected']:
                            self.performance_stats['total_speakers_detected'] = current_speakers
                    
            except Exception as e:
                print(f"Enhanced speaker identification error: {e}")
                time.sleep(0.1)
    
    def monitor_performance(self):
        """Monitor and report performance statistics"""
        last_report_time = time.time()
        
        while self.is_transcribing:
            try:
                current_time = time.time()
                
                # Report every 60 seconds
                if current_time - last_report_time >= 60:
                    self.print_performance_update()
                    last_report_time = current_time
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                print(f"Performance monitoring error: {e}")
                time.sleep(10)
    
    def print_performance_update(self):
        """Print performance update"""
        session_duration = time.time() - self.performance_stats['session_start']
        transcription_stats = self.transcriber.get_transcription_stats()
        audio_stats = self.audio_processor.get_audio_stats()
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        
        print("\n" + "="*60)
        print("📊 ENHANCED TRANSCRIPTION PERFORMANCE UPDATE")
        print("="*60)
        print(f"⏱️  Session Duration: {session_duration/60:.1f} minutes")
        print(f"📝 Total Transcriptions: {self.performance_stats['total_transcriptions']}")
        print(f"🗣️  Speakers Detected: {self.performance_stats['total_speakers_detected']}")
        print(f"⚡ Avg Processing Time: {self.performance_stats['average_processing_time']:.3f}s")
        print(f"🎯 Transcription Success Rate: {transcription_stats['success_rate']}")
        print(f"🔧 Primary Engine: {transcription_stats['primary_engine']}")
        print(f"🎙️  Background Noise Level: {audio_stats['background_noise_level']}")
        print(f"📊 Audio Queue Size: {audio_stats['queue_sizes']['processed_audio']}")
        print("="*60 + "\n")
    
    def print_session_statistics(self):
        """Print comprehensive session statistics"""
        session_duration = time.time() - self.performance_stats['session_start']
        transcription_stats = self.transcriber.get_transcription_stats()
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        
        print("\n" + "="*70)
        print("📈 ENHANCED TRANSCRIPTION SESSION SUMMARY")
        print("="*70)
        print(f"⏱️  Total Session Time: {session_duration/60:.1f} minutes")
        print(f"📝 Total Transcriptions: {self.performance_stats['total_transcriptions']}")
        print(f"🗣️  Total Speakers: {speaker_stats['total_speakers']}")
        print(f"🎯 Success Rate: {transcription_stats['success_rate']}")
        print(f"⚡ Avg Response Time: {transcription_stats['average_response_time']}")
        
        print("\n🔧 Engine Usage:")
        for engine, count in transcription_stats['engine_usage'].items():
            print(f"   • {engine}: {count} times")
        
        print("\n🗣️  Speaker Details:")
        for speaker_id, details in speaker_stats['speaker_details'].items():
            print(f"   • {speaker_id}: {details['voice_type']} ({details['sample_count']} samples)")
        
        print("="*70 + "\n")
    
    def run_auto_mode(self):
        """Run in enhanced automatic mode"""
        print("🤖 Running Enhanced Automatic Mode...")
        print("   Waiting for Microsoft Teams meeting with advanced detection...")
        
        # Start Teams monitoring
        self.teams_detector.start_monitoring(check_interval=5)
        
        # Start UI
        self.ui.run()
    
    def run_manual_mode(self):
        """Run in enhanced manual mode"""
        print("🎮 Running Enhanced Manual Mode...")
        print("   Use the enhanced UI to control transcription")
        
        # Start Teams monitoring (for status display)
        self.teams_detector.start_monitoring(check_interval=10)
        
        # Start UI
        self.ui.run()
    
    def run(self, auto_mode=True):
        """Main enhanced run method"""
        self.is_running = True
        
        try:
            if auto_mode:
                self.run_auto_mode()
            else:
                self.run_manual_mode()
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down enhanced transcriber...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Enhanced cleanup"""
        print("🧹 Enhanced cleanup...")
        
        self.is_running = False
        self.is_transcribing = False
        
        # Stop components
        try:
            self.audio_processor.stop_capture()
            self.speaker_identifier.save_speaker_profiles()
            self.teams_detector.stop_monitoring()
            self.ui.destroy()
        except:
            pass
        
        # Print final session summary
        self.print_session_statistics()
        
        print("✅ Enhanced cleanup completed")

def print_enhanced_usage():
    """Print enhanced usage information"""
    print("🚀 Enhanced Albanian Teams Transcriber")
    print("="*50)
    print("Usage:")
    print("  python enhanced_main.py [mode]")
    print("")
    print("Modes:")
    print("  auto   - Enhanced automatic mode (default)")
    print("  manual - Enhanced manual control mode")
    print("")
    print("🌟 Enhanced Features:")
    print("  ✓ Advanced audio processing with noise reduction")
    print("  ✓ Superior speaker identification with voice analysis")
    print("  ✓ Multiple Albanian transcription engines with fallback")
    print("  ✓ Real-time performance monitoring")
    print("  ✓ Albanian language enhancements and corrections")
    print("  ✓ Persistent speaker profiles and voice characteristics")
    print("  ✓ Automatic echo cancellation and gain control")
    print("  ✓ Confidence indicators and processing statistics")
    print("")
    print("Requirements:")
    print("  - Microsoft Teams")
    print("  - Enhanced audio drivers")
    print("  - Additional Python packages (scipy, librosa, scikit-learn)")

def main():
    """Enhanced main entry point"""
    # Parse command line arguments
    auto_mode = True
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "manual":
            auto_mode = False
        elif mode == "help" or mode == "-h" or mode == "--help":
            print_enhanced_usage()
            return
        elif mode != "auto":
            print(f"Unknown mode: {mode}")
            print_enhanced_usage()
            return
    
    try:
        # Create and run enhanced transcriber
        transcriber = EnhancedAlbanianTeamsTranscriber()
        transcriber.run(auto_mode=auto_mode)
        
    except KeyboardInterrupt:
        print("\n🛑 Enhanced application closed by user")
        sys.exit(0)
    except ImportError as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
        error_msg = f"""
🚀 Enhanced Albanian Teams Transcriber

Missing Enhanced Module: {missing_module}

To use enhanced features, please install:
pip install scipy librosa scikit-learn

Or run the basic version:
python main.py

Would you like installation instructions?
"""
        
        result = messagebox.askyesno("Enhanced Features", error_msg)
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
🚀 Enhanced Albanian Teams Transcriber Error

{str(e)}

This might be due to:
• Missing enhanced audio drivers
• Teams not running
• Permission issues
• Missing enhanced dependencies

Try running the basic version: python main.py
"""
            messagebox.showerror("Enhanced Application Error", error_msg)
        except:
            print(f"Enhanced transcriber error: {e}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()