import json
import numpy as np
from pathlib import Path


class LoadFiles:
    ''' Singleton class for centralized file loading across all layers '''
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data = {}
        return cls._instance
    
    def load_maps(self, maps_file: str) -> bool:
        ''' Load maps file containing score alignment data '''
        try:
            with open(str(maps_file), 'r') as f:
                data = json.load(f)
            
            # Validate maps file structure
            if not isinstance(data, list) or len(data) == 0:
                print("✗ Maps file ERROR: Expected a non-empty array")
                return False
            
            self._data['maps'] = data
            print(f"✓ Loaded maps from {Path(maps_file).name} ({len(data)} entries)")
            return True
        except Exception as e:
            print(f"✗ Error loading maps: {e}")
            return False
    
    def load_beat_data(self, beat_file: str) -> bool:
        ''' Load beat analysis data from .npz file '''
        try:
            data = np.load(str(beat_file))
            self._data['beat_data'] = {
                'beat_times': data['beat_times'],
                'beat_probs': data['beat_probs'],
                'downbeat_probs': data['downbeat_probs'],
                'detected_beats': data.get('detected_beats', np.array([])),
                'detected_downbeats': data.get('detected_downbeats', np.array([])),
            }
            print(f"✓ Loaded beat data from {Path(beat_file).name}")
            return True
        except Exception as e:
            print(f"✗ Error loading beat data: {e}")
            return False
    
    def load_score(self, score_file: str) -> bool:
        ''' Load score file containing score data '''
        try:
            with open(str(score_file), 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, dict) or 'score' not in data:
                print("✗ Score file ERROR: Expected a dictionary with 'score' key")
                return False
            
            self._data['score'] = data['score']
            print(f"✓ Loaded score with {len(data['score'])} entries")
            return True
        except Exception as e:
            print(f"✗ Error loading score: {e}")
            return False
    
    def load_audio(self, audio_file: str) -> bool:
        ''' Load audio file path for later processing '''
        try:
            audio_path = Path(audio_file)
            
            if not audio_path.exists():
                print(f"✗ Audio file not found: {audio_file}")
                return False
            
            self._data['audio_path'] = str(audio_path)
            print(f"✓ Loaded audio file: {audio_path.name}")
            return True
        except Exception as e:
            print(f"✗ Error loading audio: {e}")
            return False
    
    def load_png(self, png_files: list) -> bool:
        ''' Load PNG files containing visualization data '''
        try:
            png_data = []
            for png_file in png_files:
                with open(str(png_file), 'r') as f:
                    data = json.load(f)
                    png_data.append(data)
            
            if not isinstance(png_data, list) or len(png_data) == 0:
                print("✗ PNG files ERROR: Expected a non-empty array of PNG data")
                return False
            
            self._data['pngs'] = png_data
            print(f"✓ Loaded {len(png_data)} PNG files")
            return True
        except Exception as e:
            print(f"✗ Error loading PNG files: {e}")
            return False
    
    def load_svg(self, svg_files: list) -> bool:
        ''' Load SVG files containing visualization data '''
        try:
            svg_data = []
            for svg_file in svg_files:
                with open(str(svg_file), 'r') as f:
                    data = json.load(f)
                    svg_data.append(data)
            
            if not isinstance(svg_data, list) or len(svg_data) == 0:
                print("✗ SVG files ERROR: Expected a non-empty array of SVG data")
                return False
            
            self._data['svgs'] = svg_data
            print(f"✓ Loaded {len(svg_data)} SVG files")
            return True
        except Exception as e:
            print(f"✗ Error loading SVG files: {e}")
            return False
    
    def get_data(self, key: str = None):
        ''' 
        Retrieve loaded data. 
        If key is None, return all data.
        Returns None if key doesn't exist.
        '''
        if key is None:
            return self._data
        return self._data.get(key)
    
    def clear_data(self):
        ''' Clear all loaded data '''
        self._data = {}
        print("✓ Cleared all loaded data")