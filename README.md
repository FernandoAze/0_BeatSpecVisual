# BeatSpecVisual

## Project Structure

```
0_BeatSpecVisual/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── src/
│   └── beat_spec_visual/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── beat_detection.py
│       ├── visualization/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── visualizer.py
│       │   ├── layers/
│       │   │   ├── __init__.py
│       │   │   ├── spectrogram.py
│       │   │   ├── beat_this.py
│       │   │   ├── lego.py
│       │   │   └── scorewarp.py
│       │   └── output/
│       │       ├── __init__.py
│       │       └── svg.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── data/
│   ├── PARTITURAS_MEI/
│   │   ├── *.mei
│   │   └── peaks/
│   └── outputs/
├── tests/
│   ├── __init__.py
│   ├── test_beat_detection.py
│   └── test_visualization.py
└── examples/
	 └── run_pipeline.py
```

## Usage

1. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
2. **Run the pipeline example:**
	```bash
	python examples/run_pipeline.py
	```

## Description

BeatSpecVisual is a modular system for beat detection and visualization. The codebase is organized for clarity and extensibility, with core logic, visualization layers, and utilities separated into logical modules.