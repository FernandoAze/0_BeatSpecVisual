# BeatSpec Visual

A visualization system for beat tracking and spectrogram analysis using a modular, lego-like architecture with Python's OOP principles.

## Features

- **Modular Layer Architecture**: Add visualization layers independently (Spectrogram, Beat Probabilities, Downbeat Probabilities)
- **Spectrogram Analysis**: Loads and displays spectrograms of audio files
- **Beat Detection**: Visualizes beat probabilities and downbeat predictions from the BeatThis! algorithm
- **Easy Integration**: Simple fluent API for adding and configuring layers

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd 0_BeatSpecVisual
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install beat_this algorithm:
```bash
pip install beat_this
```

## Usage

Run the example visualization script:
```bash
python3 lego_layers.py
```

This will:
1. Load audio from `PARTITURAS_MEI/ChopinNocOP27n2-Full.wav`
2. Load beat probabilities from `beat_probs.npz`
3. Display layers for spectrogram, beat probabilities, and downbeat probabilities
4. Show an interactive matplotlib visualization

## Project Structure

```
├── visualization_system.py      # Main visualization engine (Visualizer, Layer base class)
├── Spectogram_layer.py          # Audio spectrogram visualization
├── BeatThis_layers.py           # BeatThis! algorithm visualization layers
├── lego_layers.py               # Example usage script
├── beat_this_call.py            # BeatThis! algorithm implementation
├── BeatThis_layers.py           # Beat tracking layer definitions
├── requirements.txt             # Python dependencies
├── beat_probs.npz               # Precomputed beat probabilities
└── PARTITURAS_MEI/              # Musical scores and audio files
    ├── nocturne-op-27-no-2.mei
    ├── clair-de-lune FULL.mei
    └── peaks/
```

## Architecture

### Layer-Based Design

All visualization elements inherit from the `Layer` abstract base class:

```python
class Layer(ABC):
    @abstractmethod
    def load_data(self, **kwargs) -> bool:
        """Load layer-specific data"""
        pass
    
    @abstractmethod
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        """Draw the layer on matplotlib axes"""
        pass
```

### Available Layers

- **SpectrogramLayer**: Displays audio spectrogram
- **BeatProbabilityLayer**: Visualizes beat probability predictions
- **DownbeatProbabilityLayer**: Visualizes downbeat probability predictions

### Visualizer

The `Visualizer` class orchestrates all layers:

```python
viz = Visualizer()
viz.add_layer(SpectrogramLayer())
viz.add_layer(BeatProbabilityLayer())
viz.load_all_layers(audio_path="...", beat_probs_file="...")
fig, ax = viz.draw()
viz.show()
```

## Dependencies

- **modusa**: Music dataset utilities
- **matplotlib**: Data visualization
- **numpy**: Numerical computing
- **librosa**: Audio analysis
- **soundfile**: Audio file I/O
- **torch**: Deep learning framework