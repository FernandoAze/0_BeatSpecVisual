"""
Beat Visualization Package
"""

import importlib.util

# Helper function to import modules with number-prefixed names
def _import_module_by_filename(filename):
    spec = importlib.util.spec_from_file_location(filename.replace(".py", ""), filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Import modules and expose their functions
_beat_detection = _import_module_by_filename("beat_this_call.py")
_spectrogram = _import_module_by_filename("spectrogram.py")
_beat_layer = _import_module_by_filename("bt_probability_layer.py")

run_beat_detection = _beat_detection.run_beat_detection
compute_spectrogram = _spectrogram.compute_spectrogram
visualize_spectrogram = _spectrogram.visualize_spectrogram
draw_spectrogram = _spectrogram.draw_spectrogram
load_beat_probabilities = _beat_layer.load_beat_probabilities
draw_beat_probability = _beat_layer.draw_beat_probability

__all__ = [
    "run_beat_detection",
    "compute_spectrogram",
    "visualize_spectrogram",
    "draw_spectrogram",
    "load_beat_probabilities",
    "draw_beat_probability",
]
