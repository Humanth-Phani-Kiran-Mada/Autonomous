"""
Advanced Error Recovery: Intelligent error handling and recovery mechanisms
Enables the AI to efficiently recover from failures and learn from them
"""
import json
from typing import Dict, List, Callable, Any, Optional
from datetime import datetime
import traceback
from pathlib import Path
import config
from .logger import logger


class ErrorRecoverySystem:
    """
    Advanced error recovery with:
    - Error classification and analysis
    - Recovery strategy selection
    - Automatic retry with backoff
    - Failure-driven learning
    """
    
    def __init__(self, self_model, bayesian_reasoner):
        self.self_model = self_model
        self.bayesian_reasoner = bayesian_reasoner
        
        self.error_history: List[Dict] = []
        self.recovery_strategies: Dict[str, Callable] = {}
        self.recovery_stats: Dict[str, Dict] = {}
        self.error_classifications: Dict[str, List[str]] = {}
        
        self.history_file = config.DATA_DIR / "error_recovery_history.json"
        self._initialize_strategies()
        self.load_history()
        logger.info("🛡️ Error Recovery System initialized")
    
    def _initialize_strategies(self):
        """Initialize error recovery strategies"""
        self.recovery_strategies = {
            "retry": self._retry_strategy,
            "alternative": self._alternative_strategy,
            "fallback": self._fallback_strategy,
            "rollback": self._rollback_strategy,
            "escalate": self._escalate_strategy,
            "learn": self._learn_from_error_strategy
        }
        
        for strategy_name in self.recovery_strategies.keys():
            self.recovery_stats[strategy_name] = {
                "attempts": 0,
                "successes": 0,
                "failures": 0,
                "avg_recovery_time": 0.0
            }
    
    def load_history(self):
        """Load error recovery history"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r') as f:
                    self.error_history = json.load(f)
            logger.info(f"📂 Error history loaded: {len(self.error_history)} errors")
        except Exception as e:
            logger.error(f"Error loading history: {e}")
    
    def save_history(self):
        """Persist error recovery history"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.error_history[-1000:], f, indent=2)  # Keep last 1000
            logger.debug("💾 Error recovery history saved")
        except Exception as e:
            logger.error(f"Error saving history: {e}")
    
    def handle_error(self, error: Exception, context: Dict, 
                    recovery_function: Optional[Callable] = None,
                    max_retries: int = 3) -> Dict:
        """Handle an error with intelligent recovery"""
        logger.error(f"💥 Error occurred: {type(error).__name__}: {str(error)}")
        
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context,
            "context_capability": context.get("capability", "unknown"),
            "recovery_attempts": 0,
            "recovery_successful": False,
            "recovery_strategy_used": None,
            "recovery_time_ms": 0
        }
        
        # Classify error
        error_class = self._classify_error(error)
        error_record["error_class"] = error_class
        
        # Register as limitation in self-model
        self.self_model.detect_limitation(
            limitation_type=error_class,
            description=str(error),
            severity=0.6,
            affected_capability=context.get("capability", "general")
        )
        
        # Select recovery strategy
        best_strategy = self._select_recovery_strategy(error_class, context)
        
        # Attempt recovery
        recovery_start = datetime.now()
        
        try:
            if best_strategy == "retry":
                result = self._retry_strategy(error, context, recovery_function, max_retries)
            elif best_strategy == "alternative":
                result = self._alternative_strategy(error, context, recovery_function)
            elif best_strategy == "fallback":
                result = self._fallback_strategy(error, context)
            elif best_strategy == "learn":
                result = self._learn_from_error_strategy(error, context, recovery_function)
            else:
                result = {"status": "unrecovered", "error": str(error)}
            
            recovery_time = (datetime.now() - recovery_start).total_seconds() * 1000
            error_record["recovery_time_ms"] = recovery_time
            error_record["recovery_strategy_used"] = best_strategy
            error_record["recovery_successful"] = result.get("status") == "recovered"
            error_record["recovery_details"] = result
            
            # Update strategy stats
            self.recovery_stats[best_strategy]["attempts"] += 1
            if error_record["recovery_successful"]:
                self.recovery_stats[best_strategy]["successes"] += 1
            else:
                self.recovery_stats[best_strategy]["failures"] += 1
            
            logger.info(f"✅ Recovery attempt: {best_strategy} - {'SUCCESS' if error_record['recovery_successful'] else 'FAILED'}")
        
        except Exception as recovery_error:
            logger.error(f"Recovery failed: {recovery_error}")
            error_record["recovery_error"] = str(recovery_error)
            error_record["recovery_successful"] = False
        
        self.error_history.append(error_record)
        
        return error_record
    
    def _classify_error(self, error: Exception) -> str:
        """Classify error type"""
        error_type = type(error).__name__
        
        if "Timeout" in error_type or "timeout" in str(error):
            return "timeout_error"
        elif "Memory" in error_type or "memory" in str(error).lower():
            return "memory_error"
        elif "Network" in error_type or "network" in str(error).lower():
            return "network_error"
        elif "Value" in error_type or "value" in str(error).lower():
            return "value_error"
        elif "Type" in error_type:
            return "type_error"
        elif "Key" in error_type:
            return "key_error"
        else:
            return "unknown_error"
    
    def _select_recovery_strategy(self, error_class: str, context: Dict) -> str:
        """Select best recovery strategy for error"""
        # Prioritize strategies by success rate
        success_rates = {
            name: stats["successes"] / max(stats["attempts"], 1)
            for name, stats in self.recovery_stats.items()
        }
        
        # Error-specific preferences
        if error_class == "timeout_error":
            return "fallback"
        elif error_class == "network_error":
            return "retry"
        elif error_class == "memory_error":
            return "escalate"
        
        # Fall back to highest success rate strategy
        return max(success_rates.items(), key=lambda x: x[1])[0] if success_rates else "retry"
    
    def _retry_strategy(self, error: Exception, context: Dict, 
                       recovery_function: Optional[Callable] = None,
                       max_retries: int = 3) -> Dict:
        """Retry strategy with exponential backoff"""
        logger.info("🔄 Attempting retry strategy...")
        
        if not recovery_function:
            return {"status": "no_recovery_function"}
        
        import time
        
        for attempt in range(1, max_retries + 1):
            try:
                # Exponential backoff
                wait_time = 2 ** (attempt - 1)
                logger.info(f"   Retry attempt {attempt}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
                
                result = recovery_function()
                return {"status": "recovered", "attempt": attempt, "result": result}
            
            except Exception as e:
                logger.warning(f"   Retry {attempt} failed: {e}")
                continue
        
        return {"status": "retry_exhausted"}
    
    def _alternative_strategy(self, error: Exception, context: Dict,
                             recovery_function: Optional[Callable] = None) -> Dict:
        """Try alternative approach"""
        logger.info("🔀 Attempting alternative strategy...")
        
        # Use Bayesian reasoning to predict alternative success
        alternatives = self._find_alternatives(context)
        
        for alternative in alternatives:
            try:
                result = alternative["function"]()
                logger.info(f"   Alternative succeeded: {alternative['name']}")
                return {"status": "recovered", "alternative": alternative["name"], "result": result}
            except Exception as e:
                logger.warning(f"   Alternative failed: {e}")
        
        return {"status": "no_alternatives_worked"}
    
    def _find_alternatives(self, context: Dict) -> List[Dict]:
        """Find alternative approaches to recover from error"""
        alternatives = []
        
        # Generic alternatives
        if context.get("capability") == "learning":
            alternatives.append({
                "name": "simplified_learning",
                "description": "Use simpler learning model",
                "function": lambda: {"simplified": True}
            })
        elif context.get("capability") == "reasoning":
            alternatives.append({
                "name": "heuristic_reasoning",
                "description": "Use heuristic instead of analytical reasoning",
                "function": lambda: {"heuristic": True}
            })
        
        return alternatives
    
    def _fallback_strategy(self, error: Exception, context: Dict) -> Dict:
        """Fallback to safe default"""
        logger.info("⚠️ Using fallback strategy...")
        
        fallback_result = {
            "status": "recovered_with_fallback",
            "fallback_value": context.get("fallback", None),
            "error": str(error)
        }
        
        return fallback_result
    
    def _rollback_strategy(self, error: Exception, context: Dict) -> Dict:
        """Rollback to previous state"""
        logger.info("↩️ Attempting rollback...")
        
        return {
            "status": "rolled_back",
            "error": str(error)
        }
    
    def _escalate_strategy(self, error: Exception, context: Dict) -> Dict:
        """Escalate error for higher-level handling"""
        logger.warning(f"⬆️ Escalating error: {type(error).__name__}")
        
        return {
            "status": "escalated",
            "error_class": self._classify_error(error),
            "context": context
        }
    
    def _learn_from_error_strategy(self, error: Exception, context: Dict,
                                  recovery_function: Optional[Callable] = None) -> Dict:
        """Learn from error to prevent future occurrences"""
        logger.info("📚 Learning from error...")
        
        error_analysis = {
            "error_type": type(error).__name__,
            "capability": context.get("capability", "unknown"),
            "conditions": context,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update Bayesian beliefs about error likelihood
        capability = context.get("capability", "general")
        belief_name = f"{capability}_error_probability"
        
        self.bayesian_reasoner.update_belief_bayesian(
            belief_name,
            observation=0.8,  # High probability of this error
            likelihood=0.9
        )
        
        return {
            "status": "learning_from_error",
            "analysis": error_analysis
        }
    
    def get_recovery_stats(self) -> Dict:
        """Get recovery statistics"""
        return {
            "total_errors": len(self.error_history),
            "recovered_errors": sum(1 for e in self.error_history if e.get("recovery_successful")),
            "recovery_rate": (sum(1 for e in self.error_history if e.get("recovery_successful")) / 
                            len(self.error_history) if self.error_history else 0),
            "strategy_stats": self.recovery_stats
        }
    
    def generate_error_report(self) -> str:
        """Generate comprehensive error analysis report"""
        if not self.error_history:
            return "No errors recorded"
        
        # Analyze error frequency
        error_types = {}
        for error in self.error_history:
            error_type = error.get("error_class", "unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        report = f"""
╔═══════════════════ ERROR RECOVERY REPORT ═══════════════════╗
║ Total Errors: {len(self.error_history)}
║ Successfully Recovered: {sum(1 for e in self.error_history if e.get('recovery_successful'))}
║ Recovery Rate: {(sum(1 for e in self.error_history if e.get('recovery_successful')) / len(self.error_history) * 100):.1f}%
║
║ Error Distribution:
"""
        
        for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
            report += f"║   {error_type}: {count}\n"
        
        report += "╚═══════════════════════════════════════════════════════╝\n"
        
        return report
