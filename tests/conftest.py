import sys
from pathlib import Path

# Ensure src directory is on path
src_path = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(src_path))
