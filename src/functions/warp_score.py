from abc import ABC, abstractmethod
import sys
from matplotlib import lines
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from typing import Dict, Any, List, Tuple, Optional
import json
import xml.etree.ElementTree as ET
from PIL import Image
import base64
import io
from pathlib import Path
from sklearn import tree
import soundfile


from .visualization_system import Layer

class Onsets_Layer(Layer):
    def __init__(self, name: str = "obs_mean_onsets", onset_color: str = 'yellow'):
        super().__init__(name)
        self.onset_color = onset_color

    def load_data(self, maps_file: str = None, **kwargs) -> bool:
        """Load onsets from MAPS JSON file"""
        try:
            if maps_file is None:
                print(f"✗ {self.name}: Maps file path must be provided")
                return False
            
            with open(str(maps_file), 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list) or len(data) == 0:
                print("✗ Maps file ERROR: Expected a non-empty array")
                return False
            
            ''' Check if obs_mean_onset exists in the first entry '''
            if 'obs_mean_onset' not in data[0]:
                print("✗ Maps file ERROR: 'obs_mean_onset' not found in data")
                return False
            
            onset_times = [entry['obs_mean_onset'] for entry in data]
            
            ''' Subtract the first onset time from all onset times to normalize '''
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
            linestyle='--', linewidth=0.2, label='Onset')
            lines.append(line)
        
        if lines:
            labels = [self.name]
        
        return lines, labels
    
    #========================================================
    # Methods for Layers that are vector based for SVG output
    #========================================================
    def to_svg_group(self, shared_data: Dict[str, Any]) -> Optional[str]:
        '''Convert onsets to SVG dashed vertical lines'''
        if self._data is None or "svg_context" not in shared_data:
            return None
        
        ctx = shared_data["svg_context"]
        onset_times = self._data.get("onset_times", [])
        
        if len(onset_times) == 0:
            return None
        
        lines = []
        color_hex = self._rgb_to_hex(self.onset_color)
        
        ''' Draw dashed vertical lines for each onset '''
        for onset_time in onset_times:
            if ctx["x_max"] == ctx["x_min"]:
                x = 0
            else:
                x = ((onset_time - ctx["x_min"]) / (ctx["x_max"] - ctx["x_min"])) * ctx["width_px"]
            
            lines.append(f'    <line x1="{x:.2f}" y1="0" x2="{x:.2f}" y2="{ctx["height_px"]}" stroke="{color_hex}" stroke-width="0.2" stroke-dasharray="2,2"/>')
        
        svg_group = f'''  <g id="{self.name}" class="layer onsets">
{chr(10).join(lines)}
  </g>'''
        
        return svg_group

    def _rgb_to_hex(self, rgb):
        '''Convert RGB tuple (0-1) or matplotlib color to hex'''
        if isinstance(rgb, tuple) and len(rgb) >= 3:
            r, g, b = [int(c * 255) if c <= 1 else int(c) for c in rgb[:3]]
            return f'#{r:02x}{g:02x}{b:02x}'
        ''' Handle matplotlib color names '''
        try:
            from matplotlib.colors import to_hex
            return to_hex(rgb)
        except:
            return '#000000'
    #========================================================
    # Methods for Layers that are vector based for SVG output
    #========================================================

