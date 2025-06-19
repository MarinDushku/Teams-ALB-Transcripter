import numpy as np
import threading
import time
from collections import deque
import hashlib

class SpeakerIdentifier:
    def __init__(self):
        self.speaker_profiles = {}
        self.current_speaker = None
        self.audio_features_history = deque(maxlen=100)
        self.speaker_counter = 0
        self.silence_threshold = 500  # Threshold for detecting silence
        self.speaker_change_threshold = 0.3  # Threshold for detecting speaker change
        
    def extract_audio_features(self, audio_chunk):
        """Extract basic audio features for speaker identification"""
        try:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            
            if len(audio_data) == 0:
                return None
            
            # Basic features for speaker identification
            features = {
                'energy': np.mean(audio_data ** 2),
                'zero_crossings': self._zero_crossing_rate(audio_data),
                'spectral_centroid': self._spectral_centroid(audio_data),
                'rms': np.sqrt(np.mean(audio_data ** 2))
            }
            
            return features
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            return None
    
    def _zero_crossing_rate(self, audio_data):
        """Calculate zero crossing rate"""
        return np.sum(np.abs(np.diff(np.sign(audio_data)))) / (2 * len(audio_data))
    
    def _spectral_centroid(self, audio_data):
        """Calculate spectral centroid (simplified version)"""
        # Simple approximation using frequency bins
        fft_data = np.abs(np.fft.fft(audio_data))
        freqs = np.fft.fftfreq(len(fft_data))
        return np.sum(freqs * fft_data) / np.sum(fft_data) if np.sum(fft_data) > 0 else 0
    
    def detect_voice_activity(self, audio_chunk):
        """Simple voice activity detection"""
        try:
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            energy = np.mean(audio_data ** 2)
            return energy > self.silence_threshold
        except:
            return False
    
    def identify_speaker(self, audio_chunk):
        """Identify speaker from audio chunk"""
        # Check if there's voice activity
        if not self.detect_voice_activity(audio_chunk):
            return None
        
        # Extract features
        features = self.extract_audio_features(audio_chunk)
        if not features:
            return None
        
        # Add to history
        self.audio_features_history.append(features)
        
        # Determine speaker
        speaker_id = self._classify_speaker(features)
        
        # Update current speaker if changed
        if speaker_id != self.current_speaker:
            self.current_speaker = speaker_id
            
        return speaker_id
    
    def _classify_speaker(self, features):
        """Classify speaker based on audio features"""
        if not self.speaker_profiles:
            # First speaker
            self.speaker_counter += 1
            speaker_id = f"Speaker {self.speaker_counter}"
            self.speaker_profiles[speaker_id] = {
                'features': [features],
                'last_seen': time.time()
            }
            return speaker_id
        
        # Find closest matching speaker
        best_match = None
        best_distance = float('inf')
        
        for speaker_id, profile in self.speaker_profiles.items():
            distance = self._calculate_feature_distance(features, profile['features'])
            if distance < best_distance:
                best_distance = distance
                best_match = speaker_id
        
        # If the best match is too far, create new speaker
        if best_distance > self.speaker_change_threshold:
            self.speaker_counter += 1
            new_speaker_id = f"Speaker {self.speaker_counter}"
            self.speaker_profiles[new_speaker_id] = {
                'features': [features],
                'last_seen': time.time()
            }
            return new_speaker_id
        else:
            # Update existing speaker profile
            self.speaker_profiles[best_match]['features'].append(features)
            self.speaker_profiles[best_match]['last_seen'] = time.time()
            
            # Keep only recent features (sliding window)
            if len(self.speaker_profiles[best_match]['features']) > 20:
                self.speaker_profiles[best_match]['features'] = \
                    self.speaker_profiles[best_match]['features'][-20:]
            
            return best_match
    
    def _calculate_feature_distance(self, features1, feature_list):
        """Calculate distance between current features and speaker profile"""
        if not feature_list:
            return float('inf')
        
        # Calculate average features for the speaker
        avg_features = {}
        for key in features1.keys():
            avg_features[key] = np.mean([f[key] for f in feature_list if key in f])
        
        # Calculate Euclidean distance
        distance = 0
        for key in features1.keys():
            if key in avg_features:
                distance += (features1[key] - avg_features[key]) ** 2
        
        return np.sqrt(distance)
    
    def get_speaker_statistics(self):
        """Get statistics about identified speakers"""
        stats = {}
        for speaker_id, profile in self.speaker_profiles.items():
            stats[speaker_id] = {
                'samples': len(profile['features']),
                'last_seen': time.time() - profile['last_seen'],
                'avg_energy': np.mean([f['energy'] for f in profile['features']]),
                'avg_rms': np.mean([f['rms'] for f in profile['features']])
            }
        return stats
    
    def reset_speakers(self):
        """Reset all speaker profiles"""
        self.speaker_profiles = {}
        self.current_speaker = None
        self.speaker_counter = 0
        self.audio_features_history.clear()
    
    def get_current_speaker(self):
        """Get the currently active speaker"""
        return self.current_speaker
    
    def set_sensitivity(self, threshold):
        """Adjust speaker change sensitivity (0.1 = very sensitive, 1.0 = less sensitive)"""
        self.speaker_change_threshold = max(0.1, min(1.0, threshold))