import numpy as np
import tempfile
import os
import json
from scipy.spatial.distance import cosine
try:
    from speechbrain.inference.speaker import EncoderClassifier
    SPEECHBRAIN_AVAILABLE = True
except ImportError:
    SPEECHBRAIN_AVAILABLE = False
    print("speechbrain not available, speaker enrollment disabled")

class SpeakerEnrollment:
    def __init__(self):
        self.known_speakers = {}  # {name: embedding}
        self.speaker_db_file = "speaker_profiles.json"
        
        # Initialize speaker encoder if available
        if SPEECHBRAIN_AVAILABLE:
            try:
                self.encoder = EncoderClassifier.from_hparams(
                    source="speechbrain/spkrec-ecapa-voxceleb"
                )
                print("SpeechBrain speaker encoder loaded")
            except Exception as e:
                print(f"Failed to load SpeechBrain encoder: {e}")
                self.encoder = None
        else:
            self.encoder = None
        
        # Load existing speaker profiles
        self.load_speaker_profiles()
    
    def enroll_speaker(self, name, audio_samples):
        """Enroll a known speaker with their name"""
        if not self.encoder:
            print("Speaker encoder not available")
            return False
        
        try:
            embeddings = []
            for audio_sample in audio_samples:
                # Save audio sample to temporary file
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    temp_file.write(audio_sample)
                    temp_path = temp_file.name
                
                # Extract embedding
                emb = self.encoder.encode_batch(temp_path)
                embeddings.append(emb.squeeze().cpu().numpy())
                
                # Clean up
                os.unlink(temp_path)
            
            # Average embeddings for robustness
            avg_embedding = np.mean(embeddings, axis=0)
            self.known_speakers[name] = avg_embedding.tolist()  # Convert to list for JSON serialization
            
            # Save to disk
            self.save_speaker_profiles()
            print(f"Speaker {name} enrolled successfully")
            return True
            
        except Exception as e:
            print(f"Error enrolling speaker {name}: {e}")
            return False
    
    def identify_speaker(self, audio_segment):
        """Identify speaker by comparing to enrolled speakers"""
        if not self.encoder or not self.known_speakers:
            return "Unknown Speaker"
        
        try:
            # Save audio segment to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_segment)
                temp_path = temp_file.name
            
            # Extract embedding for the segment
            segment_emb = self.encoder.encode_batch(temp_path)
            segment_emb = segment_emb.squeeze().cpu().numpy()
            
            # Clean up
            os.unlink(temp_path)
            
            best_match = None
            best_similarity = 0.5  # Threshold for positive identification
            
            for name, known_emb in self.known_speakers.items():
                known_emb = np.array(known_emb)  # Convert back from list
                similarity = 1 - cosine(segment_emb, known_emb)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = name
            
            return best_match or "Unknown Speaker"
            
        except Exception as e:
            print(f"Error identifying speaker: {e}")
            return "Unknown Speaker"
    
    def save_speaker_profiles(self):
        """Save speaker profiles to disk"""
        try:
            with open(self.speaker_db_file, 'w') as f:
                json.dump(self.known_speakers, f, indent=2)
        except Exception as e:
            print(f"Error saving speaker profiles: {e}")
    
    def load_speaker_profiles(self):
        """Load speaker profiles from disk"""
        try:
            if os.path.exists(self.speaker_db_file):
                with open(self.speaker_db_file, 'r') as f:
                    self.known_speakers = json.load(f)
                print(f"Loaded {len(self.known_speakers)} speaker profiles")
            else:
                print("No existing speaker profiles found")
        except Exception as e:
            print(f"Error loading speaker profiles: {e}")
            self.known_speakers = {}
    
    def list_enrolled_speakers(self):
        """List all enrolled speakers"""
        return list(self.known_speakers.keys())
    
    def remove_speaker(self, name):
        """Remove a speaker from the database"""
        if name in self.known_speakers:
            del self.known_speakers[name]
            self.save_speaker_profiles()
            print(f"Speaker {name} removed")
            return True
        else:
            print(f"Speaker {name} not found")
            return False
    
    def get_speaker_count(self):
        """Get the number of enrolled speakers"""
        return len(self.known_speakers)