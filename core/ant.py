#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ant agent model for the AI Ant Colony Simulator
"""

import numpy as np
from utils.vector import Vector2D
from ml.agent import MLAgent
import config


class Ant:
    """
    An individual ant in the colony with ML-based decision making
    """
    
    def __init__(self, colony, position=None, brain=None):
        """
        Initialize an ant
        
        Args:
            colony: The colony this ant belongs to
            position: Initial position (default: at nest)
            brain: Neural network brain (default: create new one)
        """
        self.colony = colony
        self.environment = colony.environment
        
        # Initialize position
        if position is None:
            self.position = Vector2D(colony.nest.position.x, colony.nest.position.y)
        else:
            self.position = Vector2D(position.x, position.y)
            
        # Movement properties
        self.velocity = Vector2D(0, 0)
        self.direction = Vector2D.random_unit_vector()
        self.speed = config.ANT_SPEED
        
        # Status
        self.age = 0
        self.energy = config.INITIAL_ENERGY
        self.carrying_food = False
        self.food_item = None
        self.alive = True
        
        # Create ML agent brain
        self.brain = brain if brain is not None else MLAgent()
        
        # Memory
        self.last_food_distance = float('inf')
        self.last_nest_distance = float('inf')
        self.memory = []
        self.was_carrying_food = False
        
    def sense_environment(self):
        """
        Collect sensory inputs from the environment
        
        Returns:
            numpy array of sensory inputs for the neural network
        """
        # Position relative to nest
        nest_vector = self.colony.nest.position - self.position
        if config.WRAP_WORLD:
            nest_vector = self.environment.wrap_vector(nest_vector)
        
        distance_to_nest = nest_vector.magnitude()
        direction_to_nest = nest_vector.normalized()
        
        # Food detection
        nearest_food = None
        nearest_food_distance = float('inf')
        direction_to_food = Vector2D(0, 0)
        
        for food in self.environment.food_sources:
            food_vector = food.position - self.position
            if config.WRAP_WORLD:
                food_vector = self.environment.wrap_vector(food_vector)
                
            food_distance = food_vector.magnitude()
            
            if food_distance < nearest_food_distance and food_distance < config.ANT_VISION_RANGE:
                nearest_food = food
                nearest_food_distance = food_distance
                direction_to_food = food_vector.normalized()
        
        # Pheromone detection
        food_pheromone = self.environment.get_pheromone_intensity(
            self.position, 'food', radius=config.ANT_VISION_RANGE
        )
        home_pheromone = self.environment.get_pheromone_intensity(
            self.position, 'home', radius=config.ANT_VISION_RANGE
        )
        
        # Combine into sensory input vector
        inputs = np.array([
            # Nest information
            distance_to_nest / config.WORLD_WIDTH,  # Normalized distance
            direction_to_nest.x,  # Direction components
            direction_to_nest.y,
            
            # Food information
            1.0 if nearest_food else 0.0,  # Food detected?
            nearest_food_distance / config.ANT_VISION_RANGE if nearest_food else 1.0,
            direction_to_food.x,
            direction_to_food.y,
            
            # Pheromone information
            food_pheromone['ahead'] / config.PHEROMONE_DEPOSIT,
            food_pheromone['left'] / config.PHEROMONE_DEPOSIT,
            food_pheromone['right'] / config.PHEROMONE_DEPOSIT,
            home_pheromone['ahead'] / config.PHEROMONE_DEPOSIT,
            home_pheromone['left'] / config.PHEROMONE_DEPOSIT,
            home_pheromone['right'] / config.PHEROMONE_DEPOSIT,
            
            # Status information
            1.0 if self.carrying_food else 0.0,
            self.energy / config.INITIAL_ENERGY,
        ])
        
        # Print input vector shape for debugging
        print(f"Input vector length: {len(inputs)}")
        # print(f"Input vector: {inputs}")
        
        return inputs
    
    def think(self, inputs):
        """
        Process sensory inputs through the neural network to get an action
        
        Args:
            inputs: Sensory input array
            
        Returns:
            Action outputs from the neural network
        """
        return self.brain.process(inputs)
    
    def apply_action(self, action_outputs):
        """
        Apply the chosen action
        
        Args:
            action_outputs: Neural network outputs
        """
        # Extract action components
        turn_amount = action_outputs[0] * 2 - 1  # Range [-1, 1]
        speed_factor = action_outputs[1]  # Range [0, 1]
        drop_pheromone = action_outputs[2] > 0.5  # Boolean decision
        pickup_food = action_outputs[3] > 0.5  # Boolean decision
        
        # Update direction vector based on turn amount
        self.direction = self.direction.rotate(turn_amount * np.pi / 4)
        
        # Update velocity and position
        self.velocity = self.direction * self.speed * speed_factor
        new_position = self.position + self.velocity
        
        # Apply world boundaries
        if config.WRAP_WORLD:
            new_position.x %= config.WORLD_WIDTH
            new_position.y %= config.WORLD_HEIGHT
        else:
            new_position.x = max(0, min(new_position.x, config.WORLD_WIDTH))
            new_position.y = max(0, min(new_position.y, config.WORLD_HEIGHT))
        
        self.position = new_position
        
        # Handle pheromone dropping
        if drop_pheromone:
            pheromone_type = 'home' if self.carrying_food else 'food'
            self.environment.add_pheromone(self.position, pheromone_type, config.PHEROMONE_DEPOSIT)
        
        # Handle food pickup/drop
        if self.carrying_food:
            # Check if we're at the nest
            distance_to_nest = (self.position - self.colony.nest.position).magnitude()
            if distance_to_nest < config.NEST_RADIUS:
                # Drop food at nest
                self.carrying_food = False
                self.colony.add_food(config.FOOD_ENERGY)
                self.environment.remove_food(self.food_item)
                self.food_item = None
        elif pickup_food and not self.carrying_food:
            # Try to pick up food
            for food in self.environment.food_sources:
                distance = (self.position - food.position).magnitude()
                if distance < config.ANT_SIZE + config.FOOD_SIZE:
                    self.carrying_food = True
                    self.food_item = food
                    break
        
        # Update energy
        self.energy -= config.ANT_ENERGY_CONSUMPTION
        if self.energy <= 0:
            self.alive = False
            
        # Update age
        self.age += 1
        if self.age > config.ANT_LIFESPAN:
            self.alive = False
    
    def update(self):
        """
        Perform a single update step
        """
        if not self.alive:
            return
            
        # Sense the environment
        inputs = self.sense_environment()
        
        # Think about what to do
        outputs = self.think(inputs)
        
        # Apply the chosen action
        self.apply_action(outputs)
        
        # Update memory for learning
        self.update_memory(inputs, outputs)
    
    def update_memory(self, inputs, outputs):
        """Store experience in memory for learning"""
        # Calculate reward
        reward = 0
        
        # Reward for getting closer to food when not carrying
        if not self.carrying_food:
            food_distance = inputs[4] * config.ANT_VISION_RANGE
            if food_distance < self.last_food_distance:
                reward += 0.1
            self.last_food_distance = food_distance
        
        # Reward for getting closer to nest when carrying food
        if self.carrying_food:
            nest_distance = inputs[0] * config.WORLD_WIDTH
            if nest_distance < self.last_nest_distance:
                reward += 0.1
            self.last_nest_distance = nest_distance
        
        # Big reward for picking up food
        if self.carrying_food and self.food_item is not None:
            reward += 1.0
            
        # Big reward for delivering food to nest
        if not self.carrying_food and self.food_item is None and self.was_carrying_food:
            reward += 10.0
            
        self.was_carrying_food = self.carrying_food
        
        # Store experience
        experience = (inputs, outputs, reward)
        self.memory.append(experience)
        
        # Keep memory at a reasonable size
        if len(self.memory) > 1000:
            self.memory.pop(0)
    
    def get_fitness(self):
        """Calculate fitness score for genetic selection"""
        # Base fitness on food delivered and distance traveled
        return self.colony.food_delivered