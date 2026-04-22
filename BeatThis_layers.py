"""
BeatThis! algorithm visualization layers.
Contains all visualization layers specific to the BeatThis! beat tracking algorithm.
"""

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Dict, Any, List, Tuple, Optional


# Import Layer base class
from visualization_system import Layer


class BeatThisLayer(Layer):
    """Base class for BeatThis! algorithm visualization layers.
    
    Manages shared audio/beat data loading and probability visualization.
    All BeatThis! output layers inherit from this class to share common parameters.
    """
    
    def __init__(self, name: str = "BeatThis Layer"):
        super().__init__(name)
        self._beat_times = None
    
    def _load_beat_times(self, beat_probs_file: str = "beat_probs.npz") -> bool:
        """Load beat times from .npz file (shared across all BeatThis! layers)"""
        try:
            data = np.load(beat_probs_file)
            self._beat_times = data['beat_times']
            return True
        except Exception as e:
            print(f"✗ {self.name}: Error loading beat times - {e}")
            return False
    
    def _normalize_probabilities(self, probs: np.ndarray) -> np.ndarray:
        """Convert raw probabilities to 0-100% scale"""
        prob_min, prob_max = np.min(probs), np.max(probs)
        if prob_max > prob_min:
            return ((probs - prob_min) / (prob_max - prob_min)) * 100
        return probs * 100
    
    def _setup_probability_axis(self, ax: Axes, shared_data: Dict[str, Any]) -> Axes:
        """Get or create secondary axis for probability visualization"""
        if "ax2" not in shared_data:
            ax2 = ax.twinx()
            shared_data["ax2"] = ax2
        else:
            ax2 = shared_data["ax2"]
        
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Probability (%)', fontweight='bold', fontsize=11)
        return ax2
    
    def _register_ylim_callback(self, ax: Axes, ax2: Axes):
        """Register callback to maintain probability axis at 0-100% during zoom"""
        def on_ylim_change(event):
            """Keep secondary y-axis at 0-100% when user zooms on frequency axis"""
            ax2.set_ylim(0, 100)
        ax.callbacks.connect('ylim_changed', on_ylim_change)


class BeatProbabilityLayer(BeatThisLayer):
    """Visualizes beat probability outputs from BeatThis! algorithm."""
    
    def load_data(self, beat_probs_file: str = "beat_probs.npz", **kwargs) -> bool:
        if not self._load_beat_times(beat_probs_file):
            return False
        try:
            data = np.load(beat_probs_file)
            self._data = {
                "beat_times": self._beat_times,
                "beat_probs": data['beat_probs'],
            }
            print(f"✓ {self.name}: Loaded beat data")
            return True
        except Exception as e:
            print(f"✗ {self.name} error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        if self._data is None:
            print(f"✗ {self.name}: No data loaded")
            return [], []
        
        ax2 = self._setup_probability_axis(ax, shared_data)
        beat_percent = self._normalize_probabilities(self._data["beat_probs"])
        
        line1, = ax2.plot(self._data["beat_times"], beat_percent, 'r-', 
                         linewidth=2, label='Beat Probability', alpha=0.9)
        
        self._register_ylim_callback(ax, ax2)
        
        return [line1], ['Beat Probability']


class DownbeatProbabilityLayer(BeatThisLayer):
    """Visualizes downbeat probability outputs from BeatThis! algorithm."""
    
    def load_data(self, beat_probs_file: str = "beat_probs.npz", **kwargs) -> bool:
        if not self._load_beat_times(beat_probs_file):
            return False
        try:
            data = np.load(beat_probs_file)
            self._data = {
                "beat_times": self._beat_times,
                "downbeat_probs": data['downbeat_probs'],
            }
            print(f"✓ {self.name}: Loaded downbeat data")
            return True
        except Exception as e:
            print(f"✗ {self.name} error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        if self._data is None:
            print(f"✗ {self.name}: No data loaded")
            return [], []
        
        ax2 = self._setup_probability_axis(ax, shared_data)
        downbeat_percent = self._normalize_probabilities(self._data["downbeat_probs"])
        
        line2, = ax2.plot(self._data["beat_times"], downbeat_percent, 'b-',
                         linewidth=2, label='Downbeat Probability', alpha=0.9)
        
        self._register_ylim_callback(ax, ax2)
        
        return [line2], ['Downbeat Probability']
