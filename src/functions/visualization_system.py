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
        print(f"Added layer: {layer.name}")
        return self
    
    def load_all_layers(self, **kwargs) -> bool:
        for layer in self.layers:
            if not layer.load_data(**kwargs):
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
        
        if self.all_lines:
            self.ax.legend(self.all_lines, self.all_labels, loc='upper right')
        
        plt.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.1)
        
        return self.fig, self.ax
    
    def show(self):
        plt.show()
    
    def TurnInToSVG(self, filename: str) -> bool:
        """
        Save visualization as an SVG file.
        
        """
        try:
            if self.fig is None:
                print("⚠ Error: No figure to save. Call draw() first.")
                return False
            
            # Hardcoded high quality DPI
            save_dpi = 150
            
            # Save figure as SVG
            self.fig.savefig(
                filename, 
                format='svg',
                dpi=save_dpi,
                bbox_inches='tight',
                facecolor='white'
            )
            print(f"✅ SVG saved successfully: {filename}")
            return True
        
        except Exception as e:
            print(f"❌ Error saving SVG: {e}")
            return False
    
    def TurnPlotIntoSVG(self, filename: str, width_px: int, height_px: int, dpi: int = 150) -> bool:
        """
        Save visualization as an SVG file with custom dimensions and no padding/axis.
        
        Args:
            filename: Output SVG filename
            width_px: Width in pixels
            height_px: Height in pixels
            dpi: Dots per inch (default 150). Use same DPI for figure creation and saving for efficiency.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if self.fig is None:
                print("⚠ Error: No figure to save. Call draw() first.")
                return False
            
            # Convert pixels to inches using provided DPI
            figsize_inches = (width_px / dpi, height_px / dpi)
            
            # Create new figure with specified DPI
            fig_export, ax_export = plt.subplots(figsize=figsize_inches, dpi=dpi)
            
            # Redraw all layers on the new figure without axis/padding
            for layer in self.layers:
                layer.draw(ax_export, self.shared_data)
            
            # Remove axis completely
            ax_export.axis('off')

            # Remove any title that might be set
            ax_export.set_title('')

            # Remove all margins and padding
            fig_export.subplots_adjust(left=0, right=1, top=1, bottom=0)
            
            # Save figure as SVG with same DPI for consistency
            fig_export.savefig(
                filename,
                format='svg',
                dpi=dpi,
                pad_inches=0,
                facecolor='white'
            )
            
            # Clean up the temporary figure
            plt.close(fig_export)
            
            print(f"✅ SVG saved successfully: {filename} (~{width_px}x{height_px}px @ {dpi}dpi)")
            return True
        
        except Exception as e:
            print(f"❌ Error saving SVG: {e}")
            return False
    
    def TurnPlotIntoPNG(self, filename: str, plot_size: Tuple[int, int], dpi: int = 150) -> bool:
        """
        Save visualization as PNG with exact pixel dimensions and no padding/axis.
        
        Args:
            filename: Output PNG filename
            plot_size: Tuple of (width, height) in pixels (exact)
            dpi: Dots per inch (default 150). PNG will be exactly width × height pixels.
        
        Returns:
            bool: True if successful, False otherwise
        """
        import os
        
        try:
            if self.fig is None:
                print("⚠ Error: No figure to save. Call draw() first.")
                return False
            
            # Unpack plot_size tuple
            width_px, height_px = plot_size
            
            # Convert pixels to inches using provided DPI for figure creation
            figsize_inches = (width_px / dpi, height_px / dpi)
            
            # Create new figure with specified DPI
            fig_export, ax_export = plt.subplots(figsize=figsize_inches, dpi=dpi)
            
            # Redraw all layers on the new figure without axis/padding
            for layer in self.layers:
                layer.draw(ax_export, self.shared_data)
            
            # Remove axis completely
            ax_export.axis('off')

            # Remove any title that might be set
            ax_export.set_title('')

            # Remove all margins and padding
            fig_export.subplots_adjust(left=0, right=1, top=1, bottom=0)
            
            # Define output directories
            output_dirs = [
                'src/input_files',
                'output'
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
                print(f"✅ PNG saved successfully: {output_path} ({width_px}x{height_px}px @ {dpi}dpi)")
            
            # Clean up the temporary figure
            plt.close(fig_export)
            
            return True
        
        except Exception as e:
            print(f"❌ Error saving PNG: {e}")
            return False
        
    
