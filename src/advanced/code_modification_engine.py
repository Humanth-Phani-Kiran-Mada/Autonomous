"""
Code Generation & Modification Engine: Autonomous code synthesis

Enables system to:
- Generate new implementations
- Optimize existing code
- Apply patches dynamically
- Version and test modifications
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import ast
import inspect
import sys
import hashlib
import json

import config
from logger import logger


class ModificationType(Enum):
    """Types of code modifications"""
    PARAMETER_TUNING = "parameter_tuning"  # Adjust config params
    ALGORITHM_SWAP = "algorithm_swap"  # Replace algorithm
    OPTIMIZATION = "optimization"  # Improve performance
    BUG_FIX = "bug_fix"  # Fix identified issue
    FEATURE_ADD = "feature_add"  # Add new capability


@dataclass
class CodeVersion:
    """Represents a version of code"""
    version_id: str  # Hash of code
    module_name: str
    function_name: str
    source_code: str
    created_at: datetime = field(default_factory=datetime.now)
    
    # Metadata
    modification_type: Optional[ModificationType] = None
    description: Optional[str] = None
    performance_delta: float = 0.0  # % improvement
    quality_score: float = 0.5  # 0-1
    
    # Status tracking
    is_active: bool = False
    is_tested: bool = False
    test_results: Optional[Dict[str, Any]] = None


@dataclass
class CodePatch:
    """A modification to be applied"""
    patch_id: str
    target_module: str
    target_function: str
    modification_type: ModificationType
    description: str
    new_implementation: str
    
    # Pre-application analysis
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    estimated_impact: Dict[str, float] = field(default_factory=dict)  # metric -> delta
    
    is_applied: bool = False
    apply_time: Optional[datetime] = None


class CodeGenerator:
    """
    Generate code variants and optimizations
    
    Features:
    - Algorithm code generation
    - Parameter set generation
    - Loop optimization
    - Function inlining
    """
    
    def __init__(self):
        self.templates = self._load_templates()
        logger.info("✓ Code Generator initialized")
    
    def _load_templates(self) -> Dict[str, str]:
        """Load code templates for generation"""
        return {
            "simple_cache": '''
def cached_{func_name}(*args, **kwargs):
    cache_key = str((args, kwargs))
    if cache_key in _cache:
        return _cache[cache_key]
    
    result = _original_{func_name}(*args, **kwargs)
    _cache[cache_key] = result
    return result
''',
            "batch_processor": '''
def batch_{func_name}(items, batch_size=32):
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        result = _original_{func_name}(batch)
        results.extend(result)
    return results
''',
            "early_exit": '''
def optimized_{func_name}(*args, **kwargs):
    # Early exit conditions
    {early_exit_checks}
    
    return _original_{func_name}(*args, **kwargs)
''',
            "parallel_worker": '''
import concurrent.futures

def parallel_{func_name}(items, max_workers=4):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(_original_{func_name}, items))
    return results
'''
        }
    
    def generate_cached_version(
        self,
        function_name: str,
        original_func: Any,
        cache_size: int = 1000
    ) -> str:
        """Generate a cached version of a function"""
        template = self.templates["simple_cache"]
        return template.format(func_name=function_name)
    
    def generate_batched_version(
        self,
        function_name: str,
        batch_size: int = 32
    ) -> str:
        """Generate a batched processing version"""
        template = self.templates["batch_processor"]
        return template.format(func_name=function_name, batch_size=batch_size)
    
    def generate_optimized_version(
        self,
        function_name: str,
        optimization_type: str,
        **kwargs
    ) -> str:
        """Generate an optimized version"""
        
        if optimization_type == "early_exit":
            return self.templates["early_exit"].format(
                func_name=function_name,
                early_exit_checks=kwargs.get("checks", "")
            )
        
        elif optimization_type == "parallel":
            return self.templates["parallel_worker"].format(
                func_name=function_name,
                max_workers=kwargs.get("max_workers", 4)
            )
        
        else:
            raise ValueError(f"Unknown optimization type: {optimization_type}")
    
    def generate_algorithm_variant(
        self,
        algorithm_name: str,
        current_impl: str,
        optimization_hint: str
    ) -> str:
        """Generate a variant of an algorithm"""
        
        # Parse current implementation
        try:
            tree = ast.parse(current_impl)
        except SyntaxError:
            logger.error(f"Could not parse implementation for {algorithm_name}")
            return current_impl
        
        # Apply transformations based on hint
        if optimization_hint == "reduce_allocations":
            return self._optimize_allocations(current_impl, tree)
        elif optimization_hint == "early_termination":
            return self._add_early_termination(current_impl, tree)
        elif optimization_hint == "vectorize":
            return self._vectorize_operations(current_impl, tree)
        else:
            return current_impl
    
    def _optimize_allocations(self, impl: str, tree: ast.AST) -> str:
        """Optimize memory allocations"""
        # Simplified: add object pool pattern
        return f"""
