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

''' Import Layer base class and shape primitives '''
from .visualization_system import Layer
from .shapes import Curve, Events, Intervals
"""
Utility class to run BeatThis! beat detection and save results.
Wraps the run_beat_detection function from beat_this_analysis_gen.py.
"""

def Run_BeatThis(audio_path, output_path: str = None, print_output: bool = False) -> str:
    #This functions makes a beat prediction using BeatThis! Algorithm. 
    #It saves the output in a .npz that will be loaded into the beat visualization layers.
    from beat_this.inference import Audio2Frames, Audio2Beats
    from beat_this.preprocessing import load_audio
    from pathlib import Path
    import numpy as np

    if print_output:
        print("\033[92m\n" + "="*60)
        print("RUNNING BEATTHIS!")
        print("="*60 + "\033[0m")
    
    waveform, sample_rate = load_audio(audio_path)
    
    if print_output:
        print(f"✓ Audio loaded. Sample rate: {sample_rate}, Duration: {len(waveform) / sample_rate:.2f}s")
    
    if print_output:
        print("Initializing model (downloading checkpoint if needed)...")
    detector = Audio2Frames(checkpoint_path="final0", device="cpu")
    if print_output:
        print("✓ Model initialized. Processing audio...")

    beat_logits, downbeat_logits = detector(waveform, sample_rate)

    hop_length = 441
    target_sr = 22050
    beat_times = np.arange(len(beat_logits)) * (hop_length / target_sr)
    
    if print_output:
        print("Detecting beat positions...")
    beat_detector = Audio2Beats(checkpoint_path="final0", device="cpu")
    detected_beats, detected_downbeats = beat_detector(waveform, sample_rate)
    
    if print_output:
        print(f"✓ Detected {len(detected_beats)} beats and {len(detected_downbeats)} downbeats")
    
    # Create absolute path for output
    module_dir = Path(__file__).parent
    output_dir = module_dir.parent / "input_files" / "beat_this_analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "beat_activation.npz"
    
    if print_output:
        print("✓ Saving output files...")
    if output_path is None:
        output_path = str(output_file)

    np.savez(output_path,
            beat_times=beat_times,
            beat_activation=beat_logits.numpy(),
            downbeat_activation=downbeat_logits.numpy(),
            detected_beats=detected_beats,
            detected_downbeats=detected_downbeats)
    if print_output:
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
    
    def _normalize_threshold(self, threshold: float) -> float:
        '''Convert threshold to 0-100 scale if needed'''
        return threshold * 100 if threshold <= 1.0 else threshold

    def _probability_threshold_to_logit(self, threshold: float) -> float:
        '''Convert a percentage threshold to the equivalent raw logit threshold.'''
        probability = np.clip(threshold / 100, np.finfo(float).eps, 1 - np.finfo(float).eps)
        return float(np.log(probability / (1 - probability)))

    def _find_windows(self, probs: np.ndarray) -> List[Tuple[int, int, float]]:
        '''Find contiguous regions where probability exceeds logit_threshold.'''
        above_threshold = probs >= self.logit_threshold

        windows = []
        in_window = False
        window_start = 0
        window_probs = []

        for i, is_above in enumerate(above_threshold):
            if is_above:
                if not in_window:
                    window_start = i
                    in_window = True
                window_probs.append(probs[i])
            else:
                if in_window:
                    peak_prob = np.max(window_probs)
                    windows.append((window_start, i - 1, peak_prob))
                    in_window = False
                    window_probs = []

        if in_window:
            peak_prob = np.max(window_probs)
            windows.append((window_start, len(probs) - 1, peak_prob))

        return windows

    def _logit_axis_limits(self, logits: np.ndarray) -> Tuple[float, float]:
        '''Return symmetric logit limits that include the zero decision boundary.'''
        max_abs_logit = np.max(np.abs(logits))
        limit = max(1.0, float(np.ceil(max_abs_logit)))
        return -limit, limit

    def _setup_logit_axis(self, ax: Axes, shared_data: Dict[str, Any], logits: np.ndarray) -> Axes:
        '''Get or create the secondary axis used for raw BeatThis logits.'''
        if "ax2" not in shared_data:
            ax2 = ax.twinx()
            shared_data["ax2"] = ax2
        else:
            ax2 = shared_data["ax2"]
        
        ''' Match the primary axis x-limits to avoid extra whitespace '''
        if "times" in shared_data:
            ax2.set_xlim(shared_data["times"][0], shared_data["times"][-1])

        logit_y_min, logit_y_max = self._logit_axis_limits(logits)
        current_y_min, current_y_max = ax2.get_ylim()
        ax2.set_ylim(min(current_y_min, logit_y_min), max(current_y_max, logit_y_max))
        ax2.set_ylabel('Beat activation (logit)', fontweight='bold', fontsize=11)
        return ax2
    
    def _rgb_to_hex(self, rgb):
        '''Convert RGB tuple (0-1) or matplotlib color to hex'''
        if isinstance(rgb, tuple) and len(rgb) >= 3:
            r, g, b = [int(c * 255) if c <= 1 else int(c) for c in rgb[:3]]
            return f'#{r:02x}{g:02x}{b:02x}'
        ''' Handle matplotlib color names '''
        try:
            from matplotlib.colors import to_hex
            return to_hex(rgb)
        except:
            return '#000000'
    
    def _time_to_pixel_x(self, t: float, ctx: Dict) -> float:
        '''Convert time coordinate to pixel X coordinate'''
        if ctx["x_max"] == ctx["x_min"]:
            return 0
        return ((t - ctx["x_min"]) / (ctx["x_max"] - ctx["x_min"])) * ctx["width_px"]
    
    def _logit_to_pixel_y(self, logit: float, ctx: Dict) -> float:
        '''Convert a logit to an inverted SVG Y coordinate.'''
        logit_y_min = ctx["logit_y_min"]
        logit_y_max = ctx["logit_y_max"]
        if logit_y_max == logit_y_min:
            return ctx["height_px"] / 2
        return (1 - (logit - logit_y_min) / (logit_y_max - logit_y_min)) * ctx["height_px"]

    def _logit_axes_to_svg(self, ctx: Dict) -> List[str]:
        '''Build the shared logit and timeline axes for SVG beat layers.'''
        if not ctx.get("show_axes", False) or ctx.get("logit_axes_added", False):
            return []

        width_px = ctx["width_px"]
        height_px = ctx["height_px"]
        x_min = ctx["x_min"]
        x_max = ctx["x_max"]
        logit_y_min = ctx["logit_y_min"]
        logit_y_max = ctx["logit_y_max"]

        if x_max == x_min or logit_y_min is None or logit_y_max is None:
            return []

        ctx["logit_axes_added"] = True
        parts = [
            f'    <line x1="0" y1="0" x2="0" y2="{height_px}" stroke="#111" stroke-width="1"/>',
            f'    <line x1="0" y1="{height_px}" x2="{width_px}" y2="{height_px}" stroke="#111" stroke-width="1"/>',
        ]

        for logit in np.linspace(logit_y_min, logit_y_max, 5):
            y = self._logit_to_pixel_y(logit, ctx)
            parts.append(f'    <line x1="-4" y1="{y:.1f}" x2="0" y2="{y:.1f}" stroke="#111" stroke-width="1"/>')
            parts.append(f'    <text x="-6" y="{y + 3:.1f}" text-anchor="end" font-size="8" font-family="Arial,sans-serif" fill="#111">{logit:.0f}</text>')

        zero_y = self._logit_to_pixel_y(0, ctx)
        parts.append(f'    <line x1="0" y1="{zero_y:.1f}" x2="{width_px}" y2="{zero_y:.1f}" stroke="#999" stroke-width="0.5" stroke-dasharray="4,3"/>')

        t_start = int(np.ceil(x_min))
        t_end = int(np.floor(x_max))
        for time in range(t_start, t_end + 1):
            x = self._time_to_pixel_x(time, ctx)
            if time % 5 == 0:
                parts.append(f'    <line x1="{x:.1f}" y1="{height_px}" x2="{x:.1f}" y2="{height_px + 6}" stroke="#111" stroke-width="1"/>')
                parts.append(f'    <text x="{x:.1f}" y="{height_px + 14:.1f}" text-anchor="middle" font-size="8" font-family="Arial,sans-serif" fill="#111">{time}s</text>')
            else:
                parts.append(f'    <line x1="{x:.1f}" y1="{height_px}" x2="{x:.1f}" y2="{height_px + 4}" stroke="#111" stroke-width="0.7"/>')

        return parts
    
    def _probability_to_svg_group(self, shared_data: Dict[str, Any], prob_key: str, svg_class: str, opacity: float = 1.0, line_width: float = 0.5) -> Optional[str]:
        '''
        Generic method to convert probability curve to SVG polyline.
        
        Args:
            shared_data: Shared visualization data
            prob_key: Key for probability data in self._data (e.g., 'beat_activation', 'downbeat_activation')
            svg_class: CSS class for the SVG group (e.g., 'beat-probability')
            opacity: Optional opacity for the polyline (default 1.0)
        '''
        if self._data is None or "svg_context" not in shared_data:
            return None
        
        ctx = shared_data["svg_context"]
        beat_times = self._data.get("beat_times", [])
        logits = self._data.get(prob_key, [])
        
        if len(beat_times) == 0:
            return None
        
        ''' Convert data points to SVG coordinates '''
        points = []
        for t, logit in zip(beat_times, logits):
            x = self._time_to_pixel_x(t, ctx)
            y = self._logit_to_pixel_y(logit, ctx)
            points.append(f"{x:.2f},{y:.2f}")
        
        points_str = " ".join(points)
        color_hex = self._rgb_to_hex(self.color)
        opacity_attr = f' opacity="{opacity}"' if opacity < 1.0 else ''

        parts = [f'  <g id="{self.name}" class="layer {svg_class}">']
        parts.extend(self._logit_axes_to_svg(ctx))
        parts.append(f'    <polyline points="{points_str}" stroke="{color_hex}" stroke-width="{line_width}" fill="none"{opacity_attr}/>')
        parts.append('  </g>')
        return '\n'.join(parts)

