#!/usr/bin/env python
"""Fix all imports from src.*  to . in src/ directory files"""

import os
import glob
from pathlib import Path

src_dir = Path(r"c:\Users\hphaniki\Downloads\Autonomous\src")
os.chdir(src_dir)

# List of files that need fixing
files_to_fix = [
    "autonomous_goal_generator.py",
    "bayesian_reasoner.py",
    "error_recovery.py",
    "introspection_engine.py",
    "knowledge_base.py",
    "learning_engine.py",
    "memory_consolidation.py",
    "memory_manager.py",
    "meta_learner.py",
    "self_model.py",
    "web_crawler.py"
]

for filename in files_to_fix:
    filepath = src_dir / filename
    if filepath.exists():
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Replace all "from src." with "from ."
            original = content
            content = content.replace('from src.', 'from .')
            content = content.replace('import src.', 'import ')
            
            # Also fix escaped quotes that might be there
            content = content.replace(r'\"\"\"', '"""')
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed {filename}")
            else:
                print(f"   {filename} (no changes needed)")
        except Exception as e:
            print(f"⚠️ Error fixing {filename}: {e}")
    else:
        print(f"❌ {filename} not found")

print("\n✅ All import fixes completed!")