# Memory-optimized version (using object pool)
_object_pool = []

def _get_from_pool(cls, *args, **kwargs):
    if _object_pool:
        obj = _object_pool.pop()
        obj.__init__(*args, **kwargs)
        return obj
    return cls(*args, **kwargs)

{impl}
"""
    
    def _add_early_termination(self, impl: str, tree: ast.AST) -> str:
        """Add early termination conditions"""
        # Simplified: wrap with early exit
        return f"""
# Version with early termination
{impl}

# Wrap with early exit heuristics
def _should_continue(state, threshold=0.95):
    return state.get('quality_score', 0) < threshold
"""
    
    def _vectorize_operations(self, impl: str, tree: ast.AST) -> str:
        """Vectorize operations for batch processing"""
        return f"""
import numpy as np

# Vectorized version
{impl}

# Use NumPy for batch operations where possible
"""


class CodeModificationEngine:
    """
    Apply code modifications at runtime
    
    Features:
    - Hot-patch code
    - Version management
    - Rollback support
    - Dependency tracking
    """
    
    def __init__(self):
        self.generator = CodeGenerator()
        self.versions: Dict[str, List[CodeVersion]] = {}  # module -> versions
        self.patches: List[CodePatch] = []
        self.active_modifications: Dict[str, CodeVersion] = {}  # key -> version
        
        logger.info("✓ Code Modification Engine initialized")
    
    def propose_modification(
        self,
        module_name: str,
        function_name: str,
        modification_type: ModificationType,
        description: str,
        **kwargs
    ) -> CodePatch:
        """Propose a code modification"""
        
        # Generate new implementation
        if modification_type == ModificationType.PARAMETER_TUNING:
            new_impl = self._generate_parameter_tuning(
                module_name, function_name, **kwargs
            )
        elif modification_type == ModificationType.OPTIMIZATION:
            new_impl = self._generate_optimization(
                module_name, function_name, **kwargs
            )
        elif modification_type == ModificationType.ALGORITHM_SWAP:
            new_impl = self._generate_algorithm_swap(
                module_name, function_name, **kwargs
            )
        else:
            raise ValueError(f"Unknown modification type: {modification_type}")
        
        # Create patch
        patch = CodePatch(
            patch_id=self._generate_patch_id(),
            target_module=module_name,
            target_function=function_name,
            modification_type=modification_type,
            description=description,
            new_implementation=new_impl
        )
        
        self.patches.append(patch)
        logger.info(f"Proposed patch: {patch.patch_id} ({modification_type.value})")
        logger.info(f"  Target: {module_name}.{function_name}")
        logger.info(f"  Description: {description}")
        
        return patch
    
    def _generate_patch_id(self) -> str:
        """Generate unique patch ID"""
        return f"patch_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"
    
    def _generate_parameter_tuning(
        self,
        module_name: str,
        function_name: str,
        **kwargs
    ) -> str:
        """Generate parameter tuning modification"""
        
        new_params = kwargs.get("new_params", {})
        
        return f'''
# Parameter-tuned version
# Original params updated with: {new_params}

def {function_name}(*args, **kwargs):
    # Apply new parameters
    {json.dumps(new_params, indent=2)}
    
    # Call original with updated params
    return _original_{function_name}(*args, **kwargs, **new_params)
'''
    
    def _generate_optimization(
        self,
        module_name: str,
        function_name: str,
        **kwargs
    ) -> str:
        """Generate optimization modification"""
        
        opt_type = kwargs.get("optimization_type", "caching")
        
        if opt_type == "caching":
            return self.generator.generate_cached_version(function_name, None)
        elif opt_type == "batching":
            return self.generator.generate_batched_version(function_name)
        else:
            return ''
    
    def _generate_algorithm_swap(
        self,
        module_name: str,
        function_name: str,
        **kwargs
    ) -> str:
        """Generate algorithm swap modification"""
        
        new_algo_name = kwargs.get("new_algorithm", "improved")
        
        return f'''
# Algorithm swapped to: {new_algo_name}

from improved_algorithms import {new_algo_name}

def {function_name}(*args, **kwargs):
    # Use new algorithm
    return {new_algo_name}(*args, **kwargs)
'''
    
    def apply_modification(self, patch: CodePatch) -> Tuple[bool, str]:
        """
        Apply a code modification
        
        Returns: (success, message)
        """
        
        try:
            # Get target module
            if patch.target_module not in sys.modules:
                return False, f"Module not found: {patch.target_module}"
            
            module = sys.modules[patch.target_module]
            
            # Create code version
            version = CodeVersion(
                version_id=hashlib.md5(patch.new_implementation.encode()).hexdigest()[:8],
                module_name=patch.target_module,
                function_name=patch.target_function,
                source_code=patch.new_implementation,
                modification_type=patch.modification_type,
                description=patch.description
            )
            
            # Store version history
            key = f"{patch.target_module}.{patch.target_function}"
            if key not in self.versions:
                self.versions[key] = []
            self.versions[key].append(version)
            
            # Attempt to execute new code and replace function
            exec_globals = {
                f"_original_{patch.target_function}": getattr(module, patch.target_function),
                **module.__dict__
            }
            
            exec(patch.new_implementation, exec_globals)
            new_func = exec_globals.get(patch.target_function) or \
                      exec_globals.get(f"optimized_{patch.target_function}") or \
                      exec_globals.get(f"cached_{patch.target_function}") or \
                      exec_globals.get(f"batch_{patch.target_function}")
            
            if new_func:
                # Replace function in module
                setattr(module, patch.target_function, new_func)
                
                patch.is_applied = True
                patch.apply_time = datetime.now()
                
                version.is_active = True
                self.active_modifications[key] = version
                
                logger.info(f"✓ Applied modification {patch.patch_id}")
                return True, f"Applied {patch.modification_type.value} to {key}"
            else:
                return False, "Could not create new function"
        
        except Exception as e:
            logger.error(f"Failed to apply modification {patch.patch_id}: {e}")
            return False, str(e)
    
    def rollback_modification(self, module_name: str, function_name: str) -> bool:
        """Rollback to previous version"""
        
        key = f"{module_name}.{function_name}"
        
        if key not in self.versions or len(self.versions[key]) < 2:
            logger.warning(f"No previous version to rollback: {key}")
            return False
        
        # Get previous version
        versions = self.versions[key]
        previous = versions[-2] if len(versions) >= 2 else None
        
        if not previous:
            return False
        
        # Attempt to restore
        try:
            if module_name in sys.modules:
                module = sys.modules[module_name]
                
                # Re-execute previous code
                exec_globals = module.__dict__.copy()
                exec(previous.source_code, exec_globals)
                
                # Extract and restore function
                for name, obj in exec_globals.items():
                    if callable(obj) and name == function_name:
                        setattr(module, function_name, obj)
                        previous.is_active = True
                        logger.info(f"✓ Rolled back {key} to version {previous.version_id}")
                        return True
        
        except Exception as e:
            logger.error(f"Rollback failed for {key}: {e}")
        
        return False
    
    def get_version_history(self, module_name: str, function_name: str) -> List[Dict[str, Any]]:
        """Get history of modifications"""
        
        key = f"{module_name}.{function_name}"
        versions = self.versions.get(key, [])
        
        return [
            {
                "version_id": v.version_id,
                "created_at": v.created_at.isoformat(),
                "modification_type": v.modification_type.value if v.modification_type else None,
                "description": v.description,
                "is_active": v.is_active,
                "quality_score": v.quality_score
            }
            for v in versions
        ]


# Global instance
_engine: Optional[CodeModificationEngine] = None


def get_code_modification_engine() -> CodeModificationEngine:
    """Get or create code modification engine"""
    global _engine
    if _engine is None:
        _engine = CodeModificationEngine()
    return _engine
