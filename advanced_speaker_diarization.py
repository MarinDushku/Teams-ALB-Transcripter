import numpy as np
import threading
import time
from collections import deque
import pickle
import os
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import librosa

class AdvancedSpeakerDiarization:
    def __init__(self):
        self.speaker_profiles = {}
        self.current_speaker = None
        self.audio_features_history = deque(maxlen=200)
        self.speaker_counter = 0
        
        # Enhanced parameters
        self.silence_threshold = 300
        self.speaker_change_threshold = 0.4
        self.min_speech_duration = 0.5  # Minimum seconds to consider as speech
        self.voice_activity_buffer = deque(maxlen=10)
        
        # Voice embeddings for better identification
        self.feature_scaler = StandardScaler()
        self.clustering_model = DBSCAN(eps=0.3, min_samples=3)
        
        # Speaker profile persistence
        self.profiles_file = "speaker_profiles.pkl"
        self.load_speaker_profiles()
        
        # Advanced feature extraction
        self.sample_rate = 16000
        self.frame_length = int(0.025 * self.sample_rate)  # 25ms frames
        self.hop_length = int(0.010 * self.sample_rate)    # 10ms hop
        
        print("Advanced Speaker Diarization initialized")
    
    def extract_advanced_features(self, audio_chunk):
        """Extract comprehensive audio features for speaker identification"""
        try:
            # Convert bytes to numpy array
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32)
            audio_data = audio_data / 32768.0  # Normalize to [-1, 1]
            
            if len(audio_data) < self.frame_length:
                return None
            
            # Basic features
            energy = np.mean(audio_data ** 2)
            rms = np.sqrt(energy)
            zero_crossings = self._zero_crossing_rate(audio_data)
            
            # Spectral features
            try:
                # MFCCs (Mel-frequency cepstral coefficients)
                mfccs = librosa.feature.mfcc(
                    y=audio_data,
                    sr=self.sample_rate,
                    n_mfcc=13,
                    hop_length=self.hop_length,
                    n_fft=self.frame_length
                )
                mfcc_mean = np.mean(mfccs, axis=1)
                mfcc_std = np.std(mfccs, axis=1)
                
                # Spectral features
                spectral_centroid = np.mean(librosa.feature.spectral_centroid(
                    y=audio_data, sr=self.sample_rate, hop_length=self.hop_length
                ))
                spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(
                    y=audio_data, sr=self.sample_rate, hop_length=self.hop_length
                ))
                spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(
                    y=audio_data, sr=self.sample_rate, hop_length=self.hop_length
                ))
                
                # Fundamental frequency (pitch)
                f0 = librosa.yin(audio_data, fmin=50, fmax=400, sr=self.sample_rate)
                f0_mean = np.mean(f0[f0 > 0]) if np.any(f0 > 0) else 0
                f0_std = np.std(f0[f0 > 0]) if np.any(f0 > 0) else 0
                
            except Exception as e:
                print(f"Advanced feature extraction warning: {e}")
                # Fallback to basic features
                mfcc_mean = np.zeros(13)
                mfcc_std = np.zeros(13)
                spectral_centroid = self._simple_spectral_centroid(audio_data)
                spectral_rolloff = spectral_centroid * 1.2
                spectral_bandwidth = spectral_centroid * 0.5
                f0_mean = self._estimate_pitch(audio_data)
                f0_std = f0_mean * 0.1
            
            # Combine all features into a vector
            features = np.concatenate([
                [energy, rms, zero_crossings],
                [spectral_centroid, spectral_rolloff, spectral_bandwidth],
                [f0_mean, f0_std],
                mfcc_mean,
                mfcc_std
            ])
            
            return {
                'vector': features,
                'energy': energy,
                'rms': rms,
                'pitch': f0_mean,
                'spectral_centroid': spectral_centroid,
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            return None
    
    def _zero_crossing_rate(self, audio_data):
        """Calculate zero crossing rate"""
        return np.sum(np.abs(np.diff(np.sign(audio_data)))) / (2 * len(audio_data))
    
    def _simple_spectral_centroid(self, audio_data):
        """Simple spectral centroid calculation"""
        fft_data = np.abs(np.fft.fft(audio_data))
        freqs = np.fft.fftfreq(len(fft_data), 1/self.sample_rate)
        positive_freqs = freqs[:len(freqs)//2]
        positive_fft = fft_data[:len(fft_data)//2]
        
        if np.sum(positive_fft) > 0:
            return np.sum(positive_freqs * positive_fft) / np.sum(positive_fft)
        return 0
    
    def _estimate_pitch(self, audio_data):
        """Simple pitch estimation using autocorrelation"""
        try:
            # Autocorrelation
            correlation = np.correlate(audio_data, audio_data, mode='full')
            correlation = correlation[len(correlation)//2:]
            
            # Find peaks (excluding the first peak at lag 0)
            min_period = int(self.sample_rate / 400)  # Max 400 Hz
            max_period = int(self.sample_rate / 50)   # Min 50 Hz
            
            if len(correlation) > max_period:
                peaks = correlation[min_period:max_period]
                if len(peaks) > 0:
                    peak_idx = np.argmax(peaks) + min_period
                    return self.sample_rate / peak_idx
            
            return 150  # Default pitch
        except:
            return 150
    
    def detect_voice_activity(self, audio_chunk):
        """Enhanced voice activity detection with temporal smoothing"""
        try:
            audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
            energy = np.mean(audio_data ** 2)
            
            # Add to buffer for temporal smoothing
            self.voice_activity_buffer.append(energy > self.silence_threshold)
            
            # Require sustained activity
            if len(self.voice_activity_buffer) >= 3:
                return sum(self.voice_activity_buffer[-3:]) >= 2
            
            return energy > self.silence_threshold
        except:
            return False
    
    def identify_speaker(self, audio_chunk):
        """Advanced speaker identification using machine learning"""
        # Check voice activity first
        if not self.detect_voice_activity(audio_chunk):
            return None
        
        # Extract advanced features
        features = self.extract_advanced_features(audio_chunk)
        if not features:
            return None
        
        # Add to history
        self.audio_features_history.append(features)
        
        # Need minimum samples for reliable identification
        if len(self.audio_features_history) < 5:
            return self._simple_speaker_identification(features)
        
        # Use clustering for speaker identification
        speaker_id = self._advanced_speaker_classification(features)
        
        # Update current speaker with temporal consistency
        if speaker_id != self.current_speaker:
            # Require consistent detection before switching
            recent_identifications = [
                self._advanced_speaker_classification(f) 
                for f in list(self.audio_features_history)[-5:]
            ]
            
            if recent_identifications.count(speaker_id) >= 3:
                self.current_speaker = speaker_id
                print(f"Speaker changed to: {speaker_id}")
        
        return self.current_speaker or speaker_id
    
    def _simple_speaker_identification(self, features):
        """Fallback simple speaker identification"""
        if not self.speaker_profiles:
            self.speaker_counter += 1
            speaker_id = f"Speaker {self.speaker_counter}"
            self.speaker_profiles[speaker_id] = {
                'features': [features],
                'last_seen': time.time(),
                'total_speech_time': 0
            }
            return speaker_id
        
        # Find best match
        best_match = None
        best_distance = float('inf')
        
        for speaker_id, profile in self.speaker_profiles.items():
            if profile['features']:
                avg_vector = np.mean([f['vector'] for f in profile['features']], axis=0)
                distance = np.linalg.norm(features['vector'] - avg_vector)
                
                if distance < best_distance:
                    best_distance = distance
                    best_match = speaker_id
        
        # Create new speaker if distance too large
        if best_distance > self.speaker_change_threshold:
            self.speaker_counter += 1
            new_speaker_id = f"Speaker {self.speaker_counter}"
            self.speaker_profiles[new_speaker_id] = {
                'features': [features],
                'last_seen': time.time(),
                'total_speech_time': 0
            }
            return new_speaker_id
        else:
            # Update existing speaker
            self.speaker_profiles[best_match]['features'].append(features)
            self.speaker_profiles[best_match]['last_seen'] = time.time()
            
            # Limit feature history per speaker
            if len(self.speaker_profiles[best_match]['features']) > 50:
                self.speaker_profiles[best_match]['features'] = \
                    self.speaker_profiles[best_match]['features'][-50:]
            
            return best_match
    
    def _advanced_speaker_classification(self, features):
        """Advanced speaker classification using clustering"""
        try:
            # Collect recent feature vectors
            recent_features = [f['vector'] for f in list(self.audio_features_history)[-50:]]
            if len(recent_features) < 10:
                return self._simple_speaker_identification(features)
            
            # Normalize features
            feature_matrix = np.array(recent_features)
            normalized_features = self.feature_scaler.fit_transform(feature_matrix)
            
            # Cluster speakers
            cluster_labels = self.clustering_model.fit_predict(normalized_features)
            
            # Map current features to cluster
            current_normalized = self.feature_scaler.transform([features['vector']])
            distances = [
                np.linalg.norm(current_normalized[0] - normalized_features[i])
                for i in range(len(normalized_features))
            ]
            
            closest_idx = np.argmin(distances)
            cluster_id = cluster_labels[closest_idx]
            
            # Map cluster to speaker ID
            if cluster_id == -1:  # Noise/outlier
                return self._simple_speaker_identification(features)
            
            # Check if we've seen this cluster before
            speaker_id = f"Speaker {cluster_id + 1}"
            
            if speaker_id not in self.speaker_profiles:
                self.speaker_profiles[speaker_id] = {
                    'features': [features],
                    'last_seen': time.time(),
                    'total_speech_time': 0,
                    'cluster_id': cluster_id
                }
            else:
                self.speaker_profiles[speaker_id]['features'].append(features)
                self.speaker_profiles[speaker_id]['last_seen'] = time.time()
            
            return speaker_id
            
        except Exception as e:
            print(f"Advanced classification error: {e}")
            return self._simple_speaker_identification(features)
    
    def get_speaker_characteristics(self, speaker_id):
        """Get detailed characteristics of a speaker"""
        if speaker_id not in self.speaker_profiles:
            return None
        
        profile = self.speaker_profiles[speaker_id]
        features = profile['features']
        
        if not features:
            return None
        
        # Calculate statistics
        pitches = [f['pitch'] for f in features if f['pitch'] > 0]
        energies = [f['energy'] for f in features]
        spectral_centroids = [f['spectral_centroid'] for f in features]
        
        return {
            'speaker_id': speaker_id,
            'sample_count': len(features),
            'avg_pitch': np.mean(pitches) if pitches else 0,
            'pitch_range': np.std(pitches) if pitches else 0,
            'avg_energy': np.mean(energies),
            'energy_range': np.std(energies),
            'avg_spectral_centroid': np.mean(spectral_centroids),
            'voice_type': self._classify_voice_type(pitches, energies),
            'last_seen': profile['last_seen'],
            'total_speech_time': profile.get('total_speech_time', 0)
        }
    
    def _classify_voice_type(self, pitches, energies):
        """Classify voice type based on pitch and energy"""
        if not pitches:
            return "Unknown"
        
        avg_pitch = np.mean(pitches)
        avg_energy = np.mean(energies)
        
        if avg_pitch > 200:
            return "High Voice (likely female/child)"
        elif avg_pitch > 150:
            return "Medium Voice"
        else:
            return "Low Voice (likely male)"
    
    def save_speaker_profiles(self):
        """Save speaker profiles to disk"""
        try:
            with open(self.profiles_file, 'wb') as f:
                pickle.dump(self.speaker_profiles, f)
            print(f"Speaker profiles saved to {self.profiles_file}")
        except Exception as e:
            print(f"Error saving speaker profiles: {e}")
    
    def load_speaker_profiles(self):
        """Load speaker profiles from disk"""
        try:
            if os.path.exists(self.profiles_file):
                with open(self.profiles_file, 'rb') as f:
                    self.speaker_profiles = pickle.load(f)
                self.speaker_counter = len(self.speaker_profiles)
                print(f"Loaded {len(self.speaker_profiles)} speaker profiles")
            else:
                print("No existing speaker profiles found")
        except Exception as e:
            print(f"Error loading speaker profiles: {e}")
            self.speaker_profiles = {}
    
    def reset_speakers(self):
        """Reset all speaker profiles"""
        self.speaker_profiles = {}
        self.current_speaker = None
        self.speaker_counter = 0
        self.audio_features_history.clear()
        self.voice_activity_buffer.clear()
        
        # Remove saved profiles
        if os.path.exists(self.profiles_file):
            os.remove(self.profiles_file)
        
        print("All speaker profiles reset")
    
    def get_speaker_statistics(self):
        """Get comprehensive speaker statistics"""
        stats = {}
        total_speakers = len(self.speaker_profiles)
        
        for speaker_id, profile in self.speaker_profiles.items():
            characteristics = self.get_speaker_characteristics(speaker_id)
            if characteristics:
                stats[speaker_id] = characteristics
        
        return {
            'total_speakers': total_speakers,
            'current_speaker': self.current_speaker,
            'speaker_details': stats,
            'feature_history_size': len(self.audio_features_history)
        }
    
    def set_sensitivity(self, threshold):
        """Adjust speaker change sensitivity"""
        self.speaker_change_threshold = max(0.1, min(1.0, threshold))
        print(f"Speaker sensitivity set to: {self.speaker_change_threshold}")
    
    def get_current_speaker(self):
        """Get the currently active speaker"""
        return self.current_speaker