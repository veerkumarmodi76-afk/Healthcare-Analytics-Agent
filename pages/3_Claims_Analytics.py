from pathlib import Path
from runpy import run_path

PAGE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "dashboard"
    / "pages"
    / "3_Claims_Analytics.py"
)

run_path(str(PAGE), run_name="__main__")
