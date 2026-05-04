"""
Spectrogram visualization layer.
Visualizes audio spectrograms with mel-scale frequency binning.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Dict, Any, List, Tuple, Optional


from .visualization_system import Layer
from .Load_Files import LoadFiles


class SpectrogramLayer(Layer):
    def __init__(self, name: str = "Spectrogram"):
        super().__init__(name)
        self.loader = LoadFiles()
    
    def load_data(self, audio_path: str = None, **kwargs) -> bool:
        # ========================================================
        # LOAD AUDIO & COMPUTE SPECTROGRAM
        try:
            from modusa import load
            import librosa
            
            ''' Try to get audio path from singleton first, or use provided parameter '''
            loaded_audio_path = self.loader.get_data('audio_path')
            if loaded_audio_path:
                audio_path = loaded_audio_path
            elif audio_path is None:
                return False
            
            if audio_path and not self.loader.get_data('audio_path'):
                if not self.loader.load_audio(audio_path):
                    return False
            
            audio_path = self.loader.get_data('audio_path')
            audio, sr, filename = load.audio(audio_path)
            print(f"✓ {self.name}: Loaded {filename}")
            if audio.ndim == 2:
                audio = np.mean(audio, axis=0)
            
            winlen = int(0.256 * sr)
            hoplen = winlen // 16
            S_mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=winlen,
                                                   hop_length=hoplen, n_mels=512)
            S_db = librosa.power_to_db(S_mel, ref=np.max)
            mel_freqs = librosa.mel_frequencies(n_mels=512, fmin=20, fmax=4000)
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
            print(f"✗ {self.name}: No data loaded")
            return [], []
        
        paint.image(
            ax,
            self._data["S_db"],
            x=self._data["times"],
            y=self._data["freqs"],
            c="magma",
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
