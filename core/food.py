# food.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Food source representation for the AI Ant Colony Simulator
"""

from utils.vector import Vector2D
import config


class Food:
    """
    Represents a food source in the environment
    """
    
    def __init__(self, x, y, energy=config.FOOD_ENERGY):
        """
        Initialize a food source
        
        Args:
            x: X-coordinate
            y: Y-coordinate
            energy: Energy value of the food
        """
        self.position = Vector2D(x, y)
        self.energy = energy
        self.size = config.FOOD_SIZE
        self.color = config.COLOR_FOOD
        
    def update(self):
        """Update the food source (currently no behavior)"""
        pass