"""
Main entry point for the Self-Evolving AI System
"""
import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.infrastructure.logger import logger
from src.integration.autonomous_agent import AutonomousAgent

def main():
    """Main entry point"""
    logger.info(" Starting Self-Evolving AI System")
    logger.info(f"Configuration: {config.PROJECT_ROOT}")
    
    try:
        # Initialize agent
        agent = AutonomousAgent()
        
        # Set autonomous goals
        agent.reasoning.set_goal(
            goal_name="Continuous Learning",
            description="Acquire knowledge from web sources and improve understanding",
            priority=0.9
        )
        
        agent.reasoning.set_goal(
            goal_name="Skill Development",
            description="Develop and improve specialized skills in various domains",
            priority=0.8
        )
        
        agent.reasoning.set_goal(
            goal_name="Knowledge Integration",
            description="Integrate learned knowledge for better reasoning and planning",
            priority=0.8
        )
        
        # Run autonomous loop
        if config.AUTONOMOUS_MODE_ENABLED:
            logger.info(" Running in AUTONOMOUS mode")
            max_iterations = int(input("Enter max iterations (default 100): ") or "100")
            asyncio.run(agent.autonomous_loop(max_iterations=int(max_iterations)))
        else:
            logger.info(" Running in INTERACTIVE mode")
            interactive_mode(agent)
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

def interactive_mode(agent):
    """Interactive mode for user interaction"""
    logger.info("\n" + "=" * 60)
    logger.info("INTERACTIVE MODE")
    logger.info("=" * 60)
    logger.info("Commands:")
    logger.info("  learn    - Run learning cycle")
    logger.info("  crawl    - Run crawling cycle")
    logger.info("  reason   - Run reasoning cycle")
    logger.info("  improve  - Run improvement cycle")
    logger.info("  query    - Ask a question")
    logger.info("  status   - Show agent status")
    logger.info("  auto     - Run autonomous loop")
    logger.info("  exit     - Exit program")
    logger.info("=" * 60 + "\n")
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "exit":
                logger.info(" Goodbye!")
                break
            
            elif command == "learn":
                asyncio.run(agent.learn_cycle())
            
            elif command == "crawl":
                asyncio.run(agent.crawl_cycle())
            
            elif command == "reason":
                agent.reasoning_cycle()
            
            elif command == "improve":
                agent.improvement_cycle()
            
            elif command == "query":
                question = input("Enter your question: ")
                response = agent.query(question)
                logger.info(f"Response: {response}")
            
            elif command == "status":
                print_status(agent)
            
            elif command == "auto":
                iterations = int(input("Enter iterations (default 20): ") or "20")
                asyncio.run(agent.autonomous_loop(max_iterations=iterations))
            
            else:
                logger.warning(f"Unknown command: {command}")
        
        except KeyboardInterrupt:
            logger.info("\n Command interrupted")
        except Exception as e:
            logger.error(f"Error: {e}")

def print_status(agent):
    """Print agent status"""
    logger.info("\n" + "=" * 60)
    logger.info("AGENT STATUS")
    logger.info("=" * 60)
    
    kb_stats = agent.kb.get_statistics()
    mem_stats = agent.memory.get_memory_statistics()
    reasoning_stats = agent.reasoning.get_reasoning_stats()
    
    logger.info(f"\n Knowledge Base: {kb_stats['total_entries']} entries")
    logger.info(f" Memory: {mem_stats['long_term_entries']} long-term, {mem_stats['episodic_entries']} episodes")
    logger.info(f" Success rate: {reasoning_stats['success_rate']:.2%}")
    logger.info(f" Goals: {len(agent.reasoning.goals)}")
    logger.info(f" Skills: {len(agent.capabilities)}")
    logger.info(f" Iterations: {agent.iteration_count}")
    
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
