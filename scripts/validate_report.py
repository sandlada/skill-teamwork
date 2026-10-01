#!/usr/bin/env python3
"""
Validate the report block output from a subagent according to roles/shared/base.md.
Usage:
    python validate_report.py <path_to_report_or_log_file>
    cat output.txt | python validate_report.py -
"""

import sys
import re

REPORT_PATTERN = re.compile(
    r"verdict:\s*(pass|fail|blocked)\s*\n"
    r"findings:\s*(.+?)\s*\n"
    r"evidence:\s*(.+?)\s*\n"
    r"blockers:\s*(.+?)\s*\n"
    r"artifacts written:\s*(.+?)(?:\n|$)",
    re.DOTALL | re.IGNORECASE
)

def validate_text(text: str) -> bool:
    match = REPORT_PATTERN.search(text)
    if not match:
        print("[FAIL] Missing or invalid report block structure.")
        print("Expected format:")
        print("verdict: pass | fail | blocked")
        print("findings: <findings>")
        print("evidence: <exact commands + output, artifact paths>")
        print("blockers: <blockers or 'none'>")
        print("artifacts written: <artifacts>")
        return False

    verdict, findings, evidence, blockers, artifacts = match.groups()
    verdict = verdict.strip().lower()

    if verdict not in ["pass", "fail", "blocked"]:
        print(f"[FAIL] Invalid verdict: '{verdict}'. Must be pass, fail, or blocked.")
        return False

    # Evidence check
    evidence_str = evidence.strip()
    if not evidence_str or len(evidence_str) < 5:
        print("[FAIL] Evidence block is too sparse or empty. Concrete evidence is required.")
        return False

    print(f"[PASS] Valid report block detected. Verdict: {verdict.upper()}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_report.py <file_or_dash>")
        sys.exit(1)

    target = sys.argv[1]
    if target == "-":
        content = sys.stdin.read()
    else:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

    success = validate_text(content)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
