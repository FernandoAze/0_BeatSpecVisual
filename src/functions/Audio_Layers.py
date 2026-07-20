"""
Spectrogram visualization layer.
Visualizes audio spectrograms with mel-scale frequency binning.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Dict, Any, List, Tuple, Optional

# Import Layer base class
from .visualization_system import Layer

class Spectrogram(Layer):
    # =========
    # INITIALIZATION AND CONFIGURATION
    def __init__(self, name: str = "Spectrogram", 
                 freq_window: Tuple[int, int] = (20, 4000),
                 color_map: str = "magma"):
        super().__init__(name)

        self.freq_window = freq_window
        self.color_map = color_map
    # =========

    def load_data(self, audio_path: str, print_output: bool = False, **kwargs) -> bool:
        # ========================================================
        # LOAD AUDIO & COMPUTE SPECTROGRAM
        from modusa import load
        import librosa
        try:
            audio, sr, filename = load.audio(audio_path)
            
            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)
            
            winlen = int(0.256 * sr)
            hoplen = winlen // 16
            S_mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=winlen,
                                                   hop_length=hoplen, n_mels=512,
                                                   fmin=self.freq_window[0], fmax=self.freq_window[1])
            S_db = librosa.power_to_db(S_mel, ref=np.max)
            mel_freqs = librosa.mel_frequencies(n_mels=512, fmin=self.freq_window[0], fmax=self.freq_window[1])
            times = librosa.frames_to_time(np.arange(S_db.shape[1]), sr=sr, hop_length=hoplen)
            
            self._data = {
                "S_db": S_db,
                "freqs": mel_freqs,
                "times": times,
                "sr": sr,
                "filename": filename,
                "audio": audio
            }
            if print_output:
                print(f"✓ SpectrogramLayer: Loaded {filename}")
            return True
        # LOAD AUDIO & COMPUTE SPECTROGRAM
        # ========================================================

        except Exception as e:      # debug info in case of errors
            print(f"✗ SpectrogramLayer error: {e}")
            return False
        
    
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:

        # ========================================================
        # PAINT SPECTROGRAM
        from modusa import paint

        if self._data is None:
            print("✗ SpectrogramLayer: No data loaded")
            return [], []
        
        paint.image(
            ax,
            self._data["S_db"],
            x=self._data["times"],
            y=self._data["freqs"],
            c=self.color_map,
            o="lower",
            clabel="Magnitude (dB)"
        )
        
        shared_data.update(self._data)
        
        ax.set_ylim(self._data["freqs"][0], self._data["freqs"][-1])
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")
        ax.set_title(f"Spectrogram: {self._data['filename']}")
        # PAINT SPECTROGRAM
        # ========================================================

        return [], []


class Chromagram(Layer):
    # =========
    # INITIALIZATION AND CONFIGURATION
    def __init__(self, name: str = "Chromagram",
                 color_map: str = "coolwarm",
                 n_chroma: int = 12):
        super().__init__(name)
        self.color_map = color_map
        self.n_chroma = n_chroma
    # =========

    def load_data(self, audio_path: str, print_output: bool = False, **kwargs) -> bool:
        # ========================================================
        # LOAD AUDIO & COMPUTE CHROMAGRAM
        from modusa import load
        import librosa
        try:
            audio, sr, filename = load.audio(audio_path)

            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)

            hoplen = 512
            chroma = librosa.feature.chroma_cqt(y=audio, sr=sr,
                                                 hop_length=hoplen,
                                                 n_chroma=self.n_chroma)
            times = librosa.frames_to_time(np.arange(chroma.shape[1]), sr=sr, hop_length=hoplen)
            pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F',
                             'F#', 'G', 'G#', 'A', 'A#', 'B']

            self._data = {
                "chroma": chroma,
                "times": times,
                "sr": sr,
                "filename": filename,
                "audio": audio,
                "pitch_classes": pitch_classes
            }
            if print_output:
                print(f"✓ Chromagram: Loaded {filename}")
            return True
        # LOAD AUDIO & COMPUTE CHROMAGRAM
        # ========================================================

        except Exception as e:
            print(f"✗ Chromagram error: {e}")
            return False

    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        # ========================================================
        # PAINT CHROMAGRAM
        import librosa.display
        if self._data is None:
            print("✗ Chromagram: No data loaded")
            return [], []

        img = librosa.display.specshow(
            self._data["chroma"],
            x_axis='time',
            y_axis='chroma',
            sr=self._data["sr"],
            hop_length=512,
            cmap=self.color_map,
            ax=ax
        )

        ax.set_title(f"Chromagram: {self._data['filename']}")

        pitch_classes = self._data["pitch_classes"]
        import matplotlib.transforms as transforms
        for i, label in enumerate(pitch_classes):
            offset = transforms.ScaledTranslation(0, -5 / ax.get_figure().dpi, ax.get_figure().dpi_scale_trans)
            trans = ax.get_yaxis_transform() + offset
            ax.text(
                0, i + 0.35, f" {label}",
                transform=trans,
                ha='left', va='center',
                fontsize=3, fontweight='bold', color='white',
    
            )

        shared_data.update(self._data)
        # PAINT CHROMAGRAM
        # ========================================================

        return [], []


class Waveform(Layer):
    # =========
    # INITIALIZATION AND CONFIGURATION
    def __init__(self, name: str = "Waveform",
                 color: str = "steelblue",
                 alpha: float = 0.8,
                 normalize: bool = False):
        super().__init__(name)
        self.color = color
        self.alpha = alpha
        self.normalize = normalize
    # =========

    def load_data(self, audio_path: str, print_output: bool = False, **kwargs) -> bool:
        # ========================================================
        # LOAD AUDIO
        from modusa import load
        try:
            audio, sr, filename = load.audio(audio_path)

            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)

            duration = len(audio) / sr
            times = np.linspace(0, duration, num=len(audio))

            self._data = {
                "audio": audio,
                "times": times,
                "sr": sr,
                "filename": filename,
                "duration": duration
            }
            if print_output:
                print(f"✓ Waveform: Loaded {filename}, duration={duration:.2f}s")
            return True
        # LOAD AUDIO
        # ========================================================

        except Exception as e:
            print(f"✗ Waveform error: {e}")
            return False

    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        # ========================================================
        # PAINT WAVEFORM
        if self._data is None:
            print("✗ Waveform: No data loaded")
            return [], []

        audio = self._data["audio"]
        if self.normalize:
            peak = np.max(np.abs(audio))
            if peak > 0:
                audio = audio / peak

        line, = ax.plot(
            self._data["times"],
            audio,
            color=self.color,
            linewidth=0.4,
            alpha=self.alpha,
            label="Waveform"
        )

        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.set_title(f"Waveform: {self._data['filename']}")
        ax.set_ylim(-1.05, 1.05)

        shared_data.update(self._data)
        # PAINT WAVEFORM
        # ========================================================

        return [line], ["Waveform"]

    def to_svg_group(self, shared_data: Dict[str, Any]) -> Optional[str]:
        '''Convert waveform to SVG polyline, downsampled to ~4 points per pixel'''
        if self._data is None or "svg_context" not in shared_data:
            return None

        ctx = shared_data["svg_context"]
        times = self._data["times"]
        audio = self._data["audio"]
        if self.normalize:
            peak = np.max(np.abs(audio))
            if peak > 0:
                audio = audio / peak

        x_min, x_max = ctx["x_min"], ctx["x_max"]
        y_min, y_max = ctx["y_min"], ctx["y_max"]
        width_px, height_px = ctx["width_px"], ctx["height_px"]

        if x_max == x_min or y_max == y_min:
            return None

        target_points = int(width_px * 4)
        if len(times) > target_points:
            indices = np.linspace(0, len(times) - 1, target_points, dtype=int)
            times = times[indices]
            audio = audio[indices]

        points = []
        for t, amp in zip(times, audio):
            x = ((t - x_min) / (x_max - x_min)) * width_px
            y = (1.0 - (amp - y_min) / (y_max - y_min)) * height_px
            points.append(f"{x:.2f},{y:.2f}")

        points_str = " ".join(points)

        if isinstance(self.color, tuple) and len(self.color) >= 3:
            r, g, b = [int(c * 255) if c <= 1 else int(c) for c in self.color[:3]]
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
        else:
            try:
                from matplotlib.colors import to_hex
                color_hex = to_hex(self.color)
            except Exception:
                color_hex = '#000000'

        opacity_attr = f' opacity="{self.alpha}"' if self.alpha < 1.0 else ''

        return f'''  <g id="{self.name}" class="layer waveform">
    <polyline points="{points_str}" stroke="{color_hex}" stroke-width="0.4" fill="none"{opacity_attr}/>
  </g>'''