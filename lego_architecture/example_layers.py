"""
Example implementations of additional layers.

These show how easy it is to extend the system with new notation types!
"""

from visualization_system import Layer
import numpy as np
from typing import Dict, Any, List, Tuple
import matplotlib.pyplot as plt
from matplotlib.axes import Axes


# ============================================================================
# EXAMPLE 1: ONSET DETECTION LAYER
# ============================================================================

class OnsetLayer(Layer):
    """
    Detects note onsets and displays them as vertical lines.
    
    This is NEW functionality - but notice how simple it is to add!
    """
    
    def load_data(self, audio_path: str, **kwargs) -> bool:
        """Load onsets using librosa."""
        try:
            import librosa
            from modusa import load
            
            audio, sr, filename = load.audio(audio_path)
            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)
            
            # Detect onsets
            onsets = librosa.onset.onset_frames(audio, sr=sr)
            onset_times = librosa.frames_to_time(onsets, sr=sr)
            
            self._data = {
                "onset_times": onset_times,
                "num_onsets": len(onset_times)
            }
            print(f"✓ OnsetLayer: Detected {len(onset_times)} onsets")
            return True
        except Exception as e:
            print(f"✗ OnsetLayer error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw vertical lines at each onset."""
        if self._data is None:
            return [], []
        
        onset_times = self._data["onset_times"]
        
        # Draw vertical lines
        for onset in onset_times:
            ax.axvline(x=onset, color='green', alpha=0.3, linewidth=0.8, linestyle='--')
        
        # Add one line to legend (just the first one, to avoid clutter)
        if len(onset_times) > 0:
            line = ax.axvline(x=onset_times[0], color='green', alpha=0.3, 
                             linewidth=0.8, linestyle='--', label='Onsets')
            return [line], ['Onsets']
        
        return [], []


# ============================================================================
# EXAMPLE 2: CHROMA (PITCH CLASS) LAYER
# ============================================================================

class ChromaLayer(Layer):
    """
    Displays chroma features (pitch class distribution).
    
    Shows which pitch classes are most prominent over time.
    """
    
    def load_data(self, audio_path: str, **kwargs) -> bool:
        """Compute chroma features from audio."""
        try:
            import librosa
            from modusa import load
            
            audio, sr, filename = load.audio(audio_path)
            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)
            
            # Compute chroma features
            chroma = librosa.feature.chroma_cqt(y=audio, sr=sr)
            times = librosa.frames_to_time(np.arange(chroma.shape[1]), sr=sr)
            
            self._data = {
                "chroma": chroma,
                "times": times,
                "sr": sr
            }
            print(f"✓ ChromaLayer: Computed chroma features")
            return True
        except Exception as e:
            print(f"✗ ChromaLayer error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw chroma features as a heatmap."""
        if self._data is None:
            return [], []
        
        # Create a new subplot below the main one
        # (This is more complex - would need to handle figure layout)
        # For now, just print that chroma was loaded
        print(f"  - Chroma features shape: {self._data['chroma'].shape}")
        
        return [], []


# ============================================================================
# EXAMPLE 3: ENERGY ENVELOPE LAYER
# ============================================================================

class EnergyEnvelopeLayer(Layer):
    """
    Shows the energy envelope (loudness over time) of the audio.
    
    Useful for correlating with beat/onset detection.
    """
    
    def load_data(self, audio_path: str, **kwargs) -> bool:
        """Compute energy envelope."""
        try:
            import librosa
            from modusa import load
            
            audio, sr, filename = load.audio(audio_path)
            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)
            
            # Compute energy
            S = np.abs(librosa.stft(audio))
            energy = np.sqrt(np.sum(S**2, axis=0))
            times = librosa.frames_to_time(np.arange(len(energy)), sr=sr, hop_length=512)
            
            # Normalize to 0-100 for display
            energy_norm = (energy - np.min(energy)) / (np.max(energy) - np.min(energy)) * 100
            
            self._data = {
                "energy": energy_norm,
                "times": times
            }
            print(f"✓ EnergyEnvelopeLayer: Computed energy envelope")
            return True
        except Exception as e:
            print(f"✗ EnergyEnvelopeLayer error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw energy envelope on secondary y-axis."""
        if self._data is None:
            return [], []
        
        # Create secondary y-axis for energy
        ax2 = ax.twinx()
        
        # Plot energy
        line, = ax2.plot(self._data["times"], self._data["energy"], 
                        'orange', linewidth=1.5, alpha=0.7, label='Energy')
        
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Energy (%)', fontweight='bold', fontsize=10)
        
        return [line], ['Energy']


# ============================================================================
# EXAMPLE 4: TEMPOGRAM LAYER (Tempo changes over time)
# ============================================================================

class TempogramLayer(Layer):
    """
    Shows how the tempo changes throughout the piece.
    
    Useful for understanding rhythmic structure.
    """
    
    def load_data(self, beat_times: np.ndarray = None, **kwargs) -> bool:
        """Estimate tempo from beat times."""
        try:
            if beat_times is None:
                # Estimate from beat probabilities if available
                if 'beat_probs_file' in kwargs:
                    import numpy as np
                    data = np.load(kwargs['beat_probs_file'])
                    beat_times = data['beat_times']
                else:
                    print("⚠ TempogramLayer: No beat times provided")
                    return False
            
            # Compute inter-beat intervals (in BPM)
            ibi = np.diff(beat_times)  # Inter-beat intervals in seconds
            tempo_bpm = 60 / ibi  # Convert to BPM
            
            # Smooth tempo curve
            from scipy.ndimage import uniform_filter1d
            tempo_smooth = uniform_filter1d(tempo_bpm, size=5)
            
            self._data = {
                "beat_times": beat_times[:-1],  # Align with IBI
                "tempo": tempo_smooth
            }
            print(f"✓ TempogramLayer: Estimated tempo (avg: {np.mean(tempo_smooth):.1f} BPM)")
            return True
        except Exception as e:
            print(f"✗ TempogramLayer error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw tempo changes."""
        if self._data is None:
            return [], []
        
        ax2 = ax.twinx()
        
        line, = ax2.plot(self._data["beat_times"], self._data["tempo"],
                        'purple', linewidth=2, alpha=0.7, label='Tempo')
        
        ax2.set_ylabel('Tempo (BPM)', fontweight='bold', fontsize=10)
        
        return [line], ['Tempo']


# ============================================================================
# QUICK TEST: Try different combinations!
# ============================================================================

if __name__ == "__main__":
    # Note: You need the visualization_system module imported
    from visualization_system import Visualizer, SpectrogramLayer, BeatProbabilityLayer
    
    print("\n" + "="*70)
    print("EXAMPLE: Using multiple layers together")
    print("="*70)
    
    # Build a visualization with spectrogram + beats + onsets
    viz = Visualizer()
    viz.add_layer(SpectrogramLayer("Spectrogram"))
    viz.add_layer(BeatProbabilityLayer("Beat Probabilities"))
    viz.add_layer(OnsetLayer("Onsets"))
    
    # Load all data
    viz.load_all_layers(audio_path="Chopin_OP9_n2.wav")
    
    # Draw
    viz.draw()
    viz.show()
