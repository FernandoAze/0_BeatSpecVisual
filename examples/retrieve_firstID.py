import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions.Load_Files import LoadFiles

from src.functions.warp_score import  Warp_Score_Layer

loader=LoadFiles()
loader.load_maps(str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01-mei.maps.json"))  # Load maps file (score alignment data)

Warp_Score_Layer().Retrieve_First_Onset()
