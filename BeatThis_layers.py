"""
BeatThis! algorithm visualization layers.
Contains all visualization layers specific to the BeatThis! beat tracking algorithm.
"""

from abc import ABC, abstractmethod
from matplotlib import lines
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
    
    def _load_beat_times(self, beat_file: str = "beat_probs.npz") -> bool:
        """Load beat times from .npz file (shared across all BeatThis! layers)"""
        try:
            data = np.load(beat_file)
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
    
    def _setup_beat_lines_axis(self, ax: Axes, shared_data: Dict[str, Any]) -> Axes:
        """Get or create third axis for beat line visualization"""
        if "ax3" not in shared_data:
            ax3 = ax.twinx()
            ax3.spines['right'].set_position(('outward', 60))  # Offset from the right edge
            ax3.set_yticks([])
            ax3.set_ylabel('')
            shared_data["ax3"] = ax3
        else:
            ax3 = shared_data["ax3"]
        
        return ax3
    



class BeatProbabilityLayer(BeatThisLayer):
    """Visualizes beat probability outputs from BeatThis! algorithm."""
    
    def __init__(self, name: str = "Beat Probability", color = 'r'):
        super().__init__(name)
        self.color = color
    
    def load_data(self, beat_file: str = "beat_probs.npz", **kwargs) -> bool:
        if not self._load_beat_times(beat_file):
            return False
        try:
            data = np.load(beat_file)
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
        
        line1, = ax2.plot(self._data["beat_times"], beat_percent, '-', 
                         color=self.color, linewidth=2, label='Beat Probability', alpha=0.9)
        
        return [line1], ['Beat Probability']


class DownbeatProbabilityLayer(BeatThisLayer):
    """Visualizes downbeat probability outputs from BeatThis! algorithm."""
    
    def __init__(self, name: str = "Downbeat Probability", color = 'b'):
        super().__init__(name)
        self.color = color
    
    def load_data(self, beat_file: str = "beat_probs.npz", **kwargs) -> bool:
        if not self._load_beat_times(beat_file):
            return False
        try:
            data = np.load(beat_file)
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
        
        line2, = ax2.plot(self._data["beat_times"], downbeat_percent, '-',
                         color=self.color, linewidth=2, label='Downbeat Probability', alpha=0.9)
        
        return [line2], ['Downbeat Probability']

class BeatAccurateLayer(BeatThisLayer):
    """Visualizes detected beat times as vertical lines on the spectrogram."""
    
    def __init__(self, name: str = "Beat Accurate", beat_color: str = 'red', downbeat_color: str = 'blue'):
        super().__init__(name)
        self.beat_color = beat_color
        self.downbeat_color = downbeat_color
    
    def load_data(self, beat_file: str = "beat_probs.npz", **kwargs) -> bool:
        """Load detected beat and downbeat timestamps from .npz file"""
        if not self._load_beat_times(beat_file):
            return False
        try:
            data = np.load(beat_file)
            
            # Check if detected beats exist in file
            if 'detected_beats' not in data or 'detected_downbeats' not in data:
                print(f"✗ {self.name}: detected_beats or detected_downbeats not found in {beat_file}")
                print("  Please run beat detection first to generate detected beat positions")
                return False
            
            self._data = {
                "beat_times": self._beat_times,
                "detected_beats": data['detected_beats'],
                "detected_downbeats": data['detected_downbeats'],
            }
            print(f"✓ {self.name}: Loaded {len(self._data['detected_beats'])} beats and {len(self._data['detected_downbeats'])} downbeats")
            return True
        except Exception as e:
            print(f"✗ {self.name} error: {e}")
            return False
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw vertical lines for detected beats and downbeats"""
        if self._data is None:
            print(f"✗ {self.name}: No data loaded")
            return [], []
        
        ax3 = self._setup_beat_lines_axis(ax, shared_data)
        lines_list = []
        labels_list = []
        
        # Get downbeat times for comparison
        downbeat_times = set(np.round(self._data["detected_downbeats"], 6))  # Round for float comparison
        
        # Draw beats
        beat_lines = []
        for beat_time in self._data["detected_beats"]:
            beat_time_rounded = round(beat_time, 6)
            # Skip if this beat coincides with a downbeat
            if beat_time_rounded not in downbeat_times:
                line = ax3.axvline(x=beat_time, color=self.beat_color, linewidth=1.5, 
                                 alpha=0.7, linestyle='-', label='Beat')
                beat_lines.append(line)
        
        if beat_lines:
            lines_list.extend(beat_lines)
            labels_list.append('Beat')
        
        # Draw downbeats
        downbeat_lines = []
        for downbeat_time in self._data["detected_downbeats"]:
            line = ax3.axvline(x=downbeat_time, color=self.downbeat_color, linewidth=1.5, 
                             alpha=0.6, linestyle='-', label='Downbeat')
            downbeat_lines.append(line)
        
        if downbeat_lines:
            lines_list.extend(downbeat_lines)
            labels_list.append('Downbeat')
        
        return lines_list, labels_list

       