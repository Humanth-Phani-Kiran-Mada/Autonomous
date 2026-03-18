# Using VS Code for Project Reorganization

**Goal**: Use VS Code to efficiently complete remaining reorganization phases.

---

## 🚀 Getting Started with VS Code

### Step 1: Open Project in VS Code

**Option A: Command Line**
```bash
# Navigate to project
cd c:\Users\human\Downloads\Project\Autonomous

# Open in VS Code
code .
```

**Option B: VS Code GUI**
1. Open VS Code
2. File → Open Folder
3. Select: `c:\Users\human\Downloads\Project\Autonomous`

### Step 2: Verify Structure

**You should see in Explorer (left sidebar)**:
```
📁 Autonomous
├── 📁 src/
│   ├── 📁 core/
│   ├── 📁 advanced/
│   ├── 📁 infrastructure/
│   ├── 📁 integration/
│   └── 📁 utils/
├── 📁 docs/
├── 📁 tests/
├── 📁 config/
├── 📁 scripts/
└── 📝 README.md
```

---

## 📂 Phase 1: Move Source Code Files (Using VS Code)

### Method 1: Drag & Drop (Easiest)

1. **Expand `src/` in Explorer**
   - See all flat Python files

2. **Identify core modules** (these 7 go to `src/core/`):
   - `web_crawler.py`
   - `knowledge_base.py`
   - `memory_manager.py`
   - `learning_engine.py`
   - `reasoning_engine.py`
   - `autonomous_agent.py`
   - `logger.py`

3. **Right-click each file** → Cut (or Ctrl+X)

4. **Go to `src/core/`** → Paste (Ctrl+V)

---

### Method 2: Multi-Select & Move

1. **Ctrl+click** to select multiple files in `src/`
   - Select the 7 core files above

2. **Right-click** → Cut

3. **Open `src/core/`**

4. **Paste**: Right-click → Paste (or Ctrl+V)

---

### Method 3: File Command Palette

**For each file**:

1. Open file in editor (Ctrl+P, type filename)
2. Ctrl+Shift+P (Command Palette)
3. Type: "File: Reveal in File Explorer"
4. Cut/Paste to new location

---

## 🔄 Phase 2: Update Imports (Most Efficient in VS Code)

This is where **VS Code shines** with Find & Replace!

### Step 1: Open Find & Replace

```
Ctrl+H  (or Cmd+Shift+H on Mac)
```

You'll see a two-panel interface:
- **Top**: Find
- **Bottom**: Replace

### Step 2: Replace All Web Crawler Imports

**In Find box**:
```
from src.web_crawler import
```

**In Replace box**:
```
from src.core.web_crawler import
```

**Then click**: Replace All (Ctrl+Alt+Enter)

✅ All imports updated instantly!

---

### Step 3: Repeat for Other Imports

**Knowledge Base**:
- Find: `from src.knowledge_base import`
- Replace: `from src.core.knowledge_base import`

**Memory Manager**:
- Find: `from src.memory_manager import`
- Replace: `from src.core.memory_manager import`

**Learning Engine**:
- Find: `from src.learning_engine import`
- Replace: `from src.core.learning_engine import`

**Reasoning Engine**:
- Find: `from src.reasoning_engine import`
- Replace: `from src.core.reasoning_engine import`

**Logger**:
- Find: `from src.logger import`
- Replace: `from src.infrastructure.logger import`

---

### Step 4: Advanced Engines

For the 20+ advanced modules:

**Pattern**:
- Find: `from src.adaptive_reasoning_engine import`
- Replace: `from src.advanced.adaptive_reasoning_engine import`

**Do this for each advanced module**:
```
attention_system.py
bayesian_reasoner.py
capability_expansion_engine.py
evolutionary_decision_engine.py
meta_learner.py
[... etc]
```

---

### Step 5: Infrastructure Components

```
Find: from src.exceptions import
Replace: from src.infrastructure.exceptions import

Find: from src.validators import
Replace: from src.infrastructure.validators import

Find: from src.utilities import
Replace: from src.infrastructure.utilities import

Find: from src.types_and_constants import
Replace: from src.infrastructure.types_and_constants import
```

---

### Pro Tip: Use Regex for Pattern Matching

1. Click the **`.*`** button (regex mode) in Find & Replace
2. Use regex patterns:

```
Find: from src\.([a-z_]+) import
Replace: from src.core.$1 import
```

This matches all imports and can bulk-replace patterns!

---

