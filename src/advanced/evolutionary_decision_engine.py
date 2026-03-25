"""
Evolutionary Self-Decision Making Engine: Ultra-fast probabilistic decision-making

Features:
- Millisecond decision latency
- Evolutionary algorithms (genetic)
- Probability-based optimization
- Game playing strategies
- Lottery prediction
- Multi-scenario reasoning
- Adaptive learning
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from typing import List, Dict, Any, Tuple, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random
import math
from enum import Enum
import time

import config
from src.logger import logger


class DecisionContext(Enum):
    """Types of decision contexts"""
    GAME = "game"              # Chess, poker, etc.
    LOTTERY = "lottery"        # Number prediction
    RESOURCE = "resource"      # Resource allocation
    STRATEGY = "strategy"      # Strategic choices
    OPTIMIZATION = "optimization"  # Parameter tuning
    PREDICTION = "prediction"  # Future prediction
    TRADING = "trading"        # Market/financial decisions


@dataclass
class Gene:
    """A single gene in evolutionary algorithm"""
    trait: str                 # What this gene represents
    value: float              # Current value (0-1)
    mutation_rate: float = 0.01
    
    def mutate(self) -> None:
        """Mutate this gene"""
        if random.random() < self.mutation_rate:
            change = random.gauss(0, 0.05)
            self.value = max(0, min(1, self.value + change))


@dataclass
class Chromosome:
    """A decision chromosome (full decision blueprint)"""
    genes: List[Gene]
    fitness: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    
    def crossover(self, other: 'Chromosome') -> 'Chromosome':
        """Create offspring from two chromosomes"""
        offspring_genes = []
        for i in range(len(self.genes)):
            if random.random() < 0.5:
                offspring_genes.append(Gene(
                    trait=self.genes[i].trait,
                    value=self.genes[i].value
                ))
            else:
                offspring_genes.append(Gene(
                    trait=other.genes[i].trait,
                    value=other.genes[i].value
                ))
        
        return Chromosome(genes=offspring_genes)
    
    def mutate(self) -> None:
        """Mutate all genes"""
        for gene in self.genes:
            gene.mutate()


@dataclass
class Decision:
    """A made decision with confidence"""
    choice: Any
    confidence: float          # 0-1
    probability: float        # Probability of success
    reasoning: Dict[str, Any]
    context: DecisionContext
    execution_time_ms: float
    expected_value: float     # Expected value calculation


class EvolutionaryDecisionMaker:
    """
    Makes decisions using evolutionary algorithms
    
    Operates at millisecond scale with probabilistic reasoning
    """
    
    def __init__(self, population_size: int = 100, generations: int = 10):
        self.population_size = population_size
        self.generations = generations
        self.population: List[Chromosome] = []
        self.best_decision: Optional[Chromosome] = None
        self.decision_history: List[Decision] = []
        
        logger.info("✓ Evolutionary Decision Maker initialized")
    
    def initialize_population(self, traits: List[str]) -> None:
        """Initialize population with random chromosomes"""
        
        self.population = []
        
        for _ in range(self.population_size):
            genes = [Gene(trait=trait, value=random.random()) for trait in traits]
            chromosome = Chromosome(genes=genes)
            self.population.append(chromosome)
    
    def evaluate_fitness(
        self, 
        chromosome: Chromosome,
        fitness_func: Callable
    ) -> float:
        """Evaluate fitness of a chromosome"""
        
        values = {gene.trait: gene.value for gene in chromosome.genes}
        fitness = fitness_func(values)
        chromosome.fitness = fitness
        
        return fitness
    
    def select_best(self, count: int = 10) -> List[Chromosome]:
        """Select best chromosomes (tournament selection)"""
        
        # Sort by fitness
        sorted_pop = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        return sorted_pop[:count]
    
    def evolve(self, fitness_func: Callable) -> Chromosome:
        """
        Evolve population for one generation
        
        Returns best chromosome found
        """
        
        start_time = time.time_ns()
        
        # Evaluate all
        for chromosome in self.population:
            self.evaluate_fitness(chromosome, fitness_func)
        
        best_solutions = self.select_best(count=10)
        
        # Create next generation
        new_population = best_solutions.copy()
        
        while len(new_population) < self.population_size:
            # Select two parents
            parent1 = random.choice(best_solutions)
            parent2 = random.choice(best_solutions)
            
            # Create offspring
            offspring = parent1.crossover(parent2)
            offspring.mutate()
            
            new_population.append(offspring)
        
        self.population = new_population[:self.population_size]
        
        best = best_solutions[0]
        
        if not self.best_decision or best.fitness > self.best_decision.fitness:
            self.best_decision = best
        
        elapsed_ms = (time.time_ns() - start_time) / 1_000_000
        
        return best
    
    def make_decision(
        self,
        traits: List[str],
        fitness_func: Callable,
        context: DecisionContext,
        max_time_ms: float = 50
    ) -> Decision:
        """
        Make a decision within time constraint
        
        Uses evolution to find best decision in milliseconds
        """
        
        start_time = time.time_ns()
        
        # Initialize
        self.initialize_population(traits)
        
        # Evolve for max time
        gen = 0
        while (time.time_ns() - start_time) / 1_000_000 < max_time_ms and gen < self.generations:
            best = self.evolve(fitness_func)
            gen += 1
        
        final_best = sorted(self.population, key=lambda x: x.fitness, reverse=True)[0]
        
        execution_time = (time.time_ns() - start_time) / 1_000_000
        
        # Extract decision
        choice = {gene.trait: gene.value for gene in final_best.genes}
        confidence = min(1.0, final_best.fitness / 100)  # Normalize
        
        decision = Decision(
            choice=choice,
            confidence=confidence,
            probability=self._calculate_probability(final_best),
            reasoning={
                "generations": gen,
                "fitness": final_best.fitness
            },
            context=context,
            execution_time_ms=execution_time,
            expected_value=final_best.fitness
        )
        
        self.decision_history.append(decision)
        
        return decision
    
    def _calculate_probability(self, chromosome: Chromosome) -> float:
        """Calculate probability of success"""
        
        # Higher fitness = higher probability
        # Sigmoid function for smooth probability
        fitness = chromosome.fitness
        probability = 1 / (1 + math.exp(-fitness / 50))
        
        return probability


class ProbabilisticPredictor:
    """
    Probabilistic prediction using Bayesian inference
    
    For lottery, games, and general predictions
    """
    
    def __init__(self):
        self.historical_data: List[Dict] = []
        self.probability_models: Dict[str, Any] = {}
        
        logger.info("✓ Probabilistic Predictor initialized")
    
    def calculate_conditional_probability(
        self,
        event_a: Any,
        event_b: Any,
        occurrences: Dict[Tuple, int]
    ) -> float:
        """
        Calculate P(A|B) - Probability of A given B
        Using Bayes' theorem
        """
        
        # P(A|B) = P(B|A) * P(A) / P(B)
        
        total = sum(occurrences.values())
        
        # Count occurrences
        a_and_b = occurrences.get((event_a, event_b), 0)
        b_total = sum(1 for k, v in occurrences.items() if k[1] == event_b for _ in range(v))
        a_total = sum(1 for k, v in occurrences.items() if k[0] == event_a for _ in range(v))
        
        if b_total == 0 or total == 0:
            return 0
        
        p_a = a_total / total
        p_b = b_total / total
        p_b_given_a = a_and_b / max(a_total, 1)
        
        p_a_given_b = (p_b_given_a * p_a) / p_b if p_b > 0 else 0
        
        return p_a_given_b
    
    def predict_next_sequence(
        self,
        historical_sequence: List[int],
        possible_values: List[int],
        method: str = "frequency"
    ) -> Tuple[int, float]:
        """
        Predict next value in sequence
        
        Uses frequency analysis, pattern matching, or Markov chains
        """
        
        if not historical_sequence:
            return random.choice(possible_values), 0.25
        
        # Frequency analysis
        if method == "frequency":
            freq = {}
            for val in possible_values:
                freq[val] = historical_sequence.count(val)
            
            # Add smoothing for unseen values
            min_freq = min(freq.values()) if freq else 0
            for val in possible_values:
                if val not in freq:
                    freq[val] = max(0, min_freq - 1)
            
            total = sum(freq.values())
            if total == 0:
                return random.choice(possible_values), 1.0 / len(possible_values)
            
            # Find most likely
            best_val = max(freq, key=freq.get)
            probability = freq[best_val] / total
            
            return best_val, probability
        
        # Pattern matching (look for last pair, predict third)
        elif method == "pattern":
            if len(historical_sequence) < 2:
                return random.choice(possible_values), 0.25
            
            last_pair = (historical_sequence[-2], historical_sequence[-1])
            
            patterns = {}
            for i in range(2, len(historical_sequence)):
                pair = (historical_sequence[i-2], historical_sequence[i-1])
                if pair not in patterns:
                    patterns[pair] = {}
                
                next_val = historical_sequence[i]
                patterns[pair][next_val] = patterns[pair].get(next_val, 0) + 1
            
            if last_pair in patterns:
                next_options = patterns[last_pair]
                total = sum(next_options.values())
                best_next = max(next_options, key=next_options.get)
                probability = next_options[best_next] / total
                
                return best_next, probability
            
            return random.choice(possible_values), 0.25
        
        # Markov chain
        elif method == "markov":
            transitions = {}
            
            for i in range(len(historical_sequence) - 1):
                current = historical_sequence[i]
                next_val = historical_sequence[i + 1]
                
                if current not in transitions:
                    transitions[current] = {}
                
                transitions[current][next_val] = transitions[current].get(next_val, 0) + 1
            
            last_val = historical_sequence[-1]
            
            if last_val in transitions:
                options = transitions[last_val]
                total = sum(options.values())
                best_next = max(options, key=options.get)
                probability = options[best_next] / total
                
                return best_next, probability
            
            return random.choice(possible_values), 0.25
        
        return random.choice(possible_values), 0.25


class GamePlayingEngine:
    """
    Strategic game playing engine
    
    Supports multiple game types with tactical decision-making
    """
    
    def __init__(self):
        self.game_states: Dict[str, Any] = {}
        self.strategy_cache: Dict[str, Any] = {}
        
        logger.info("✓ Game Playing Engine initialized")
    
    def minimax_decision(
        self,
        state: Dict,
        depth: int = 5,
        is_maximizing: bool = True,
        time_limit_ms: float = 100
    ) -> Tuple[Any, float]:
        """
        Minimax algorithm for game decisions
        
        Fast implementation with time limit
        """
        
        start_time = time.time_ns()
        
        def minimax(
            s: Dict,
            d: int,
            is_max: bool
        ) -> float:
            
            # Time check
            if (time.time_ns() - start_time) / 1_000_000 > time_limit_ms:
                return self._evaluate_position(s)
            
            # Terminal check
            is_terminal, value = self._is_terminal_state(s)
            if is_terminal or d == 0:
                return value
            
            if is_max:
                max_eval = -float('inf')
                for move in self._get_legal_moves(s, is_max):
                    next_state = self._apply_move(s, move)
                    eval = minimax(next_state, d - 1, False)
                    max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = float('inf')
                for move in self._get_legal_moves(s, is_max):
                    next_state = self._apply_move(s, move)
                    eval = minimax(next_state, d - 1, True)
                    min_eval = min(min_eval, eval)
                return min_eval
        
        best_move = None
        best_value = -float('inf') if is_maximizing else float('inf')
        
        for move in self._get_legal_moves(state, is_maximizing):
            next_state = self._apply_move(state, move)
            value = minimax(next_state, depth - 1, not is_maximizing)
            
            if is_maximizing and value > best_value:
                best_value = value
                best_move = move
            elif not is_maximizing and value < best_value:
                best_value = value
                best_move = move
        
        execution_time = (time.time_ns() - start_time) / 1_000_000
        
        logger.info(f"Minimax decision in {execution_time:.2f}ms")
        
        return best_move, best_value
    
    def alpha_beta_pruning(
        self,
        state: Dict,
        depth: int = 5,
        alpha: float = -float('inf'),
        beta: float = float('inf'),
        is_maximizing: bool = True,
        time_limit_ms: float = 50
    ) -> Tuple[Any, float]:
        """
        Alpha-beta pruning for faster game search
        """
        
        start_time = time.time_ns()
        
        def ab_search(
            s: Dict,
            d: int,
            a: float,
            b: float,
            is_max: bool
        ) -> float:
            
            if (time.time_ns() - start_time) / 1_000_000 > time_limit_ms:
                return self._evaluate_position(s)
            
            is_terminal, value = self._is_terminal_state(s)
            if is_terminal or d == 0:
                return value
            
            if is_max:
                max_eval = -float('inf')
                for move in self._get_legal_moves(s, is_max):
                    next_state = self._apply_move(s, move)
                    eval = ab_search(next_state, d - 1, a, b, False)
                    max_eval = max(max_eval, eval)
                    a = max(a, eval)
                    if b <= a:
                        break  # Beta cutoff
                return max_eval
            else:
                min_eval = float('inf')
                for move in self._get_legal_moves(s, is_max):
                    next_state = self._apply_move(s, move)
                    eval = ab_search(next_state, d - 1, a, b, True)
                    min_eval = min(min_eval, eval)
                    b = min(b, eval)
                    if b <= a:
                        break  # Alpha cutoff
                return min_eval
        
        best_move = None
        best_value = -float('inf') if is_maximizing else float('inf')
        
        for move in self._get_legal_moves(state, is_maximizing):
            next_state = self._apply_move(state, move)
            value = ab_search(
                next_state, depth - 1,
                alpha, beta,
                not is_maximizing
            )
            
            if is_maximizing and value > best_value:
                best_value = value
                best_move = move
            elif not is_maximizing and value < best_value:
                best_value = value
                best_move = move
        
        execution_time = (time.time_ns() - start_time) / 1_000_000
        
        return best_move, best_value
    
    def _get_legal_moves(self, state: Dict, is_max: bool) -> List[Any]:
        """Get legal moves in current state"""
        return state.get("legal_moves", [])
    
    def _apply_move(self, state: Dict, move: Any) -> Dict:
        """Apply move to state"""
        return state.get("apply_move", lambda m: state)(move)
    
    def _is_terminal_state(self, state: Dict) -> Tuple[bool, float]:
        """Check if state is terminal"""
        return state.get("is_terminal", False), state.get("value", 0)
    
    def _evaluate_position(self, state: Dict) -> float:
        """Evaluate position heuristically"""
        return state.get("evaluation", 0.0)


class FastDecisionEngine:
    """
    Ultra-fast decision making (millisecond latency)
    
    Combines all techniques for optimal sub-millisecond decisions
    """
    
    def __init__(self):
        self.evolutionary_maker = EvolutionaryDecisionMaker()
        self.probabilistic_predictor = ProbabilisticPredictor()
        self.game_engine = GamePlayingEngine()
        
        self.decision_count = 0
        self.total_time_ms = 0
        
        logger.info("✓ Fast Decision Engine initialized")
    
    def make_fast_decision(
        self,
        context: DecisionContext,
        parameters: Dict[str, Any],
        max_latency_ms: float = 10  # 10ms default
    ) -> Decision:
        """
        Make fastest possible decision
        
        Under 10ms typically
        """
        
        start_time = time.time_ns()
        
        if context == DecisionContext.GAME:
            move, value = self.game_engine.alpha_beta_pruning(
                parameters.get("state", {}),
                depth=parameters.get("depth", 5),
                time_limit_ms=max_latency_ms
            )
            
            choice = move
            confidence = self._value_to_confidence(value)
        
        elif context == DecisionContext.LOTTERY:
            sequence = parameters.get("historical_sequence", [])
            possible = parameters.get("possible_values", list(range(1, 50)))
            
            next_num, probability = self.probabilistic_predictor.predict_next_sequence(
                sequence,
                possible,
                method=parameters.get("method", "pattern")
            )
            
            choice = next_num
            confidence = probability
        
        elif context == DecisionContext.STRATEGY:
            traits = parameters.get("traits", [])
            fitness_func = parameters.get("fitness_function", lambda x: 50)
            
            decision = self.evolutionary_maker.make_decision(
                traits,
                fitness_func,
                context,
                max_time_ms=max_latency_ms
            )
            
            execution_time = (time.time_ns() - start_time) / 1_000_000
            self.decision_count += 1
            self.total_time_ms += execution_time
            
            return decision
        
        else:
            # Default decision
            choice = "default"
            confidence = 0.5
        
        execution_time = (time.time_ns() - start_time) / 1_000_000
        
        decision = Decision(
            choice=choice,
            confidence=confidence,
            probability=confidence,
            reasoning={"context": context.value},
            context=context,
            execution_time_ms=execution_time,
            expected_value=confidence
        )
        
        self.decision_count += 1
        self.total_time_ms += execution_time
        
        return decision
    
    def _value_to_confidence(self, value: float) -> float:
        """Convert minimax value to confidence"""
        return min(1.0, max(0.0, (value + 100) / 200))
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get decision-making performance statistics"""
        
        avg_latency = self.total_time_ms / max(self.decision_count, 1)
        
        return {
            "total_decisions": self.decision_count,
            "total_time_ms": self.total_time_ms,
            "average_latency_ms": avg_latency,
            "decisions_per_second": 1000 / max(avg_latency, 0.1)
        }


# Global instance
_engine: Optional[FastDecisionEngine] = None


def get_fast_decision_engine() -> FastDecisionEngine:
    """Get or create fast decision engine"""
    global _engine
    if _engine is None:
        _engine = FastDecisionEngine()
    return _engine
