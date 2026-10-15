"""Align existing decision alternatives without additional model calls."""
from __future__ import annotations
import json


def _text(value) -> str:
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def compare_decisions(decisions: list[dict]) -> dict:
    if not 2 <= len(decisions) <= 12:
        raise ValueError("Choose 2 to 12 decisions to compare")
    if any(not isinstance(item, dict) for item in decisions):
        raise ValueError("Each decision must be an object")
    alternatives, departments = [], []
    for index, decision in enumerate(decisions):
        reports = {}
        for report in decision.get("dept_reports") or []:
            if not isinstance(report, dict):
                continue
            name = str(report.get("dept") or "未命名部门")
            text = _text(report.get("summary") or report.get("report") or report.get("content") or report)
            reports[name] = (reports[name] + "\n\n" + text) if name in reports else text
            if name not in departments:
                departments.append(name)
        alternatives.append({"label": decision.get("label") or f"方案 {index + 1}",
            "decision_id": decision.get("decision_id"), "task": decision.get("task", ""),
            "conclusion": _text(decision.get("ceo_decision", "")), "departments": reports})
    rows = []
    for name in departments:
        texts = [item["departments"].get(name) for item in alternatives]
        rows.append({"department": name, "opinions": texts,
            "same_text": all(text is not None for text in texts) and len(set(texts)) == 1})
    md = ["# 多方案对照", ""]
    for item in alternatives:
        md.extend([f"## {item['label']}", str(item["task"]), "", item["conclusion"], ""])
    for row in rows:
        md.extend([f"## 部门：{row['department']}", ""])
        for item, opinion in zip(alternatives, row["opinions"]):
            md.extend([f"### {item['label']}", opinion if opinion is not None else "此方案没有该部门结果。", ""])
    return {"alternatives": alternatives, "department_comparison": rows, "markdown": "\n".join(md)}
