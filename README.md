# BeatSpec Visual

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

## Available Methods

*[Add list of available methods and their descriptions here]*


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