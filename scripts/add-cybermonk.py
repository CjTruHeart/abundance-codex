#!/usr/bin/env python3
"""Add CyberMonk as AI Co-Creative Partner to all Abundance Codex entries.

Updates:
1. YAML frontmatter: adds co_creative_partner: "CyberMonk" after co_author_human
2. Governance section: updates Curator line to include CyberMonk

Idempotent — safe to run multiple times.
"""

import os
import re
import sys

DOMAINS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "domains")

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    modified = False

    # 1. Add co_creative_partner to YAML frontmatter
    if 'co_creative_partner:' not in content:
        # Insert after co_author_human line
        pattern = r'(co_author_human:\s*"[^"]*"\n)'
        replacement = r'\1co_creative_partner: "CyberMonk"\n'
        new_content = re.sub(pattern, replacement, content, count=1)
        if new_content != content:
            content = new_content
            modified = True

    # 2. Update Governance Curator line
    if 'CyberMonk' not in content.split('Curator')[1] if 'Curator' in content else True:
        # Match: co-created (Cj TruHeart + Claude Opus 4.6)
        old_curator = 'co-created (Cj TruHeart + Claude Opus 4.6)'
        new_curator = 'co-created (Cj TruHeart + Claude Opus 4.6 + CyberMonk)'
        if old_curator in content and new_curator not in content:
            content = content.replace(old_curator, new_curator)
            modified = True

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return modified

def main():
    modified_count = 0
    total_count = 0

    for root, dirs, files in os.walk(DOMAINS_DIR):
        dirs.sort()
        for fname in sorted(files):
            if fname.endswith(".md"):
                total_count += 1
                filepath = os.path.join(root, fname)
                if process_file(filepath):
                    modified_count += 1
                    print(f"  ✓ {os.path.relpath(filepath, os.path.dirname(DOMAINS_DIR))}")
                else:
                    print(f"  — {os.path.relpath(filepath, os.path.dirname(DOMAINS_DIR))} (already up to date)")

    print(f"\nTotal: {total_count} files, {modified_count} modified")
    return 0

if __name__ == "__main__":
    sys.exit(main())
