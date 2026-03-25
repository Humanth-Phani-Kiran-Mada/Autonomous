"""
Request Processing Engine: NLP-based autonomous request interpretation

Converts natural language requests into executable tasks

Features:
- Parse user requests
- Detect task type automatically
- Extract parameters
- Handle complex workflows
- Learn from request patterns
"""
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import re

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import config
from src.logger import logger
from src.task_management_engine import (
    TaskType, TaskManagementEngine, Task, TaskExecutor
)


@dataclass
class ParsedRequest:
    """Parsed natural language request"""
    original: str
    detected_tasks: List[TaskType]
    primary_task: TaskType
    
    intent: str  # What user wants
    context: Dict[str, Any]  # Context information
    entities: Dict[str, Any]  # Extracted entities
    parameters: Dict[str, Any]  # Task parameters
    
    confidence: float  # Parsing confidence 0-1


class RequestParser:
    """Parse natural language requests into tasks"""
    
    # Keyword mappings
    KEYWORDS: Dict[TaskType, List[str]] = {
        TaskType.CODE_GENERATION: [
            "generate code", "write code", "create function", "build script",
            "write program", "code", "function", "algorithm", "implement",
            "write a", "create a", "develop"
        ],
        TaskType.IMAGE_GENERATION: [
            "generate image", "create image", "draw", "image", "picture",
            "visual", "photo", "render", "create visual"
        ],
        TaskType.VIDEO_GENERATION: [
            "generate video", "create video", "make video", "video", "animation",
            "render video", "movie", "scene"
        ],
        TaskType.DATA_ANALYSIS: [
            "analyze", "analyze data", "data analysis", "insights", "statistics",
            "summary", "report", "extraction", "process data"
        ],
        TaskType.TEXT_PROCESSING: [
            "process text", "summarize", "translate", "rewrite", "text",
            "transform", "convert", "parse text"
        ],
        TaskType.AUDIO_GENERATION: [
            "generate audio", "text to speech", "audio", "voice", "narrate",
            "speech", "sound"
        ],
        TaskType.RESEARCH: [
            "research", "find information", "look up", "search", "investigate",
            "find", "gather information", "explore"
        ],
        TaskType.OPTIMIZATION: [
            "optimize", "improve", "faster", "better", "enhance", "speed up",
            "performance", "efficiency"
        ],
        TaskType.TESTING: [
            "test", "validate", "verify", "check", "unit test", "integration test",
            "quality", "qa"
        ],
        TaskType.DEPLOYMENT: [
            "deploy", "release", "launch", "publish", "upload", "build",
            "compile", "package"
        ]
    }
    
    def __init__(self):
        self.request_history: List[ParsedRequest] = []
        logger.info("✓ Request Parser initialized")
    
    def parse_request(self, request: str) -> ParsedRequest:
        """Parse a natural language request"""
        
        logger.info(f"Parsing request: {request[:100]}")
        
        request_lower = request.lower()
        
        # Detect task types
        detected = self._detect_task_types(request_lower)
        
        if not detected:
            detected = [TaskType.CUSTOM]
        
        primary = detected[0] if detected else TaskType.CUSTOM
        
        # Extract intent
        intent = self._extract_intent(request_lower)
        
        # Extract entities
        entities = self._extract_entities(request)
        
        # Extract parameters
        parameters = self._extract_parameters(request, primary)
        
        # Calculate confidence
        confidence = len(detected) / 11.0 + (0.5 if intent else 0)
        confidence = min(1.0, confidence)
        
        parsed = ParsedRequest(
            original=request,
            detected_tasks=detected,
            primary_task=primary,
            intent=intent,
            context={
                "length": len(request),
                "complexity": self._estimate_complexity(request)
            },
            entities=entities,
            parameters=parameters,
            confidence=confidence
        )
        
        self.request_history.append(parsed)
        
        return parsed
    
    def _detect_task_types(self, text: str) -> List[TaskType]:
        """Detect task types from text"""
        
        detected = []
        
        for task_type, keywords in self.KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    if task_type not in detected:
                        detected.append(task_type)
                    break
        
        return detected
    
    def _extract_intent(self, text: str) -> str:
        """Extract user intent"""
        
        intents = {
            "creation": ["create", "generate", "build", "make", "write"],
            "analysis": ["analyze", "analyze", "check", "examine", "review"],
            "optimization": ["optimize", "improve", "speed", "enhance"],
            "learning": ["learn", "understand", "explain", "teach"],
            "automation": ["automate", "batch", "script", "flow"]
        }
        
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in text:
                    return intent
        
        return "action"
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract named entities"""
        
        entities = {
            "languages": [],
            "frameworks": [],
            "file_types": [],
            "parameters": {}
        }
        
        # Language detection
        languages = ["python", "javascript", "java", "c++", "rust", "go", "ruby"]
        for lang in languages:
            if lang in text.lower():
                entities["languages"].append(lang)
        
        # Framework detection
        frameworks = ["react", "django", "flask", "fastapi", "express", "vue"]
        for fw in frameworks:
            if fw in text.lower():
                entities["frameworks"].append(fw)
        
        # File type detection
        extensions = [
            ".py", ".js", ".ts", ".java", ".cpp", ".rs", ".go", ".rb",
            ".png", ".jpg", ".mp4", ".mp3", ".pdf"
        ]
        for ext in extensions:
            if ext in text.lower():
                entities["file_types"].append(ext)
        
        return entities
    
    def _extract_parameters(
        self, 
        text: str, 
        task_type: TaskType
    ) -> Dict[str, Any]:
        """Extract task-specific parameters"""
        
        params = {}
        
        if task_type == TaskType.CODE_GENERATION:
            # Language
            languages = ["python", "javascript", "java", "c++", "rust", "go"]
            for lang in text.lower().split():
                if lang in languages:
                    params["language"] = lang
                    break
            if "language" not in params:
                params["language"] = "python"
            
            # Get spec from text
            parts = text.split("to ")
            if len(parts) > 1:
                params["specification"] = parts[-1][:200]
            else:
                params["specification"] = text[:200]
        
        elif task_type == TaskType.IMAGE_GENERATION:
            params["description"] = text[:250]
            
            # Style detection
            styles = ["realistic", "abstract", "cartoon", "oil painting", "digital"]
            for style in styles:
                if style in text.lower():
                    params["style"] = style
                    break
            
            # Size
            if "large" in text.lower():
                params["size"] = "1024x1024"
            elif "small" in text.lower():
                params["size"] = "256x256"
            else:
                params["size"] = "512x512"
        
        elif task_type == TaskType.VIDEO_GENERATION:
            params["scene_description"] = text[:250]
            
            # Duration
            import re
            duration_match = re.search(r'(\d+)\s*(?:second|sec|s)', text.lower())
            params["duration"] = int(duration_match.group(1)) if duration_match else 30
            
            params["fps"] = 30
        
        elif task_type == TaskType.DATA_ANALYSIS:
            params["type"] = "summary"
            params["data"] = []
        
        elif task_type == TaskType.TEXT_PROCESSING:
            params["operation"] = self._detect_text_operation(text)
            params["text"] = text[:500]
        
        elif task_type == TaskType.AUDIO_GENERATION:
            params["text"] = text[:500]
            params["voice"] = "default"
        
        return params
    
    def _detect_text_operation(self, text: str) -> str:
        """Detect text processing operation"""
        
        text_lower = text.lower()
        
        if "summarize" in text_lower:
            return "summarize"
        elif "translate" in text_lower:
            return "translate"
        elif "rewrite" in text_lower:
            return "rewrite"
        elif "extract" in text_lower:
            return "extract"
        else:
            return "process"
    
    def _estimate_complexity(self, text: str) -> str:
        """Estimate request complexity"""
        
        word_count = len(text.split())
        
        if word_count < 10:
            return "simple"
        elif word_count < 50:
            return "medium"
        else:
            return "complex"


class RequestDispatcher:
    """
    Dispatch parsed requests to task management
    
    Handles:
    - Request routing
    - Multi-task workflows
    - Error handling
    - Response formatting
    """
    
    def __init__(self):
        self.parser = RequestParser()
        self.task_engine = TaskManagementEngine()
        self.execution_history: List[Dict[str, Any]] = []
        
        logger.info("✓ Request Dispatcher initialized")
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """Process a natural language request end-to-end"""
        
        logger.info(f"Processing request: {request[:100]}")
        
        # Parse request
        parsed = self.parser.parse_request(request)
        
        logger.info(f"Detected task type: {parsed.primary_task.value}")
        
        # Create task
        task = self.task_engine.create_task(
            task_type=parsed.primary_task,
            title=f"Auto: {parsed.primary_task.value}",
            description=request[:200],
            request=parsed.parameters
        )
        
        # Execute task immediately
        results = self.task_engine.process_tasks(max_tasks=1)
        
        # Get the executed task
        executed_task = (
            self.task_engine.completed_tasks[-1]
            if self.task_engine.completed_tasks
            else None
        )
        
        response = {
            "request": request,
            "parsed": {
                "task_type": parsed.primary_task.value,
                "intent": parsed.intent,
                "confidence": parsed.confidence
            },
            "execution": results,
            "output": executed_task.output if executed_task else None,
            "success": executed_task.success if executed_task else False
        }
        
        self.execution_history.append(response)
        
        return response
    
    def process_multiple_requests(
        self, 
        requests: List[str]
    ) -> Dict[str, Any]:
        """Process multiple requests as a workflow"""
        
        logger.info(f"Processing workflow with {len(requests)} requests")
        
        results = {
            "total_requests": len(requests),
            "completed": 0,
            "successful": 0,
            "responses": []
        }
        
        for request in requests:
            response = self.process_request(request)
            results["responses"].append(response)
            results["completed"] += 1
            
            if response["success"]:
                results["successful"] += 1
        
        return results
    
    def get_dispatcher_status(self) -> Dict[str, Any]:
        """Get dispatcher status"""
        
        return {
            "requests_processed": len(self.execution_history),
            "task_queue_status": self.task_engine.get_task_status(),
            "learning": self.task_engine.get_learning_summary()
        }


# Global instance
_dispatcher: Optional[RequestDispatcher] = None


def get_request_dispatcher() -> RequestDispatcher:
    """Get or create request dispatcher"""
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = RequestDispatcher()
    return _dispatcher
