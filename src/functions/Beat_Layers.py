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

''' Import Layer base class '''
from .visualization_system import Layer
"""
Utility class to run BeatThis! beat detection and save results.
Wraps the run_beat_detection function from beat_this_analysis_gen.py.
"""
@staticmethod
def Run_BeatThis(audio_path, output_path: str = None):
    #This functions makes a beat prediction using BeatThis! Algorithm. 
    #It saves the output in a .npz that will be loaded into the beat visualization layers.
    from beat_this.inference import Audio2Frames, Audio2Beats
    from beat_this.preprocessing import load_audio
    from pathlib import Path
    import numpy as np

    print("\n" + "="*60)
    print("RUNNING BEATHIS!")
    print("="*60)
    
    waveform, sample_rate = load_audio(audio_path)
    print(f"✓ Audio loaded. Sample rate: {sample_rate}, Duration: {len(waveform) / sample_rate:.2f}s")
    
    print("Initializing model (downloading checkpoint if needed)...")
    detector = Audio2Frames(checkpoint_path="final0", device="cpu")
    print("✓ Model initialized. Processing audio...")

    beat_logits, downbeat_logits = detector(waveform, sample_rate)

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
    if output_path is None:
        output_path = str(output_file)

    np.savez(output_path,
            beat_times=beat_times,
            beat_probs=beat_logits.numpy(),
            downbeat_probs=downbeat_logits.numpy(),
            detected_beats=detected_beats,
            detected_downbeats=detected_downbeats)
    print(f"✓ File saved: {output_path}")
    return output_path

class BeatLayer(Layer):
    """Base class for BeatThis! algorithm visualization layers.
    
    Manages shared audio/beat data loading and probability visualization.
    All BeatThis! output layers inherit from this class to share common parameters.
    """
    
    def __init__(self, name: str = "BeatThis Layer"):
        super().__init__(name)
    
    def _load_npz_data(self, beat_file: str, required_keys: List[str]) -> Optional[Dict]:
        ''' Load and validate .npz file with required keys '''
        try:
            if beat_file is None:
                return None
            beat_data = np.load(beat_file, allow_pickle=True)
            beat_data_dict = {key: value for key, value in beat_data.items()}
            
            missing = [k for k in required_keys if k not in beat_data_dict]
            if missing:
                print(f"✗ {self.name}: Missing keys {missing}")
                return None
            return beat_data_dict
        except Exception as e:
            print(f"✗ {self.name} error: {e}")
            return None
    
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
        
        ''' Match the primary axis x-limits to avoid extra whitespace '''
        if "times" in shared_data:
            ax2.set_xlim(shared_data["times"][0], shared_data["times"][-1])
        
        ax2.set_ylim(0, 100)
        ax2.set_ylabel('Probability (%)', fontweight='bold', fontsize=11)
        return ax2
    

    
class BeatProbabilityLayer(BeatLayer):
    """Visualizes beat probability outputs from BeatThis! algorithm."""
    
    def __init__(self, name: str = "Beat Probability", color='r'):
        super().__init__(name)
        self.color = color
    
    def load_data(self, beat_file: str = None, **kwargs) -> bool:
        data = self._load_npz_data(beat_file, ['beat_times', 'beat_probs'])
        if data is None:
            return False
        self._data = data
        print(f"✓ {self.name}: Loaded beat data")
        return True
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        if self._data is None:
            print(f"✗ {self.name}: No data loaded")
            return [], []
        
        ax2 = self._setup_probability_axis(ax, shared_data)
        beat_percent = self._normalize_probabilities(self._data["beat_probs"])
        
        line, = ax2.plot(self._data["beat_times"], beat_percent, '-', 
                        color=self.color, linewidth=0.5, label='Beat Probability')
        return [line], ['Beat Probability']


class DownbeatProbabilityLayer(BeatLayer):
    """Visualizes downbeat probability outputs from BeatThis! algorithm."""
    
    def __init__(self, name: str = "Downbeat Probability", color='blue'):
        super().__init__(name)
        self.color = color
    
    def load_data(self, beat_file: str = None, **kwargs) -> bool:
        data = self._load_npz_data(beat_file, ['beat_times', 'downbeat_probs'])
        if data is None:
            return False
        self._data = data
        print(f"✓ {self.name}: Loaded downbeat data")
        return True
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        if self._data is None:
            print(f"✗ {self.name}: No data loaded")
            return [], []
        
        ax2 = self._setup_probability_axis(ax, shared_data)
        downbeat_percent = self._normalize_probabilities(self._data["downbeat_probs"])
        
        line, = ax2.plot(self._data["beat_times"], downbeat_percent, '-',
                        color=self.color, linewidth=0.5, label='Downbeat Probability', alpha=0.9)
        return [line], ['Downbeat Probability']

class BeatAccurateLayer(BeatLayer):
    """Visualizes detected beat times as vertical lines."""
    
    def __init__(self, name: str = "Beat Accurate", beat_color='red', downbeat_color='blue'):
        super().__init__(name)
        self.beat_color = beat_color
        self.downbeat_color = downbeat_color
    
    def load_data(self, beat_file: str = None, **kwargs) -> bool:
        data = self._load_npz_data(beat_file, ['detected_beats', 'detected_downbeats'])
        if data is None:
            return False
        self._data = data
        print(f"✓ {self.name}: Loaded {len(self._data['detected_beats'])} beats, {len(self._data['detected_downbeats'])} downbeats")
        return True
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        if self._data is None:
            print(f"✗ {self.name}: No data loaded")
            return [], []
        
        ax2 = self._setup_probability_axis(ax, shared_data)
        downbeat_set = set(np.round(self._data["detected_downbeats"], 6))
        
        ''' Draw regular beats (exclude downbeats) '''
        beat_lines = [ax2.axvline(x=t, color=self.beat_color, linewidth=1) 
                     for t in self._data["detected_beats"]
                     if round(t, 6) not in downbeat_set]
        
        ''' Draw downbeats '''
        downbeat_lines = [ax2.axvline(x=t, color=self.downbeat_color, linewidth=1) 
                         for t in self._data["detected_downbeats"]]
        
        labels = []
        if beat_lines:
            labels.append('Beat')
        if downbeat_lines:
            labels.append('Downbeat')
        
        return beat_lines + downbeat_lines, labels 

       