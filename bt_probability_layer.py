import numpy as np

def load_beat_probabilities(beat_probs_file="beat_probs.npz"):
    """Load beat and downbeat probabilities and their timestamps from .npz file"""
    print("\n" + "="*60)
    print("BEAT PROBABILITY LAYER")
    print("="*60)
    
    beat_probs = None
    downbeat_probs = None
    beat_times = None
    
    # Load beat probabilities and timestamps
    try:
        data = np.load(beat_probs_file)
        beat_times = data['beat_times']
        beat_probs = data['beat_probs']
        downbeat_probs = data['downbeat_probs']
        print(f"✓ Loaded beat probabilities: {beat_probs.shape}")
        print(f"✓ Loaded downbeat probabilities: {downbeat_probs.shape}")
        print(f"✓ Loaded beat times: {beat_times.shape}")
    except FileNotFoundError as e:
        print(f"✗ Error loading beat probabilities: {e}")
    except KeyError as e:
        print(f"✗ Error: Missing key in npz file: {e}")
    
    return beat_times, beat_probs, downbeat_probs

def draw_beat_probability(ax, spec_times, spec_freqs, beat_times=None, beat_probs=None, downbeat_probs=None):
    """Draw beat probability lines on secondary y-axis (does not configure axis)"""
    # Create secondary y-axis for probabilities
    ax2 = ax.twinx()
    
    # Store line objects for legend
    lines = []
    labels = []
    
    if beat_probs is not None and beat_times is not None:
        # Normalize to 0-100% range using min-max normalization
        beat_min = np.min(beat_probs)
        beat_max = np.max(beat_probs)
        beat_percent = ((beat_probs - beat_min) / (beat_max - beat_min)) * 100 if beat_max > beat_min else beat_probs * 100
        
        # Plot beat probabilities on secondary axis as continuous line
        line1, = ax2.plot(beat_times, beat_percent, 'r-', linewidth=2, label='Beat Probability', alpha=0.9)
        lines.append(line1)
        labels.append('Beat Probability')
    
    if downbeat_probs is not None and beat_times is not None:
        # Normalize to 0-100% range using min-max normalization
        downbeat_min = np.min(downbeat_probs)
        downbeat_max = np.max(downbeat_probs)
        downbeat_percent = ((downbeat_probs - downbeat_min) / (downbeat_max - downbeat_min)) * 100 if downbeat_max > downbeat_min else downbeat_probs * 100
        
        # Plot downbeat probabilities on secondary axis as continuous line
        line2, = ax2.plot(beat_times, downbeat_percent, 'b-', linewidth=2, label='Downbeat Probability', alpha=0.9)
        lines.append(line2)
        labels.append('Downbeat Probability')
    
    return ax2, lines, labels

if __name__ == "__main__":
    import importlib.util
    import matplotlib.pyplot as plt
    
    # For standalone testing, import the spectrogram layer
    spec = importlib.util.spec_from_file_location("spectrogram", "spectrogram.py")
    spectrogram_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(spectrogram_module)
    
    # Load beat probabilities
    beat_probs, downbeat_probs = load_beat_probabilities()
    
    print("\nStandalone test - use layers.py for full visualization")