class Warp_Score():

    def __init__(self):
        self._data = None

    def load_data(self, maps_file: str = None, **kwargs) -> bool:
        ''' Load maps file containing score alignment data '''
        try:
            if maps_file is None:
                print("✗ Warp_Score: Maps file path must be provided")
                return False
            
            with open(str(maps_file), 'r') as f:
                self._data = json.load(f)
            
            if not isinstance(self._data, list) or len(self._data) == 0:
                print("✗ Maps file ERROR: Expected a non-empty array")
                return False
            
            print(f"✓ Warp_Score: Loaded {len(self._data)} entries from maps file")
            return True
        except Exception as e:
            print(f"✗ Warp_Score error: {e}")
            return False

    def extract_viewBox_dimensions(self, svg_file: str, print_output: bool = False):
        svg_tree = ET.parse(svg_file)
        root = svg_tree.getroot()
        ns = {'svg': 'http://www.w3.org/2000/svg'}

        ''' Get viewBox from root or nested SVG '''
        viewbox = root.get('viewBox')
        if not viewbox:
            ''' Look for viewBox in nested SVG elements '''
            nested_svg = root.find(".//svg:svg", ns)
            if nested_svg is not None:
                viewbox = nested_svg.get('viewBox')

        if not viewbox:
            return None

        vb_parts = viewbox.split()
        vb_x, vb_y, vb_width, vb_height = map(float, vb_parts)

        ''' Get display dimensions from root SVG '''
        width_str = root.get('width')
        height_str = root.get('height')

        if width_str:
            display_width = float(width_str.replace('px', ''))
        else:
            display_width = vb_width

        if height_str:
            display_height = float(height_str.replace('px', ''))
        else:
            display_height = vb_height
        
        ''' Calculate scale factors '''
        scale_x = display_width / vb_width
        scale_y = display_height / vb_height

        if print_output==True:
            print(f"✓ SVG viewBox: x={vb_x}, y={vb_y}, width={vb_width}, height={vb_height}")
            print(f"✓ SVG display dimensions: width={display_width}, height={display_height}")
            print(f"✓ Scale factors: scale_x={scale_x}, scale_y={scale_y}")
        else:
            pass

        return {
            'display_width': display_width,
            'display_height': display_height,
            'viewbox_width': vb_width,
            'viewbox_height': vb_height,
            'scale_x': scale_x,
            'scale_y': scale_y
        }
    
    def extract_ScoreSVG_dimensions(self, svg_file: str, print_output: bool = False):

        svg_tree = ET.parse(svg_file)
        root = svg_tree.getroot()
        ns = {'svg': 'http://www.w3.org/2000/svg'}

        ''' Get viewBox from root or nested SVG '''
        viewbox = root.get('viewBox')
        if not viewbox:
            ''' Look for viewBox in nested SVG elements '''
            nested_svg = root.find(".//svg:svg", ns)
            if nested_svg is not None:
                viewbox = nested_svg.get('viewBox')
        
        vb_parts = viewbox.split()
        dimensions = list(map(float, vb_parts))
        score_width = dimensions[2]
        score_height = dimensions[3]

        if print_output==True:
            print(f"Score segment WIDTH: {score_width} ")
            print(f"Score segment HEIGHT: {score_height} ")

        return score_width, score_height
    
    def scale_Factor(self, score_svg_file: str, print_output: bool = False):
        ''' Calculate scale factor between score SVG dimensions and PNG dimensions '''
        svg_dims = self.extract_ScoreSVG_dimensions(score_svg_file, print_output)
        score_width = svg_dims[0]
        score_height = svg_dims[1]

        ''' Get actual SVG display dimensions '''
        viewbox_dims = self.extract_viewBox_dimensions(score_svg_file, print_output)
        svg_true_width = viewbox_dims['display_width']
        svg_true_height = viewbox_dims['display_height']

        scale_x = score_width / svg_true_width
        scale_y = score_height / svg_true_height
        scale_factor=(scale_x, scale_y)

        if print_output:
            print(f"✓ Scale factor calculated: scale_x={scale_x}, scale_y={scale_y}")
        
        return  scale_factor
    

    def get_first_and_last_note_positions(self, svg_file: str, maps_file: str, print_output: bool = False):
        ''' Retrieve the x1 attribute (timeline begin) from the first note and last note in SVG using maps file for reference '''
        if svg_file is None or maps_file is None:
            print("✗ valid svg_file and maps_file must be provided")
            return None
    
        tree = ET.parse(svg_file)
        root = tree.getroot()
        
        # Load maps data
        with open(str(maps_file), 'r') as f:
            maps = json.load(f)
        
        first_note_id = maps[0].get('xml_id')
        last_note_id = maps[-1].get('xml_id')
        
        ''' Look up the actual x position in the SVG using xml_id, finding use element inside note '''
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        first_element = root.find(f".//*[@data-id='{first_note_id}']//svg:use", ns)
        last_element = root.find(f".//*[@data-id='{last_note_id}']//svg:use", ns)
        
        if first_element is None or last_element is None:
            print(f"✗ Could not find use elements with ids: {first_note_id}, {last_note_id}")
            return None
        
        first_note_x = float(first_element.get('x', 0))
        last_note_x = float(last_element.get('x', 0))
        
        score_timeline_length = last_note_x - first_note_x

        if print_output == True:
            print(f"First note id: {first_note_id}, Last note id: {last_note_id}")
            print(f"First note x1: {first_note_x}, Last note x1: {last_note_x}")
            print(f"Score timeline length: {score_timeline_length}")

        return first_note_x, last_note_x, score_timeline_length
    
    def get_first_and_last_onsets(self, maps_file: str, print_output: bool = False):
        # Retrieve the first and last onset times from the maps file
        with open(str(maps_file), 'r') as f:
            data = json.load(f)  

        # Scorewarp offestes the first onset by it's time.
        first_onset = data[0].get('obs_mean_onset') - data[0].get('obs_mean_onset') 
        last_onset = data[-1].get('obs_mean_onset') - data[0].get('obs_mean_onset')

        if print_output == True:
            print(f"✓ First onset time: {first_onset}, Last onset time: {last_onset}")
        
        return first_onset, last_onset

    
    def crop_png(self, maps_file: str = None, png_file: str = None, audio_file: str = None, print_output: bool = False) -> Optional[str]:
        # crops the png so that the spectrogram corresponds to the first and last onsets.

        last_onset_time = self.get_first_and_last_onsets(maps_file, print_output)[1]
        png_img = Image.open(png_file)
        png_width, png_height = png_img.size

        #  Calculate time per pixel
        audio_data, samplerate = soundfile.read(audio_file)
        audio_duration = len(audio_data) / samplerate
        time_per_pixel = png_width/audio_duration
        
        #Calculate the pixel of last onset
        last_onset_pixel = int(time_per_pixel * last_onset_time)

        cropped_img = png_img.crop((0, 0, last_onset_pixel, png_height))

        # Save cropped PNG to output folder 
        root_dir = Path(__file__).parent.parent.parent
        output_dir = root_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / "cropped_png.png")
        
        cropped_img.save(output_path)
        
        return output_path
    
    def Allign_Score_and_PNG(self, png_plot: str, svg_image: str, maps_json_file: str, print_output: bool = False) -> bool:
    
        ''' Get timeline positions: start, end, and length '''
        start_and_width = self.get_first_and_last_note_positions(svg_image, maps_json_file, print_output)
        plot_begin = start_and_width[0]
        timeline_length = start_and_width[2]
        
        #check plot width and height
        png_img = Image.open(png_plot)
        png_width, png_height = png_img.size

        ''' Parse SVG file to use as base '''
        svg_tree = ET.parse(svg_image)
        composite_svg = svg_tree.getroot()
        
        # Get Actual Score segment Dimensions
        scoreSegment_dims = self.extract_ScoreSVG_dimensions(svg_image)
        scoreSegment_width = scoreSegment_dims[0]
        scoreSegment_height = scoreSegment_dims[1]
        

        ''' Register namespace '''
        svg_ns = 'http://www.w3.org/2000/svg'
        ET.register_namespace('', svg_ns)

        ''' Embed PNG as base64 '''
        png_buffer = io.BytesIO()
        png_img.save(png_buffer, format='PNG')
        png_base64 = base64.b64encode(png_buffer.getvalue()).decode('utf-8')

        # This tells the parser: "all elements in this document follow the SVG standard." 
        # It ensures there's no confusion if you mix SVG with other XML formats.
        ns = {'svg': 'http://www.w3.org/2000/svg'}
        
        # Inside:   class='definition-scale'
        # Find the <g> element with:    class='page-margin' 
        definition_scale = composite_svg.find(".//svg:svg[@class='definition-scale']", ns)
        if definition_scale is None:
            print("✗ Could not find nested <svg> element with class='definition-scale'")
            return False
        page_margin = definition_scale.find(".//svg:g[@class='page-margin']", ns)
        if page_margin is None:
            print("✗ Could not find <g> element with class='page-margin' inside definition-scale")
            return False
        
        # Create PNG image element
        png_image_elem = ET.Element('image', {
            'x': str(plot_begin),
            'y': '0',
            'width': str(timeline_length),
            'height': str(scoreSegment_height),
            'href': f'data:image/png;base64,{png_base64}'
        })
        
        ''' Insert PNG as first child of page-margin '''
        page_margin.insert(0, png_image_elem)

        ''' Save composite SVG '''
        root_dir = Path(__file__).parent.parent.parent
        sys.path.insert(0, str(root_dir))
        output_dir = root_dir / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = str(output_dir / "composite.svg")
        
        composite_tree = ET.ElementTree(composite_svg)
        composite_tree.write(output_path, encoding='UTF-8', xml_declaration=True)
        
        print(f"✓ Composite SVG created: {output_path}")
        return True

    def combine_AllignedScore_with_Layers(self, filename: str, alligned_svg: str, layers_svg: str, scale_factor: tuple, print_output: bool = False):
        ''' Combine aligned score SVG with visualization layers from TurnLayersIntoSVG '''
        try:
            ''' Parse both SVG files '''
            aligned_tree = ET.parse(alligned_svg)
            aligned_root = aligned_tree.getroot()
            
            layers_tree = ET.parse(layers_svg)
            layers_root = layers_tree.getroot()
            
            ''' Define SVG namespace '''
            svg_ns = 'http://www.w3.org/2000/svg'
            ns = {'svg': svg_ns}
            
            ''' Find the page-margin group in the aligned SVG '''
            definition_scale = aligned_root.find(".//svg:svg[@class='definition-scale']", ns)
            if definition_scale is None:
                print("✗ Could not find nested <svg> element with class='definition-scale'")
                return False
            
            page_margin = definition_scale.find(".//svg:g[@class='page-margin']", ns)
            if page_margin is None:
                print("✗ Could not find <g> element with class='page-margin'")
                return False
            
            ''' Extract all layer groups from the layers SVG '''
            layer_groups = layers_root.findall(".//svg:g", ns)
            
            if len(layer_groups) > 0:
                ''' Insert layer groups after the PNG (starting at index 1) '''
                for i, layer_group in enumerate(layer_groups):
                    ''' Deep copy the layer group to avoid modifying the original tree '''
                    layer_copy = ET.fromstring(ET.tostring(layer_group))
                    ''' Apply scale transform to layer group '''
                    current_transform = layer_copy.get('transform', '')
                    new_transform = f"scale({scale_factor[0]}, {scale_factor[1]}) {current_transform}".strip()
                    layer_copy.set('transform', new_transform)
                    page_margin.insert(1 + i, layer_copy)
                if print_output:
                    print(f"✓ Added {len(layer_groups)} layer groups to the aligned SVG")
                    print(f"✓ Scale factors applied: scale_x={scale_factor[0]}, scale_y={scale_factor[1]}")
            else:
                if print_output:
                    print("⚠ Warning: No layer groups found in layers SVG")
            
            ''' Save the combined SVG to output folder '''
            root_dir = Path(__file__).parent.parent.parent
            output_dir = root_dir / "output"
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = str(output_dir / filename)
            
            aligned_tree.write(output_path, encoding='UTF-8', xml_declaration=True)
            
            if print_output:
                print(f"✓ Combined SVG created: {output_path}")
            return True
            
        except Exception as e:
            print(f"✗ Error combining SVG files: {e}")
            return False

