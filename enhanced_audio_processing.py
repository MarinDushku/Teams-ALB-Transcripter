import pyaudio
try:
    import pyaudiowpatch as pyaudio
except ImportError:
    import pyaudio
import threading
import queue
import wave
import numpy as np
import scipy.signal
from scipy.fft import fft, fftfreq
import time

class EnhancedAudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.device = self.find_best_audio_device()
        self.audio_queue = queue.Queue()
        self.processed_queue = queue.Queue()
        self.is_recording = False
        self.stream = None
        
        # Enhanced audio parameters
        self.sample_rate = 16000
        self.channels = 1  # Mono for better processing
        self.chunk_size = 1024
        self.format = pyaudio.paInt16
        
        # Noise reduction parameters
        self.noise_profile = None
        self.noise_gate_threshold = 0.01
        self.noise_reduction_factor = 0.5
        
        # Audio enhancement settings
        self.enable_noise_reduction = True
        self.enable_echo_cancellation = True
        self.enable_gain_control = True
        self.enable_high_pass_filter = True
        
        # Adaptive parameters
        self.background_noise_estimate = 0
        self.signal_history = []
        self.max_history_length = 100
        
        print("Enhanced Audio Processor initialized")
    
    def find_best_audio_device(self):
        """Find the best available audio input device"""
        best_device = None
        best_score = 0
        
        for i in range(self.p.get_device_count()):
            try:
                device_info = self.p.get_device_info_by_index(i)
                
                # Score devices based on capabilities
                score = 0
                device_name = device_info["name"].lower()
                
                # Prefer WASAPI loopback devices for system audio
                if "wasapi" in device_name and "loopback" in device_name:
                    score += 100
                elif "stereo mix" in device_name:
                    score += 90
                elif "what u hear" in device_name:
                    score += 85
                
                # Prefer devices with good input capabilities
                if device_info["maxInputChannels"] >= 2:
                    score += 20
                elif device_info["maxInputChannels"] >= 1:
                    score += 10
                
                # Prefer higher sample rates
                if device_info["defaultSampleRate"] >= 44100:
                    score += 15
                elif device_info["defaultSampleRate"] >= 16000:
                    score += 10
                
                # Avoid problematic devices
                if any(term in device_name for term in ["bluetooth", "virtual", "mapper"]):
                    score -= 20
                
                if score > best_score:
                    best_score = score
                    best_device = device_info
                    
            except Exception as e:
                print(f"Error checking device {i}: {e}")
                continue
        
        if best_device:
            print(f"Selected audio device: {best_device['name']} (score: {best_score})")
            return best_device
        else:
            # Fallback to default input device
            return self.p.get_default_input_device_info()
    
    def estimate_noise_profile(self, duration=2.0):
        """Estimate background noise profile for noise reduction"""
        print("Estimating noise profile... Please remain quiet.")
        
        try:
            # Record silence for noise profiling
            noise_stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device['index'],
                frames_per_buffer=self.chunk_size
            )
            
            noise_samples = []
            frames_to_record = int((duration * self.sample_rate) / self.chunk_size)
            
            for _ in range(frames_to_record):
                data = noise_stream.read(self.chunk_size, exception_on_overflow=False)
                audio_array = np.frombuffer(data, dtype=np.int16).astype(np.float32)
                noise_samples.extend(audio_array)
            
            noise_stream.stop_stream()
            noise_stream.close()
            
            # Calculate noise spectrum
            noise_array = np.array(noise_samples)
            noise_fft = np.abs(fft(noise_array))
            self.noise_profile = noise_fft[:len(noise_fft)//2]
            self.background_noise_estimate = np.mean(np.abs(noise_array))
            
            print(f"Noise profile estimated: {self.background_noise_estimate:.4f}")
            return True
            
        except Exception as e:
            print(f"Error estimating noise profile: {e}")
            return False
    
    def apply_noise_reduction(self, audio_data):
        """Apply spectral subtraction noise reduction"""
        if not self.enable_noise_reduction or self.noise_profile is None:
            return audio_data
        
        try:
            # Convert to frequency domain
            audio_fft = fft(audio_data)
            audio_magnitude = np.abs(audio_fft)
            audio_phase = np.angle(audio_fft)
            
            # Apply spectral subtraction
            half_length = len(audio_magnitude) // 2
            noise_estimate = self.noise_profile[:min(half_length, len(self.noise_profile))]
            
            # Extend noise profile if needed
            if len(noise_estimate) < half_length:
                noise_estimate = np.tile(noise_estimate, (half_length // len(noise_estimate) + 1))[:half_length]
            
            # Spectral subtraction with over-subtraction factor
            alpha = 2.0  # Over-subtraction factor
            enhanced_magnitude = audio_magnitude[:half_length] - alpha * noise_estimate
            
            # Apply spectral floor to prevent artifacts
            spectral_floor = 0.1 * audio_magnitude[:half_length]
            enhanced_magnitude = np.maximum(enhanced_magnitude, spectral_floor)
            
            # Reconstruct full spectrum
            full_magnitude = np.concatenate([enhanced_magnitude, enhanced_magnitude[-2:0:-1]])
            full_phase = audio_phase[:len(full_magnitude)]
            
            # Convert back to time domain
            enhanced_fft = full_magnitude * np.exp(1j * full_phase)
            enhanced_audio = np.real(np.fft.ifft(enhanced_fft))
            
            return enhanced_audio.astype(np.float32)
            
        except Exception as e:
            print(f"Noise reduction error: {e}")
            return audio_data
    
    def apply_high_pass_filter(self, audio_data, cutoff_freq=100):
        """Apply high-pass filter to remove low-frequency noise"""
        if not self.enable_high_pass_filter:
            return audio_data
        
        try:
            # Design Butterworth high-pass filter
            nyquist = self.sample_rate / 2
            normalized_cutoff = cutoff_freq / nyquist
            b, a = scipy.signal.butter(4, normalized_cutoff, btype='high')
            
            # Apply filter
            filtered_audio = scipy.signal.filtfilt(b, a, audio_data)
            return filtered_audio.astype(np.float32)
            
        except Exception as e:
            print(f"High-pass filter error: {e}")
            return audio_data
    
    def apply_noise_gate(self, audio_data):
        """Apply noise gate to remove quiet background noise"""
        try:
            # Calculate audio energy
            energy = np.mean(audio_data ** 2)
            
            # Adaptive threshold based on background noise
            threshold = max(self.noise_gate_threshold, self.background_noise_estimate * 2)
            
            if energy < threshold:
                # Apply soft gating (gradual reduction rather than hard cut)
                gate_factor = energy / threshold
                return audio_data * gate_factor
            
            return audio_data
            
        except Exception as e:
            print(f"Noise gate error: {e}")
            return audio_data
    
    def apply_automatic_gain_control(self, audio_data):
        """Apply automatic gain control for consistent volume"""
        if not self.enable_gain_control:
            return audio_data
        
        try:
            # Calculate RMS level
            rms = np.sqrt(np.mean(audio_data ** 2))
            
            if rms > 0:
                # Target RMS level (adjust as needed)
                target_rms = 0.1
                gain = target_rms / rms
                
                # Limit gain to prevent over-amplification
                gain = np.clip(gain, 0.1, 10.0)
                
                # Apply smooth gain adjustment
                return audio_data * gain
            
            return audio_data
            
        except Exception as e:
            print(f"AGC error: {e}")
            return audio_data
    
    def apply_echo_cancellation(self, audio_data):
        """Simple echo cancellation using adaptive filtering"""
        if not self.enable_echo_cancellation:
            return audio_data
        
        try:
            # Simple echo suppression using spectral subtraction
            # This is a basic implementation - professional AEC is much more complex
            
            # Store recent signal history
            self.signal_history.append(audio_data.copy())
            if len(self.signal_history) > self.max_history_length:
                self.signal_history.pop(0)
            
            # Look for delayed versions of the signal (echo detection)
            if len(self.signal_history) >= 10:
                # Cross-correlation with delayed versions
                correlations = []
                for i in range(5, min(len(self.signal_history), 20)):
                    correlation = np.corrcoef(audio_data, self.signal_history[-i])[0, 1]
                    correlations.append(correlation)
                
                # If high correlation found, apply echo suppression
                max_correlation = np.max(correlations)
                if max_correlation > 0.7:  # Echo detected
                    echo_reduction_factor = 0.7
                    return audio_data * echo_reduction_factor
            
            return audio_data
            
        except Exception as e:
            print(f"Echo cancellation error: {e}")
            return audio_data
    
    def process_audio_chunk(self, raw_audio):
        """Apply comprehensive audio processing pipeline"""
        try:
            # Convert to float32 for processing
            audio_data = np.frombuffer(raw_audio, dtype=np.int16).astype(np.float32)
            audio_data = audio_data / 32768.0  # Normalize to [-1, 1]
            
            # Apply processing pipeline
            if len(audio_data) > 0:
                # 1. High-pass filter (remove low-frequency noise)
                audio_data = self.apply_high_pass_filter(audio_data)
                
                # 2. Noise gate (remove quiet background)
                audio_data = self.apply_noise_gate(audio_data)
                
                # 3. Noise reduction (spectral subtraction)
                audio_data = self.apply_noise_reduction(audio_data)
                
                # 4. Echo cancellation
                audio_data = self.apply_echo_cancellation(audio_data)
                
                # 5. Automatic gain control
                audio_data = self.apply_automatic_gain_control(audio_data)
                
                # Update background noise estimate
                current_energy = np.mean(np.abs(audio_data))
                self.background_noise_estimate = (
                    0.95 * self.background_noise_estimate + 0.05 * current_energy
                )
            
            # Convert back to int16
            processed_audio = (audio_data * 32767).astype(np.int16)
            return processed_audio.tobytes()
            
        except Exception as e:
            print(f"Audio processing error: {e}")
            return raw_audio  # Return original if processing fails
    
    def start_capture(self):
        """Start enhanced audio capture with processing"""
        if self.is_recording:
            return
        
        try:
            # Estimate noise profile before starting
            if self.noise_profile is None:
                self.estimate_noise_profile(1.0)  # Quick noise estimation
            
            # Open audio stream
            self.stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device['index'],
                frames_per_buffer=self.chunk_size
            )
            
            self.is_recording = True
            
            # Start capture and processing threads
            self.capture_thread = threading.Thread(target=self._capture_loop)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            self.processing_thread = threading.Thread(target=self._processing_loop)
            self.processing_thread.daemon = True
            self.processing_thread.start()
            
            print(f"Enhanced audio capture started from: {self.device['name']}")
            
        except Exception as e:
            print(f"Error starting enhanced audio capture: {e}")
            self.is_recording = False
    
    def _capture_loop(self):
        """Raw audio capture loop"""
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                self.audio_queue.put(data)
            except Exception as e:
                print(f"Enhanced capture error: {e}")
                break
    
    def _processing_loop(self):
        """Audio processing loop"""
        while self.is_recording:
            try:
                # Get raw audio with timeout
                raw_audio = self.audio_queue.get(timeout=1)
                
                # Process audio
                processed_audio = self.process_audio_chunk(raw_audio)
                
                # Put processed audio in output queue
                self.processed_queue.put(processed_audio)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Enhanced processing error: {e}")
                continue
    
    def get_audio_chunk(self, timeout=1):
        """Get processed audio chunk"""
        try:
            return self.processed_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def stop_capture(self):
        """Stop enhanced audio capture"""
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        print("Enhanced audio capture stopped")
    
    def get_audio_stats(self):
        """Get audio processing statistics"""
        return {
            'device_name': self.device['name'],
            'sample_rate': self.sample_rate,
            'channels': self.channels,
            'background_noise_level': f"{self.background_noise_estimate:.4f}",
            'noise_reduction_enabled': self.enable_noise_reduction,
            'echo_cancellation_enabled': self.enable_echo_cancellation,
            'gain_control_enabled': self.enable_gain_control,
            'high_pass_filter_enabled': self.enable_high_pass_filter,
            'queue_sizes': {
                'raw_audio': self.audio_queue.qsize(),
                'processed_audio': self.processed_queue.qsize()
            }
        }
    
    def configure_processing(self, **kwargs):
        """Configure audio processing parameters"""
        if 'noise_reduction' in kwargs:
            self.enable_noise_reduction = kwargs['noise_reduction']
        if 'echo_cancellation' in kwargs:
            self.enable_echo_cancellation = kwargs['echo_cancellation']
        if 'gain_control' in kwargs:
            self.enable_gain_control = kwargs['gain_control']
        if 'high_pass_filter' in kwargs:
            self.enable_high_pass_filter = kwargs['high_pass_filter']
        if 'noise_gate_threshold' in kwargs:
            self.noise_gate_threshold = kwargs['noise_gate_threshold']
        
        print("Audio processing configuration updated")
    
    def __del__(self):
        """Cleanup"""
        self.stop_capture()
        if hasattr(self, 'p'):
            self.p.terminate()