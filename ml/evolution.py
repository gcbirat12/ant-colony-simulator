# evolution.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Evolutionary algorithm for the AI Ant Colony Simulator
"""

import numpy as np
import pickle
import os
import time
from core.ant import Ant
import config


class EvolutionManager:
    """
    Manages the evolutionary process for the ant colony
    """
    
    def __init__(self, colony):
        """
        Initialize the evolution manager
        
        Args:
            colony: The ant colony to evolve
        """
        self.colony = colony
        self.generation = 0
        self.best_fitness = 0
        self.best_agent = None
        self.fitness_history = []
        
        # Create directory for model saving if it doesn't exist
        os.makedirs(os.path.dirname(config.MODEL_SAVE_PATH), exist_ok=True)
    
    def evaluate_fitness(self, ant):
        """
        Calculate fitness for an individual ant
        
        Args:
            ant: The ant to evaluate
            
        Returns:
            Fitness score
        """
        # Individual fitness - for now, use the ant's built-in fitness method
        return ant.get_fitness()
    
    def select_parents(self, population, fitnesses):
        """
        Select parent ants for reproduction using tournament selection
        
        Args:
            population: List of ants
            fitnesses: List of fitness scores
            
        Returns:
            Two parent ants
        """
        # Tournament selection
        tournament_size = max(2, int(len(population) * 0.1))
        
        # Function to select one parent
        def select_one():
            # Randomly select contestants for the tournament
            tournament_indices = np.random.choice(
                len(population), tournament_size, replace=False
            )
            tournament_fitnesses = [fitnesses[i] for i in tournament_indices]
            
            # Select the winner (highest fitness)
            winner_idx = tournament_indices[np.argmax(tournament_fitnesses)]
            return population[winner_idx]
        
        # Select two parents
        parent1 = select_one()
        parent2 = select_one()
        
        return parent1, parent2
    
    def create_offspring(self, parent1, parent2):
        """
        Create a new ant by crossing over two parents
        
        Args:
            parent1: First parent ant
            parent2: Second parent ant
            
        Returns:
            New ant created through crossover and mutation
        """
        # Crossover the neural networks
        offspring_brain = parent1.brain.crossover(
            parent2.brain, 
            config.CROSSOVER_RATE
        )
        
        # Apply mutation
        offspring_brain.mutate(config.MUTATION_RATE)
        
        # Create a new ant with this brain
        offspring = Ant(self.colony, brain=offspring_brain)
        
        return offspring
    
    def evolve_generation(self):
        """
        Perform one round of evolution on the colony
        """
        # Only evolve if we have enough ants
        if len(self.colony.ants) < 10:
            return
            
        # Evaluate fitness for all ants
        population = self.colony.ants
        fitnesses = [self.evaluate_fitness(ant) for ant in population]
        
        # Keep track of the best agent
        max_fitness_idx = np.argmax(fitnesses)
        current_best_fitness = fitnesses[max_fitness_idx]
        
        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_agent = population[max_fitness_idx].brain
        
        # Track fitness history
        self.fitness_history.append({
            'generation': self.generation,
            'max_fitness': current_best_fitness,
            'avg_fitness': np.mean(fitnesses),
            'population_size': len(population)
        })
        
        # Create new population through selection, crossover, and mutation
        new_population = []
        
        # Keep the best 10% (elitism)
        elitism_count = max(1, int(len(population) * 0.1))
        elite_indices = np.argsort(fitnesses)[-elitism_count:]
        
        for idx in elite_indices:
            new_population.append(population[idx])
        
        # Fill the rest with offspring
        while len(new_population) < len(population):
            # Select parents
            parent1, parent2 = self.select_parents(population, fitnesses)
            
            # Create and add offspring
            offspring = self.create_offspring(parent1, parent2)
            new_population.append(offspring)
        
        # Replace the colony's ants with the new population
        self.colony.ants = new_population
        
        # Update generation counter
        self.generation += 1
        self.colony.set_generation(self.generation)
        
        print(f"Generation {self.generation}: "
              f"Max Fitness = {current_best_fitness:.2f}, "
              f"Avg Fitness = {np.mean(fitnesses):.2f}, "
              f"Population = {len(population)}")
    
    def run_headless(self, generations=config.TRAINING_GENERATIONS):
        """
        Run evolution for a number of generations without UI
        
        Args:
            generations: Number of generations to evolve
        """
        start_time = time.time()
        
        print(f"Starting headless evolution for {generations} generations...")
        
        for i in range(generations):
            # Run simulation for one generation length
            for _ in range(config.GENERATION_LENGTH):
                self.colony.update()
                self.colony.environment.update()
            
            # Evolve to the next generation
            self.evolve_generation()
            
            # Print progress
            elapsed = time.time() - start_time
            print(f"Generation {i+1}/{generations} completed "
                  f"({elapsed:.2f} seconds elapsed)")
        
        print(f"Evolution completed in {time.time() - start_time:.2f} seconds")
    
    def save_model(self, filename=config.MODEL_SAVE_PATH):
        """
        Save the best model to a file
        
        Args:
            filename: Path to save the model
        """
        if self.best_agent is None:
            print("No model to save yet.")
            return
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save the model
        with open(filename, 'wb') as f:
            pickle.dump({
                'weights': self.best_agent.get_weights(),
                'generation': self.generation,
                'fitness': self.best_fitness,
                'history': self.fitness_history
            }, f)
            
        print(f"Model saved to {filename}")
    
    def load_model(self, filename):
        """
        Load a saved model
        
        Args:
            filename: Path to the model file
        """
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
            
        # Create a new agent with the saved weights
        from ml.agent import MLAgent
        self.best_agent = MLAgent()
        self.best_agent.set_weights(model_data['weights'])
        
        # Restore evolution state
        self.generation = model_data.get('generation', 0)
        self.best_fitness = model_data.get('fitness', 0)
        self.fitness_history = model_data.get('history', [])
        
        # Apply the model to all ants
        for ant in self.colony.ants:
            ant.brain.set_weights(model_data['weights'])
        
        print(f"Model loaded from {filename} (generation {self.generation})")