def _load_beat_npz(beat_file: str, required_keys: List[str], layer_name: str) -> Optional[Dict]:
    ''' Load and validate a BeatThis! .npz file with the required keys '''
    try:
        if beat_file is None:
            return None
        beat_data = np.load(beat_file, allow_pickle=True)
        beat_data_dict = {key: value for key, value in beat_data.items()}

        missing = [k for k in required_keys if k not in beat_data_dict]
        if missing:
            print(f"✗ {layer_name}: Missing keys {missing}")
            return None
        return beat_data_dict
    except Exception as e:
        print(f"✗ {layer_name} error: {e}")
        return None


class BeatProbabilityLayer(Curve):
    """Visualizes raw beat logits from the BeatThis! algorithm."""

    def __init__(self, name: str = "Beat Probability", color='r', line_width: float = 0.5):
        super().__init__(name, color=color, line_width=line_width, label='Beat Logit',
                          secondary_axis=True, axis_label='Beat activation (logit)',
                          svg_class='beat-probability')

    def load_data(self, beat_file: str = None, print_output: bool = False, **kwargs) -> bool:
        data = _load_beat_npz(beat_file, ['beat_times', 'beat_activation'], self.name)
        if data is None:
            return False
        self._data = data
        if print_output==True:
            print(f"✓ {self.name}: Loaded beat data")
        return True

    def _get_xy(self, shared_data: Dict[str, Any]) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        if self._data is None:
            return None
        return self._data["beat_times"], self._data["beat_activation"]


