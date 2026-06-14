import sys
from pathlib import Path

# Add parent directory to path so we can import src
script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions.warp_score import TXT_to_Maps

TXT_to_Maps("/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV856/marta.txt", "/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV856/marta.maps.json")

TXT_to_Maps("/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV856/glenn.txt", "/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV856/glenn.maps.json")

TXT_to_Maps("/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV856/andras.txt", "/home/macacomalandro/Documents/GitHub/0_BeatSpecVisual/src/input_files/BWV856/andras.maps.json")