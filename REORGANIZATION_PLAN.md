# PROJECT REORGANIZATION PLAN
## Self-Evolving Autonomous AI System

**Date**: March 18, 2026  
**Status**: PLANNING PHASE  
**Effort**: 2-3 hours for restructuring

---

## 🔴 CURRENT PROBLEMS

### 1. Root Directory Chaos
- 50+ markdown files scattered
- Duplicate names: `QUICK_START.md`, `QUICKSTART.md`, `QUICK_REFERENCE.md`
- Phase files mixed: `PHASE1_*`, `PHASE_2_*`, `PHASE2_*`, `PHASE4_*`
- No clear organization by topic

### 2. Python Scripts Scattered
- Main code in root: `main.py`, `config.py`
- Test files: both in root and in `tests/` directory
- Utility scripts: `clean_*.py`, `fix_*.py`, `verify*.py`
- No clear runner entry points

### 3. Inconsistent Naming
- Files use UPPERCASE with underscores (legacy)
- Some use lowercase (newer)
- No clear pattern
- Examples:
  - `EXAMPLES_AND_USAGE.py` (should be lowercase)
  - `COMPLETE_START.py` (unclear purpose)
  - `QUICK_START_GUIDE.py` vs `QUICK_START.md`

### 4. Documentation Not Organized
- Getting started docs scattered
- Reference docs mixed with quick starts
- Phase-specific docs not isolated

---

## ✅ PROPOSED NEW STRUCTURE

```
autonomous-ai-system/
│
├── README.md                    # Main project overview
├── requirements.txt             # Dependencies
├── pyproject.toml              # Project metadata (NEW)
├── .gitignore                  # Git ignore
│
├── 📦 src/                      # Source code (core system)
│   ├── __init__.py
│   ├── config.py                # Configuration (moved here)
│   ├── logger.py
│   ├── main.py                  # Main entry point (moved here)
│   │
│   ├── core/                    # Core modules (~7 files)
│   │   ├── __init__.py
│   │   ├── web_crawler.py
│   │   ├── knowledge_base.py
│   │   ├── memory_manager.py
│   │   ├── learning_engine.py
│   │   ├── reasoning_engine.py
│   │   └── autonomous_agent.py
│   │
│   ├── advanced/                # Advanced components (~20+ files)
│   │   ├── __init__.py
│   │   ├── adaptive_reasoning.py
│   │   ├── attention_system.py
│   │   ├── bayesian_reasoner.py
│   │   ├── capability_expansion.py
│   │   ├── evolutionary_decision.py
│   │   ├── meta_learner.py
│   │   └── ... (other advanced modules)
│   │
│   ├── infrastructure/          # System infrastructure
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   ├── validators.py
│   │   ├── utilities.py
│   │   ├── types_and_constants.py
│   │   ├── logger.py
│   │   ├── monitoring.py
│   │   └── health_checker.py
│   │
│   ├── integration/             # Integration layer
│   │   ├── __init__.py
│   │   ├── integration_layer.py
│   │   ├── cycle_coordinator.py
│   │   ├── system_orchestrator.py
│   │   └── component_wrapper.py
│   │
│   └── utils/                   # Utility helpers
│       ├── __init__.py
│       ├── cache.py
│       ├── resource_adapter.py
│       └── distributed_tracing.py
│
├── 📝 docs/                     # Documentation (organized)
│   ├── README.md                # Docs index
│   │
│   ├── getting-started/         # For new users
│   │   ├── 01-quickstart.md     # 5-minute guide
│   │   ├── 02-setup.md          # Detailed setup
│   │   ├── 03-first-run.md      # Your first run
│   │   └── 04-troubleshooting.md
│   │
│   ├── guide/                   # General guides
│   │   ├── architecture.md      # System design
│   │   ├── components.md        # Component reference
│   │   ├── usage.md             # How to use
│   │   └── examples.md          # Usage examples
│   │
│   ├── development/             # For developers
│   │   ├── contributing.md
│   │   ├── code-quality.md
│   │   ├── review-checklist.md
│   │   └── standards.md
│   │
│   └── reference/               # Technical reference
│       ├── api.md
│       ├── configuration.md
│       └── performance.md
│
├── 📋 docs-archive/             # Historical docs (read-only)
│   ├── phase1-complete.md
│   ├── phase2-complete.md
│   ├── phase4-complete.md
│   └── ... (legacy files)
│
├── 🧪 tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest config
│   ├── fixtures/                # Test fixtures
│   │   └── __init__.py
│   │
│   ├── unit/                    # Unit tests
│   │   ├── test_core/
│   │   ├── test_advanced/
│   │   ├── test_infrastructure/
│   │   └── test_utils/
│   │
│   ├── integration/             # Integration tests
│   │   ├── test_system.py
│   │   └── test_workflows.py
│   │
│   └── performance/             # Performance tests
│       └── test_benchmarks.py
│
├── 📊 data/                     # Runtime data (gitignore)
│   ├── cache/
│   ├── knowledge/
│   ├── memory/
│   └── models/
│
├── 📢 logs/                     # Log files (gitignore)
│   ├── system.log
│   └── debug.log
│
├── ⚙️ config/                   # Configuration files
│   ├── default.yaml
│   ├── development.yaml
│   ├── production.yaml
│   └── .env.example
│
├── 🔧 scripts/                  # Utility scripts
│   ├── __init__.py
│   ├── setup.sh
│   ├── setup.bat
│   ├── run_demo.py
│   ├── run_tests.py
│   ├── check_quality.py
│   └── verify_installation.py
│
├── 📦 build/                    # Build artifacts (gitignore)
│   └── dist/
│
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── pyproject.toml               # Modern Python project config
├── setup.py                     # Installation script
├── Makefile                     # Common commands
└── CHANGELOG.md                 # Version history
```