class DownbeatProbabilityLayer(Curve):
    """Visualizes raw downbeat logits from the BeatThis! algorithm."""

    def __init__(self, name: str = "Downbeat Probability", color='blue', line_width: float = 0.5):
        super().__init__(name, color=color, line_width=line_width, alpha=0.9, label='Downbeat Logit',
                          secondary_axis=True, axis_label='Beat activation (logit)',
                          svg_class='downbeat-probability')

    def load_data(self, beat_file: str = None, print_output: bool = False, **kwargs) -> bool:
        data = _load_beat_npz(beat_file, ['beat_times', 'downbeat_activation'], self.name)
        if data is None:
            return False
        self._data = data
        if print_output==True:    
            print(f"✓ {self.name}: Loaded downbeat data")
        return True

    def _get_xy(self, shared_data: Dict[str, Any]) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        if self._data is None:
            return None
        return self._data["beat_times"], self._data["downbeat_activation"]


class BeatsLayer(Events):
    """Visualizes detected beat times (excluding downbeats) as vertical markers."""

    def __init__(self, name: str = "Beat", color='red', line_width: float = 1):
        super().__init__(name, color=color, line_width=line_width, secondary_axis=True, svg_class='beat-marker')

    def load_data(self, beat_file: str = None, print_output: bool = False, **kwargs) -> bool:
        data = _load_beat_npz(beat_file, ['detected_beats', 'detected_downbeats'], self.name)
        if data is None:
            return False
        self._data = data
        if print_output==True:
            print(f"✓ {self.name}: Loaded {len(self._data['detected_beats'])} beats")
        return True

    def _get_times(self, shared_data: Dict[str, Any]) -> Optional[np.ndarray]:
        if self._data is None:
            return None
        downbeat_set = set(np.round(self._data["detected_downbeats"], 6))
        return np.array([t for t in self._data["detected_beats"] if round(t, 6) not in downbeat_set])


