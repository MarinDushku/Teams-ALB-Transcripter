import whisper
import queue
import threading
import time
import wave
import io
import numpy as np
import tempfile
import os
from datetime import datetime

class WhisperAlbanianTranscriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)
        self.audio_buffer = []
        self.buffer_lock = threading.Lock()
        self.transcription_callback = None
        
        print(f"Whisper {model_size} model loaded for Albanian transcription")
    
    def _init_albanian_asr(self):
        """Legacy method - now using Whisper"""
        pass
        
    def set_transcription_callback(self, callback):
        """Set callback function for real-time transcription results"""
        self.transcription_callback = callback
    
    def transcribe_albanian(self, audio_data):
        """Transcribe audio data to Albanian text using Whisper"""
        try:
            # Save audio data to temporary file for Whisper
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            # Transcribe with Whisper
            result = self.model.transcribe(
                temp_path,
                language="sq",  # Albanian language code
                word_timestamps=True,
                verbose=False
            )
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return result["text"].strip(), result.get("segments", [])
                
        except Exception as e:
            print(f"Whisper transcription error: {e}")
            return "", []
    
    def transcribe(self, audio_chunk):
        """Main transcription method"""
        text, segments = self.transcribe_albanian(audio_chunk)
        return text, segments
    
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
                        text, segments = self.transcribe_albanian(wav_data)
                        
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