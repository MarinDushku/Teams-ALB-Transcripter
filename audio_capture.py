try:
    import pyaudiowpatch as pyaudio
    WASAPI_AVAILABLE = True
except ImportError:
    import pyaudio
    WASAPI_AVAILABLE = False
import threading
import queue
import wave
import numpy as np

class TeamsAudioCapture:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device = self.find_wasapi_loopback() if WASAPI_AVAILABLE else self.find_system_audio_device()
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.stream = None
        
    def find_wasapi_loopback(self):
        """Find WASAPI loopback device for capturing speaker output"""
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if ("WASAPI" in dev['name'] and 
                dev['maxInputChannels'] > 0 and 
                dev['hostApi'] == 3):  # WASAPI host API
                print(f"Found WASAPI loopback device: {dev['name']}")
                return dev
        return None
    
    def find_system_audio_device(self):
        """Find the system audio output device (speakers/headphones) - fallback"""
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            # Look for devices with input capability
            if device_info["maxInputChannels"] > 0:
                return device_info
        
        # Fallback to default input device
        return self.p.get_default_input_device_info()
    
    def start_capture(self):
        """Start capturing system audio"""
        if self.is_recording:
            return
            
        if not self.device:
            print("No suitable audio device found!")
            return
            
        try:
            # Configure stream parameters based on device capabilities
            stream_kwargs = {
                'format': pyaudio.paInt16,
                'channels': min(2, self.device['maxInputChannels']),
                'rate': 16000,  # Standard for speech recognition
                'input': True,
                'input_device_index': self.device['index'],
                'frames_per_buffer': 1024
            }
            
            # Add loopback parameter if using WASAPI
            if WASAPI_AVAILABLE and "WASAPI" in self.device['name']:
                stream_kwargs['as_loopback'] = True
                
            self.stream = self.p.open(**stream_kwargs)
            
            self.is_recording = True
            self.capture_thread = threading.Thread(target=self._capture_loop)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            print(f"Started audio capture from: {self.device['name']}")
            
        except Exception as e:
            print(f"Error starting audio capture: {e}")
            self.is_recording = False
    
    def _capture_loop(self):
        """Main audio capture loop"""
        while self.is_recording:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                print(f"Audio capture error: {e}")
                break
    
    def stop_capture(self):
        """Stop audio capture"""
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
    def get_audio_chunk(self, timeout=1):
        """Get audio chunk from queue"""
        try:
            return self.audio_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def save_audio_buffer(self, filename, audio_data):
        """Save audio buffer to WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(2)
            wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(16000)
            wf.writeframes(b''.join(audio_data))
    
    def __del__(self):
        """Cleanup"""
        self.stop_capture()
        if hasattr(self, 'p'):
            self.p.terminate()