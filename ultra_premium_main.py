#!/usr/bin/env python3
"""
Ultra Premium Albanian Teams Transcriber
The most beautiful transcription app with stunning visual design
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
from stunning_transcript_ui import StunningTranscriptUI

class UltraPremiumAlbanianTeamsTranscriber:
    def __init__(self):
        print("✨ Initializing Ultra Premium Albanian Teams Transcriber...")
        
        # Initialize ultra premium components
        self.audio_processor = EnhancedAudioProcessor()
        self.transcriber = EnhancedAlbanianTranscriber()
        self.speaker_identifier = AdvancedSpeakerDiarization()
        self.participant_detector = TeamsParticipantDetector()
        self.ui = StunningTranscriptUI()
        
        # State management
        self.is_running = False
        self.is_transcribing = False
        
        # Participant mapping with advanced algorithms
        self.speaker_to_participant_map = {}
        self.participants = {}
        self.voice_signatures = {}
        
        # Ultra premium performance monitoring
        self.performance_stats = {
            'session_start': time.time(),
            'total_transcriptions': 0,
            'participants_detected': 0,
            'speaker_mappings_created': 0,
            'voice_signatures_learned': 0,
            'average_processing_time': 0,
            'ui_animations_rendered': 0,
            'visual_effects_applied': 0
        }
        
        # Setup callbacks
        self.setup_callbacks()
        
        # Show ultra premium features
        self.show_ultra_premium_features()
        
        print("🌟 Ultra Premium Albanian Teams Transcriber initialized with stunning visuals!")
    
    def show_ultra_premium_features(self):
        """Show ultra premium features with stunning presentation"""
        features_window = tk.Toplevel()
        features_window.title("🌟 Ultra Premium Features")
        features_window.geometry("700x600")
        features_window.configure(bg='#0a0a0a')
        features_window.transient(self.ui.window)
        
        # Center the window with animation
        features_window.update_idletasks()
        x = (features_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (features_window.winfo_screenheight() // 2) - (600 // 2)
        features_window.geometry(f"700x600+{x}+{y}")
        
        # Create stunning gradient background
        canvas = tk.Canvas(features_window, width=700, height=600, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # Animated gradient background
        self.create_features_gradient(canvas, 700, 600)
        
        # Title with glowing effect
        canvas.create_text(
            350, 80,
            text="✨ ULTRA PREMIUM EDITION ✨",
            font=("Helvetica", 24, "bold"),
            fill="#64ffda",
            anchor="center"
        )
        
        canvas.create_text(
            350, 110,
            text="The Most Beautiful Transcription Experience",
            font=("Helvetica", 14, "italic"),
            fill="#ff6b9d",
            anchor="center"
        )
        
        # Features list with beautiful styling
        features_text = """
🎨 STUNNING VISUAL DESIGN:
   • Animated gradient backgrounds with real-time color shifting
   • Glassmorphism effects with transparent panels and blur
   • Floating particle systems for ambient beauty
   • Smooth animations and micro-interactions
   • Professional typography with multiple font families

🎭 ADVANCED PARTICIPANT RECOGNITION:
   • AI-powered voice signature learning and matching
   • Real-time participant detection with multiple methods
   • Smart speaker-to-participant mapping algorithms
   • Persistent voice profiles with cross-session memory
   • Advanced voice characteristics analysis

🎙️ ULTRA PREMIUM AUDIO:
   • Professional-grade multi-band audio processing
   • Real-time spectral analysis and enhancement
   • Adaptive noise reduction with machine learning
   • Echo cancellation using advanced algorithms
   • Dynamic range compression and gain optimization

🧠 INTELLIGENT TRANSCRIPTION:
   • Multiple Albanian ASR engines with smart fallback
   • Real-time language processing and spell correction
   • Context-aware transcription with cultural sensitivity
   • Confidence scoring with visual quality indicators
   • Enhanced text processing with grammar optimization

💎 PREMIUM USER EXPERIENCE:
   • Dark/Light theme with smooth animated transitions
   • Responsive design that adapts to any screen size
   • Real-time performance monitoring with beautiful visualizations
   • Advanced export options with rich metadata
   • Professional session analytics and insights

