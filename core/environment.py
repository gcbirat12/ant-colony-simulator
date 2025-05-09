# environment.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Environment simulation for the AI Ant Colony Simulator
"""

import numpy as np
from core.food import Food
from core.pheromone import PheromoneSystem
from utils.vector import Vector2D
import config


class Environment:
    """
    The environment where the ant colony exists, including food, pheromones,
    and other environmental factors.
    """
    
    def __init__(self, width=config.WORLD_WIDTH, height=config.WORLD_HEIGHT):
        """
        Initialize a new environment
        
        Args:
            width: Width of the environment
            height: Height of the environment
        """
        self.width = width
        self.height = height
        
        # Initialize food sources
        self.food_sources = []
        
        # Initialize pheromone system
        self.pheromone_system = PheromoneSystem(width, height)
        
        # Environment state tracking
        self.elapsed_steps = 0
    
    def update(self):
        """
        Update the environment for one time step
        """
        # Update pheromones (evaporation, diffusion)
        self.pheromone_system.update()
        
        # Randomly add new food with a small probability
        if np.random.random() < config.FOOD_SPAWN_RATE:
            self.generate_food(1)
            
        # Increment step counter
        self.elapsed_steps += 1
    
    def generate_food(self, count=1):
        """
        Generate new food sources in the environment
        
        Args:
            count: Number of food sources to generate
        """
        for _ in range(count):
            # Generate food clusters rather than completely random positions
            if len(self.food_sources) > 0 and np.random.random() < 0.7:
                # Pick a random existing food and create nearby
                parent_food = np.random.choice(self.food_sources)
                offset = Vector2D(
                    np.random.normal(0, 50),
                    np.random.normal(0, 50)
                )
                position = parent_food.position + offset
            else:
                # Generate completely new food location
                # Avoid putting food too close to the center (assumed nest location)
                while True:
                    x = np.random.uniform(0, self.width)
                    y = np.random.uniform(0, self.height)
                    position = Vector2D(x, y)
                    
                    # Check if far enough from center
                    center = Vector2D(self.width/2, self.height/2)
                    if (position - center).magnitude() > 150:
                        break
            
            # Create the food
            food = Food(position.x, position.y, energy=config.FOOD_ENERGY)
            self.food_sources.append(food)
    
    def remove_food(self, food):
        """
        Remove a food source from the environment
        
        Args:
            food: The food object to remove
        """
        if food in self.food_sources:
            self.food_sources.remove(food)
    
    def add_pheromone(self, position, pheromone_type, amount):
        """
        Add a pheromone marker at the specified position
        
        Args:
            position: Position vector
            pheromone_type: Type of pheromone ('food' or 'home')
            amount: Amount of pheromone to deposit
        """
        self.pheromone_system.add_pheromone(position, pheromone_type, amount)
    
    def get_pheromone_intensity(self, position, pheromone_type, radius=10):
        """
        Get the pheromone intensity around a position
        
        Args:
            position: Position vector
            pheromone_type: Type of pheromone ('food' or 'home')
            radius: Radius to check
            
        Returns:
            Dictionary with pheromone intensities in different directions
        """
        return self.pheromone_system.get_intensity(position, pheromone_type, radius)
    
    def wrap_vector(self, vector):
        """
        Apply wrapping to a vector based on world boundaries
        
        Args:
            vector: The vector to wrap
            
        Returns:
            Wrapped vector
        """
        # Handle x-component wrapping
        if abs(vector.x) > self.width / 2:
            # We're better off going the other way around
            if vector.x > 0:
                vector.x -= self.width
            else:
                vector.x += self.width
                
        # Handle y-component wrapping
        if abs(vector.y) > self.height / 2:
            # We're better off going the other way around
            if vector.y > 0:
                vector.y -= self.height
            else:
                vector.y += self.height
                
        return vector