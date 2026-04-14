import numpy as np
from modusa import load, compute, paint
import librosa

def compute_spectrogram(audio_path):
    """Compute spectrogram from audio file"""
    
    # ============================================
    # Load audio using modusa
    # ============================================
    try:
        audio, sr, filename = load.audio(audio_path)
        print(f"✓ Loaded: {filename}")
        print(f"  Sampling Rate: {sr} Hz")
        print(f"  Shape: {audio.shape}")
        
        # Convert stereo to mono if needed
        if audio.ndim == 2:
            audio = np.mean(audio, axis=0)
            print(f"  Converted to mono: {audio.shape}")
    except FileExistsError as e:
        print(f"✗ Error: {e}")
        return False

    # ============================================
    # Compute mel spectrogram
    # ============================================
    # Set window parameters for high resolution
    winlen = int(0.256 * sr)   # 256ms window (larger = better freq resolution)
    hoplen = winlen // 16      # ~6.25% hop (~93.75% overlap, very dense time sampling)

    # Compute mel spectrogram directly using librosa
    S_mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=winlen, 
                                           hop_length=hoplen, n_mels=512)
    S_db = librosa.power_to_db(S_mel, ref=np.max)
    
    # Get mel frequencies and times
    mel_freqs = librosa.mel_frequencies(n_mels=512, fmin=0, fmax=6000)
    times = librosa.frames_to_time(np.arange(S_db.shape[1]), sr=sr, hop_length=hoplen)

    print(f"✓ Mel Spectrogram computed (High Resolution)")
    print(f"  Mel bins: 512")
    print(f"  Time frames: {len(times)}")

    print(f"✓ Spectrogram ready for visualization")
    
    # Return spectrogram data
    return {
        "S_db": S_db,
        "freqs": mel_freqs,
        "times": times,
        "sr": sr,
        "filename": filename,
        "audio": audio
    }

def draw_spectrogram(ax, spec_data, cax=None):
    """Draw spectrogram on an existing axes (does not configure axis)"""
    
    paint.image(
        ax,
        spec_data["S_db"],
        x=spec_data["times"],
        y=spec_data["freqs"],
        c="viridis",
        o="lower",
        clabel="Magnitude (dB)",
        cax=cax
    )
    ax.set_ylabel("Frequency (Mel scale)")

def visualize_spectrogram(spec_data):
    """Visualize spectrogram from computed data"""
    import matplotlib.pyplot as plt
    
    print("\n" + "="*60)
    print("SPECTROGRAM VISUALIZATION")
    print("="*60)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    
    draw_spectrogram(ax, spec_data, cax)
    
    plt.tight_layout(rect=[0, 0, 0.9, 1])
    
    return fig

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    spec_data = compute_spectrogram()
    if spec_data:
        fig = visualize_spectrogram(spec_data)
        plt.show()