---

## 📋 FILE RENAMING RULES

### 1. **Markdown Documentation Files**
- **Before**: `QUICK_START.md`, `QUICKSTART.md`, `GETTING_STARTED.md`
- **After**: `01-quickstart.md`, `02-setup.md`
- **Rule**: `NN-descriptive-name.md` (numbered for ordering)

### 2. **Python Scripts**
- **Before**: `EXAMPLES_AND_USAGE.py`, `QUICK_START_GUIDE.py`
- **After**: `examples.py`, `quickstart_guide.py`
- **Rule**: `lowercase_with_underscores.py`

### 3. **Main Entry Point**
- **Before**: `main.py` (in root)
- **After**: `src/main.py` (in src/)
- **Rule**: Main executable inside src/ directory

### 4. **Configuration**
- **Before**: `config.py` (in root), `.env` files scattered
- **After**: `src/config.py` + `config/` directory for YAML configs
- **Rule**: Single source of truth in config directory

### 5. **Test Files**
- **Before**: `test_*.py` in root + `tests/`
- **After**: `tests/unit/test_*.py`, `tests/integration/test_*.py`
- **Rule**: Organized by test type in tests/ only

### 6. **Utility Scripts**
- **Before**: `clean_*.py`, `fix_*.py`, `verify*.py` in root
- **After**: `scripts/improve_code_quality.py`, `scripts/verify_setup.py`
- **Rule**: All utilities in scripts/ directory

---

## 🔄 MIGRATION STEPS

### Phase 1: Create Directory Structure
```bash
mkdir -p src/{core,advanced,infrastructure,integration,utils}
mkdir -p docs/{getting-started,guide,development,reference}
mkdir -p docs-archive
mkdir -p tests/{unit,integration,performance,fixtures}
mkdir -p config
mkdir -p scripts
mkdir -p build
```

### Phase 2: Move Source Code
```
src/core/
  ✓ web_crawler.py
  ✓ knowledge_base.py
  ✓ memory_manager.py
  ✓ learning_engine.py
  ✓ reasoning_engine.py
  ✓ autonomous_agent.py

src/advanced/
  ✓ adaptive_reasoning_engine.py
  ✓ attention_system.py
  ✓ bayesian_reasoner.py
  ✓ capability_expansion_engine.py
  ✓ evolutionary_decision_engine.py
  ✓ meta_learner.py
  → (20+ other advanced modules)

src/infrastructure/
  ✓ exceptions.py
  ✓ validators.py
  ✓ utilities.py
  ✓ types_and_constants.py
  ✓ logger.py
  ✓ health_checker.py

src/integration/
  ✓ integration_layer.py
  ✓ cycle_coordinator.py
  ✓ system_orchestrator.py
  ✓ component_wrapper_factory.py
```

