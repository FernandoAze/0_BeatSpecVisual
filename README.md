# BeatSpec Visual 
THIS README IS STILL ON THE WORKS

## Description

BeatSpecVisual is a modular system for beat detection and visualization. The codebase is organized for clarity and extensibility, with core logic, visualization layers, and utilities separated into logical modules.

---

## Requirements

- Python 3.12.3+

---

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
# Create a virtual environment with Python 3.12.3
python3.12 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install dependencies from requirements.txt
pip install -r requirements.txt
```
---

## How to Run

### Running Example Files

The project includes example scripts in the `examples/` folder.

```bash
# Navigate to the examples folder
cd examples

# Run any example script ex:
python lego_layers.py

```

## Project Structure

```
0_BeatSpecVisual/
├── README.md
├── requirements.txt
├── src/
│   └── functions/
│       ├── __init__.py
│       ├── BeatThis_layers.py 
│       ├── Spectogram_layer.py
│       ├── visualization_system.py
│       ├── warp_score.py
│       └── input_files/
│           ├── beat_this_analysis/
│           │   └── beat_probs.npz
│           └── PARTITURAS_MEI/
│               ├── Chopin_Op10_3_1.mei
│               └── Chopin_op10no3_p01-mei.maps.json
├── examples/
│   ├── lego_layers.py
│   ├── ouput_svg.py
│   └── plot_ouput_svg.py
└── output/
```
---

## Layers and Components Description
!!!!!!!!!CAPITULO PLACEHOLDER ESCRITO PELO AI TENHO DE REVER ISTO E RESCREVER DE FORMA MAIS PORREIRA
### visualization_system.py

#### Visualizer
Assembles multiple visualization layers. Use this as the main entry point to build composite visualizations.

**Key methods:**
- `add_layer(layer)` — Add a layer (e.g., spectrogram, beats, onsets)
- `load_all_layers(audio_path=..., beat_file=..., maps_file=...)` — Pass your file paths here to load all layers at once
- `draw()` — Render the visualization
- `show()` — Display in window
- `TurnPlotIntoPNG(filename, plot_size=(width, height))` — Save as PNG with exact pixel size
- `TurnInToSVG(filename)` — Save as high-quality SVG

**Usage example:**
```python
viz = Visualizer(figsize=(12, 8))
viz.add_layer(Spectrogram())
viz.add_layer(BeatProbabilityLayer())
viz.load_all_layers(audio_path="audio.wav", beat_file="beat_probs.npz")
viz.draw()
viz.show()
```

#### Layer
Abstract base class for all visualization components. Inherit from this to create custom layers.

---
### BeatThis_layers.py

#### Run_BeatThis (Function)
Runs beat detection on audio and saves results to .npz file.

**Inputs:**
- `audio_path` — Path to audio file
- `output_path` — Where to save .npz (default: `src/input_files/beat_this_analysis/beat_probs.npz`)

**Returns:** Path to saved .npz file

#### BeatProbabilityLayer
Shows beat detection probability as a line graph.

**Key tuning:**
- `color` — Line color (default: red)

**Inputs (via load_data):**
- `beat_file` — Path to .npz from Run_BeatThis()

#### DownbeatProbabilityLayer
Shows downbeat probability as a line graph.

**Key tuning:**
- `color` — Line color (default: blue)

**Inputs (via load_data):**
- `beat_file` — Path to .npz from Run_BeatThis()


#### BeatAccurateLayer
Shows detected beat and downbeat times as vertical lines.

**Key tuning:**
- `beat_color` — Color for beats (default: red)
- `downbeat_color` — Color for downbeats (default: blue)

**Inputs (via load_data):**
- `beat_file` — Path to .npz from Run_BeatThis()

---
### Spectogram_layer.py

#### Spectrogram
Displays mel-scale spectrogram of audio.

**Key tuning:**
- `freq_window` — Frequency range in Hz (default: 20-4000)
- `color_map` — Colormap name (default: "magma")

**Inputs (via load_data):**
- `audio_path` — Path to audio file

---

### warp_score.py

#### Onsets_Layer
Shows note onset times from score alignment as vertical lines.

**Key tuning:**
- `onset_color` — Line color (default: yellow)

**Inputs (via load_data):**
- `maps_file` — Path to .maps.json file from score alignment

#### Warp_Score
Aligns and warps score with spectrogram PNG. Creates composite visualizations.

**Key methods:**
- `crop_png(maps_file, png_file, audio_file)` — Crop spectrogram to match score timeline. Saves to `/output/cropped_png.png`
- `Allign_Score_and_PNG(png_plot, svg_image, maps_json_file)` — Create composite SVG with embedded spectrogram. Saves to `/output/composite.svg`
- `extract_viewBox_dimensions(svg_file)` — Get SVG dimensions
- `get_first_and_last_onsets(maps_file)` — Get onset times from maps file

**Inputs:**
- `maps_file` — Path to .maps.json file from score alignment
- `png_file` — Path to spectrogram PNG
- `audio_file` — Path to audio file (for duration info)
- `svg_image` — Path to score SVG

---

## Notes:

BeatThis_layers.py 
	This script is divided into multiple classes that should just be methods of a "class BeatThis()". 
	I will correct this in the future. 

Folder src/input_files structure also will be changed to have be:
```bash
├── src/
│   └── input_files/
│           ├── PlotPNG/
│           │   └── PLOT.png			#store the image that is used as input for .Combine_plotPNG_Score()	
│           ├── Tracked_Beat/			#instead of "beat_this_analysis/"
│           │   └── tracked_beat.npz 	#instead of "beat_probs.npz"
│           └── WarpedScores/ 				#For Storing the warped Scores and MAPS file. 
│               ├── Chopin_op10no3_p01-mei.maps.json.svg  
│               └── Chopin_op10no3_p01-mei.maps.json
	
```