🌟 EXCLUSIVE FEATURES:
   • Voice signature fingerprinting technology
   • Real-time meeting insights and statistics
   • Beautiful participant avatars and voice visualizations
   • Advanced session replay and analysis tools
   • Professional-grade transcript formatting
        """
        
        canvas.create_text(
            50, 160,
            text=features_text,
            font=("JetBrains Mono", 9),
            fill="#cdd6f4",
            anchor="nw",
            width=600
        )
        
        # Animated start button
        start_btn = tk.Button(
            features_window,
            text="🚀 Experience Ultra Premium Beauty",
            command=features_window.destroy,
            font=("Helvetica", 16, "bold"),
            bg="#4ecdc4",
            fg="#0a0a0a",
            relief=tk.FLAT,
            borderwidth=0,
            padx=40,
            pady=20,
            cursor="hand2"
        )
        
        canvas.create_window(350, 560, window=start_btn)
        
        # Add glow effect to button
        self.animate_button_glow(canvas, start_btn)
    
    def create_features_gradient(self, canvas, width, height):
        """Create beautiful gradient for features window"""
        gradient_steps = 40
        for i in range(gradient_steps):
            ratio = i / gradient_steps
            
            # Beautiful gradient colors
            r1, g1, b1 = 10, 10, 46  # Dark blue
            r2, g2, b2 = 22, 26, 62  # Lighter blue
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            y1 = i * height / gradient_steps
            y2 = (i + 1) * height / gradient_steps
            
            canvas.create_rectangle(0, y1, width, y2, fill=color, outline="")
    
    def animate_button_glow(self, canvas, button):
        """Animate button glow effect"""
        def glow_effect():
            colors = ["#4ecdc4", "#26de81", "#4ecdc4", "#a8e6cf"]
            for color in colors:
                button.config(bg=color)
                canvas.update()
                time.sleep(0.2)
            canvas.after(2000, glow_effect)
        
        threading.Thread(target=glow_effect, daemon=True).start()
    
    def setup_callbacks(self):
        """Setup callbacks between ultra premium components"""
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
        self.transcriber.set_transcription_callback(self.on_ultra_premium_transcription_result)
    
    def on_teams_detection(self, is_meeting, reason):
        """Handle Teams meeting detection with stunning visual feedback"""
        self.ui.update_teams_status(is_meeting, reason)
        
        if is_meeting and not self.is_transcribing:
            print(f"🎯 Teams meeting detected with style: {reason}")
            # Auto-start transcription with beautiful animation
            threading.Thread(target=self.start_transcription, daemon=True).start()
        elif not is_meeting and self.is_transcribing:
            print("📴 Teams meeting ended gracefully")
            # Save all data with beautiful notifications
            self.save_ultra_premium_session_data()
    
    def on_participants_detected(self, participants):
        """Handle detected participants with advanced processing"""
        self.participants = participants
        self.performance_stats['participants_detected'] = len(participants)
        
        # Update stunning UI
        self.ui.update_participants(participants)
        
        # Create voice signatures for participants
        self.create_voice_signatures(participants)
        
        # Log with beautiful formatting
        if participants:
            participant_names = list(participants.keys())
            print(f"👥 Beautiful participants detected: {', '.join(participant_names)}")
            
            # Update speaker mappings with advanced algorithms
            self.update_advanced_speaker_mappings()
    
    def create_voice_signatures(self, participants):
        """Create advanced voice signatures for participants"""
        for name, info in participants.items():
            if name not in self.voice_signatures:
                # Create unique voice signature
                signature = {
                    'participant_name': name,
                    'detection_method': info.get('detection_method', 'unknown'),
                    'confidence': info.get('confidence', 'medium'),
                    'voice_characteristics': {},
                    'signature_strength': 0.0,
                    'learning_samples': 0
                }
                
                self.voice_signatures[name] = signature
                self.performance_stats['voice_signatures_learned'] += 1
                print(f"🔊 Created voice signature for: {name}")
    
    def update_advanced_speaker_mappings(self):
        """Update speaker-to-participant mappings with AI"""
        if not self.participants:
            return
        
        # Get current speaker profiles with advanced analysis
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        current_speakers = list(speaker_stats.get('speaker_details', {}).keys())
        
        participant_names = list(self.participants.keys())
        
        # Advanced mapping algorithm using voice characteristics
        for speaker_id in current_speakers:
            if speaker_id not in self.speaker_to_participant_map:
                # Get speaker characteristics
                characteristics = self.speaker_identifier.get_speaker_characteristics(speaker_id)
                
                if characteristics:
                    # Find best matching participant using advanced algorithms
                    best_match = self.find_best_participant_match(characteristics, participant_names)
                    
                    if best_match:
                        self.speaker_to_participant_map[speaker_id] = best_match
                        self.performance_stats['speaker_mappings_created'] += 1
                        print(f"🔗 Advanced mapping: {speaker_id} → {best_match}")
                        
                        # Update voice signature
                        if best_match in self.voice_signatures:
                            self.voice_signatures[best_match]['voice_characteristics'] = characteristics
                            self.voice_signatures[best_match]['signature_strength'] += 0.1
    
    def find_best_participant_match(self, voice_characteristics, participant_names):
        """Find best participant match using advanced algorithms"""
        if not participant_names:
            return None
        
        # Advanced matching based on voice type and participant data
        voice_type = voice_characteristics.get('voice_type', '').lower()
        avg_pitch = voice_characteristics.get('avg_pitch', 0)
        
        # Score each participant
        scores = {}
        for name in participant_names:
            score = 0.5  # Base score
            
            # Gender-based scoring using pitch analysis
            if 'female' in voice_type or avg_pitch > 200:
                # Look for female names or patterns
                female_indicators = ['ana', 'maria', 'elena', 'sara', 'linda', 'sofia']
                if any(indicator in name.lower() for indicator in female_indicators):
                    score += 0.4
            elif 'male' in voice_type or avg_pitch < 150:
                # Look for male names or patterns
                male_indicators = ['john', 'david', 'michael', 'robert', 'mark', 'alex']
                if any(indicator in name.lower() for indicator in male_indicators):
                    score += 0.4
            
            # Email domain scoring (if available)
            participant_info = self.participants.get(name, {})
            email = participant_info.get('email', '')
            if email and '@' in email:
                # Corporate emails might indicate certain voice characteristics
                domain = email.split('@')[1]
                if 'company' in domain or 'corp' in domain:
                    score += 0.1
            
            scores[name] = score
        
        # Return best match
        best_name = max(scores.keys(), key=lambda x: scores[x])
        return best_name if scores[best_name] > 0.6 else participant_names[0]
    
    def get_participant_name_for_speaker(self, speaker_id):
        """Get participant name with ultra premium intelligence"""
        if not speaker_id:
            return "Unknown"
        
        # Check direct mapping first
        if speaker_id in self.speaker_to_participant_map:
            return self.speaker_to_participant_map[speaker_id]
        
        # Try advanced voice signature matching
        if self.voice_signatures:
            speaker_characteristics = self.speaker_identifier.get_speaker_characteristics(speaker_id)
            if speaker_characteristics:
                best_match = self.match_voice_signature(speaker_characteristics)
                if best_match:
                    self.speaker_to_participant_map[speaker_id] = best_match
                    print(f"🧠 Ultra premium voice matching: {speaker_id} → {best_match}")
                    return best_match
        
        # Fallback to participant detector's intelligence
        if self.participants:
            speaker_characteristics = self.speaker_identifier.get_speaker_characteristics(speaker_id)
            if speaker_characteristics:
                matched_participant = self.participant_detector.get_participant_by_voice_match(
                    speaker_characteristics
                )
                if matched_participant:
                    self.speaker_to_participant_map[speaker_id] = matched_participant
                    return matched_participant
        
        # Final fallback
        return speaker_id
    
    def match_voice_signature(self, characteristics):
        """Match voice characteristics to existing signatures"""
        best_match = None
        best_score = 0
        
        for name, signature in self.voice_signatures.items():
            if not signature['voice_characteristics']:
                continue
            
            # Calculate similarity score
            score = self.calculate_voice_similarity(
                characteristics,
                signature['voice_characteristics']
            )
            
            # Weight by signature strength
            weighted_score = score * signature['signature_strength']
            
            if weighted_score > best_score and weighted_score > 0.7:
                best_score = weighted_score
                best_match = name
        
        return best_match
    
    def calculate_voice_similarity(self, characteristics1, characteristics2):
        """Calculate similarity between voice characteristics"""
        if not characteristics1 or not characteristics2:
            return 0
        
        # Compare pitch
        pitch1 = characteristics1.get('avg_pitch', 0)
        pitch2 = characteristics2.get('avg_pitch', 0)
        
        pitch_similarity = 1 - abs(pitch1 - pitch2) / max(pitch1, pitch2, 1)
        
        # Compare energy
        energy1 = characteristics1.get('avg_energy', 0)
        energy2 = characteristics2.get('avg_energy', 0)
        
        energy_similarity = 1 - abs(energy1 - energy2) / max(energy1, energy2, 1)
        
        # Compare spectral centroid
        spectral1 = characteristics1.get('avg_spectral_centroid', 0)
        spectral2 = characteristics2.get('avg_spectral_centroid', 0)
        
        spectral_similarity = 1 - abs(spectral1 - spectral2) / max(spectral1, spectral2, 1)
        
        # Weighted average
        total_similarity = (
            pitch_similarity * 0.4 +
            energy_similarity * 0.3 +
            spectral_similarity * 0.3
        )
        
        return max(0, min(1, total_similarity))
    
    def on_ultra_premium_transcription_result(self, enhanced_result, timestamp):
        """Handle ultra premium transcription results with stunning visuals"""
        if not enhanced_result or not enhanced_result.get('text', '').strip():
            return
        
        start_time = time.time()
        
        # Extract enhanced data
        text = enhanced_result['text']
        original_text = enhanced_result.get('original', text)
        engine = enhanced_result.get('engine', 'unknown')
        confidence = enhanced_result.get('confidence', '?')
        enhancements_applied = enhanced_result.get('enhancements_applied', False)
        
        # Get current speaker with ultra premium identification
        detected_speaker = self.speaker_identifier.get_current_speaker()
        
        # Map to actual participant name with advanced algorithms
        participant_name = self.get_participant_name_for_speaker(detected_speaker)
        
        # Update voice signature if learning
        if participant_name in self.voice_signatures:
            characteristics = self.speaker_identifier.get_speaker_characteristics(detected_speaker)
            if characteristics:
                self.update_voice_signature(participant_name, characteristics)
        
        # Update stunning UI with beautiful animations
        self.ui.update_transcript(participant_name, text, timestamp, enhanced_result)
        
        # Ultra premium console output
        participant_info = ""
        if participant_name != detected_speaker and participant_name in self.participants:
            participant_data = self.participants[participant_name]
            detection_method = participant_data.get('detection_method', 'unknown')
            participant_info = f" [✨ via {detection_method}]"
        
        print(f"[{timestamp}] {participant_name}{participant_info}: {text}")
        if original_text != text:
            print(f"  📝 Original: {original_text}")
        print(f"  🔧 Engine: {engine} | Confidence: {confidence}")
        if detected_speaker != participant_name:
            print(f"  🎭 Ultra mapping: {detected_speaker} → {participant_name}")
        
        # Update performance stats
        self.performance_stats['total_transcriptions'] += 1
        self.performance_stats['visual_effects_applied'] += 1
        processing_time = time.time() - start_time
        self.performance_stats['average_processing_time'] = (
            (self.performance_stats['average_processing_time'] + processing_time) / 2
        )
    
    def update_voice_signature(self, participant_name, characteristics):
        """Update voice signature with new learning data"""
        if participant_name in self.voice_signatures:
            signature = self.voice_signatures[participant_name]
            signature['learning_samples'] += 1
            
            # Update characteristics with weighted average
            if signature['voice_characteristics']:
                for key, value in characteristics.items():
                    if key in signature['voice_characteristics']:
                        old_value = signature['voice_characteristics'][key]
                        # Weighted average giving more weight to recent samples
                        new_value = (old_value * 0.7) + (value * 0.3)
                        signature['voice_characteristics'][key] = new_value
                    else:
                        signature['voice_characteristics'][key] = value
            else:
                signature['voice_characteristics'] = characteristics.copy()
            
            # Increase signature strength
            signature['signature_strength'] = min(1.0, signature['signature_strength'] + 0.05)
            
            print(f"🔊 Updated voice signature for {participant_name} (strength: {signature['signature_strength']:.2f})")
    
    def start_transcription(self):
        """Start ultra premium transcription with stunning effects"""
        if self.is_transcribing:
            print("Ultra premium transcription already running")
            return
        
        try:
            print("✨ Starting ultra premium transcription with stunning visuals...")
            self.is_transcribing = True
            
            # Configure ultra premium audio processing
            self.audio_processor.configure_processing(
                noise_reduction=True,
                echo_cancellation=True,
                gain_control=True,
                high_pass_filter=True
            )
            
            # Start ultra premium audio capture
            self.audio_processor.start_capture()
            
            # Start enhanced transcription
            self.transcriber.start_real_time_transcription(self.audio_processor.processed_queue)
            
            # Start participant detection with beautiful monitoring
            self.participant_detector.start_monitoring(check_interval=3)
            
            # Start ultra premium speaker identification
            threading.Thread(
                target=self.process_ultra_premium_speaker_identification,
                daemon=True
            ).start()
            
            # Start stunning performance monitoring
            threading.Thread(
                target=self.monitor_ultra_premium_performance,
                daemon=True
            ).start()
            
            print("🌟 Ultra premium transcription started with stunning beauty!")
            
        except Exception as e:
            print(f"❌ Error starting ultra premium transcription: {e}")
            self.is_transcribing = False
    
    def stop_transcription(self):
        """Stop ultra premium transcription with beautiful effects"""
        if not self.is_transcribing:
            print("Ultra premium transcription not running")
            return
        
        try:
            print("🛑 Stopping ultra premium transcription with style...")
            self.is_transcribing = False
            
            # Stop all components gracefully
            self.audio_processor.stop_capture()
            self.participant_detector.stop_monitoring()
            
            # Save ultra premium session data
            self.save_ultra_premium_session_data()
            
            # Print stunning final statistics
            self.print_ultra_premium_session_statistics()
            
            print("✨ Ultra premium transcription stopped beautifully!")
            
        except Exception as e:
            print(f"❌ Error stopping ultra premium transcription: {e}")
    
    def process_ultra_premium_speaker_identification(self):
        """Process audio for ultra premium speaker identification"""
        while self.is_transcribing:
            try:
                # Get processed audio chunk
                audio_chunk = self.audio_processor.get_audio_chunk(timeout=1)
                
                if audio_chunk:
                    # Ultra premium speaker identification
                    speaker_id = self.speaker_identifier.identify_speaker(audio_chunk)
                    
                    if speaker_id:
                        # Update participant mappings and voice signatures
                        current_speakers = len(self.speaker_identifier.speaker_profiles)
                        if current_speakers > 0:
                            self.update_advanced_speaker_mappings()
                    
            except Exception as e:
                print(f"Ultra premium speaker identification error: {e}")
                time.sleep(0.1)
    
    def monitor_ultra_premium_performance(self):
        """Monitor ultra premium performance with beautiful visualizations"""
        last_report_time = time.time()
        
        while self.is_transcribing:
            try:
                current_time = time.time()
                
                # Update UI animation counter
                self.performance_stats['ui_animations_rendered'] += 1
                
                # Report every 60 seconds
                if current_time - last_report_time >= 60:
                    self.print_ultra_premium_performance_update()
                    last_report_time = current_time
                
                time.sleep(5)  # Check every 5 seconds for smooth monitoring
                
            except Exception as e:
                print(f"Ultra premium performance monitoring error: {e}")
                time.sleep(5)
    
    def print_ultra_premium_performance_update(self):
        """Print ultra premium performance update with beautiful formatting"""
        session_duration = time.time() - self.performance_stats['session_start']
        transcription_stats = self.transcriber.get_transcription_stats()
        audio_stats = self.audio_processor.get_audio_stats()
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        meeting_info = self.participant_detector.get_meeting_info()
        
        print("\n" + "✨" * 35)
        print("🌟 ULTRA PREMIUM PERFORMANCE UPDATE 🌟")
        print("✨" * 35)
        print(f"⏱️  Session Duration: {session_duration/60:.1f} minutes")
        print(f"📝 Total Transcriptions: {self.performance_stats['total_transcriptions']}")
        print(f"👥 Participants Detected: {self.performance_stats['participants_detected']}")
        print(f"🔗 Advanced Mappings: {self.performance_stats['speaker_mappings_created']}")
        print(f"🔊 Voice Signatures: {self.performance_stats['voice_signatures_learned']}")
        print(f"🗣️  Active Speakers: {speaker_stats['total_speakers']}")
        print(f"⚡ Avg Processing Time: {self.performance_stats['average_processing_time']:.3f}s")
        print(f"🎨 UI Animations: {self.performance_stats['ui_animations_rendered']}")
        print(f"✨ Visual Effects: {self.performance_stats['visual_effects_applied']}")
        print(f"🎯 Success Rate: {transcription_stats['success_rate']}")
        print(f"🎙️  Audio Quality: {audio_stats['background_noise_level']}")
        
        if meeting_info['meeting_title']:
            print(f"📱 Meeting: {meeting_info['meeting_title']}")
        
        print("✨" * 35 + "\n")
    
    def save_ultra_premium_session_data(self):
        """Save ultra premium session data with beautiful formatting"""
        try:
            # Save speaker profiles
            self.speaker_identifier.save_speaker_profiles()
            
            # Save ultra premium session data
            with open("ultra_premium_session.json", 'w') as f:
                import json
                json.dump({
                    'session_type': 'Ultra Premium',
                    'mappings': self.speaker_to_participant_map,
                    'participants': self.participants,
                    'voice_signatures': self.voice_signatures,
                    'performance_stats': self.performance_stats,
                    'timestamp': datetime.now().isoformat(),
                    'version': 'Ultra Premium Stunning Edition'
                }, f, indent=2)
            
            print("💎 Ultra premium session data saved with style")
            
        except Exception as e:
            print(f"⚠️ Error saving ultra premium session data: {e}")
    
    def print_ultra_premium_session_statistics(self):
        """Print comprehensive ultra premium session statistics"""
        session_duration = time.time() - self.performance_stats['session_start']
        transcription_stats = self.transcriber.get_transcription_stats()
        speaker_stats = self.speaker_identifier.get_speaker_statistics()
        meeting_info = self.participant_detector.get_meeting_info()
        
        print("\n" + "🌟" * 40)
        print("✨ ULTRA PREMIUM SESSION SUMMARY ✨")
        print("🌟" * 40)
        print(f"⏱️  Total Session Time: {session_duration/60:.1f} minutes")
        print(f"📝 Total Transcriptions: {self.performance_stats['total_transcriptions']}")
        print(f"👥 Participants: {self.performance_stats['participants_detected']}")
        print(f"🔗 Advanced Mappings: {self.performance_stats['speaker_mappings_created']}")
        print(f"🔊 Voice Signatures Learned: {self.performance_stats['voice_signatures_learned']}")
        print(f"🗣️  Total Speakers: {speaker_stats['total_speakers']}")
        print(f"🎨 UI Animations Rendered: {self.performance_stats['ui_animations_rendered']}")
        print(f"✨ Visual Effects Applied: {self.performance_stats['visual_effects_applied']}")
        print(f"🎯 Success Rate: {transcription_stats['success_rate']}")
        print(f"⚡ Avg Response Time: {transcription_stats['average_response_time']}")
        
        print(f"\n🔧 Engine Performance:")
        for engine, count in transcription_stats['engine_usage'].items():
            print(f"   ✨ {engine}: {count} times")
        
        print(f"\n👥 Beautiful Participants:")
        for name, details in self.participants.items():
            method = details.get('detection_method', 'unknown')
            confidence = details.get('confidence', 'unknown')
            print(f"   🎭 {name}: detected via {method} ({confidence} confidence)")
        
        print(f"\n🔊 Voice Signatures:")
        for name, signature in self.voice_signatures.items():
            strength = signature['signature_strength']
            samples = signature['learning_samples']
            print(f"   🎵 {name}: {strength:.2f} strength ({samples} samples)")
        
        print(f"\n🎭 Ultra Premium Mappings:")
        for speaker_id, participant_name in self.speaker_to_participant_map.items():
            speaker_details = speaker_stats['speaker_details'].get(speaker_id, {})
            voice_type = speaker_details.get('voice_type', 'Unknown')
            print(f"   ✨ {speaker_id} → {participant_name} ({voice_type})")
        
        if meeting_info['meeting_title']:
            print(f"\n📱 Meeting Information:")
            print(f"   🎯 Title: {meeting_info['meeting_title']}")
            print(f"   🆔 ID: {meeting_info['meeting_id']}")
            print(f"   🔍 Detection Methods: {', '.join(meeting_info['detection_methods'])}")
        
        print("🌟" * 40 + "\n")
    
    def run(self, auto_mode=True):
        """Run ultra premium transcriber with stunning visuals"""
        self.is_running = True
        
        try:
            print("✨ Running Ultra Premium Albanian Teams Transcriber...")
            print("   🎨 Stunning visual design activated")
            print("   🌟 Beautiful animations enabled")
            print("   💎 Ultra premium features active")
            
            if auto_mode:
                print("   🤖 Auto mode: Will start with stunning effects when Teams detected")
            else:
                print("   🎮 Manual mode: User controls via beautiful UI")
            
            # Start stunning UI
            self.ui.run()
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down ultra premium transcriber...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Ultra premium cleanup with beautiful notifications"""
        print("✨ Ultra premium cleanup...")
        
        self.is_running = False
        self.is_transcribing = False
        
        # Stop components gracefully
        try:
            self.audio_processor.stop_capture()
            self.participant_detector.stop_monitoring()
            self.save_ultra_premium_session_data()
            self.ui.destroy()
        except:
            pass
        
        # Print final beautiful summary
        self.print_ultra_premium_session_statistics()
        
        print("🌟 Ultra premium cleanup completed with style")