### Phase 3: Rename & Move Documentation
```
docs/getting-started/
  ✓ 01-quickstart.md (from QUICKSTART.md)
  ✓ 02-setup.md (from GETTING_STARTED.md)
  ✓ 03-first-run.md (new)
  ✓ 04-troubleshooting.md (new)

docs/guide/
  ✓ architecture.md (from ARCHITECTURE.md)
  ✓ components.md (new, extracted from README)
  ✓ usage.md (new)
  ✓ examples.md (from EXAMPLES_AND_USAGE.py)

docs/development/
  ✓ contributing.md (new)
  ✓ code-quality.md (from CODE_QUALITY_IMPROVEMENTS.md)
  ✓ review-checklist.md (from CODE_REVIEW_CHECKLIST.md)
  ✓ standards.md (from IMPROVEMENT_STANDARDS.md)

docs-archive/
  → PHASE1_FOUNDATION_COMPLETE.md
  → PHASE2_ADVANCED_ORCHESTRATION.md
  → IMPLEMENTATION_COMPLETE_PHASE1.md
  → (all legacy files)
```

### Phase 4: Organize Tests
```
tests/unit/test_core/
  ✓ test_web_crawler.py
  ✓ test_knowledge_base.py
  ✓ test_memory_manager.py

tests/unit/test_infrastructure/
  ✓ test_exceptions.py
  ✓ test_validators.py
  ✓ test_utilities.py

tests/integration/
  ✓ test_system.py
  ✓ test_workflows.py
```

### Phase 5: Move & Rename Utilities
```
scripts/
  ✓ verify_setup.py (from verify.py)
  ✓ run_tests.py (new)
  ✓ check_quality.py (from clean_*.py, fix_*.py)
  ✓ setup.sh (from root)
  ✓ setup.bat (from root)
```

### Phase 6: Root Directory Cleanup
```
Keep in root:
  ✓ README.md (updated, points to docs/)
  ✓ requirements.txt
  ✓ pyproject.toml (new)
  ✓ Makefile (new)
  ✓ .gitignore
  ✓ .env.example
  ✓ LICENSE (if exists)
  
Remove/Archive:
  ✗ All 50+ phase/*.md files → docs-archive/
  ✗ All PHASE_*.md files → docs-archive/
  ✗ All QUICK_START*.md files → docs/
  ✗ All START_HERE*.md files → docs/
  ✗ Test files from root → tests/
  ✗ Utility scripts → scripts/
```

---

## 📊 NAMING CONVENTIONS

### Python Files
```
Good:     core_module.py, advanced_engine.py, test_utils.py
Bad:      ADVANCED_UPGRADE.py, COMPLETE_START.py
Pattern:  lowercase_with_underscores.py
```

### Markdown Files
```
Good:     01-quickstart.md, getting-started.md, architecture.md
Bad:      QUICK_START.md, IMPLEMENTATION_COMPLETE_PHASE1.md
Pattern:  lowercase-with-hyphens.md (optionally numbered)
```

### Directories
```
Good:     src/, tests/, docs/, config/, scripts/
Bad:      SRC/, Tests/, DOCS/
Pattern:  lowercase (lowercase_with_underscore if multiple words)
```

### Configuration Files
```
Good:     pyproject.toml, setup.py, Makefile
Bad:      PROJECT.TOML, SETUP.PY
Pattern:  Standard names, lowercase (except Makefile)
```

---

## 🎯 BENEFITS AFTER REORGANIZATION

| Aspect | Before | After |
|--------|--------|-------|
| Root Files | 50+ (chaos) | <10 (clean) |
| Doc Organization | Flat | Hierarchical by audience |
| Python Organization | Mixed | Clear layer separation |
| Test Files | Scattered | Organized by type |
| Configuration | Scattered | Centralized |
| Entry Point | Unclear | `src/main.py` |
| **Developer Experience** | Confusing | Clear & professional |

---

## ✅ IMPLEMENTATION CHECKLIST

- [ ] Create directory structure
- [ ] Move src/ files to organized subdirs
- [ ] Move test files to tests/ directory
- [ ] Rename documentation files
- [ ] Arc hive legacy docs
- [ ] Move utilities to scripts/
- [ ] Update all imports in files
- [ ] Create pyproject.toml
- [ ] Create Makefile
- [ ] Update README.md
- [ ] Update .gitignore
- [ ] Test that everything runs
- [ ] Verify imports work
- [ ] Final git commit

---

## ⏱️ TIME ESTIMATE

| Task | Time |
|------|------|
| Create directories | 5 min |
| Move & rename files | 20 min |
| Update imports | 15 min |
| Create config files | 10 min |
| Test system | 15 min |
| Documentation update | 15 min |
| **Total** | **80 minutes** |

---

**Next Step**: Proceed with automation of this plan? (Y/N)