## 🧪 Phase 3: Update Tests (Quick in VS Code)

### Move Test Files to tests/

1. **In Explorer**:
   - Expand root directory
   - Find: `test_*.py` files in root

2. **For each test file**:
   - Right-click → Cut
   - Navigate to: `tests/unit/` or `tests/integration/`
   - Right-click → Paste

### Update Test Imports

Same as application imports:
```
Find: from src.web_crawler import
Replace: from src.core.web_crawler import
```

Run in test files (should have same imports).

---

## 🔧 Phase 4: Run Tests (VS Code Terminal)

### Open Terminal

```
Ctrl+` (backtick)
```

Or: View → Terminal

### Run All Tests

```bash
pytest tests/ -v
```

**If you see errors**, click on error → Jump to file automatically!

### Run Specific Test File

```bash
pytest tests/unit/test_core/test_knowledge_base.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

---

## ✨ Phase 5: Check Type Safety (In VS Code)

### Setup Mypy Extension

1. **Install Mypy extension**:
   - Ctrl+Shift+X (Extensions)
   - Search: "Python: mypy"
   - Install

2. **Enable for project**:
   - Ctrl+, (Settings)
   - Search: "mypy"
   - Enable mypy checking

3. **See errors as you code**:
   - Red squiggles show type errors
   - Hover for details

### Run Type Check

```bash
# In VS Code Terminal
mypy src/ --config-file=mypy.ini
```

---

## 🎨 Phase 6: Format Code (In VS Code)

### Setup Black Formatter

1. **Install Black extension**:
   - Ctrl+Shift+X
   - Search: "black"
   - Install

2. **Set as default formatter**:
   - Select Python file
   - Right-click → "Format Document"
   - Select "black"

3. **Auto-format on save**:
   - Ctrl+, (Settings)
   - Search: "format on save"
   - Enable ✓

### Format Selected Code

1. Ctrl+A (select all)
2. Shift+Alt+F (format)

Or:
1. Select lines
2. Right-click → Format Selection

---

## 📝 Phase 7: Update .gitignore (In VS Code)

1. **Open `.gitignore`**:
   - Ctrl+P
   - Type: `.gitignore`
   - Enter

2. **Add new directories**:
   ```
   data/
   logs/
   build/
   dist/
   *.egg-info/
   __pycache__/
   .pytest_cache/
   .mypy_cache/
   .coverage
   htmlcov/
   .env
   ```

3. **Save**: Ctrl+S

---

## 💾 Phase 8: Git Workflow (In VS Code)

### View Git Status

1. **Click Source Control** icon (left sidebar)
   - Or: Ctrl+Shift+G

2. **See all changes**:
   - Green (added files)
   - Modified (changed files)
   - Red (deleted)

### Stage Changes

1. **Stage all**:
   - Click the **+** icon next to "Changes"

2. **Or stage individual files**:
   - Hover over file
   - Click **+** icon

### Create Commit

1. **Type message** in "Message" field at top

2. **Press** Ctrl+Enter (Commit)

---

## 🚀 Complete Reorganization Workflow in VS Code

### Workflow for Completing Phase 1-3 (20 minutes)

```
1. Open project: code .
   
2. Move core files (drag & drop):
   - src/web_crawler.py → src/core/
   - src/knowledge_base.py → src/core/
   - ... (rest of 7 core files)
   
3. Move advanced files:
   - src/adaptive_reasoning_engine.py → src/advanced/
   - ... (all 20+ advanced files)
   
4. Move infrastructure:
   - src/exceptions.py → src/infrastructure/
   - ... (rest)
   
5. Move integration:
   - src/integration_layer.py → src/integration/
   - ... (rest)
   
6. Update imports (Ctrl+H):
   - Find: from src.web_crawler import
   - Replace: from src.core.web_crawler import
   - Replace All
   - Repeat for all modules
   
7. Move test files (drag & drop):
   - test_*.py → tests/unit/ or tests/integration/
   
8. Run tests (Ctrl+`):
   - pytest tests/ -v
   
9. Check types:
   - mypy src/ --config-file=mypy.ini
   
10. Stage & commit:
    - Ctrl+Shift+G (Git)
    - Add message
    - Ctrl+Enter (Commit)
    - Ctrl+Shift+P → Git: Push
