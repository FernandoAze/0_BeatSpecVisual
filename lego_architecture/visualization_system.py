"""
Lego-like visualization system using OOP.

The key idea: Each visual element is a Layer that knows how to draw itself.
The Visualizer assembles layers together without caring what they are.
"""

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Dict, Any, List, Tuple, Optional


# ============================================================================
# BASE LAYER CLASS (The "Lego brick" interface)
# ============================================================================

class Layer(ABC):
    """
    Abstract base class for all visualization layers.
    
    Think of this as the "Lego brick blueprint". Every layer must:
    1. Load its own data
    2. Know how to draw itself on an axes
    3. Return any lines/labels for legends
    """
    
    def __init__(self, name: str):
        """Initialize layer with a name"""
        self.name = name
        self._data = None
        self._lines = []
        self._labels = []
    
    @abstractmethod
    def load_data(self, **kwargs) -> bool:
        """Load data needed for this layer. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """
        Draw this layer on the given axes.
        
        Args:
            ax: The matplotlib axis to draw on
            shared_data: Dict with shared data (times, freqs, audio, etc)
        
        Returns:
            (lines, labels) for legend
        """
        pass
    
    def get_secondary_axis(self, ax: Axes) -> Optional[Axes]:
        """
        Some layers need a secondary axis (e.g., probabilities).
        Return None if not needed.
        """
        return None


# ============================================================================
# CONCRETE LAYERS (Different "Lego brick types")
# ============================================================================

class SpectrogramLayer(Layer):
    """The background spectrogram visualization."""
    
    def load_data(self, audio_path: str, **kwargs) -> bool:
        """Load and compute spectrogram from audio."""
        from modusa import load, compute
        import librosa
        
        try:
            audio, sr, filename = load.audio(audio_path)
            print(f"✓ SpectrogramLayer: Loaded {filename}")
            
            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)
            
            # Compute mel spectrogram
            winlen = int(0.256 * sr)
            hoplen = winlen // 16
            S_mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=winlen,
                                                   hop_length=hoplen, n_mels=512)
            S_db = librosa.power_to_db(S_mel, ref=np.max)
            
            mel_freqs = librosa.mel_frequencies(n_mels=512, fmin=0, fmax=6000)
            times = librosa.frames_to_time(np.arange(S_db.shape[1]), sr=sr, hop_length=hoplen)
            
            self._data = {
                "S_db": S_db,
                "freqs": mel_freqs,
                "times": times,
                "sr": sr,
                "filename": filename,
                "audio": audio
            }
            return True
        except Exception as e:
            print(f"✗ SpectrogramLayer error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw the spectrogram background."""
        from modusa import paint
        
        if self._data is None:
            print("✗ SpectrogramLayer: No data loaded")
            return [], []
        
        # Draw spectrogram
        paint.image(
            ax,
            self._data["S_db"],
            x=self._data["times"],
            y=self._data["freqs"],
            c="viridis",
            o="lower",
            clabel="Magnitude (dB)",
        )
        
        # Update shared data with spectrogram info
        shared_data.update(self._data)
        
        # Configure axes
        ax.set_ylim(self._data["freqs"][0], self._data["freqs"][-1])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_title(f"Spectrogram: {self._data['filename']}")
        
        return [], []  # No legend lines


