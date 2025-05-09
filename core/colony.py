# colony.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colony management for the AI Ant Colony Simulator
"""

import numpy as np
from core.ant import Ant
from core.nest import Nest
import config


class Colony:
    """
    A colony of ants that work together and evolve over time
    """
    
    def __init__(self, environment, initial_ants=config.DEFAULT_ANT_COUNT):
        """
        Initialize a new colony
        
        Args:
            environment: The environment the colony exists in
            initial_ants: Number of ants to start with
        """
        self.environment = environment
        
        # Create the nest at a somewhat central position with some randomness
        center_x = config.WORLD_WIDTH / 2 + np.random.uniform(-100, 100)
        center_y = config.WORLD_HEIGHT / 2 + np.random.uniform(-100, 100)
        self.nest = Nest(center_x, center_y, radius=config.NEST_RADIUS)
        
        # Initialize statistics
        self.food_collected = 0
        self.food_delivered = 0
        self.total_steps = 0
        self.generation = 0
        self.ants_born = initial_ants
        self.ants_died = 0
        
        # Create initial ant population
        self.ants = []
        for _ in range(initial_ants):
            self.ants.append(Ant(self))
    
    def update(self):
        """
        Update all ants and colony state for one time step
        """
        # Update all living ants
        active_ants = [ant for ant in self.ants if ant.alive]
        
        for ant in active_ants:
            ant.update()
        
        # Remove dead ants and potentially spawn new ones
        self.process_dead_ants()
        self.spawn_new_ants()
        
        # Increment step counter
        self.total_steps += 1
    
    def process_dead_ants(self):
        """
        Handle dead ants - track statistics and remove them
        """
        initial_count = len(self.ants)
        self.ants = [ant for ant in self.ants if ant.alive]
        newly_dead = initial_count - len(self.ants)
        self.ants_died += newly_dead
    
    def spawn_new_ants(self):
        """
        Spawn new ants based on colony resources
        """
        # Only spawn new ants if we have enough food and are under the max colony size
        if (self.food_collected > config.ANT_ENERGY_FROM_FOOD and 
                len(self.ants) < config.MAX_COLONY_SIZE):
            # Spawn a new ant using resources
            self.food_collected -= config.ANT_ENERGY_FROM_FOOD
            new_ant = Ant(self)
            self.ants.append(new_ant)
            self.ants_born += 1
    
    def add_food(self, amount):
        """
        Add collected food to the colony's stores
        
        Args:
            amount: Amount of food energy to add
        """
        self.food_collected += amount
        self.food_delivered += 1
    
    def get_population_size(self):
        """Get the current number of living ants"""
        return len([ant for ant in self.ants if ant.alive])
    
    def get_colony_stats(self):
        """
        Get colony statistics for display
        
        Returns:
            Dictionary of colony statistics
        """
        return {
            'population': self.get_population_size(),
            'food_collected': self.food_collected,
            'food_delivered': self.food_delivered,
            'total_steps': self.total_steps,
            'generation': self.generation,
            'ants_born': self.ants_born,
            'ants_died': self.ants_died,
            'efficiency': self.food_delivered / max(1, self.total_steps),
        }
    
    def set_generation(self, gen):
        """Update the generation counter"""
        self.generation = gen