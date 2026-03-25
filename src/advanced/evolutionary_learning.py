"""
Evolutionary Learning Engine: Discovers optimal learning strategies through evolution
Uses genetic algorithms to evolve learning parameters, strategies, and architectures.
Enables continuous discovery of better ways to learn and improve.
"""
import json
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import numpy as np
from pathlib import Path
from copy import deepcopy
import random
import config
from .logger import logger


class Individual:
    """Represents an individual learning strategy or parameter set"""
    def __init__(self, genes: Dict, strategy_type: str = "learning"):
        self.genes = genes  # Strategy parameters
        self.strategy_type = strategy_type
        self.fitness = 0.0
        self.age = 0
        self.created_at = datetime.now()
        self.effective_generations = 0
        
    def to_dict(self) -> Dict:
        return {
            "genes": self.genes,
            "strategy_type": self.strategy_type,
            "fitness": self.fitness,
            "age": self.age
        }


class EvolutionaryLearningEngine:
    """
    Evolves learning strategies, parameters, and even architectural elements
    through population-based search. Discovers optimal approaches for
    different types of learning challenges.
    Strategy: maintain population, evaluate fitness, breed best, mutate, repeat.
    """
    
    def __init__(self, population_size: int = 100):
        self.population_size = population_size
        self.population: List[Individual] = []
        self.generation_count = 0
        self.fitness_history: List[Dict] = []
        self.best_individuals: List[Individual] = []
        self.mutation_rates: Dict[str, float] = {}
        self.inheritance_patterns: List[Dict] = []
        self.evolved_strategies: Dict[str, Individual] = {}
        
        self.evolution_file = config.DATA_DIR / "evolution.json"
        self._initialize_population()
        
        logger.info(f"[EVOLUTION] Evolutionary Learning Engine initialized with population size {population_size}")
    
    def _initialize_population(self):
        """Initialize starting population with diverse strategies"""
        try:
            # Create diverse initial individuals
            strategy_templates = [
                {
                    "learning_rate": random.uniform(0.001, 0.1),
                    "batch_size": random.randint(32, 512),
                    "epochs": random.randint(10, 100),
                    "dropout": random.uniform(0.0, 0.5),
                    "strategy_name": "standard_sgd"
                },
                {
                    "momentum": random.uniform(0.0, 0.99),
                    "learning_rate": random.uniform(0.001, 0.1),
                    "nesterov": random.choice([True, False]),
                    "strategy_name": "momentum_based"
                },
                {
                    "beta_1": random.uniform(0.8, 0.99),
                    "beta_2": random.uniform(0.99, 0.9999),
                    "epsilon": random.uniform(1e-8, 1e-6),
                    "strategy_name": "adam_style"
                },
                {
                    "update_frequency": random.randint(1, 100),
                    "target_network_delay": random.randint(100, 10000),
                    "exploration_rate": random.uniform(0.0, 1.0),
                    "strategy_name": "reinforcement"
                },
                {
                    "curriculum_difficulty": random.uniform(0.0, 1.0),
                    "task_ordering": "difficulty",
                    "pacing_factor": random.uniform(0.5, 2.0),
                    "strategy_name": "curriculum"
                }
            ]
            
            # Create initial population
            for i in range(self.population_size):
                template = random.choice(strategy_templates)
                genes = deepcopy(template)
                individual = Individual(genes, strategy_type="learning_strategy")
                self.population.append(individual)
            
            logger.info("[EVOLUTION] Initial population created")
            
        except Exception as e:
            logger.error(f"[EVOLUTION] Error initializing population: {e}")
    
    def evaluate_fitness(self, individual: Individual, 
                        performance_metrics: Dict) -> float:
        """
        Evaluate fitness of individual strategy based on performance.
        Higher fitness = better strategy.
        """
        fitness = 0.0
        
        try:
            # Fitness components
            # 1. Learning speed: how quickly does it learn?
            learning_speed = min(1.0, performance_metrics.get("learning_speed", 0.5))
            fitness += learning_speed * 0.3
            
            # 2. Final performance: how good is final accuracy?
            final_accuracy = min(1.0, performance_metrics.get("accuracy", 0.5))
            fitness += final_accuracy * 0.4
            
            # 3. Stability: does performance plateau or keep improving?
            stability = min(1.0, 1.0 - (performance_metrics.get("variance", 0.5) / 2))
            fitness += stability * 0.2
            
            # 4. Efficiency: does it use resources well?
            efficiency = min(1.0, performance_metrics.get("efficiency", 0.5))
            fitness += efficiency * 0.1
            
            individual.fitness = fitness
            
        except Exception as e:
            logger.error(f"[EVOLUTION] Error evaluating fitness: {e}")
        
        return fitness
    
    def selection(self, tournament_size: int = 5) -> Individual:
        """
        Tournament selection: pick random individuals and return best.
        """
        tournament = random.sample(self.population, min(tournament_size, len(self.population)))
        winner = max(tournament, key=lambda ind: ind.fitness)
        return winner
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        """
        Genetic crossover: combine genes from both parents.
        Create offspring with traits from both.
        """
        offspring_genes = {}
        
        try:
            # 50/50 mixing of parent genes
            for key in set(list(parent1.genes.keys()) + list(parent2.genes.keys())):
                if key in parent1.genes and key in parent2.genes:
                    if random.random() < 0.5:
                        offspring_genes[key] = parent1.genes[key]
                    else:
                        offspring_genes[key] = parent2.genes[key]
                elif key in parent1.genes:
                    offspring_genes[key] = parent1.genes[key]
                else:
                    offspring_genes[key] = parent2.genes[key]
            
            offspring = Individual(offspring_genes, strategy_type=parent1.strategy_type)
            
        except Exception as e:
            logger.error(f"[EVOLUTION] Error in crossover: {e}")
            offspring = Individual(deepcopy(parent1.genes), strategy_type=parent1.strategy_type)
        
        return offspring
    
    def mutate(self, individual: Individual, mutation_rate: float = 0.1) -> Individual:
        """
        Mutation: randomly change some genes.
        Introduces variation for exploration.
        """
        mutated = Individual(deepcopy(individual.genes), strategy_type=individual.strategy_type)
        
        try:
            for key in mutated.genes:
                if random.random() < mutation_rate:
                    value = mutated.genes[key]
                    
                    # Mutate based on type
                    if isinstance(value, float):
                        # Gaussian mutation for floats
                        mutated.genes[key] = max(0.0, min(1.0, value + np.random.normal(0, 0.1)))
                    elif isinstance(value, int):
                        # Small integer mutation
                        mutated.genes[key] = max(1, value + np.random.randint(-5, 6))
                    elif isinstance(value, bool):
                        # Flip boolean
                        mutated.genes[key] = not value
                    elif isinstance(value, str):
                        # Don't mutate strings by default
                        pass
            
        except Exception as e:
            logger.error(f"[EVOLUTION] Error in mutation: {e}")
        
        return mutated
    
    def evolve_generation(self, performance_data: Dict) -> Dict:
        """
        Execute one generation of evolution.
        Evaluate, select, crossover, mutate.
        """
        try:
            # Phase 1: Evaluate all individuals
            for individual in self.population:
                self.evaluate_fitness(individual, performance_data)
            
            # Phase 2: Track best
            best = max(self.population, key=lambda ind: ind.fitness)
            self.best_individuals.append(best)
            
            # Phase 3: Track stats
            fitness_scores = [ind.fitness for ind in self.population]
            generation_record = {
                "generation": self.generation_count,
                "best_fitness": max(fitness_scores),
                "avg_fitness": np.mean(fitness_scores),
                "worst_fitness": min(fitness_scores),
                "timestamp": datetime.now().isoformat()
            }
            self.fitness_history.append(generation_record)
            
            # Phase 4: Create new generation
            new_population = []
            
            # Keep best (elitism)
            elite_count = max(1, self.population_size // 10)
            elite = sorted(self.population, key=lambda ind: ind.fitness, reverse=True)[:elite_count]
            new_population.extend(elite)
            
            # Fill rest through selection, crossover, mutation
            while len(new_population) < self.population_size:
                parent1 = self.selection()
                parent2 = self.selection()
                
                offspring = self.crossover(parent1, parent2)
                offspring = self.mutate(offspring)
                
                new_population.append(offspring)
            
            self.population = new_population
            self.generation_count += 1
            
            logger.info(f"[EVOLUTION] Generation {self.generation_count - 1}: " +
                       f"best fitness {best.fitness:.4f}, avg {np.mean(fitness_scores):.4f}")
            
            return generation_record
            
        except Exception as e:
            logger.error(f"[EVOLUTION] Error in evolution: {e}")
            return {"error": str(e)}
    
    def get_best_strategy(self) -> Optional[Individual]:
        """Get the best evolved strategy found so far"""
        if not self.best_individuals:
            return None
        return max(self.best_individuals, key=lambda ind: ind.fitness)
    
    def archive_strategy(self, name: str, individual: Individual):
        """Save a good strategy for future use"""
        self.evolved_strategies[name] = individual
        logger.info(f"[EVOLUTION] Archived strategy: {name} (fitness: {individual.fitness:.4f})")
    
    def restore_strategy(self, name: str) -> Optional[Individual]:
        """Restore a previously archived strategy"""
        strategy = self.evolved_strategies.get(name)
        if strategy:
            logger.info(f"[EVOLUTION] Restored strategy: {name}")
        return strategy
    
    def adapt_mutation_rate(self, diversity_metric: float):
        """
        Adapt mutation rate based on population diversity.
        Low diversity -> increase mutation to explore.
        High diversity -> decrease mutation to exploit.
        """
        if diversity_metric < 0.5:
            # Low diversity, increase mutation
            increase_factor = 1.2
        else:
            # Good diversity, keep or decrease mutation
            increase_factor = 0.95
        
        for key in self.mutation_rates:
            self.mutation_rates[key] *= increase_factor
            self.mutation_rates[key] = max(0.01, min(0.3, self.mutation_rates[key]))
    
    def calculate_population_diversity(self) -> float:
        """Calculate diversity of population (0-1)"""
        if len(self.population) < 2:
            return 0.0
        
        # Simple diversity: average pairwise difference in fitness
        fitness_values = [ind.fitness for ind in self.population]
        variance = np.var(fitness_values) if fitness_values else 0.0
        
        # Normalize to 0-1
        diversity = min(1.0, variance)
        
        return diversity
    
    def multi_objective_optimization(self, objectives: List[str]) -> List[Individual]:
        """
        Handle multiple objectives (e.g., speed AND accuracy, not just one).
        Returns Pareto frontier of non-dominated solutions.
        """
        pareto_front = []
        
        try:
            for individual in self.population:
                is_dominated = False
                
                for other in self.population:
                    if individual == other:
                        continue
                    
                    # Check if other dominates individual
                    better_on_all = True
                    for obj in objectives:
                        obj_value_individual = individual.genes.get(obj, 0.5)
                        obj_value_other = other.genes.get(obj, 0.5)
                        
                        if obj_value_individual >= obj_value_other:
                            better_on_all = False
                            break
                    
                    if better_on_all:
                        is_dominated = True
                        break
                
                if not is_dominated:
                    pareto_front.append(individual)
            
            logger.info(f"[EVOLUTION] Pareto frontier has {len(pareto_front)} individuals")
            
        except Exception as e:
            logger.error(f"[EVOLUTION] Error in multi-objective optimization: {e}")
        
        return pareto_front
    
    def save_evolution_state(self):
        """Save evolution state and learned strategies to disk"""
        try:
            data = {
                "generation_count": self.generation_count,
                "best_strategy": self.get_best_strategy().to_dict() if self.get_best_strategy() else None,
                "evolved_strategies": {name: ind.to_dict() for name, ind in self.evolved_strategies.items()},
                "fitness_history": self.fitness_history[-100:],  # Last 100 generations
                "population_size": len(self.population)
            }
            
            with open(self.evolution_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"[EVOLUTION] Saved evolution state at generation {self.generation_count}")
        except Exception as e:
            logger.error(f"[EVOLUTION] Error saving evolution state: {e}")
    
    def get_evolution_summary(self) -> Dict:
        """Get summary of evolutionary learning progress"""
        best = self.get_best_strategy()
        
        return {
            "generation_count": self.generation_count,
            "population_size": len(self.population),
            "population_diversity": self.calculate_population_diversity(),
            "best_fitness": best.fitness if best else 0.0,
            "evolved_strategies_archived": len(self.evolved_strategies),
            "fitness_improvement": self._calculate_improvement(),
            "top_performers": [ind.to_dict() for ind in sorted(
                self.population, key=lambda x: x.fitness, reverse=True)[:5]]
        }
    
    def _calculate_improvement(self) -> float:
        """Calculate improvement over evolutionary history"""
        if len(self.fitness_history) < 2:
            return 0.0
        
        first_avg = self.fitness_history[0].get("avg_fitness", 0.0)
        last_avg = self.fitness_history[-1].get("avg_fitness", 0.0)
        
        improvement = (last_avg - first_avg) / (first_avg + 1e-6)
        return improvement
