"""
Attention System: Allocates computational resources to most important problems
Enables focus and prevents diffusion of effort across too many tasks.
Critical for efficient learning and problem-solving.
"""
import json
from typing import Dict, List, Tuple, Optional, Any, Set
from datetime import datetime
from collections import defaultdict
import numpy as np
from pathlib import Path
import config
from .logger import logger


class AttentionTarget:
    """Represents something worthy of attention"""
    def __init__(self, target_id: str, name: str, priority: float = 0.5,
                 urgency: float = 0.5, importance: float = 0.5):
        self.target_id = target_id
        self.name = name
        self.priority = priority  # 0-1
        self.urgency = urgency    # 0-1
        self.importance = importance  # 0-1
        self.attention_allocated = 0.0
        self.attention_history: List[float] = []
        self.deadline = None
        self.expected_impact = 0.0
        self.created_at = datetime.now()
        
    def compute_attention_score(self) -> float:
        """Compute combined attention score"""
        # Combine priority, urgency, importance
        # Urgency gets more weight for limited short-term resources
        return (self.urgency * 0.5 + self.importance * 0.3 + self.priority * 0.2)


class AttentionSystem:
    """
    Manages the AI's cognitive attention/resource allocation.
    Focuses effort on high-priority, high-impact problems.
    Prevents resource dilution across too many tasks.
    """
    
    def __init__(self, total_attention_budget: float = 1.0):
        self.total_attention_budget = total_attention_budget
        self.current_targets: Dict[str, AttentionTarget] = {}
        self.attention_history: List[Dict] = []
        self.allocation_log: List[Dict] = []
        self.focus_switches: List[Dict] = []
        self.attention_drain: Dict[str, float] = defaultdict(float)  # What consumes attention
        self.context: Dict[str, Any] = {}  # Current context
        
        self.attention_file = config.DATA_DIR / "attention.json"
        
        logger.info("[ATTENTION] Attention System initialized")
    
    def add_target(self, target_id: str, name: str, priority: float = 0.5,
                  urgency: float = 0.5, importance: float = 0.5) -> AttentionTarget:
        """Add something to attend to"""
        target = AttentionTarget(target_id, name, priority, urgency, importance)
        self.current_targets[target_id] = target
        
        logger.info(f"[ATTENTION] Added target: {name} (score: {target.compute_attention_score():.2f})")
        
        return target
    
    def allocate_attention(self, num_top_targets: int = 3) -> Dict[str, float]:
        """
        Allocate attention budget to top-priority targets.
        Returns allocation: {target_id: attention_amount}
        """
        allocation = {}
        
        try:
            if not self.current_targets:
                return allocation
            
            # Compute attention scores for all targets
            scored_targets = [
                (tid, target, target.compute_attention_score())
                for tid, target in self.current_targets.items()
            ]
            
            # Sort by score
            scored_targets.sort(key=lambda x: x[2], reverse=True)
            
            # Select top targets
            top_targets = scored_targets[:min(num_top_targets, len(scored_targets))]
            
            # Allocate budget proportional to scores
            total_score = sum(score for _, _, score in top_targets)
            
            if total_score > 0:
                for target_id, target, score in top_targets:
                    allocated = (score / total_score) * self.total_attention_budget
                    allocation[target_id] = allocated
                    target.attention_allocated = allocated
                    target.attention_history.append(allocated)
            
            # Log allocation
            allocation_record = {
                "allocated_at": datetime.now().isoformat(),
                "allocation": allocation,
                "top_targets": [tid for tid, _, _ in top_targets],
                "total_budget": self.total_attention_budget
            }
            self.allocation_log.append(allocation_record)
            
            logger.info(f"[ATTENTION] Allocated attention to {len(allocation)} targets")
            
        except Exception as e:
            logger.error(f"[ATTENTION] Error allocating attention: {e}")
        
        return allocation
    
    def update_attention_weights(self, target_id: str, 
                               priority_delta: float = 0.0,
                               urgency_delta: float = 0.0,
                               importance_delta: float = 0.0):
        """Update attention weights for a target"""
        if target_id not in self.current_targets:
            return
        
        target = self.current_targets[target_id]
        
        # Update and clamp to [0, 1]
        target.priority = max(0.0, min(1.0, target.priority + priority_delta))
        target.urgency = max(0.0, min(1.0, target.urgency + urgency_delta))
        target.importance = max(0.0, min(1.0, target.importance + importance_delta))
        
        logger.debug(f"[ATTENTION] Updated weights for {target_id}")
    
    def record_focus_switch(self, from_target: str, to_target: str, reason: str = ""):
        """Record when attention switches from one target to another"""
        switch_record = {
            "from_target": from_target,
            "to_target": to_target,
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "context": self.context.copy()
        }
        self.focus_switches.append(switch_record)
        
        logger.debug(f"[ATTENTION] Focus switch: {from_target} -> {to_target}")
    
    def add_attention_drain(self, source: str, drain_amount: float):
        """Record what drains attention (distractions, processes, etc.)"""
        self.attention_drain[source] += drain_amount
        
        # If too much drain, should reduce it
        if self.attention_drain[source] > 0.3:
            logger.warning(f"[ATTENTION] High attention drain from {source}: " +
                          f"{self.attention_drain[source]:.2f}")
    
    def get_remaining_attention(self) -> float:
        """Calculate remaining attention after drains"""
        total_drain = sum(self.attention_drain.values())
        remaining = self.total_attention_budget - total_drain
        return max(0.0, remaining)
    
    def prioritize_targets(self) -> List[Tuple[str, AttentionTarget, float]]:
        """Get targets sorted by attention score"""
        scored = [
            (tid, target, target.compute_attention_score())
            for tid, target in self.current_targets.items()
        ]
        scored.sort(key=lambda x: x[2], reverse=True)
        return scored
    
    def identify_distractions(self) -> List[Dict]:
        """Identify low-priority targets consuming attention (distractions)"""
        distractions = []
        
        try:
            for target_id, target in self.current_targets.items():
                score = target.compute_attention_score()
                allocated = target.attention_allocated
                
                # Distraction = low score but attention allocated
                if score < 0.3 and allocated > 0.1:
                    distractions.append({
                        "target_id": target_id,
                        "name": target.name,
                        "score": score,
                        "allocated": allocated,
                        "wasted": allocated,
                        "recommendation": "reduce attention"
                    })
            
            if distractions:
                logger.info(f"[ATTENTION] Identified {len(distractions)} distractions")
            
        except Exception as e:
            logger.error(f"[ATTENTION] Error identifying distractions: {e}")
        
        return distractions
    
    def focus_on_critical(self, threshold: float = 0.7) -> List[str]:
        """
        Identify targets above criticality threshold.
        AI should focus here.
        """
        critical = []
        
        for target_id, target in self.current_targets.items():
            score = target.compute_attention_score()
            if score > threshold:
                critical.append(target_id)
        
        logger.info(f"[ATTENTION] {len(critical)} critical targets identified")
        
        return critical
    
    def remove_target(self, target_id: str):
        """Remove a target from attention"""
        if target_id in self.current_targets:
            target = self.current_targets[target_id]
            del self.current_targets[target_id]
            
            # Redistribute released attention
            released = target.attention_allocated
            self.total_attention_budget += released
            
            logger.info(f"[ATTENTION] Removed target {target_id}, released {released:.2f} attention")
    
    def recalibrate_attention(self, performance_data: Dict):
        """
        Recalibrate attention allocation based on actual performance.
        If something isn't progressing despite attention, de-prioritize.
        """
        try:
            for target_id, target in self.current_targets.items():
                performance = performance_data.get(target_id, {})
                
                progress = performance.get("progress", 0.0)
                outcome = performance.get("outcome", "neutral")
                
                # Adjust priority based on progress
                if outcome == "success":
                    # Keep attention, maybe increase
                    self.update_attention_weights(target_id, importance_delta=0.1)
                elif outcome == "failure":
                    # Reduce attention to failed target
                    self.update_attention_weights(target_id, priority_delta=-0.2)
                elif progress < 0.1 and target.attention_allocated > 0.1:
                    # Low progress despite attention - reduce
                    self.update_attention_weights(target_id, priority_delta=-0.15)
            
            logger.info("[ATTENTION] Recalibrated attention based on performance")
            
        except Exception as e:
            logger.error(f"[ATTENTION] Error recalibrating attention: {e}")
    
    def get_focused_context(self) -> Dict:
        """Get context with emphasis on focused targets"""
        focused_targets = []
        high_budget = self.allocate_attention(num_top_targets=3)
        
        for target_id, amount in high_budget.items():
            if target_id in self.current_targets:
                focused_targets.append({
                    "target": self.current_targets[target_id].name,
                    "allocation": amount
                })
        
        return {
            "focused_targets": focused_targets,
            "remaining_attention": self.get_remaining_attention(),
            "distraction_count": len(self.identify_distractions()),
            "critical_targets": len(self.focus_on_critical())
        }
    
    def save_attention_state(self):
        """Save attention system state"""
        try:
            data = {
                "total_budget": self.total_attention_budget,
                "current_targets": len(self.current_targets),
                "total_allocations": len(self.allocation_log),
                "focus_switches": len(self.focus_switches),
                "recent_allocations": self.allocation_log[-20:]
            }
            
            with open(self.attention_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("[ATTENTION] Saved attention system state")
        except Exception as e:
            logger.error(f"[ATTENTION] Error saving attention state: {e}")
    
    def get_attention_summary(self) -> Dict:
        """Get comprehensive attention system summary"""
        distractions = self.identify_distractions()
        critical = self.focus_on_critical()
        
        return {
            "total_targets": len(self.current_targets),
            "critical_targets": len(critical),
            "distractions": len(distractions),
            "remaining_attention": self.get_remaining_attention(),
            "attention_drain_sources": dict(self.attention_drain),
            "focus_switch_count": len(self.focus_switches),
            "allocation_count": len(self.allocation_log),
            "top_priorities": [(tid, target.name, target.compute_attention_score()) 
                             for tid, target in sorted(
                                 self.current_targets.items(),
                                 key=lambda x: x[1].compute_attention_score(),
                                 reverse=True)[:5]]
        }
