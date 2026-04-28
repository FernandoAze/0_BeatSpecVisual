from abc import ABC, abstractmethod
from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Dict, Any, List, Tuple, Optional
import json

from .visualization_system import Layer

class Onsets_Layer(Layer):
    def __init__(self, name: str = "obs_mean_onsets", onset_color: str = 'yellow'):
        super().__init__(name)
        self.onset_color = onset_color

    def load_data(self, maps_file: str = None, **kwargs) -> bool:
        """Load onsets from MAPS file"""
        if maps_file is None:
            from pathlib import Path
            module_dir = Path(__file__).parent
            maps_file = module_dir.parent / "input_files" / "PARTITURAS_MEI" / "Chopin_op10_no3_p01-mei.maps.json"
        
        try:
            with open(str(maps_file), 'r') as f:
                data = json.load(f)
            
            # Extract obs_mean_onset times from each object in the array
            if not isinstance(data, list) or len(data) == 0:
                print("!!!!Maps file ERROR: Expected a non-empty array!!!!")
                return False
            
            # Check if obs_mean_onset exists in the first entry
            if 'obs_mean_onset' not in data[0]:
                print("!!!!Maps file ERROR: 'obs_mean_onset' not found in data!!!!")
                return False
            
            onset_times = [entry['obs_mean_onset'] for entry in data]
            
            self._data = {
                "onset_times": onset_times,
            }
            print(f"✓ {self.name}: Loaded {len(self._data['onset_times'])} onsets")
            return True
        except Exception as e:
            print(f"✗ {self.name} error: {e}")
            return False
    
    def draw(self, ax, shared_data) -> Tuple[List, List]:
        if self._data is None:
            print("✗ Onsets_Layer: No data loaded")
            return [], []
        
        lines = []

        for onset in self._data['onset_times']:
            line = ax.axvline(x=onset, color=self.onset_color, linestyle='--', linewidth=0.5)
            lines.append(line)
        
        if lines:
            labels = [self.name]
        
        return lines, labels