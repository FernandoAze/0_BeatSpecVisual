import sys
from pathlib import Path
import json

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))
input_parent_dir = str("src/input_files/PARTITURAS_MEI")

from src.functions.warp_score import Warp_Score

WS = Warp_Score()

# Define input file paths 

svg_score = str(root_dir / input_parent_dir / "Chopin_Op10_3_1.mei-Chopin_op10_no3_p01-mei.maps.json.svg")
mapJson = str(root_dir / input_parent_dir / "Chopin_op10_no3_p01-mei.maps.json")

# element_id2="zybwlzz"
# WS.get_translate_value(svg_score, element_id2, True)

# WS.get_FirstLast_NoteID(mapJson, True)

WS.get_LastTranslation(svg_score, mapJson, True)
