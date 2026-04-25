
0_BeatSpecVisual/
├── README.md                 # Project documentation
├── requirements.txt
├── setup.py                  # For package installation
├── .gitignore
│
├── src/                      # Main source code
│   └── beat_spec_visual/
│       ├── __init__.py
│       ├── core/             # Core functionality
│       │   ├── __init__.py
│       │   └── beat_detection.py  # (rename from beat_this_call.py)
│       │
│       ├── visualization/    # Visualization system & layers
│       │   ├── __init__.py
│       │   ├── base.py       # (Layer base class from visualization_system.py)
│       │   ├── visualizer.py # (Visualizer class)
│       │   ├── layers/
│       │   │   ├── __init__.py
│       │   │   ├── spectrogram.py    # (from Spectogram_layer.py)
│       │   │   ├── beat_this.py      # (from BeatThis_layers.py)
│       │   │   ├── lego.py           # (from lego_layers.py)
│       │   │   └── scorewarp.py      # (from scorewarp_layer.py)
│       │   └── output/
│       │       ├── __init__.py
│       │       └── svg.py     # (from output_svg.py)
│       │
│       └── utils/            # Utility functions
│           ├── __init__.py
│           └── helpers.py    # Shared utilities
│
├── data/                     # Data files
│   ├── PARTITURAS_MEI/
│   │   ├── *.mei
│   │   └── peaks/
│   └── outputs/              # Generated outputs
│
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── test_beat_detection.py
│   └── test_visualization.py
│
└── examples/                 # Example scripts
    └── run_pipeline.py       # Main script to run everything
