# BeatSpecVisual

A modular Python system for beat detection, score alignment, and synchronized visualization of music performances with their corresponding sheet music.

## Overview

BeatSpecVisual combines audio analysis, beat tracking, and score warping into a composable visualization framework. The project uses a **layer-based architecture** where all visualization components inherit from a base `Layer` class, enabling flexible and extensible visualizations.

## Requirements

- Python 3.12.3 or higher

## Installation

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Project Architecture

### Layer-Based System

All visualization components inherit from `visualization_system.Layer` and must implement:

- `load_data(**kwargs)` — Load and validate data, return `bool`
- `draw(ax, shared_data)` — Draw visualization on axis, return `(lines, labels)`

### Core Modules

**[src/functions/visualization_system.py](src/functions/visualization_system.py)**
- `Layer` — Base class for all visualization components
- `Visualizer` — Main orchestrator for composing and rendering multiple layers

**[src/functions/Beat_Layers.py](src/functions/Beat_Layers.py)**
- Beat and downbeat detection visualization layers
- Probability graphs and accurate beat/downbeat timing overlays

**[src/functions/Spectrogram_layer.py](src/functions/Spectrogram_layer.py)**
- Mel-scale spectrogram visualization of audio

**[src/functions/warp_score.py](src/functions/warp_score.py)**
- Score alignment and warping utilities
- Score-spectrogram composite visualization creation

**[src/functions/Load_Files.py](src/functions/Load_Files.py)**
- Data loading utilities for maps, beat data, scores, and audio files

## Data Requirements

To run visualizations, you need:

1. **Audio File** — `.wav` format recording to analyze
2. **Beat Analysis** — `.npz` file containing beat tracking data
3. **Score File** — SVG image (warped score from ScoreWarp)
4. **Maps File** — `.maps.json` containing note onset times and IDs (required for score alignment)

### Obtaining Data Files

- **Maps & Score Alignment** — Use [trompa-align](https://github.com/trompamusic/trompa-align)
  - Reference: [Weigl, D. (2020). Multimodal Music Information Alignment](https://trompamusic.eu/deliverables/TR-D3.5-Multimodal_Music_Information_Alignment_v2.pdf)
- **Score Warping** — Use ScoreWarp to generate SVG from MEI/MusicXML files
  - [Verovio Online Editor](https://editor.verovio.org/) for MEI preview
  - [MusicXML Converter](https://musicxml.tools/converter) for format conversion

## Project Structure

```
0_BeatSpecVisual/
├── README.md
├── requirements.txt
├── agents.md
├── src/
│   └── functions/
│       ├── __init__.py
│       ├── Beat_Layers.py
│       ├── Spectrogram_layer.py
│       ├── visualization_system.py
│       ├── warp_score.py
│       └── Load_Files.py
├── input_files/
│   ├── beat_this_analysis/
│   └── BWV856/
│       ├── beat_Bach.npz
│       ├── BWV856.mei
│       ├── bwv856 LouJ01 asap.maps
│       ├── Performance1/
│       ├── Performance2/
│       └── Performance3/
├── examples/
│   ├── BWV856.py
│   ├── BWV856_EXAMPLE1.py
│   ├── BWV856_EXAMPLE2.py
│   ├── BWV856_COMBINE.py
│   └── Turn_txt_into_MAPS.py
├── output/
└── .gitignore
```

## Usage

### Running Examples

Example scripts in the `examples/` folder demonstrate the system:

```bash
cd examples
python BWV856_EXAMPLE1.py
```

### Creating Custom Visualizations

```python
from src.functions.visualization_system import Visualizer
from src.functions.Spectrogram_layer import Spectrogram
from src.functions.Beat_Layers import BeatProbabilityLayer

# Create visualizer
viz = Visualizer(figsize=(14, 6))

# Add layers
viz.add_layer(Spectrogram())
viz.add_layer(BeatProbabilityLayer())

# Load data
viz.load_all_layers(
    audio_path="path/to/audio.wav",
    beat_file="path/to/beat_data.npz",
    maps_file="path/to/score.maps.json"
)

# Render and save
viz.draw()
viz.show()
viz.TurnPlotIntoPNG("output.png", plot_size=(1920, 1080))
viz.TurnInToSVG("output.svg")
```

## Output

Processed visualizations are saved to the `output/` directory, including:
- PNG exports with custom pixel dimensions
- SVG exports (vector format for publication quality)
- Composite score-spectrogram alignments

## Development Notes

- **Comments**: Use `''' '''` (triple quotes) for all comments; avoid `#` comments
- **Dependencies**: See [requirements.txt](requirements.txt) before adding new packages
- **File Organization**: Output files should go to `/output`
- Maintain existing commented-out code segments — do not remove them

## Resources

- [Verovio Online Editor](https://editor.verovio.org/) — Visualize and edit MEI files
- [MusicXML Converter](https://musicxml.tools/converter) — Convert MXL to MusicXML format

