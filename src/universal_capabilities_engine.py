"""
Universal Capabilities Engine: Unified AI capability system

Integrates all AI capabilities:
- Code generation
- Image/video/audio creation
- Data analysis
- Self-learning
- Task execution
- Request processing
- Everything AI can do

Features:
- Autonomous capability expansion
- Performance tracking
- Learning across domains
- Multi-capability workflows
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import config
from src.logger import logger
from src.task_management_engine import (
    get_task_management_engine, TaskType, TaskStatus
)
from src.request_processing_engine import get_request_dispatcher


@dataclass
class CapabilityMetrics:
    """Metrics for a capability"""
    name: str
    domain: str  # code, media, analysis, etc
    
    total_uses: int = 0
    successful_uses: int = 0
    failed_uses: int = 0
    
    avg_execution_time: float = 0.0
    avg_quality_score: float = 0.0
    
    last_used: Optional[datetime] = None
    discovered_at: datetime = field(default_factory=datetime.now)


class CapabilityDomain(Enum):
    """AI capability domains"""
    GENERATION = "generation"  # Create code, images, videos, etc
    ANALYSIS = "analysis"      # Analyze, extract, report
    TRANSFORMATION = "transformation"  # Convert, optimize, improve
    AUTOMATION = "automation"  # Automate tasks, workflows
    LEARNING = "learning"      # Learn, understand, improve


class UniversalCapabilitiesEngine:
    """
    Unified engine for all AI capabilities
    
    Manages:
    - All AI task types
    - Capability discovery
    - Performance optimization
    - Cross-domain learning
    """
    
    def __init__(self):
        self.task_engine = get_task_management_engine()
        self.dispatcher = get_request_dispatcher()
        
        # Capabilities tracking
        self.capabilities: Dict[str, CapabilityMetrics] = {}
        self.capability_domains: Dict[CapabilityDomain, List[str]] = {}
        
        # Workflow tracking
        self.workflows: Dict[str, List[str]] = {}
        self.workflow_results: List[Dict[str, Any]] = []
        
        self._initialize_capabilities()
        logger.info("✓ Universal Capabilities Engine initialized")
    
    def _initialize_capabilities(self) -> None:
        """Initialize all capabilities"""
        
        all_capabilities = {
            CapabilityDomain.GENERATION: [
                "code_generation",
                "image_generation",
                "video_generation",
                "audio_generation",
                "document_generation"
            ],
            CapabilityDomain.ANALYSIS: [
                "data_analysis",
                "text_analysis",
                "code_analysis",
                "performance_analysis",
                "research"
            ],
            CapabilityDomain.TRANSFORMATION: [
                "text_processing",
                "code_optimization",
                "data_transformation",
                "format_conversion"
            ],
            CapabilityDomain.AUTOMATION: [
                "task_automation",
                "workflow_automation",
                "testing_automation",
                "deployment_automation"
            ],
            CapabilityDomain.LEARNING: [
                "self_learning",
                "pattern_recognition",
                "knowledge_extraction",
                "capability_expansion"
            ]
        }
        
        # Register all capabilities
        for domain, caps in all_capabilities.items():
            self.capability_domains[domain] = caps
            
            for cap_name in caps:
                self.capabilities[cap_name] = CapabilityMetrics(
                    name=cap_name,
                    domain=domain.value
                )
    
    def execute_request(self, request: str) -> Dict[str, Any]:
        """
        Execute any request the system can handle
        
        Converts natural language to tasks and executes
        """
        
        logger.info(f"Executing request: {request[:100]}")
        
        # Process through dispatcher
        result = self.dispatcher.process_request(request)
        
        # Track capability usage
        task_type = result["parsed"]["task_type"]
        self._track_capability_usage(task_type, result["success"])
        
        return result
    
    def execute_workflow(
        self,
        workflow_name: str,
        requests: List[str]
    ) -> Dict[str, Any]:
        """
        Execute a multi-step workflow
        
        Example workflow:
        1. Generate code
        2. Analyze code
        3. Optimize code
        4. Generate documentation
        """
        
        logger.info(f"Executing workflow: {workflow_name} ({len(requests)} steps)")
        
        # Store workflow definition
        self.workflows[workflow_name] = requests
        
        # Execute through dispatcher
        result = self.dispatcher.process_multiple_requests(requests)
        
        # Extract workflow result
        workflow_result = {
            "workflow": workflow_name,
            "steps": len(requests),
            "completed": result["completed"],
            "successful": result["successful"],
            "responses": result["responses"],
            "executed_at": datetime.now().isoformat()
        }
        
        self.workflow_results.append(workflow_result)
        
        return workflow_result
    
    def _track_capability_usage(
        self,
        capability_name: str,
        success: bool
    ) -> None:
        """Track capability usage metrics"""
        
        # Map task type to capability name
        capability_map = {
            "code_generation": "code_generation",
            "image_generation": "image_generation",
            "video_generation": "video_generation",
            "data_analysis": "data_analysis",
            "text_processing": "text_processing",
            "audio_generation": "audio_generation",
            "research": "research",
            "optimization": "code_optimization"
        }
        
        actual_cap = capability_map.get(capability_name, capability_name)
        
        if actual_cap in self.capabilities:
            cap = self.capabilities[actual_cap]
            cap.total_uses += 1
            cap.last_used = datetime.now()
            
            if success:
                cap.successful_uses += 1
            else:
                cap.failed_uses += 1
    
    def get_all_capabilities(self) -> Dict[str, Any]:
        """Get all available capabilities"""
        
        result = {
            "total_capabilities": len(self.capabilities),
            "domains": {}
        }
        
        for domain in CapabilityDomain:
            caps = self.capability_domains.get(domain, [])
            result["domains"][domain.value] = {
                "count": len(caps),
                "capabilities": caps,
                "metrics": {}
            }
            
            for cap_name in caps:
                if cap_name in self.capabilities:
                    metric = self.capabilities[cap_name]
                    result["domains"][domain.value]["metrics"][cap_name] = {
                        "total_uses": metric.total_uses,
                        "success_rate": (
                            metric.successful_uses / max(metric.total_uses, 1)
                        ),
                        "last_used": metric.last_used.isoformat() if metric.last_used else None
                    }
        
        return result
    
    def discover_needed_capabilities(self) -> List[str]:
        """
        Analyze system and discover what capabilities would be most beneficial
        
        Uses learning data to recommend capability expansion
        """
        
        logger.info("Discovering needed capabilities...")
        
        recommendations = []
        
        # Analyze current usage patterns
        learning = self.task_engine.get_learning_summary()
        
        # Recommendations based on gaps
        if len(self.capabilities) < 20:
            recommendations.append("Expand capability set")
        
        # Check for low-performing domains
        for domain, metrics_dict in self.dispatcher.task_engine.learning_database.items():
            if metrics_dict.get("total", 0) > 0:
                success_rate = (
                    metrics_dict.get("successful", 0) / metrics_dict.get("total", 1)
                )
                
                if success_rate < 0.7:
                    recommendations.append(f"Improve {domain} success rate")
        
        return recommendations
    
    def get_system_capabilities_summary(self) -> Dict[str, Any]:
        """Get complete capabilities summary"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            
            # Basic stats
            "total_capabilities": len(self.capabilities),
            "domains_covered": len(self.capability_domains),
            "workflows_created": len(self.workflows),
            
            # Execution stats
            "total_executions": (
                len(self.dispatcher.execution_history)
            ),
            "total_tasks": (
                len(self.task_engine.completed_tasks) +
                len(self.task_engine.failed_tasks)
            ),
            "success_rate": (
                len(self.task_engine.completed_tasks) /
                max(len(self.task_engine.completed_tasks) +
                    len(self.task_engine.failed_tasks), 1)
            ),
            
            # Capability status
            "capabilities_by_domain": self.get_all_capabilities(),
            
            # Recommendations
            "recommendations": self.discover_needed_capabilities(),
            
            # Recent workflows
            "recent_workflows": self.workflow_results[-5:] if self.workflow_results else []
        }


