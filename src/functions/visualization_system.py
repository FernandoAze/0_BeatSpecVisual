"""
Lego-like visualization system using OOP.
Each visual element is a Layer that knows how to draw itself.
The Visualizer assembles layers together.
"""

from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Dict, Any, List, Tuple, Optional
import os

# class Layer(ABC), defines the template for all layer subclasses.
class Layer(ABC): 
    def __init__(self, name: str = "Layer"):
        self._data = None # Placeholder for layer-specific data
        self.name = name # Optional name for debugging and legend purposes

    @abstractmethod
    def load_data(self, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def draw(self, ax: Axes, shared_data: Dict[str, Any]) -> Tuple[List, List]:
        pass
    
    def to_svg_group(self, shared_data: Dict[str, Any]) -> Optional[str]:
        '''
        Convert layer drawing to SVG group markup.
        Override in subclasses to support SVG export.
        
        Returns:
            SVG group markup string, or None if not supported
        '''
        return None



class Visualizer:
    def __init__(self, figsize: Optional[Tuple[float, float]] = None, 
                 plot_size_inPxl: Optional[Tuple[int, int]] = None, 
                 dpi: int = 300):
        """
        Initialize Visualizer with customizable figure size.
        
        Args:
            figsize: Figure size as (width, height) in inches. Default (14, 8) if neither figsize nor pixel_size specified.
            pixel_size: Figure size as (width, height) in pixels. Converts to inches using dpi parameter.
            dpi: Dots per inch for pixel-to-inch conversion. Default is 96 (standard screen DPI).
        """
        self.layers: List[Layer] = []
        self.shared_data: Dict[str, Any] = {}
        self.fig = None
        self.ax = None
        self.all_lines = []
        self.all_labels = []
        self.dpi = dpi
        
        # Convert pixel_size to inches if provided, otherwise use figsize or default
        if plot_size_inPxl is not None:
            self.figsize = (plot_size_inPxl[0] / dpi, plot_size_inPxl[1] / dpi)
        elif figsize is not None:
            self.figsize = figsize
        else:
            self.figsize = (14, 8)  # Default size in inches
    
    def add_layer(self, layer: Layer) -> 'Visualizer':
        self.layers.append(layer)
        # print(f"Added layer: {layer.name}")
        return self
    
    def load_all_layers(self, audio_path: str = None, **kwargs) -> bool:
        # Calculate audio duration, store in shared_data.
        # Used to force x-axis time limit to audio duration.
        if audio_path is not None:
            from .warp_score import Warp_Score
            audio_duration = Warp_Score().audio_duration(audio_path)
            self.shared_data['audio_duration'] = audio_duration
            self.shared_data['audio_path'] = audio_path
        for layer in self.layers:
            if not layer.load_data(audio_path=audio_path, **kwargs):
                print(f"⚠ Warning: Layer '{layer.name}' failed to load")
                return False
        return True
    
    def draw(self) -> Tuple[plt.Figure, plt.Axes]:
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        
        for layer in self.layers:
            print(f"Drawing layer: {layer.name}")
            lines, labels = layer.draw(self.ax, self.shared_data)
            self.all_lines.extend(lines)
            self.all_labels.extend(labels)
        
        ''' Enforce full audio duration on x-axis '''
        if 'audio_duration' in self.shared_data:
            audio_duration = self.shared_data['audio_duration']
            self.ax.set_xlim(0, audio_duration)
            
            ''' Also set secondary axis if it exists '''
            if 'ax2' in self.shared_data:
                self.shared_data['ax2'].set_xlim(0, audio_duration)
        
        if self.all_lines:
            self.ax.legend(self.all_lines, self.all_labels, loc='upper right')
        
        plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.1)
        
        ''' Store axes for SVG conversion '''
        self.shared_data["ax"] = self.ax
        if "ax2" in self.shared_data:
            self.shared_data["ax2_exists"] = True
        
        return self.fig, self.ax
    
    def show(self):
        plt.show()
    
    def TurnLayersIntoSVG(self, filename: str, plot_size: Tuple[int, int], print_output: bool = False):
        '''
        Convert all layers to a vector-based SVG with each layer as a separate group.
        
        Args:
            filename: Output SVG filename
            plot_size: Tuple of (width, height) in pixels
            plot_axis: Whether to include axes in the SVG   
            print_output: Whether to print status messages
        
        Returns:
            filename if successful, False otherwise
        '''
        if "ax" not in self.shared_data:
            print("✗ Error: No axes found. Call draw() first.")
            return False
        
        width_px, height_px = plot_size
        ax = self.shared_data["ax"]
        
        ''' Get axis limits for coordinate conversion '''
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        
        ''' Store axis info for layer SVG conversion '''
        self.shared_data["svg_context"] = {
            "x_min": x_min,
            "x_max": x_max,
            "y_min": y_min,
            "y_max": y_max,
            "width_px": width_px,
            "height_px": height_px
        }
        
        svg_groups = []
        skipped_layers = []
        
        ''' Collect SVG groups from each layer '''
        for layer in self.layers:
            svg_content = layer.to_svg_group(self.shared_data)
            if svg_content is None:
                skipped_layers.append(layer.name)
            else:
                svg_groups.append(svg_content)
        
        ''' Print warnings for skipped layers '''
        if skipped_layers:
            for layer_name in skipped_layers:
                print(f"⚠ Warning: Layer '{layer_name}' doesn't support SVG export, skipping")
        
        ''' Build SVG markup '''
        svg_content = '\n'.join(svg_groups)
        svg_markup = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width_px}px"
     height="{height_px}px"
     viewBox="0 0 {width_px} {height_px}">
  <!-- Beat Spec Visual Layers -->
{svg_content}
</svg>'''
        
        try:
            with open(filename, 'w') as f:
                f.write(svg_markup)
            
            if print_output:
                print(f"✅ SVG saved successfully: {filename} (~{width_px}x{height_px}px)")
            return filename
        except Exception as e:
            print(f"✗ Error saving SVG: {e}")
            return False
    
    def TurnPlotIntoPNG(self, filename: str, plot_size: Tuple[int, int], dpi: int = 150, print_output: bool = False) -> bool:
        """
        Save visualization as PNG with exact pixel dimensions and no padding/axis.
        
        Args:
            filename: Output PNG filename
            plot_size: Tuple of (width, height) in pixels (exact)
            dpi: Dots per inch (default 150). PNG will be exactly width × height pixels.
        
        Returns:
            bool: True if successful, False otherwise
        """

        # Unpack plot_size tuple
        width_px, height_px = plot_size
        
        # Convert pixels to inches using provided DPI for figure creation
        figsize_inches = (width_px / dpi, height_px / dpi)
        
        # Create new figure with specified DPI
        fig_export, ax_export = plt.subplots(figsize=figsize_inches, dpi=dpi)
        
        # Redraw all layers on the new figure without axis/padding
        for layer in self.layers:
            layer.draw(ax_export, self.shared_data)
        
        # Remove axis completely and remove title
        ax_export.axis('off')
        ax_export.set_title('')

        # Remove all margins and padding
        fig_export.subplots_adjust(left=0, right=1, top=1, bottom=0)
        
        # Define output directories (relative to parent folders from script location)
        output_dirs = [
            os.path.join(os.path.dirname(__file__), '..', 'input_files'),
            os.path.join(os.path.dirname(__file__), '..', '..', 'output')
        ]
        
        # Create directories if they don't exist and save to both locations
        for output_dir in output_dirs:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
            
            # Save figure as PNG with exact dimensions
            fig_export.savefig(
                output_path,
                format='png',
                dpi=dpi,
                pad_inches=0,
                facecolor='white'
            )
        
        # Clean up the temporary figure
        plt.close(fig_export)

        if print_output==True:
                print(f"✅ PNG saved successfully: {filename} ---> ({width_px}x{height_px}px @ {dpi}dpi)")
        return output_path
