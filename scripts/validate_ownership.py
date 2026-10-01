#!/usr/bin/env python3
"""
Verify exclusive file ownership across tracks within the same milestone in plan.md.
Usage:
    python validate_ownership.py <path_to_plan.md>
"""

import sys
import os
import re
from collections import defaultdict

def check_exclusive_ownership(plan_content: str):
    # Split by Milestone
    milestones = re.split(r"(?m)^##\s+Milestone\s+", plan_content)
    has_conflict = False

    for idx, ms in enumerate(milestones[1:], 1):
        lines = ms.splitlines()
        ms_title = lines[0].strip() if lines else f"#{idx}"
        
        # Parse tracks and their files
        # Look for tracks like: ### Track: <name> or - Track <name>:
        tracks = re.split(r"(?m)^###\s+Track:\s+", ms)
        if len(tracks) <= 1:
            continue
            
        file_to_tracks = defaultdict(list)
        for t_idx, track_content in enumerate(tracks[1:], 1):
            t_lines = track_content.splitlines()
            track_name = t_lines[0].strip() if t_lines else f"Track {t_idx}"
            
            # Find assigned files block
            in_assigned = False
            for line in t_lines:
                line_strip = line.strip()
                if re.match(r"(?i)^Assigned files.*:", line_strip) or re.match(r"(?i)^Files.*:", line_strip):
                    in_assigned = True
                    continue
                if in_assigned:
                    if line_strip.startswith("-"):
                        fpath = line_strip.lstrip("-").strip()
                        # normalize path
                        if fpath and fpath.lower() != "read-only":
                            file_to_tracks[fpath].append(track_name)
                    elif line_strip.startswith("#") or line_strip == "":
                        in_assigned = False

        # Check collisions
        for fpath, assigned_tracks in file_to_tracks.items():
            if len(assigned_tracks) > 1:
                has_conflict = True
                print(f"[CONFLICT] In Milestone '{ms_title}': File '{fpath}' is assigned to multiple tracks: {assigned_tracks}")

    if not has_conflict:
        print("[PASS] Exclusive file ownership verified. No overlaps found within milestones.")
        return True
    else:
        print("[FAIL] Exclusive file ownership violated!")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Verify exclusive file ownership in plan.md")
    parser.add_argument("plan_file", help="Path to plan.md")
    args = parser.parse_args()

    if not os.path.exists(args.plan_file):
        print(f"File not found: {args.plan_file}")
        sys.exit(1)

    with open(args.plan_file, "r", encoding="utf-8") as f:
        content = f.read()

    success = check_exclusive_ownership(content)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
