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
            
            # Subtract the first onset time from all onset times to normalize
            if onset_times:
                first_onset = onset_times[0]
                onset_times = [t - first_onset for t in onset_times]
            
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
            line = ax.axvline(x=onset, color=self.onset_color,
            linestyle='--', linewidth=0.1, label='Onset')
            lines.append(line)
        
        if lines:
            labels = [self.name]
        
        return lines, labels
    
    def Retrieve_TmnTmx(_):
        print("STILL ON THE WORKS")  
        """
        A ideia aqui é fazer um método para fazer a diferença da posição x entre o primeiro e o ultimo onset.
        
        No scorewarp isto equivale ao tmn e tmx. 
        
        Isto é o que vai dar a o espaço onde o espetrograma/plot vai ser desenhado. 
        """
    def Combine_PlotPNG_wScore():
        print("STILL ON THE WORKS")
        """
        A ideia desta, é juntar o png do plot com o score em um svg só. 

        Input: input_files/PLOT.png && input_files/.../Chopin_op10_no3_p01-mei.svg
        Output: output_files/PLOT_WITH_SCORE.svg

        Este método deve juntar o png gerado com Visualizer.TurnInToSVG() com a WarpedScore.svg. 
        Para isso: 
            1 - SVG final parte do SVG da warpedScore.svg 
            (os elementos vao ser acrescentados a este SVG, para manter as proporções do score)

            2 -Retrieve_TmnTmx(_),  determina o tamanho do png e onde ele deve ser posicionado. 
            Tamanho, Width=tmx-tmn, Height=altura do svg gerado no scorewarp.

            3 - acrescentar um background branco que fica atrás do png e consequentemente, do score.
            (isto é só para evitar background transparente no início/fim do espetrograma/score)

            4 - Juntar o PLOT.png como um elemento <image> dentro do svg final. 

            5 - Fazer output do svg final.

        O SVG final deve 3 layers na seguinte ordem de sobreposição:
            1 - background branco (um retângulo branco que cobre toda a área do svg)
            2 - PLOT.png
            3 - WarpedScore.svg
        
        """