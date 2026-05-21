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
import xml.etree.ElementTree as ET

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
            # print(f"Drawing layer: {layer.name}")
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

    def getSVG_Score_Height(self, svg_score: str, maps_json_file: str) -> Optional[float]:
        '''
        Extract the height of the score from the SVG file using the maps JSON for reference.
        
        Args:
            svg_score: Path to the SVG score file
            maps_json_file: Path to the maps JSON file containing note positions
        '''
    def get_SVG_Root_Dimensions(self, svg_warped_score: str, print_output: bool = False):

        svg_tree = ET.parse(svg_warped_score)
        root = svg_tree.getroot()

        width_str = root.get('width')
        height_str = root.get('height')

        if width_str and height_str:
            width = float(width_str.replace('px', ''))
            height = float(height_str.replace('px', ''))
            if print_output:
                print(f"✓ SVG root dimensions: width={width}, height={height}")
            return width, height
        else:
            if print_output:
                print("✗ SVG root does not have explicit width and height attributes")
            return None
    
    def get_timeAxis_attributes(self, svg_warped_score: str, print_output: bool = False):
        '''
        Extract the total timeline time from the warped score SVG.
        '''
        try:
            svg_tree = ET.parse(svg_warped_score)
            root = svg_tree.getroot()
            
            ''' Handle XML namespaces in SVG files '''
            namespace = {'svg': 'http://www.w3.org/2000/svg'}
            
            ''' Find all g elements and locate the one with class='timeAxis' '''
            time_axis_group = None
            ''' Try with namespace first '''
            for group in root.iter('{http://www.w3.org/2000/svg}g'):
                if group.get('class') == 'timeAxis':
                    time_axis_group = group
                    break
            
            ''' If not found, try without namespace '''
            if time_axis_group is None:
                for group in root.iter('g'):
                    if group.get('class') == 'timeAxis':
                        time_axis_group = group
                        break
            
            if time_axis_group is None:
                if print_output:
                    print("✗ Error: timeAxis group not found")
                return None
            
            ''' Get the last child element from the timeAxis group '''
            children = list(time_axis_group)
            
            if not children:
                if print_output:
                    print("✗ Error: No child elements found in timeAxis group")
                return None
            
            ''' Get the last child element '''
            last_element = children[-1]
            last_text_content = last_element.text
            
            if last_text_content is None:
                if print_output:
                    print("✗ Error: Last text element is empty")
                return None
            
            ''' Convert to numeric value '''
            timeline_time = float(last_text_content)
            
            ''' Convert to int if it's a whole number '''
            if timeline_time.is_integer():
                timeline_time = int(timeline_time)
            
            if print_output:
                print(f"✓ Total timeline time: {timeline_time}")
            
            ''' Look for timeline start and end in pixels '''
            ''' Get the SECOND element of the timeAxis group, it should be a <line> element with x1 and x2 values '''
            if len(children) < 2:
                if print_output:
                    print("✗ Error: Expected at least 2 elements in timeAxis group")
                return None
            
            second_element = children[1]
            x1_str = second_element.get('x1')
            x2_str = second_element.get('x2')
            
            if x1_str is None or x2_str is None:
                if print_output:
                    print("✗ Error: Could not find x1 and x2 attributes in second element")
                return None
            
            x1 = float(x1_str)
            x2 = float(x2_str)
            
            timeline_lengthPx= x2 - x1

            if print_output:
                print(f"✓ Timeline x1: {x1}, x2: {x2}")

            return timeline_time, timeline_lengthPx
            
        except Exception as e:
            if print_output:
                print(f"✗ Error extracting timeline time: {e}")
            return None

    def get_Layers_WidthHeight(self, svg_warped_score: str, print_output: bool = False):
        '''
        Get the width and height for the layers based on the warped score SVG dimensions.
        Returns:
            Tuple of (width, height) in pixels, or None if error
        '''

        layersHeight = self.get_SVG_Root_Dimensions(svg_warped_score, print_output)[1]
        totalWidth = self.get_timeAxis_attributes(svg_warped_score, print_output)[1]
        
        totalTimelineTime = self.get_timeAxis_attributes(svg_warped_score, print_output)[0]
        
        audioDuration = self.shared_data.get('audio_duration', None)

        layersWidth = (totalWidth / totalTimelineTime) * audioDuration

        if print_output==True:
            print(f"✓ Layers width: {layersWidth}, Layers height: {layersHeight}")
            
        return layersWidth, layersHeight       
    
    def TurnLayersIntoSVG(self, filename: str, svg_warped_score: str, plot_size: Optional[Tuple[int, int]] = None, print_output: bool = False):
        '''
        Convert all layers to a vector-based SVG with each layer as a separate group.
        
        Args:
            filename: Output SVG filename
            svg_warped_score: Path to the warped score SVG file
            plot_size: Tuple of (width, height) in pixels
            print_output: Whether to print status messages
        
        Returns:
            filename if successful, False otherwise
        '''
        if "ax" not in self.shared_data:
            print("✗ Error: No axes found. Call draw() first.")
            return False
        
        if plot_size is None:
            width_px =self.get_Layers_WidthHeight(svg_warped_score, print_output)[0]
            height_px =self.get_Layers_WidthHeight(svg_warped_score, print_output)[1]
        else:
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
    
    def TurnPlotIntoPNG(self, filename: str, svg_warped_score: str, plot_size: Optional[Tuple[int, int]] = None, dpi: int = 150, print_output: bool = False) -> bool:
        """
        Save visualization as PNG with exact pixel dimensions and no padding/axis.
        
        Args:
            filename: Output PNG filename
            svg_warped_score: Path to the warped score SVG file
            plot_size: Tuple of (width, height) in pixels (exact)
            dpi: Dots per inch (default 150). PNG will be exactly width × height pixels.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if plot_size is None:
            width_px =self.get_Layers_WidthHeight(svg_warped_score, print_output)[0]
            height_px =self.get_Layers_WidthHeight(svg_warped_score, print_output)[1]
        else:
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
    
    def add_New_SVG_Root(self, svg_file: str, width, height, background_color: str = '#ffffff', print_output: bool = False):
        '''
        Add a new parent SVG root with specified dimensions around existing SVG content.
        
        Args:
            svg_file: Path to the existing SVG file
            width: Width in pixels for the new root SVG
            height: Height in pixels for the new root SVG
            background_color: Color for the background rectangle
            print_output: Whether to print status messages
        
        Returns:
            tuple: (width, height) of the new root, or False if error
        '''
        try:
            ''' Read the existing SVG file as text '''
            with open(svg_file, 'r', encoding='UTF-8') as f:
                svg_content = f.read()
            
            ''' Remove XML declaration if present '''
            if svg_content.startswith('<?xml'):
                svg_content = svg_content.split('?>', 1)[1].strip()

            ''' Create new root SVG wrapper with specified dimensions '''
            new_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{width}px"
     height="{height}px"
     viewBox="0 0 {width} {height}"
     transform="translate(0, 0)">
  <rect x="0" y="0" width="100%" height="100%" fill="{background_color}" />
{svg_content}
</svg>'''
            
            ''' Write the new SVG back to file '''
            with open(svg_file, 'w', encoding='UTF-8') as f:
                f.write(new_svg)
            
            if print_output:
                print(f"✅ New SVG root added: {width}x{height}px to {svg_file}")
            
            return width, height
            
        except Exception as e:
            print(f"✗ Error adding new SVG root: {e}")
            return False