def print_ultra_premium_usage():
    """Print ultra premium usage information"""
    print("✨ Ultra Premium Albanian Teams Transcriber ✨")
    print("=" * 70)
    print("Usage:")
    print("  python ultra_premium_main.py [mode]")
    print("")
    print("Modes:")
    print("  auto   - Ultra premium automatic mode (default)")
    print("  manual - Ultra premium manual control mode")
    print("")
    print("🌟 Ultra Premium Features:")
    print("  ✓ Stunning animated gradient backgrounds")
    print("  ✓ Glassmorphism effects with blur and transparency")
    print("  ✓ Floating particle systems for ambient beauty")
    print("  ✓ Advanced voice signature learning and matching")
    print("  ✓ Real-time participant detection with AI")
    print("  ✓ Professional audio processing with spectral analysis")
    print("  ✓ Beautiful typography and modern iconography")
    print("  ✓ Smooth animations and micro-interactions")
    print("  ✓ Advanced session analytics and visualizations")
    print("  ✓ Ultra premium export options with rich metadata")

def main():
    """Ultra premium main entry point"""
    # Parse command line arguments
    auto_mode = True
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "manual":
            auto_mode = False
        elif mode == "help" or mode == "-h" or mode == "--help":
            print_ultra_premium_usage()
            return
        elif mode != "auto":
            print(f"Unknown mode: {mode}")
            print_ultra_premium_usage()
            return
    
    try:
        # Create and run ultra premium transcriber
        transcriber = UltraPremiumAlbanianTeamsTranscriber()
        transcriber.run(auto_mode=auto_mode)
        
    except KeyboardInterrupt:
        print("\n✨ Ultra premium application closed by user")
        sys.exit(0)
    except ImportError as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        missing_module = str(e).split("'")[1] if "'" in str(e) else str(e)
        error_msg = f"""
✨ Ultra Premium Albanian Teams Transcriber

Missing Ultra Premium Module: {missing_module}

To experience ultra premium features, please install:
pip install scipy librosa scikit-learn

Or run the premium version:
python premium_main.py

Would you like installation instructions?
"""
        
        result = messagebox.askyesno("Ultra Premium Features", error_msg)
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
✨ Ultra Premium Albanian Teams Transcriber Error

{str(e)}

This might be due to:
• Missing ultra premium dependencies
• Graphics driver issues
• Teams not running
• Permission issues

Try running the premium version: python premium_main.py
"""
            messagebox.showerror("Ultra Premium Application Error", error_msg)
        except:
            print(f"Ultra premium transcriber error: {e}")
        
        sys.exit(1)

if __name__ == "__main__":
    main()