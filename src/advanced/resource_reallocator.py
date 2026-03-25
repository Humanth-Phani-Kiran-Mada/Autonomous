"""
Resource Reallocator: Dynamic resource rebalancing

Enables system to:
- Monitor resource utilization per component
- Rebalance allocation dynamically
- Respond to changing demand patterns
- Optimize for throughput/latency trade-offs
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import config
from logger import logger


class ResourceType(Enum):
    """Types of resources"""
    CPU = "cpu"
    MEMORY = "memory"
    CONNECTIONS = "connections"
    DISK_IO = "disk_io"
    NETWORK = "network"


@dataclass
class ResourceAllocation:
    """Resource allocation to a component"""
    component: str
    resource_type: ResourceType
    
    allocated: float  # Amount allocated
    max_allowed: float  # Hard limit
    priority: int  # 1-10, higher = more critical
    
    # Usage tracking
    current_usage: float = 0.0
    peak_usage: float = 0.0
    avg_usage: float = 0.0
    
    # History
    last_updated: datetime = field(default_factory=datetime.now)
    utilization_history: List[float] = field(default_factory=list)
    
    @property
    def utilization(self) -> float:
        """Calculate current utilization %"""
        if self.allocated == 0:
            return 0.0
        return min(100.0, (self.current_usage / self.allocated) * 100)
    
    @property
    def efficiency(self) -> float:
        """Efficiency score (0-1)"""
        # Good efficiency = high usage without hitting limits
        if self.current_usage >= self.allocated * 0.95:
            return 0.0  # About to saturate
        elif self.current_usage < self.allocated * 0.1:
            return 0.0  # Underutilized
        else:
            return self.current_usage / self.allocated


@dataclass
class ReallocationRequest:
    """Request to reallocate resources"""
    request_id: str
    component: str
    resource_type: ResourceType
    
    reason: str
    delta: float  # Amount to increase/decrease
    
    created_at: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    approved: bool = False


class ResourceReallocator:
    """
    Dynamic resource rebalancing engine
    
    Features:
    - Track component resource usage
    - Detect over/under utilization
    - Propose reallocations
    - Monitor allocation changes
    """
    
    def __init__(self):
        self.allocations: Dict[Tuple[str, ResourceType], ResourceAllocation] = {}
        self.requests: List[ReallocationRequest] = []
        self.reallocation_history: List[Dict[str, Any]] = []
        
        self.total_resources: Dict[ResourceType, float] = {
            ResourceType.CPU: 100.0,  # percentage
            ResourceType.MEMORY: 1024.0,  # MB
            ResourceType.CONNECTIONS: 1000,  # count
            ResourceType.DISK_IO: 1000.0,  # MB/s
            ResourceType.NETWORK: 1000.0  # Mbps
        }
        
        logger.info("✓ Resource Reallocator initialized")
    
    def initialize_allocation(
        self,
        component: str,
        resource_type: ResourceType,
        initial_allocation: float,
        priority: int = 5
    ) -> None:
        """Initialize resource allocation"""
        
        key = (component, resource_type)
        
        allocation = ResourceAllocation(
            component=component,
            resource_type=resource_type,
            allocated=initial_allocation,
            max_allowed=self.total_resources[resource_type] * 0.95,
            priority=priority
        )
        
        self.allocations[key] = allocation
        
        logger.info(f"Initialized allocation: {component}/{resource_type.value}")
        logger.info(f"  Allocated: {initial_allocation:.1f}")
        logger.info(f"  Priority: {priority}")
    
    def update_usage(
        self,
        component: str,
        resource_type: ResourceType,
        current_usage: float
    ) -> None:
        """Update current resource usage"""
        
        key = (component, resource_type)
        
        if key not in self.allocations:
            # Auto-initialize if not exists
            self.initialize_allocation(component, resource_type, current_usage * 1.5)
        
        alloc = self.allocations[key]
        alloc.current_usage = current_usage
        alloc.peak_usage = max(alloc.peak_usage, current_usage)
        
        # Update average
        alloc.utilization_history.append(current_usage)
        if len(alloc.utilization_history) > 1000:
            alloc.utilization_history = alloc.utilization_history[-1000:]
        
        alloc.avg_usage = sum(alloc.utilization_history) / len(alloc.utilization_history)
        alloc.last_updated = datetime.now()
    
    def analyze_allocations(self) -> Dict[str, Any]:
        """Analyze current allocation efficiency"""
        
        analysis = {
            "total_allocations": len(self.allocations),
            "over_allocated": [],  # Components with >80% usage
            "under_allocated": [],  # Components with <20% usage
            "saturating": [],  # Components nearing limits
            "recommendations": []
        }
        
        for key, alloc in self.allocations.items():
            util = alloc.utilization
            
            if util > 90:
                analysis["saturating"].append({
                    "component": alloc.component,
                    "resource": alloc.resource_type.value,
                    "utilization": f"{util:.1f}%",
                    "allocated": alloc.allocated
                })
            elif util > 70:
                analysis["over_allocated"].append({
                    "component": alloc.component,
                    "resource": alloc.resource_type.value,
                    "utilization": f"{util:.1f}%"
                })
            elif util < 20:
                analysis["under_allocated"].append({
                    "component": alloc.component,
                    "resource": alloc.resource_type.value,
                    "utilization": f"{util:.1f}%"
                })
        
        # Generate recommendations
        if analysis["saturating"]:
            analysis["recommendations"].append({
                "issue": "resource_saturation",
                "components": [s["component"] for s in analysis["saturating"]],
                "action": "Increase allocation to prevent throttling"
            })
        
        if analysis["under_allocated"]:
            analysis["recommendations"].append({
                "issue": "over_allocation",
                "components": [u["component"] for u in analysis["under_allocated"]],
                "action": "Reduce allocation to free resources"
            })
        
        return analysis
    
    def propose_reallocation(
        self,
        component: str,
        resource_type: ResourceType,
        reason: str
    ) -> Optional[ReallocationRequest]:
        """Propose resource reallocation"""
        
        key = (component, resource_type)
        
        if key not in self.allocations:
            logger.warning(f"Component not found: {component}/{resource_type.value}")
            return None
        
        alloc = self.allocations[key]
        
        # Determine if reallocation needed
        util = alloc.utilization
        
        if util > 85:
            # Need more resources
            delta = alloc.allocated * 0.5  # Increase by 50%
            
            # Check if available
            total_allocated = sum(
                a.allocated for a in self.allocations.values()
                if a.resource_type == resource_type
            )
            
            available = self.total_resources[resource_type] - total_allocated
            
            if available < delta:
                logger.warning(f"Insufficient resources available: need {delta}, have {available}")
                delta = available * 0.8  # Use 80% of available
        
        elif util < 15:
            # Can reduce allocation
            delta = -alloc.allocated * 0.3  # Reduce by 30%
        else:
            # Allocation is fine
            return None
        
        # Create request
        request_id = f"realloc_{len(self.requests)}"
        request = ReallocationRequest(
            request_id=request_id,
            component=component,
            resource_type=resource_type,
            reason=reason,
            delta=delta
        )
        
        self.requests.append(request)
        
        logger.info(f"Proposed reallocation: {request_id}")
        logger.info(f"  Component: {component}/{resource_type.value}")
        logger.info(f"  Current utilization: {util:.1f}%")
        logger.info(f"  Delta: {delta:.1f}")
        logger.info(f"  Reason: {reason}")
        
        return request
    
    def approve_reallocation(self, request_id: str) -> bool:
        """Approve and apply reallocation"""
        
        # Find request
        request = None
        for req in self.requests:
            if req.request_id == request_id:
                request = req
                break
        
        if not request:
            logger.error(f"Request not found: {request_id}")
            return False
        
        key = (request.component, request.resource_type)
        if key not in self.allocations:
            return False
        
        alloc = self.allocations[key]
        
        # Calculate new allocation
        new_alloc = alloc.allocated + request.delta
        new_alloc = max(alloc.current_usage * 1.1, new_alloc)  # Never below 1.1x usage
        new_alloc = min(alloc.max_allowed, new_alloc)  # Never exceed max
        
        # Apply
        old_alloc = alloc.allocated
        alloc.allocated = new_alloc
        request.approved = True
        request.processed_at = datetime.now()
        
        # Record
        self.reallocation_history.append({
            "timestamp": request.processed_at.isoformat(),
            "component": request.component,
            "resource_type": request.resource_type.value,
            "old_allocation": old_alloc,
            "new_allocation": new_alloc,
            "change": new_alloc - old_alloc,
            "reason": request.reason
        })
        
        logger.info(f"✓ Applied reallocation: {request_id}")
        logger.info(f"  {request.component}/{request.resource_type.value}")
        logger.info(f"  {old_alloc:.1f} → {new_alloc:.1f}")
        
        return True
    
    def auto_rebalance(self) -> Dict[str, Any]:
        """Automatically detect and apply reallocations"""
        
        logger.info("Starting auto-rebalancing...")
        
        analysis = self.analyze_allocations()
        
        results = {
            "analysis": analysis,
            "reallocations_approved": 0,
            "total_freed": 0.0,
            "total_allocated": 0.0
        }
        
        # Propose reallocations for saturating components
        for item in analysis.get("saturating", []):
            request = self.propose_reallocation(
                item["component"],
                ResourceType[item["resource"].upper()],
                "Resource saturation detected"
            )
            
            if request:
                # Auto-approve
                if self.approve_reallocation(request.request_id):
                    results["reallocations_approved"] += 1
                    if request.delta > 0:
                        results["total_allocated"] += request.delta
                    else:
                        results["total_freed"] += abs(request.delta)
        
        # Propose reallocations for under-allocated components
        for item in analysis.get("under_allocated", []):
            request = self.propose_reallocation(
                item["component"],
                ResourceType[item["resource"].upper()],
                "Over-allocated resource detected"
            )
            
            if request:
                if self.approve_reallocation(request.request_id):
                    results["reallocations_approved"] += 1
                    if request.delta > 0:
                        results["total_allocated"] += request.delta
                    else:
                        results["total_freed"] += abs(request.delta)
        
        logger.info(f"✓ Auto-rebalancing complete")
        logger.info(f"  Reallocations: {results['reallocations_approved']}")
        logger.info(f"  Freed: {results['total_freed']:.1f}")
        logger.info(f"  Allocated: {results['total_allocated']:.1f}")
        
        return results
    
    def get_allocation_status(self) -> Dict[str, Any]:
        """Get current allocation status"""
        
        by_resource = {}
        
        for key, alloc in self.allocations.items():
            rt = alloc.resource_type.value
            if rt not in by_resource:
                by_resource[rt] = []
            
            by_resource[rt].append({
                "component": alloc.component,
                "allocated": f"{alloc.allocated:.1f}",
                "usage": f"{alloc.current_usage:.1f}",
                "utilization": f"{alloc.utilization:.1f}%",
                "priority": alloc.priority
            })
        
        return {
            "timestamp": datetime.now().isoformat(),
            "allocations_by_resource": by_resource,
            "total_allocations": len(self.allocations),
            "pending_requests": len([r for r in self.requests if not r.approved])
        }


# Global instance
_reallocator: Optional[ResourceReallocator] = None


def get_resource_reallocator() -> ResourceReallocator:
    """Get or create resource reallocator"""
    global _reallocator
    if _reallocator is None:
        _reallocator = ResourceReallocator()
    return _reallocator