class BeatProbabilityLayer(Layer):
    """Beat and downbeat probability lines."""
    
    def load_data(self, beat_probs_file: str = "beat_probs.npz", **kwargs) -> bool:
        """Load beat probabilities from .npz file."""
        try:
            data = np.load(beat_probs_file)
            self._data = {
                "beat_times": data['beat_times'],
                "beat_probs": data['beat_probs'],
                "downbeat_probs": data['downbeat_probs'],
            }
            print(f"✓ BeatProbabilityLayer: Loaded beat data")
            return True
        except Exception as e:
            print(f"✗ BeatProbabilityLayer error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw beat probabilities on a secondary axis."""
        if self._data is None:
            print("✗ BeatProbabilityLayer: No data loaded")
            return [], []
        
        # Create secondary axis
        ax2 = ax.twinx()
        self._secondary_ax = ax2
        
        lines = []
        labels = []
        
        # Beat probability
        beat_probs = self._data["beat_probs"]
        beat_min, beat_max = np.min(beat_probs), np.max(beat_probs)
        beat_percent = ((beat_probs - beat_min) / (beat_max - beat_min)) * 100 if beat_max > beat_min else beat_probs * 100
        
        line1, = ax2.plot(self._data["beat_times"], beat_percent, 'r-', 
                         linewidth=2, label='Beat Probability', alpha=0.9)
        lines.append(line1)
        labels.append('Beat Probability')
        
        # Downbeat probability
        downbeat_probs = self._data["downbeat_probs"]
        downbeat_min, downbeat_max = np.min(downbeat_probs), np.max(downbeat_probs)
        downbeat_percent = ((downbeat_probs - downbeat_min) / (downbeat_max - downbeat_min)) * 100 if downbeat_max > downbeat_min else downbeat_probs * 100
        
        line2, = ax2.plot(self._data["beat_times"], downbeat_percent, 'b-',
                         linewidth=2, label='Downbeat Probability', alpha=0.9)
        lines.append(line2)
        labels.append('Downbeat Probability')
        
        # Configure secondary axis
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Probability (%)', fontweight='bold', fontsize=11)
        
        return lines, labels
    
    def get_secondary_axis(self, ax: Axes) -> Axes:
        """Return the secondary axis for this layer."""
        return ax.twinx()


# Add more layers here as needed:
# class OnsetLayer(Layer): ...
# class ChromaLayer(Layer): ...
# class TempoLayer(Layer): ...


# ============================================================================
# VISUALIZER (The "Lego assembler")
# ============================================================================

class Visualizer:
    """
    Assembles multiple layers into a visualization.
    
    This is the key: you just add layers and it handles everything!
    """
    
    def __init__(self):
        """Initialize empty layer list."""
        self.layers: List[Layer] = []
        self.shared_data: Dict[str, Any] = {}
        self.fig = None
        self.ax = None
        self.all_lines = []
        self.all_labels = []
    
    def add_layer(self, layer: Layer) -> 'Visualizer':
        """Add a layer to the visualization. Returns self for chaining."""
        self.layers.append(layer)
        print(f"➕ Added layer: {layer.name}")
        return self  # Allow chaining: viz.add_layer(...).add_layer(...)
    
    def load_all_layers(self, **kwargs) -> bool:
        """Load data for all layers."""
        print("\n" + "="*60)
        print("LOADING LAYERS")
        print("="*60)
        
        for layer in self.layers:
            if not layer.load_data(**kwargs):
                print(f"⚠ Warning: Layer '{layer.name}' failed to load")
                return False
        
        return True
    
    def draw(self) -> Tuple[plt.Figure, plt.Axes]:
        """Draw all layers on the visualization."""
        print("\n" + "="*60)
        print("DRAWING VISUALIZATION")
        print("="*60)
        
        # Create figure and main axis
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        
        # Create colorbar axis (for spectrogram)
        cax = self.fig.add_axes([0.92, 0.15, 0.02, 0.7])
        
        # Draw each layer
        for layer in self.layers:
            print(f"Drawing layer: {layer.name}")
            lines, labels = layer.draw(self.ax, self.shared_data)
            self.all_lines.extend(lines)
            self.all_labels.extend(labels)
        
        # Add legend if there are labeled lines
        if self.all_lines:
            self.ax.legend(self.all_lines, self.all_labels, loc='upper right')
        
        # Keep secondary y-axis at 0-100% when zooming
        if len(self.layers) > 1:  # If we have probability layer
            def on_ylim_change(event_ax):
                if hasattr(self.ax, '_prob_ax'):
                    self.ax._prob_ax.set_ylim(0, 100)
            self.ax.callbacks.connect('ylim_changed', on_ylim_change)
        
        plt.subplots_adjust(left=0.1, right=0.88, top=0.95, bottom=0.1)
        
        return self.fig, self.ax
    
    def show(self):
        """Display the visualization."""
        plt.show()


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create visualizer
    viz = Visualizer()
    
    # Add layers in any order you want!
    viz.add_layer(SpectrogramLayer("Mel Spectrogram")).add_layer(
        BeatProbabilityLayer("Beat & Downbeat Probabilities")
    )
    
    # Load data
    viz.load_all_layers(
        audio_path="Chopin_OP9_n2.wav",
        beat_probs_file="beat_probs.npz"
    )
    
    # Draw and show
    viz.draw()
    viz.show()
    
    print("\n✓ Visualization complete!")
