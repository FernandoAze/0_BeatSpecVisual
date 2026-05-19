import json
import os
from pathlib import Path


def txt_to_maps_json(txt_file_path, output_dir=None):
    '''
    Convert a .txt file to a .maps.json file
    
    The .txt file should have tab-separated values:
    - Column 1: onset time (float)
    - Column 2: xml_id(s) (comma-separated if multiple)
    
    Each xml_id gets its own entry in the JSON with:
    - xml_id: identifier from the txt file
    - obs_mean_onset: onset time
    - obs_num: sequential number starting from 1.0
    
    Args:
        txt_file_path (str): Path to the input .txt file
        output_dir (str): Directory to save the .maps.json file. If None, uses same directory as input file
    
    Returns:
        str: Path to the created .maps.json file
    '''
    txt_path = Path(txt_file_path)
    
    if not txt_path.exists():
        raise FileNotFoundError(f"Input file not found: {txt_file_path}")
    
    if output_dir is None:
        output_dir = txt_path.parent
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    '''Parse the txt file'''
    entries = []
    obs_num = 1.0
    
    with open(txt_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            
            try:
                onset_time = float(parts[0])
                xml_ids = parts[1].split(',')
                
                '''Create an entry for each xml_id'''
                for xml_id in xml_ids:
                    xml_id = xml_id.strip()
                    if xml_id:
                        entry = {
                            "xml_id": xml_id,
                            "obs_mean_onset": onset_time,
                            "obs_num": obs_num
                        }
                        entries.append(entry)
                        obs_num += 1.0
            
            except (ValueError, IndexError):
                continue
    
    '''Write to .maps.json file'''
    output_filename = txt_path.stem + "-mei.maps.json"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w') as f:
        json.dump(entries, f, indent=4)
    
    return str(output_path)


'''Execute the conversion'''
result_path = txt_to_maps_json(txt_file_path  ='/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV-846/annotationLayerPP.txt', 
                               output_dir     ='/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV-846')
print(f"Successfully created: {result_path}")