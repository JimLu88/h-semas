"""Compare exported decisions locally; does not start the application."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.decision_compare import compare_decisions

parser = argparse.ArgumentParser(description="把多个导出的决策结果按部门对齐")
parser.add_argument("inputs", nargs="+", type=Path)
parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
args = parser.parse_args()
result = compare_decisions([json.loads(path.read_text(encoding="utf-8-sig")) for path in args.inputs])
print(result["markdown"] if args.format == "markdown" else json.dumps(result, ensure_ascii=False, indent=2))
