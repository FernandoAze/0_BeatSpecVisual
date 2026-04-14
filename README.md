# BeatSpecVisual

BeatSpecVisual is a Python tool that visualizes beat detection results on audio spectrograms. It uses the beat_this model to detect beats and downbeats in audio files, then overlays the probability distributions on a mel-spectrogram for interactive visualization.

## Requirements

- Python 3.12
- GPU: Not required (will run on CPU). Though you can run it with PyTorch (instead of torch) if you have a CUDA compatible GPU.
## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd 0_BeatSpecVisual
```

2. Create a virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install beat_this from source:
```bash
pip install https://github.com/CPJKU/beat_this/archive/main.zip
```

## Instructions

1. Paste your audio file path ( WAV format) in:
   ```python
   AUDIO_FILE = "/path/to/your/file"
   ```
   *(Optional: Skip this step to test with the default .wav file)*

2. Run the main visualization script:
```bash
python3.12 layers.py
```

3. The script will:
   - Detect beats and downbeats using the beat_this model
   - Compute a high-resolution mel-spectrogram
   - Display an interactive visualization with:
     - Spectrogram as the background
     - Beat and downbeat probability curves overlaid
     - Interactive controls for zooming and panning

