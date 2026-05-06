import sys
from pathlib import Path
from unittest import loader

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions.Load_Files import LoadFiles

from src.functions.warp_score import  Warp_Score_Layer

Loader=LoadFiles()
Loader.load_maps(str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_op10_no3_p01-mei.maps.json"))  # Load maps file (score alignment data)
Loader.load_score(str(root_dir / "src/input_files/PARTITURAS_MEI/Chopin_Op10_3_1.mei-Chopin_op10_no3_p01-mei.maps.json.svg"))  # Load score file (score data)
# Warp_Score_Layer().Retrieve_First_Onset()
Warp_Score_Layer().get_Timeline_Length()