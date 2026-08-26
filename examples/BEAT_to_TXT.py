import sys
from pathlib import Path

script_dir = Path(__file__).parent
root_dir = script_dir.parent
sys.path.insert(0, str(root_dir))

from src.functions import NPZ_to_BeatTXT, NPZ_to_DownbeatTXT

beat_file = str(root_dir / "src/input_files/ClairDeLune/Clair_Beat.npz")

NPZ_to_BeatTXT(beat_file, print_output=True)
NPZ_to_DownbeatTXT(beat_file, print_output=True)
