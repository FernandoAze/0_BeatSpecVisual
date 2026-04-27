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
from .visualization_system import Layer

"""
Utility class to run BeatThis! beat detection and save results.
Wraps the run_beat_detection function from beat_this_analysis_gen.py.
"""
@staticmethod
def Run_BeatThis(audio_path="src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01.wav"):
    from beat_this.inference import Audio2Frames, Audio2Beats
    from beat_this.preprocessing import load_audio
    from pathlib import Path
    import numpy as np
    import os

    print("\n" + "="*60)
    print("BEAT DETECTION")
    print("="*60)
    print(f"Checking if audio file exists: {audio_path}")

    if not os.path.isfile(audio_path):
        print(f"✗ ERROR: Audio file '{audio_path}' not found.")
        return False
    try:
        print("Loading audio file...")
        waveform, sample_rate = load_audio(audio_path)
        print(f"✓ Audio loaded. Sample rate: {sample_rate}, Duration: {len(waveform) / sample_rate:.2f}s")
        
        print("Initializing model (downloading checkpoint if needed)...")
        detector = Audio2Frames(checkpoint_path="final0", device="cpu")
        print("✓ Model initialized. Processing audio...")

        beat_logits, downbeat_logits = detector(waveform, sample_rate)
        print("✓ Audio processed. Calculating timestamps...")

        hop_length = 441
        target_sr = 22050
        beat_times = np.arange(len(beat_logits)) * (hop_length / target_sr)
        
        print("Detecting beat positions...")
        beat_detector = Audio2Beats(checkpoint_path="final0", device="cpu")
        detected_beats, detected_downbeats = beat_detector(waveform, sample_rate)
        
        print(f"✓ Detected {len(detected_beats)} beats and {len(detected_downbeats)} downbeats")
        
        # Create absolute path for output
        module_dir = Path(__file__).parent
        output_dir = module_dir.parent / "input_files" / "beat_this_analysis"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "beat_probs.npz"
        
        print("✓ Saving output files...")
        np.savez(str(output_file), 
                    beat_times=beat_times, 
                    beat_probs=beat_logits.numpy(),
                    downbeat_probs=downbeat_logits.numpy(),
                    detected_beats=detected_beats,
                    detected_downbeats=detected_downbeats)
        print(f"✓ File saved: {output_file}")
        return True

    except Exception as e:
        print(f"✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False


class BeatThisLayer(Layer):
    """Base class for BeatThis! algorithm visualization layers.
    
    Manages shared audio/beat data loading and probability visualization.
    All BeatThis! output layers inherit from this class to share common parameters.
    """
    
    def __init__(self, name: str = "BeatThis Layer"):
        super().__init__(name)
        self._beat_times = None
    
    def _load_beat_times(self, beat_file: str = None) -> bool:
        """Load beat times from .npz file (shared across all BeatThis! layers)"""
        try:
            # If no file specified, use default path
            if beat_file is None:
                from pathlib import Path
                module_dir = Path(__file__).parent
                beat_file = module_dir.parent / "input_files" / "beat_this_analysis" / "beat_probs.npz"
            
            data = np.load(str(beat_file))
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
    
    def load_data(self, beat_file: str = None, **kwargs) -> bool:
        if beat_file is None:
            from pathlib import Path
            module_dir = Path(__file__).parent
            beat_file = module_dir.parent / "input_files" / "beat_this_analysis" / "beat_probs.npz"
        
        if not self._load_beat_times(beat_file):
            return False
        try:
            data = np.load(str(beat_file))
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
                         color=self.color, linewidth=1, label='Beat Probability', alpha=0.9)
        
        return [line1], ['Beat Probability']


class DownbeatProbabilityLayer(BeatThisLayer):
    """Visualizes downbeat probability outputs from BeatThis! algorithm."""
    
    def __init__(self, name: str = "Downbeat Probability", color = 'b'):
        super().__init__(name)
        self.color = color
    
    def load_data(self, beat_file: str = None, **kwargs) -> bool:
        if beat_file is None:
            from pathlib import Path
            module_dir = Path(__file__).parent
            beat_file = module_dir.parent / "input_files" / "beat_this_analysis" / "beat_probs.npz"
        
        if not self._load_beat_times(beat_file):
            return False
        try:
            data = np.load(str(beat_file))
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
                         color=self.color, linewidth=1, label='Downbeat Probability', alpha=0.9)
        
        return [line2], ['Downbeat Probability']

class BeatAccurateLayer(BeatThisLayer):
    """Visualizes detected beat times as vertical lines on the spectrogram."""
    
    def __init__(self, name: str = "Beat Accurate", beat_color: str = 'red', downbeat_color: str = 'blue'):
        super().__init__(name)
        self.beat_color = beat_color
        self.downbeat_color = downbeat_color
    
    def load_data(self, beat_file: str = None, **kwargs) -> bool:
        """Load detected beat and downbeat timestamps from .npz file"""
        if beat_file is None:
            from pathlib import Path
            module_dir = Path(__file__).parent
            beat_file = module_dir.parent / "input_files" / "beat_this_analysis" / "beat_probs.npz"
        
        if not self._load_beat_times(beat_file):
            return False
        try:
            data = np.load(str(beat_file))
            
            # Check if detected beats exist in file
            if 'detected_beats' not in data or 'detected_downbeats' not in data:
                print(f"✗ {self.name}: detected_beats or detected_downbeats not found in {beat_file}")
                print(" Tip: Use Run_BeatThis.run_beat_detection() to generate the .npz file with the correct structure.")
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
                line = ax3.axvline(x=beat_time, color=self.beat_color, linewidth=1, linestyle='-')
                beat_lines.append(line)
        
        if beat_lines:
            lines_list.extend(beat_lines)
            labels_list.append('Beat')
        
        # Draw downbeats
        downbeat_lines = []
        for downbeat_time in self._data["detected_downbeats"]:
            line = ax3.axvline(x=downbeat_time, color=self.downbeat_color, linewidth=1, linestyle='-')
            downbeat_lines.append(line)
        
        if downbeat_lines:
            lines_list.extend(downbeat_lines)
            labels_list.append('Downbeat')
        
        return lines_list, [] # labels list is making incorrect color of bars, so I just removed it for now.

       