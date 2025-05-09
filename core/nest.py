# nest.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nest representation for the AI Ant Colony Simulator
"""

from utils.vector import Vector2D
import config


class Nest:
    """
    Represents the ant colony's nest
    """
    
    def __init__(self, x, y, radius=config.NEST_RADIUS):
        """
        Initialize a nest
        
        Args:
            x: X-coordinate of the nest center
            y: Y-coordinate of the nest center
            radius: Radius of the nest
        """
        self.position = Vector2D(x, y)
        self.radius = radius
        self.color = config.COLOR_NEST
        
        # Nest properties
        self.food_stored = 0
        self.structure_level = 1
        self.chambers = {
            'food': {'size': 1, 'capacity': 100},
            'nursery': {'size': 1, 'capacity': 20},
            'queen': {'size': 1, 'capacity': 1}
        }
        
    def add_food(self, amount):
        """
        Add food to the nest storage
        
        Args:
            amount: Amount of food to add
        """
        self.food_stored += amount
        
        # Check if we can upgrade
        self._check_upgrades()
        
    def _check_upgrades(self):
        """Check if the nest can be upgraded based on food stored"""
        # Upgrade nest if we have enough food
        if self.food_stored >= self.structure_level * 100:
            self.food_stored -= self.structure_level * 100
            self.structure_level += 1
            self.radius += 5
            
            # Upgrade chambers
            for chamber in self.chambers.values():
                chamber['size'] += 1
                chamber['capacity'] = chamber['size'] * chamber['capacity']
    
    def update(self):
        """Update the nest (currently no behavior)"""
        pass