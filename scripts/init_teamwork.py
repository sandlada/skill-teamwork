#!/usr/bin/env python3
"""
Initialize the .teamwork/ runtime directory structure for a project.
Usage:
    python init_teamwork.py [--target-dir <path>] [--path <general|iterative|review|math|large_math>]
"""

import argparse
import os
import sys

def init_teamwork(target_dir: str, execution_path: str = "general"):
    teamwork_dir = os.path.join(target_dir, ".teamwork")
    scratch_dir = os.path.join(teamwork_dir, "scratch")
    knowledge_dir = os.path.join(teamwork_dir, "knowledge")

    os.makedirs(teamwork_dir, exist_ok=True)
    os.makedirs(scratch_dir, exist_ok=True)

    if "math" in execution_path.lower():
        os.makedirs(knowledge_dir, exist_ok=True)
        pitfalls_file = os.path.join(knowledge_dir, "pitfalls.md")
        if not os.path.exists(pitfalls_file):
            with open(pitfalls_file, "w", encoding="utf-8") as f:
                f.write("# Pitfall Registry\n\nDocument failed approaches and invalid lemmas here.\n")

    # Template brief
    brief_file = os.path.join(teamwork_dir, "brief.md")
    if not os.path.exists(brief_file):
        with open(brief_file, "w", encoding="utf-8") as f:
            f.write(f"""# Project Brief

- **Project Path**: {execution_path}
- **Integrity Mode**: development
- **Speed Knobs**: workers=default, team=default, deep=on
- **Target Working Directory**: {os.path.abspath(target_dir)}

## Objectives
- 

## Requirements
- 

## Acceptance Criteria
- 
""")

    print(f"[OK] Initialized .teamwork layout at: {teamwork_dir}")

def main():
    parser = argparse.ArgumentParser(description="Initialize .teamwork workspace")
    parser.add_argument("--target-dir", default=".", help="Target project directory")
    parser.add_argument("--path", default="general", choices=["general", "iterative", "review", "math", "large_math"], help="Execution path")
    args = parser.parse_args()

    init_teamwork(args.target_dir, args.path)

if __name__ == "__main__":
    main()
