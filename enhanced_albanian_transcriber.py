import speech_recognition as sr
import queue
import threading
import time
import wave
import io
import numpy as np
from datetime import datetime
import requests
import json
import re
import difflib

class EnhancedAlbanianTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Enhanced configurations
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5  # Reduced for faster response
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.3
        
        # Multiple transcription engines
        self.transcription_engines = {
            'google': self._transcribe_google,
            'azure': self._transcribe_azure,
            'openai': self._transcribe_openai,
            'local_albanian': self._transcribe_local_albanian,
            'fallback': self._transcribe_fallback
        }
        
        # Current engine configuration
        self.primary_engine = 'google'
        self.fallback_engines = ['azure', 'openai', 'fallback']
        
        # Audio buffer management
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        self.max_buffer_size = 64  # Increased buffer for better context
        
        # Transcription callback
        self.transcription_callback = None
        
        # Albanian language processing
        self.albanian_corrections = self._load_albanian_corrections()
        self.common_words = self._load_common_albanian_words()
        
        # Performance tracking
        self.transcription_stats = {
            'total_attempts': 0,
            'successful_transcriptions': 0,
            'engine_usage': {},
            'average_response_time': 0
        }
        
        print("Enhanced Albanian Transcriber initialized with multiple engines")
    
    def _load_albanian_corrections(self):
        """Load common Albanian spelling corrections"""
        return {
            # Common transcription errors and corrections
            'shqipëria': 'Shqipëria',
            'shqip': 'shqip',
            'faleminderit': 'faleminderit',
            'përshëndetje': 'përshëndetje',
            'mirupafshim': 'mirupafshim',
            'dakord': "d'akord",
            'çështje': 'çështje',
            'bashkëpunim': 'bashkëpunim',
            'projekt': 'projekt',
            'mbledhje': 'mbledhje',
            # Add more common corrections
        }
    
    def _load_common_albanian_words(self):
        """Load common Albanian words for context validation"""
        return {
            'greetings': ['përshëndetje', 'mirëdita', 'mirëmëngjes', 'mirupafshim'],
            'courtesy': ['faleminderit', 'ju lutem', 'më falni', 'keni të drejtë'],
            'business': ['mbledhje', 'projekt', 'bashkëpunim', 'zgjidhje', 'propozim'],
            'common': ['po', 'jo', 'mirë', 'keq', 'shumë', 'pak', 'gjithashtu'],
            'pronouns': ['unë', 'ti', 'ai', 'ajo', 'ne', 'ju', 'ata', 'ato'],
            'time': ['sot', 'nesër', 'dje', 'tani', 'më vonë', 'herët', 'vonë']
        }
    
    def set_transcription_callback(self, callback):
        """Set callback function for real-time transcription results"""
        self.transcription_callback = callback
    
    def set_primary_engine(self, engine_name):
        """Set the primary transcription engine"""
        if engine_name in self.transcription_engines:
            self.primary_engine = engine_name
            print(f"Primary transcription engine set to: {engine_name}")
        else:
            print(f"Unknown engine: {engine_name}. Available: {list(self.transcription_engines.keys())}")
    
    def _transcribe_google(self, audio_data):
        """Google Speech Recognition with Albanian support"""
        try:
            audio_file = io.BytesIO(audio_data)
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Try Albanian first, then multilingual
            try:
                text = self.recognizer.recognize_google(audio, language='sq-AL')
                return text, 'google-albanian'
            except:
                # Fallback to auto-detect with Albanian context
                text = self.recognizer.recognize_google(audio, language='sq')
                return text, 'google-auto'
                
        except Exception as e:
            print(f"Google transcription error: {e}")
            return None, None
    
    def _transcribe_azure(self, audio_data):
        """Azure Speech Services (placeholder - requires API key)"""
        try:
            # This would require Azure Speech Service API key
            # For now, return None to trigger fallback
            return None, None
        except Exception as e:
            print(f"Azure transcription error: {e}")
            return None, None
    
    def _transcribe_openai(self, audio_data):
        """OpenAI Whisper (placeholder - requires API key)"""
        try:
            # This would use OpenAI Whisper API
            # Whisper has excellent Albanian support
            return None, None
        except Exception as e:
            print(f"OpenAI transcription error: {e}")
            return None, None
    
    def _transcribe_local_albanian(self, audio_data):
        """Local Albanian ASR model integration"""
        try:
            # This would integrate with the Albanian-ASR GitHub project
            # Placeholder for actual implementation
            return None, None
        except Exception as e:
            print(f"Local Albanian ASR error: {e}")
            return None, None
    
    def _transcribe_fallback(self, audio_data):
        """Fallback transcription using basic speech recognition"""
        try:
            audio_file = io.BytesIO(audio_data)
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Try different languages as fallback
            for lang in ['en-US', 'it-IT', 'de-DE']:
                try:
                    text = self.recognizer.recognize_google(audio, language=lang)
                    return f"[{lang}] {text}", f'fallback-{lang}'
                except:
                    continue
            
            return None, None
        except Exception as e:
            print(f"Fallback transcription error: {e}")
            return None, None
    
    def _enhance_transcription(self, text, engine_used):
        """Enhance transcription with Albanian language processing"""
        if not text:
            return text
        
        # Apply Albanian corrections
        enhanced_text = text
        for error, correction in self.albanian_corrections.items():
            enhanced_text = re.sub(r'\b' + re.escape(error) + r'\b', correction, enhanced_text, flags=re.IGNORECASE)
        
        # Capitalize proper nouns and sentence beginnings
        enhanced_text = self._capitalize_properly(enhanced_text)
        
        # Add confidence indicator based on engine
        confidence_indicators = {
            'google-albanian': '✓✓✓',
            'google-auto': '✓✓',
            'azure': '✓✓✓',
            'openai': '✓✓✓',
            'local_albanian': '✓✓✓✓',
            'fallback': '✓'
        }
        
        confidence = confidence_indicators.get(engine_used, '?')
        
        return {
            'text': enhanced_text,
            'original': text,
            'engine': engine_used,
            'confidence': confidence,
            'enhancements_applied': text != enhanced_text
        }
    
    def _capitalize_properly(self, text):
        """Apply proper capitalization for Albanian text"""
        # Capitalize sentence beginnings
        sentences = re.split(r'[.!?]+', text)
        capitalized_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Capitalize first letter
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                
                # Capitalize proper nouns (simple approach)
                proper_nouns = ['Shqipëria', 'Tiranë', 'Prishtinë', 'Shkup', 'Microsoft', 'Teams']
                for noun in proper_nouns:
                    sentence = re.sub(r'\b' + re.escape(noun.lower()) + r'\b', noun, sentence, flags=re.IGNORECASE)
                
                capitalized_sentences.append(sentence)
        
        return '. '.join(capitalized_sentences)
    
    def transcribe_with_fallback(self, audio_data):
        """Transcribe using primary engine with fallback options"""
        start_time = time.time()
        self.transcription_stats['total_attempts'] += 1
        
        # Try primary engine first
        engines_to_try = [self.primary_engine] + self.fallback_engines
        
        for engine_name in engines_to_try:
            if engine_name in self.transcription_engines:
                try:
                    print(f"Trying {engine_name}...")
                    text, engine_used = self.transcription_engines[engine_name](audio_data)
                    
                    if text:
                        # Update statistics
                        self.transcription_stats['successful_transcriptions'] += 1
                        self.transcription_stats['engine_usage'][engine_name] = \
                            self.transcription_stats['engine_usage'].get(engine_name, 0) + 1
                        
                        # Calculate response time
                        response_time = time.time() - start_time
                        self.transcription_stats['average_response_time'] = \
                            (self.transcription_stats['average_response_time'] + response_time) / 2
                        
                        # Enhance the transcription
                        enhanced_result = self._enhance_transcription(text, engine_used or engine_name)
                        
                        print(f"✓ Transcription successful with {engine_name} in {response_time:.2f}s")
                        return enhanced_result
                        
                except Exception as e:
                    print(f"Engine {engine_name} failed: {e}")
                    continue
        
        print("All transcription engines failed")
        return None
    
    def process_audio_stream(self, audio_queue):
        """Enhanced audio stream processing with better buffering"""
        consecutive_failures = 0
        max_failures = 5
        
        while True:
            try:
                # Get audio chunk with timeout
                chunk = audio_queue.get(timeout=1)
                
                with self.buffer_lock:
                    self.audio_buffer.append(chunk)
                    
                    # Process when buffer reaches optimal size or after timeout
                    if len(self.audio_buffer) >= 24:  # ~1.5 seconds of audio
                        combined_audio = b''.join(self.audio_buffer)
                        
                        # Create WAV format for recognition
                        wav_data = self._create_wav_data(combined_audio)
                        
                        # Transcribe with fallback
                        result = self.transcribe_with_fallback(wav_data)
                        
                        if result and self.transcription_callback:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            self.transcription_callback(result, timestamp)
                            consecutive_failures = 0
                        else:
                            consecutive_failures += 1
                            
                            # If too many failures, adjust sensitivity
                            if consecutive_failures >= max_failures:
                                print("Multiple transcription failures, adjusting audio sensitivity...")
                                self.recognizer.energy_threshold *= 0.8  # Lower threshold
                                consecutive_failures = 0
                        
                        # Keep overlapping context
                        self.audio_buffer = self.audio_buffer[-8:]  # Keep last 0.5 seconds
                        
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Enhanced audio processing error: {e}")
                continue
    
    def _create_wav_data(self, audio_data):
        """Create enhanced WAV format data with preprocessing"""
        output = io.BytesIO()
        
        try:
            # Convert to numpy array for preprocessing
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            # Apply basic noise reduction (simple high-pass filter)
            if len(audio_array) > 100:
                # Remove DC offset
                audio_array = audio_array - np.mean(audio_array)
                
                # Simple noise gate (remove very quiet sounds)
                threshold = np.max(np.abs(audio_array)) * 0.05
                audio_array[np.abs(audio_array) < threshold] = 0
            
            # Convert back to bytes
            processed_audio = audio_array.astype(np.int16).tobytes()
            
            with wave.open(output, 'wb') as wav_file:
                wav_file.setnchannels(2)  # Stereo
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(16000)  # 16kHz
                wav_file.writeframes(processed_audio)
            
        except Exception as e:
            print(f"Audio preprocessing error: {e}")
            # Fallback to original method
            with wave.open(output, 'wb') as wav_file:
                wav_file.setnchannels(2)
                wav_file.setsampwidth(2)
                wav_file.setframerate(16000)
                wav_file.writeframes(audio_data)
        
        output.seek(0)
        return output.read()
    
    def get_transcription_stats(self):
        """Get transcription performance statistics"""
        success_rate = 0
        if self.transcription_stats['total_attempts'] > 0:
            success_rate = (self.transcription_stats['successful_transcriptions'] / 
                          self.transcription_stats['total_attempts']) * 100
        
        return {
            'success_rate': f"{success_rate:.1f}%",
            'total_attempts': self.transcription_stats['total_attempts'],
            'successful_transcriptions': self.transcription_stats['successful_transcriptions'],
            'average_response_time': f"{self.transcription_stats['average_response_time']:.2f}s",
            'engine_usage': self.transcription_stats['engine_usage'],
            'primary_engine': self.primary_engine
        }
    
    def start_real_time_transcription(self, audio_queue):
        """Start enhanced real-time transcription"""
        transcription_thread = threading.Thread(
            target=self.process_audio_stream,
            args=(audio_queue,)
        )
        transcription_thread.daemon = True
        transcription_thread.start()
        
        print("Enhanced real-time transcription started")
        return transcription_thread