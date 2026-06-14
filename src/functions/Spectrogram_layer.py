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