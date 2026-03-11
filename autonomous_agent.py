"""
Main Autonomous Agent - The self-evolving AI system with advanced self-improvement
"""
import asyncio
import json
from typing import Callable, Dict, List, Any
from datetime import datetime
import config
from src.logger import logger
from src.web_crawler import WebCrawler
from src.knowledge_base import KnowledgeBase
from src.memory_manager import MemoryManager
from src.learning_engine import LearningEngine
from src.reasoning_engine import ReasoningEngine
from src.self_model import SelfModel
from src.meta_learner import MetaLearner
from src.bayesian_reasoner import BayesianReasoner
from src.autonomous_goal_generator import AutonomousGoalGenerator
from src.introspection_engine import IntrospectionEngine
from src.memory_consolidation import MemoryConsolidation
from src.error_recovery import ErrorRecoverySystem

class AutonomousAgent:
    """
    Self-Evolving AI Agent with advanced autonomous learning and self-improvement.
    Integrates self-awareness, meta-learning, Bayesian reasoning, and introspection.
    """
    
    def __init__(self):
        logger.info("=" * 60)
        logger.info("🤖 INITIALIZING ADVANCED SELF-EVOLVING AI AGENT")
        logger.info("=" * 60)
        
        # Initialize core components
        self.kb = KnowledgeBase()
        self.memory = MemoryManager()
        self.learning = LearningEngine(self.kb, self.memory)
        self.reasoning = ReasoningEngine(self.kb, self.memory, self.learning)
        self.crawler = WebCrawler()
        
        # Initialize advanced systems
        self.self_model = SelfModel()
        self.bayesian_reasoner = BayesianReasoner()
        self.meta_learner = MetaLearner(self.learning, self.self_model)
        self.goal_generator = AutonomousGoalGenerator(self.self_model, self.learning)
        self.introspection = IntrospectionEngine(self.self_model, self.bayesian_reasoner)
        self.memory_consolidation = MemoryConsolidation(self.memory)
        self.error_recovery = ErrorRecoverySystem(self.self_model, self.bayesian_reasoner)
        
        # Agent state
        self.is_running = False
        self.iteration_count = 0
        self.state_file = config.DATA_DIR / "agent_state.json"
        self.capabilities: Dict[str, float] = {}
        
        # Initialize self-model with capabilities
        self._register_core_capabilities()
        
        # Advanced action registry
        self.actions: Dict[str, Callable] = {
            "crawl": self.crawl_cycle,
            "learn": self.learn_cycle,
            "consolidate_memory": self.memory_consolidation_cycle,
            "generate_goals": self.autonomous_goal_generation_cycle,
            "introspect": self.introspection_cycle,
            "reason": self.reasoning_cycle,
            "improve": self.improvement_cycle,
            "maintain": self.maintenance_cycle
        }
        
        self.load_state()
        logger.info("✅ Advanced Autonomous Agent ready for operation")
        logger.info("🧠 Advanced systems: Self-Model, Meta-Learning, Bayesian Reasoning, Introspection")
        logger.info(f"Autonomous Mode: {'ENABLED' if config.AUTONOMOUS_MODE_ENABLED else 'DISABLED'}")
    
    def _register_core_capabilities(self):
        """Register core AI capabilities in self-model"""
        core_capabilities = [
            ("web_crawling", 0.7, "information_gathering", "Autonomous web crawling and content discovery"),
            ("knowledge_management", 0.6, "information_management", "Knowledge base organization and retrieval"),
            ("learning", 0.5, "cognitive", "Learning from new information"),
            ("reasoning", 0.5, "cognitive", "Logical reasoning and planning"),
            ("goal_generation", 0.3, "autonomy", "Autonomous goal creation"),
            ("self_improvement", 0.4, "meta_cognitive", "Self-driven capability enhancement"),
            ("introspection", 0.5, "meta_cognitive", "Self-analysis and awareness"),
            ("error_recovery", 0.6, "resilience", "Recovery from failures"),
            ("memory_management", 0.7, "cognitive", "Multi-type memory management"),
            ("adaptation", 0.4, "learning", "Adaptation to new domains")
        ]
        
        for cap_name, level, domain, description in core_capabilities:
            self.self_model.register_capability(cap_name, level, domain, description)
            self.capabilities[cap_name] = level
    
    
    def load_state(self):
        """Load agent state from disk"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.iteration_count = state.get("iteration_count", 0)
                    self.capabilities = state.get("capabilities", {})
                    logger.info(f"📂 Loaded agent state: {self.iteration_count} iterations")
        except Exception as e:
            logger.error(f"Error loading agent state: {e}")
    
    def save_state(self):
        """Save agent state to disk"""
        try:
            state = {
                "iteration_count": self.iteration_count,
                "capabilities": self.capabilities,
                "last_saved": datetime.now().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving agent state: {e}")
    
    async def learn_cycle(self):
        """Learning cycle - acquire and process new knowledge"""
        logger.info("\n" + "=" * 60)
        logger.info("📚 LEARNING CYCLE")
        logger.info("=" * 60)
        
        try:
            # Crawl web for new knowledge
            knowledge_items = await self.crawler.crawl_sources(max_pages=20)
            
            if knowledge_items:
                # Process and learn from each item
                for item in knowledge_items[:10]:  # Limit to top 10 per cycle
                    # Add to knowledge base
                    knowledge_id = self.kb.add_knowledge(
                        content=item.get("content", "")[:500],
                        source=item.get("source", "unknown"),
                        knowledge_type=item.get("type", "general"),
                        metadata={"discovered_at": datetime.now().isoformat()}
                    )
                    
                    # Learn from the knowledge
                    learning_result = self.learning.learn_from_knowledge({
                        "id": knowledge_id,
                        "content": item.get("content", ""),
                        "source": item.get("source", ""),
                        "type": item.get("type", "")
                    })
                    
                    logger.info(f"✅ Processed knowledge: {learning_result['categories']}")
            
            # Save knowledge base
            self.kb.save_knowledge_base()
            
            logger.info(f"📈 Learning cycle complete - {len(knowledge_items)} items processed")
            return {"status": "success", "items_processed": len(knowledge_items)}
        
        except Exception as e:
            logger.error(f"Error in learning cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    async def crawl_cycle(self):
        """Crawling cycle - discover new resources"""
        logger.info("\n" + "=" * 60)
        logger.info("🕷️ CRAWLING CYCLE")
        logger.info("=" * 60)
        
        try:
            # Get crawler summary before
            before_summary = self.crawler.get_discovery_summary()
            
            # Perform crawling
            knowledge_items = await self.crawler.crawl_sources(max_pages=30)
            
            # Get summary after
            after_summary = self.crawler.get_discovery_summary()
            
            logger.info(f"🔍 Crawling Results:")
            logger.info(f"   URLs visited: {before_summary['total_visited_urls']} → {after_summary['total_visited_urls']}")
            logger.info(f"   Knowledge discovered: {len(knowledge_items)} items")
            logger.info(f"   Knowledge types: {after_summary['knowledge_types']}")
            
            return {"status": "success", "summary": after_summary}
        
        except Exception as e:
            logger.error(f"Error in crawling cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    def improvement_cycle(self):
        """Self-improvement cycle - enhance capabilities"""
        logger.info("\n" + "=" * 60)
        logger.info("🚀 IMPROVEMENT CYCLE")
        logger.info("=" * 60)
        
        try:
            # Analyze learning patterns
            learning_summary = self.learning.get_learning_summary()
            
            # Improve key skills
            improvements = {}
            for domain in learning_summary.get("most_learned_domains", []):
                domain_name = domain[0] if isinstance(domain, tuple) else domain
                
                # Simulate improvement
                improvement = self.learning.improve_skill(
                    domain_name,
                    [{"success": True} for _ in range(5)]
                )
                improvements[domain_name] = improvement
                
                # Update capabilities
                self.capabilities[domain_name] = improvement["new_level"]
            
            logger.info(f"📊 Improved {len(improvements)} capabilities")
            for skill, result in improvements.items():
                logger.info(f"   {skill}: {result['old_level']:.2%} → {result['new_level']:.2%}")
            
            return {"status": "success", "improvements": improvements}
        
        except Exception as e:
            logger.error(f"Error in improvement cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    def reasoning_cycle(self):
        """Reasoning cycle - analyze and plan"""
        logger.info("\n" + "=" * 60)
        logger.info("💭 REASONING CYCLE")
        logger.info("=" * 60)
        
        try:
            # Reason about different topics
            topics = ["self-improvement", "knowledge acquisition", "problem solving"]
            reasoning_results = []
            
            for topic in topics:
                result = self.reasoning.reason_about(topic, {})
                reasoning_results.append(result)
                logger.info(f"✅ Reasoned about '{topic}' - confidence: {result['confidence']:.2%}")
            
            # Get reasoning statistics
            stats = self.reasoning.get_reasoning_stats()
            logger.info(f"📈 Reasoning Statistics:")
            logger.info(f"   Total actions: {stats['total_actions']}")
            logger.info(f"   Success rate: {stats['success_rate']:.2%}")
            
            return {"status": "success", "results": reasoning_results, "stats": stats}
        
        except Exception as e:
            logger.error(f"Error in reasoning cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    def maintenance_cycle(self):
        """Maintenance cycle - clean and optimize"""
        logger.info("\n" + "=" * 60)
        logger.info("🔧 MAINTENANCE CYCLE")
        logger.info("=" * 60)
        
        try:
            # Save all persistent data
            self.memory.save_memory()
            self.kb.save_knowledge_base()
            self.learning.save_metrics()
            self.reasoning.save_goals()
            self.save_state()
            
            # Get statistics
            kb_stats = self.kb.get_statistics()
            mem_stats = self.memory.get_memory_statistics()
            
            logger.info("✅ All data persisted successfully")
            logger.info(f"📊 Knowledge Base: {kb_stats['total_entries']} entries")
            logger.info(f"🧠 Memory: {mem_stats['long_term_entries']} long-term, {mem_stats['episodic_entries']} episodes")
            
            return {
                "status": "success",
                "kb_stats": kb_stats,
                "memory_stats": mem_stats
            }
        
        except Exception as e:
            logger.error(f"Error in maintenance cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    def memory_consolidation_cycle(self):
        """Memory consolidation cycle - prevent catastrophic forgetting"""
        logger.info("\n" + "=" * 60)
        logger.info("🧠 MEMORY CONSOLIDATION CYCLE")
        logger.info("=" * 60)
        
        try:
            # Consolidate important memories
            long_term = self.memory.long_term_memory
            for key, entry in list(long_term.items())[:10]:
                self.memory_consolidation.consolidate_memory(
                    key, entry.get("value"), entry.get("importance", 0.5)
                )
            
            # Perform pending rehearsals
            rehearsal_tasks = self.memory_consolidation.get_rehearsal_tasks(due_within_days=7)
            rehearsals_done = 0
            
            for task in rehearsal_tasks[:5]:  # Limit to 5 per cycle
                self.memory_consolidation.perform_rehearsal(
                    task["memory_key"],
                    task["rehearsal_number"]
                )
                rehearsals_done += 1
            
            consolidation_summary = self.memory_consolidation.get_consolidation_summary()
            
            logger.info(f"✅ Memory consolidation complete")
            logger.info(f"   Rehearsals performed: {rehearsals_done}")
            logger.info(f"   High-stability memories: {consolidation_summary['high_stability_memories']}")
            
            return {"status": "success", "rehearsals": rehearsals_done, "summary": consolidation_summary}
        
        except Exception as e:
            logger.error(f"Error in memory consolidation cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    def autonomous_goal_generation_cycle(self):
        """Autonomous goal generation - create new goals based on state"""
        logger.info("\n" + "=" * 60)
        logger.info("🎯 AUTONOMOUS GOAL GENERATION CYCLE")
        logger.info("=" * 60)
        
        try:
            # Generate new goals
            new_goals = self.goal_generator.generate_goals_autonomously()
            
            # Get active goals
            active_goals = self.goal_generator.get_active_goals()
            
            logger.info(f"✅ Goal generation complete")
            logger.info(f"   New goals generated: {len(new_goals)}")
            logger.info(f"   Active goals: {len(active_goals)}")
            
            if active_goals:
                logger.info("   Top goals by priority:")
                for goal in active_goals[:3]:
                    logger.info(f"      - {goal['name']} (priority={goal.get('priority', 0):.1%})")
            
            return {"status": "success", "new_goals": len(new_goals), "active_goals": len(active_goals)}
        
        except Exception as e:
            logger.error(f"Error in goal generation cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    def introspection_cycle(self):
        """Introspection cycle - self-awareness and analysis"""
        logger.info("\n" + "=" * 60)
        logger.info("🔍 INTROSPECTION CYCLE")
        logger.info("=" * 60)
        
        try:
            # Run self-evaluation
            evaluation = self.introspection.self_evaluate()
            
            # Detect potential biases
            context = {"recent_decisions": len(self.reasoning.decision_log)}
            biases = self.introspection.detect_cognitive_bias(context)
            
            # Run self-diagnostics
            diagnostics = self.self_model.run_self_diagnostics()
            
            logger.info(f"✅ Introspection complete")
            logger.info(f"   Overall score: {evaluation['overall_score']:.1%}")
            logger.info(f"   Biases detected: {len(biases)}")
            logger.info(f"   Diagnostics status: {diagnostics['capability_health']['status']}")
            
            return {
                "status": "success",
                "evaluation": evaluation,
                "biases": biases,
                "diagnostics": diagnostics
            }
        
        except Exception as e:
            logger.error(f"Error in introspection cycle: {e}")
            return {"status": "error", "error": str(e)}
    
    async def autonomous_loop(self, max_iterations: int = 100):
        """Main autonomous evolution loop with advanced capabilities"""
        logger.info("\n" + "🔄" * 30)
        logger.info("STARTING ADVANCED AUTONOMOUS EVOLUTION LOOP")
        logger.info("🔄" * 30)
        
        self.is_running = True
        
        # Enhanced cycle order incorporating new systems
        cycle_order = [
            "crawl",                    # Acquire new knowledge
            "learn",                    # Learn from knowledge
            "consolidate_memory",       # Prevent forgetting
            "introspect",               # Analyze own state
            "generate_goals",           # Create autonomous goals
            "reason",                   # Reasoned planning
            "improve",                  # Self-improvement
            "maintain"                  # Save state
        ]
        
        try:
            while self.is_running and self.iteration_count < max_iterations:
                self.iteration_count += 1
                logger.info(f"\n🔁 EVOLUTION ITERATION {self.iteration_count}/{max_iterations}")
                logger.info("=" * 60)
                
                # Execute cycles in order
                cycle_results = {}
                for cycle_name in cycle_order:
                    try:
                        if cycle_name in ["crawl", "learn"]:
                            result = await self.actions[cycle_name]()
                        else:
                            result = self.actions[cycle_name]()
                        
                        cycle_results[cycle_name] = result.get("status", "unknown")
                        logger.info(f"   ✅ {cycle_name.upper()}: {result.get('status', 'unknown')}")
                    
                    except Exception as e:
                        cycle_results[cycle_name] = "error"
                        logger.error(f"   ❌ Error in {cycle_name}: {e}")
                        
                        # Use error recovery
                        self.error_recovery.handle_error(
                            error=e,
                            context={"capability": cycle_name},
                            recovery_function=lambda: {"recovered": True}
                        )
                
                logger.info(f"✅ Iteration {self.iteration_count} complete - {sum(1 for s in cycle_results.values() if s == 'success')}/{len(cycle_order)} cycles successful")
                
                # Save state periodically
                if self.iteration_count % 5 == 0:
                    self.save_state()
                    self.self_model.save_self_model()
                    self.bayesian_reasoner.save_beliefs()
                    self.memory_consolidation.save_consolidation_state()
            
            logger.info("\n✅ Autonomous evolution loop completed successfully")
            self.print_final_summary()
        
        except KeyboardInterrupt:
            logger.info("\n⏸️ Loop interrupted by user")
        except Exception as e:
            logger.error(f"Fatal error in autonomous loop: {e}")
        finally:
            self.is_running = False
            self.save_state()
            self.introspection.save_introspection_data()

    
    def print_final_summary(self):
        """Print comprehensive final summary with advanced metrics"""
        logger.info("\n" + "=" * 80)
        logger.info("🎓 ADVANCED AUTONOMOUS EVOLUTION SUMMARY")
        logger.info("=" * 80)
        
        # Knowledge summary
        kb_stats = self.kb.get_statistics()
        logger.info(f"\n📚 KNOWLEDGE BASE:")
        logger.info(f"   Total entries: {kb_stats['total_entries']}")
        logger.info(f"   Type distribution: {kb_stats['types']}")
        logger.info(f"   Sources: {len(kb_stats['sources'])} different")
        
        # Learning summary
        learning_summary = self.learning.get_learning_summary()
        logger.info(f"\n🎓 LEARNING PROGRESS:")
        logger.info(f"   Learning events: {learning_summary['total_learning_events']}")
        logger.info(f"   Patterns discovered: {learning_summary['patterns_learned']}")
        logger.info(f"   Skills developed: {len(self.capabilities)}")
        
        # Self-Model Summary
        self_model_summary = self.self_model.get_self_model_summary()
        logger.info(f"\n🔍 SELF-MODEL STATE:")
        logger.info(f"   Registered capabilities: {self_model_summary['capabilities_count']}")
        logger.info(f"   Active capabilities: {self_model_summary['active_capabilities']}")
        logger.info(f"   Average confidence: {self_model_summary['average_confidence']:.1%}")
        logger.info(f"   Limitations detected: {self_model_summary['limitations_count']}")
        
        # Meta-Learning Summary
        meta_summary = self.meta_learner.get_meta_learning_summary()
        logger.info(f"\n🧠 META-LEARNING:")
        logger.info(f"   Learning strategies: {meta_summary['strategies_count']}")
        logger.info(f"   Domain experts: {meta_summary['domain_experts']}")
        logger.info(f"   Strategy history: {meta_summary['strategy_history_size']} entries")
        logger.info(f"   Top strategy: {meta_summary['top_strategy']}")
        
        # Bayesian Reasoning Summary
        bayesian_summary = self.bayesian_reasoner.get_bayesian_summary()
        logger.info(f"\n🎯 BAYESIAN REASONING:")
        logger.info(f"   Beliefs maintained: {bayesian_summary['beliefs_count']}")
        logger.info(f"   Evidence processed: {bayesian_summary['evidence_count']}")
        logger.info(f"   Inferences made: {bayesian_summary['inferences_made']}")
        logger.info(f"   Avg belief confidence: {bayesian_summary['average_belief_confidence']:.1%}")
        
        # Goal Generation Summary
        goal_summary = self.goal_generator.get_goal_generation_summary()
        logger.info(f"\n🎯 AUTONOMOUS GOALS:")
        logger.info(f"   Total generated: {goal_summary['total_generated']}")
        logger.info(f"   Currently active: {goal_summary['active_goals']}")
        logger.info(f"   Completed: {goal_summary['completed_goals']}")
        
        # Memory Summary
        mem_stats = self.memory.get_memory_statistics()
        logger.info(f"\n🧠 MEMORY SYSTEM:")
        logger.info(f"   Long-term entries: {mem_stats['long_term_entries']}")
        logger.info(f"   Episodic entries: {mem_stats['episodic_entries']}")
        logger.info(f"   Short-term entries: {mem_stats['short_term_entries']}")
        
        # Memory Consolidation Summary
        consolidation_summary = self.memory_consolidation.get_consolidation_summary()
        logger.info(f"   Memories consolidated: {consolidation_summary['memories_in_consolidation']}")
        logger.info(f"   High-stability memories: {consolidation_summary['high_stability_memories']}")
        
        # Introspection Summary
        intro_summary = self.introspection.get_introspection_summary()
        logger.info(f"\n🔍 INTROSPECTION:")
        logger.info(f"   Reasoning traces: {intro_summary['reasoning_traces']}")
        logger.info(f"   Pattern categories: {intro_summary['pattern_categories']}")
        logger.info(f"   Anomalies detected: {intro_summary['anomalies_detected']}")
        logger.info(f"   Biases identified: {intro_summary['biases_identified']}")
        
        # Error Recovery Summary
        recovery_stats = self.error_recovery.get_recovery_stats()
        logger.info(f"\n🛡️ ERROR RECOVERY:")
        logger.info(f"   Total errors: {recovery_stats['total_errors']}")
        logger.info(f"   Successfully recovered: {recovery_stats['recovered_errors']}")
        logger.info(f"   Recovery rate: {recovery_stats['recovery_rate']:.1%}")
        
        # Reasoning summary
        reasoning_stats = self.reasoning.get_reasoning_stats()
        logger.info(f"\n💭 REASONING STATISTICS:")
        logger.info(f"   Total actions: {reasoning_stats['total_actions']}")
        logger.info(f"   Success rate: {reasoning_stats['success_rate']:.1%}")
        logger.info(f"   Decisions made: {reasoning_stats['decisions_made']}")
        logger.info(f"   Active goals: {reasoning_stats['total_goals']}")
        
        logger.info(f"\n🔄 EVOLUTION STATISTICS:")
        logger.info(f"   Total iterations: {self.iteration_count}")
        logger.info("=" * 80)
    
    def query(self, question: str) -> Dict[str, Any]:
        """Query the AI agent about something"""
        logger.info(f"\n❓ Query: {question}")
        
        # Search knowledge base
        knowledge = self.kb.search(question, top_k=3)
        
        # Reason about the question
        reasoning = self.reasoning.reason_about(question, {})
        
        response = {
            "question": question,
            "relevant_knowledge": [k.get("content", "")[:150] for k in knowledge],
            "reasoning": reasoning.get("insights", []),
            "confidence": reasoning.get("confidence", 0),
            "next_questions": reasoning.get("next_questions", [])
        }
        
        logger.info(f"✅ Query processed - confidence: {response['confidence']:.2%}")
        return response