```

---

## 🎯 VS Code Extensions Recommended

### Install These Extensions

**In VS Code**:
1. Ctrl+Shift+X (Extensions)
2. Search & install:

**Essential**:
- **Python** (Microsoft) - Python support
- **Pylance** - IntelliSense for Python
- **Black** - Code formatter
- **Flake8** - Linter
- **Mypy** - Type checker
- **Pytest** - Test runner

**Optional but helpful**:
- **GitLens** - Git integration
- **Thunder Client** - API testing
- **YAML** - YAML support
- **Markdown Preview Enhanced** - Better markdown viewing

### Quick Install Command

In Terminal (Ctrl+`):
```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker
code --install-extension littlefoxteam.vscode-python-test-adapter
```

---

## 💡 VS Code Pro Tips for Reorganization

### Tip 1: Multi-Cursor Editing

**Select multiple instances**:
1. Find a word
2. Ctrl+D (select word)
3. Ctrl+D again (select next occurrence)
4. Type to replace all selected ✨

### Tip 2: Command Palette

```
Ctrl+Shift+P (all commands)
```

Useful commands:
- "File: Delete"
- "File: Move"
- "File: Rename"
- "Git: Commit"
- "Git: Push"
- "Python: Run All Tests"

### Tip 3: Quick File Opening

```
Ctrl+P (Quick Open)
```

Type filename instantly jump to it.

### Tip 4: Folder Drag & Drop

Drag folders in Explorer to reorganize multiple files at once.

### Tip 5: Split Editor

```
Ctrl+\ (Open file in split view)
```

Edit imports on left, see original on right!

---

## 🔍 Finding Issues Fast

### Error Lens Extension

1. Install "Error Lens"
2. See errors inline as you code
3. Hover for fix suggestions

### Problems Panel

```
Ctrl+Shift+M (Problems)
```

See all errors/warnings in project.

---

## 📊 Troubleshooting in VS Code

### "Import not resolved" Errors

**VS Code thinks imports are wrong?**

Solution:
1. Ctrl+, (Settings)
2. Search: "python path"
3. Make sure Python interpreter is selected
4. Ctrl+Shift+P → "Python: Select Interpreter"
5. Choose your venv

### Tests Won't Run

**In Terminal**:
```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Then run tests
pytest tests/ -v
```

### Find & Replace Not Working

**Make sure**:
1. You're searching in the right files
2. Click "..." menu in Find & Replace
3. Include/Exclude patterns if needed
4. Check "Match Whole Word" isn't enabled

---

## 🎬 Step-by-Step Reorganization Demo

### Complete Example: Moving 1 File + Updating Imports

**1. Move web_crawler.py**:
```
In Explorer:
src/web_crawler.py
→ Right-click → Cut
→ Go to src/core/
→ Right-click → Paste
```

**2. Update all imports**:
```
Ctrl+H (Find & Replace)

Find:    from src.web_crawler import
Replace: from src.core.web_crawler import

Click: Replace All (Ctrl+Alt+Enter)
```

**3. Verify**:
```
Ctrl+` (Terminal)
pytest tests/ -v
```

---

## ✅ Checklist for Using VS Code

- [ ] Open project in VS Code
- [ ] Install recommended extensions
- [ ] Move core files using Explorer
- [ ] Update imports using Find & Replace
- [ ] Move test files
- [ ] Update test imports
- [ ] Run tests in Terminal
- [ ] Check types (mypy)
- [ ] Format code (Black)
- [ ] Use Git pane to stage & commit
- [ ] Verify everything in GitHub

---

## 🚀 Next Actions

1. **Start VS Code**:
   ```bash
   code c:\Users\human\Downloads\Project\Autonomous
   ```

2. **Install extensions** (2 min)

3. **Move core files** (5 min):
   - Drag & drop from src/ to src/core/

4. **Update imports** (5 min):
   - Ctrl+H for each module

5. **Move test files** (3 min):
   - Drag & drop to tests/

6. **Run tests** (2 min):
   - Ctrl+`, then `pytest tests/ -v`

7. **Commit changes** (3 min):
   - Ctrl+Shift+G, type message, Ctrl+Enter

**Total time: ~25 minutes!**

---

## 📞 VS Code Resources

- **Official Docs**: https://code.visualstudio.com/docs
- **Python Guide**: https://code.visualstudio.com/docs/languages/python
- **Git Support**: https://code.visualstudio.com/docs/sourcecontrol/overview
- **Extensions Search**: https://marketplace.visualstudio.com/

---

**Ready to reorganize in VS Code?** 🎯  
Open it now: `code .`  

VS Code will make this process super fast! ✨

