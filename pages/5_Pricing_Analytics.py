from pathlib import Path
from runpy import run_path

PAGE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "dashboard"
    / "pages"
    / "5_Pricing_Analytics.py"
)

run_path(str(PAGE), run_name="__main__")
