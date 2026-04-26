from beat_this.inference import Audio2Frames, Audio2Beats
from beat_this.preprocessing import load_audio
import numpy as np
import os

def run_beat_detection(audio_path="PARTITURAS_MEI/Chopin_op10_no3_p01.wav"):

    """Run beat detection and save probabilities to .npy files"""
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

        # Pass the waveform and sample_rate to the detector
        beat_logits, downbeat_logits = detector(waveform, sample_rate)
        print("✓ Audio processed. Calculating timestamps...")

        # Beat_this uses hop_length=441 at 22050 Hz (0.02 seconds per frame)
        hop_length = 441
        target_sr = 22050
        beat_times = np.arange(len(beat_logits)) * (hop_length / target_sr)
        
        # Detect actual beats and downbeats using Audio2Beats
        print("Detecting beat positions...")
        beat_detector = Audio2Beats(checkpoint_path="final0", device="cpu")
        detected_beats, detected_downbeats = beat_detector(waveform, sample_rate)
        
        # Audio2Beats already returns times in seconds, no conversion needed
        print(f"✓ Detected {len(detected_beats)} beats and {len(detected_downbeats)} downbeats")
        
        print("✓ Saving output files...")
        np.savez("beat_probs.npz", 
                 beat_times=beat_times, 
                 beat_probs=beat_logits.numpy(),
                 downbeat_probs=downbeat_logits.numpy(),
                 detected_beats=detected_beats,
                 detected_downbeats=detected_downbeats)
        print("✓ File saved: beat_probs.npz")
        return True

    except Exception as e:
        print(f"✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    run_beat_detection()
