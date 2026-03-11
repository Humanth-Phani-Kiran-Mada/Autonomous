#!/usr/bin/env python
"""Remove all escaped quotes in src/ files"""

import os
import glob
from pathlib import Path

src_dir = Path(r"c:\Users\hphaniki\Downloads\Autonomous\src")

# Process all .py files in src/
for filepath in glob.glob(str(src_dir / "*.py")):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        original = content
        # Replace escaped quotes
        content = content.replace(r'\"\"\"', '"""')
        content = content.replace(r'\"', '"')
        content = content.replace(r"\'", "'")
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {Path(filepath).name}")
        else:
            print(f"   {Path(filepath).name} (no changes)")
    except Exception as e:
        print(f"⚠️ Error processing {Path(filepath).name}: {e}")

print("\n✅ All escaped quote fixes completed!")