class UniversalAIInterface:
    """
    High-level interface to the entire AI system
    
    Users interact with this for all capabilities
    """
    
    def __init__(self):
        self.capabilities_engine = UniversalCapabilitiesEngine()
        logger.info("✓ Universal AI Interface initialized")
    
    def do(self, request: str) -> Dict[str, Any]:
        """
        Execute any request in natural language
        
        Examples:
        - "Generate a Python function to sort a list"
        - "Create an image of a sunset over mountains"
        - "Generate a 30-second video of a forest"
        - "Analyze this dataset and give me insights"
        - "Summarize this text"
        - "Generate a voice narration"
        - "Research climate change"
        - "Optimize my code for performance"
        """
        
        return self.capabilities_engine.execute_request(request)
    
    def workflow(
        self,
        name: str,
        steps: List[str]
    ) -> Dict[str, Any]:
        """
        Execute a multi-step workflow
        
        Example:
        ai.workflow("build_app", [
            "Generate a Python FastAPI application shell",
            "Add authentication endpoints",
            "Optimize the code",
            "Generate unit tests",
            "Generate documentation"
        ])
        """
        
        return self.capabilities_engine.execute_workflow(name, steps)
    
    def capabilities(self) -> Dict[str, Any]:
        """Get all available capabilities"""
        
        return self.capabilities_engine.get_all_capabilities()
    
    def status(self) -> Dict[str, Any]:
        """Get complete system status"""
        
        return self.capabilities_engine.get_system_capabilities_summary()
    
    def batch_process(
        self,
        requests: List[str]
    ) -> Dict[str, Any]:
        """Process multiple requests in batch"""
        
        logger.info(f"Processing batch of {len(requests)} requests")
        
        results = {
            "total": len(requests),
            "completed": 0,
            "successful": 0,
            "responses": []
        }
        
        for request in requests:
            response = self.do(request)
            results["responses"].append(response)
            results["completed"] += 1
            
            if response.get("success"):
                results["successful"] += 1
        
        return results


# Global instance
_ai: Optional[UniversalAIInterface] = None


def get_universal_ai() -> UniversalAIInterface:
    """Get or create universal AI interface"""
    global _ai
    if _ai is None:
        _ai = UniversalAIInterface()
    return _ai