class DownbeatsLayer(Events):
    """Visualizes detected downbeat times as vertical markers."""

    def __init__(self, name: str = "Downbeat", color='blue', line_width: float = 1):
        super().__init__(name, color=color, line_width=line_width, secondary_axis=True, svg_class='downbeat-marker')

    def load_data(self, beat_file: str = None, print_output: bool = False, **kwargs) -> bool:
        data = _load_beat_npz(beat_file, ['detected_beats', 'detected_downbeats'], self.name)
        if data is None:
            return False
        self._data = data
        if print_output==True:
            print(f"✓ {self.name}: Loaded {len(self._data['detected_downbeats'])} downbeats")
        return True

    def _get_times(self, shared_data: Dict[str, Any]) -> Optional[np.ndarray]:
        if self._data is None:
            return None
        return np.array(self._data["detected_downbeats"])


class BeatAccurateLayer(Layer):
    """Legacy combined view of detected beats and downbeats as vertical lines.

    Kept for backward compatibility; new code can use BeatsLayer and
    DownbeatsLayer directly.
    """

    def __init__(self, name: str = "Beat Accurate", beat_color='red', downbeat_color='blue', line_width: float = 1):
        super().__init__(name)
        self._beats = BeatsLayer(name="Beat", color=beat_color, line_width=line_width)
        self._downbeats = DownbeatsLayer(name="Downbeat", color=downbeat_color, line_width=line_width)

    def load_data(self, beat_file: str = None, print_output: bool = False, **kwargs) -> bool:
        loaded_beats = self._beats.load_data(beat_file=beat_file, print_output=print_output, **kwargs)
        loaded_downbeats = self._downbeats.load_data(beat_file=beat_file, print_output=print_output, **kwargs)
        return loaded_beats and loaded_downbeats

    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        beat_lines, beat_labels = self._beats.draw(ax, shared_data)
        downbeat_lines, downbeat_labels = self._downbeats.draw(ax, shared_data)
        return beat_lines + downbeat_lines, beat_labels + downbeat_labels

    def to_svg_group(self, shared_data: Dict[str, Any]) -> Optional[str]:
        lines = self._beats._lines_svg(shared_data) + self._downbeats._lines_svg(shared_data)
        if not lines:
            return None
        svg_group = f'''  <g id="{self.name}" class="layer beat-accurate">
{chr(10).join(lines)}
  </g>'''
        return svg_group


class BeatWindowLayer(Intervals):
    """Visualizes beat confidence windows with gradient transparency.

    Shows regions where beat probability exceeds a threshold, with transparency
    gradient: opaque at peak confidence, transparent at threshold boundaries.
    """

    def __init__(self, name: str = "Beat Window", beat_window: float = 70, color='red', alpha_max: float = 0.3):
        super().__init__(name, color=color, threshold=beat_window, alpha_max=alpha_max, svg_class="beat-window")

    def load_data(self, beat_file: str = None, print_output: bool = False, **kwargs) -> bool:
        data = _load_beat_npz(beat_file, ['beat_times', 'beat_activation'], self.name)
        if data is None:
            return False
        self._data = data
        if print_output==True:
            windows = self._find_windows(self._data['beat_activation'])
            print(f"✓ {self.name}: Loaded beat data with threshold {self.threshold:.1f}%, found {len(windows)} windows")
        return True

    def _get_activation(self, shared_data: Dict[str, Any]) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        if self._data is None:
            return None
        return self._data['beat_times'], self._data['beat_activation']


class DownbeatWindowLayer(Intervals):
    """Visualizes downbeat confidence windows with gradient transparency.

    Shows regions where downbeat probability exceeds a threshold, with transparency
    gradient: opaque at peak confidence, transparent at threshold boundaries.
    """

    def __init__(self, name: str = "Downbeat Window", beat_window: float = 70, color='blue', alpha_max: float = 0.3):
        super().__init__(name, color=color, threshold=beat_window, alpha_max=alpha_max, svg_class="downbeat-window")

    def load_data(self, beat_file: str = None, print_output: bool = False, **kwargs) -> bool:
        data = _load_beat_npz(beat_file, ['beat_times', 'downbeat_activation'], self.name)
        if data is None:
            return False
        self._data = data
        if print_output:
            windows = self._find_windows(self._data['downbeat_activation'])
            print(f"✓ {self.name}: Loaded downbeat data with threshold {self.threshold:.1f}%, found {len(windows)} windows")
        return True

    def _get_activation(self, shared_data: Dict[str, Any]) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        if self._data is None:
            return None
        return self._data['beat_times'], self._data['downbeat_activation']
