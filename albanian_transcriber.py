import speech_recognition as sr
import queue
import threading
import time
import wave
import io
import numpy as np
from datetime import datetime

class AlbanianRealTimeTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.albanian_model = None
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        self.transcription_callback = None
        
        # Configure recognizer for better performance
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        
        # Initialize Albanian ASR (placeholder for actual implementation)
        self._init_albanian_asr()
    
    def _init_albanian_asr(self):
        """Initialize Albanian ASR model"""
        # Placeholder for Albanian-ASR integration
        # In actual implementation, this would load the Albanian-ASR model
        # from https://github.com/florijanqosja/Albanian-ASR
        print("Albanian ASR model initialized (placeholder)")
        
    def set_transcription_callback(self, callback):
        """Set callback function for real-time transcription results"""
        self.transcription_callback = callback
    
    def transcribe_albanian(self, audio_data):
        """Transcribe audio data to Albanian text"""
        try:
            # Convert audio data to format suitable for recognition
            audio_file = io.BytesIO(audio_data)
            
            # Use speech_recognition with fallback to Google's API
            # In production, this would use the Albanian-ASR model
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # Placeholder transcription (in real implementation, use Albanian-ASR)
            # For now, using Google's API as fallback
            try:
                text = self.recognizer.recognize_google(audio, language='sq-AL')  # Albanian language code
                return text
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                # Fallback to offline Albanian processing
                return self._offline_albanian_transcribe(audio_data)
                
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
    
    def _offline_albanian_transcribe(self, audio_data):
        """Offline Albanian transcription using Albanian-ASR model"""
        # Placeholder for actual Albanian-ASR implementation
        # This would integrate with the Albanian-ASR GitHub project
        # For now, return empty string
        return ""
    
    def process_audio_stream(self, audio_queue):
        """Process continuous audio stream for real-time transcription"""
        while True:
            try:
                # Collect audio chunks
                chunk = audio_queue.get(timeout=1)
                
                with self.buffer_lock:
                    self.audio_buffer.append(chunk)
                    
                    # Process every 2-3 seconds for live transcription
                    if len(self.audio_buffer) >= 32:  # ~2 seconds at 16kHz
                        combined_audio = b''.join(self.audio_buffer)
                        
                        # Create WAV format for recognition
                        wav_data = self._create_wav_data(combined_audio)
                        text = self.transcribe_albanian(wav_data)
                        
                        if text and self.transcription_callback:
                            timestamp = datetime.now().strftime("%H:%M:%S")
                            self.transcription_callback(text, timestamp)
                        
                        # Keep some overlap for context
                        self.audio_buffer = self.audio_buffer[-8:]  # Keep last 0.5 seconds
                        
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Audio processing error: {e}")
                continue
    
    def _create_wav_data(self, audio_data):
        """Create WAV format data from raw audio"""
        output = io.BytesIO()
        
        with wave.open(output, 'wb') as wav_file:
            wav_file.setnchannels(2)  # Stereo
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(16000)  # 16kHz
            wav_file.writeframes(audio_data)
        
        output.seek(0)
        return output.read()
    
    def start_real_time_transcription(self, audio_queue):
        """Start real-time transcription in a separate thread"""
        transcription_thread = threading.Thread(
            target=self.process_audio_stream,
            args=(audio_queue,)
        )
        transcription_thread.daemon = True
        transcription_thread.start()
        return transcription_thread