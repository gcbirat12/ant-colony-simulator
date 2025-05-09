# pheromone.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pheromone system for the AI Ant Colony Simulator
"""

import numpy as np
from utils.vector import Vector2D
import config


class PheromoneSystem:
    """
    Manages pheromone deposits and diffusion in the environment
    """
    
    def __init__(self, width, height, resolution=10):
        """
        Initialize the pheromone system
        
        Args:
            width: Environment width
            height: Environment height
            resolution: Grid resolution (lower = more detailed but slower)
        """
        self.width = width
        self.height = height
        self.resolution = resolution
        
        # Calculate grid dimensions
        self.grid_width = width // resolution + 1
        self.grid_height = height // resolution + 1
        
        # Initialize pheromone grids for different types
        self.grids = {
            'food': np.zeros((self.grid_width, self.grid_height)),
            'home': np.zeros((self.grid_width, self.grid_height))
        }
        
        # Set colors for visualization
        self.colors = {
            'food': config.COLOR_PHEROMONE_FOOD,
            'home': config.COLOR_PHEROMONE_HOME
        }
    
    def add_pheromone(self, position, pheromone_type, amount):
        """
        Add pheromone at a specific position
        
        Args:
            position: Position vector
            pheromone_type: Type of pheromone ('food' or 'home')
            amount: Amount of pheromone to deposit
        """
        if pheromone_type not in self.grids:
            return
            
        # Convert world coordinates to grid coordinates
        grid_x = min(int(position.x // self.resolution), self.grid_width - 1)
        grid_y = min(int(position.y // self.resolution), self.grid_height - 1)
        
        # Add pheromone to the grid
        self.grids[pheromone_type][grid_x, grid_y] += amount
    
    def get_intensity(self, position, pheromone_type, radius=10):
        """
        Get the pheromone intensity around a position
        
        Args:
            position: Position vector
            pheromone_type: Type of pheromone ('food' or 'home')
            radius: Radius to check
            
        Returns:
            Dictionary with pheromone intensities in different directions
        """
        if pheromone_type not in self.grids:
            return {'ahead': 0, 'left': 0, 'right': 0}
            
        # Convert world coordinates to grid coordinates
        grid_x = min(int(position.x // self.resolution), self.grid_width - 1)
        grid_y = min(int(position.y // self.resolution), self.grid_height - 1)
        
        # Check grid cells around this position
        grid_radius = max(1, int(radius // self.resolution))
        
        # Function to get value at a grid cell, handling wrapping
        def get_grid_value(dx, dy):
            gx = (grid_x + dx) % self.grid_width
            gy = (grid_y + dy) % self.grid_height
            return self.grids[pheromone_type][gx, gy]
        
        # Sample in three directions (ahead, left, right)
        # For simplicity, just use fixed offsets
        intensities = {
            'ahead': get_grid_value(0, -grid_radius),
            'left': get_grid_value(-grid_radius, 0),
            'right': get_grid_value(grid_radius, 0)
        }
        
        return intensities
    
    def update(self):
        """
        Update the pheromone system (evaporation and diffusion)
        """
        for pheromone_type in self.grids:
            # Apply evaporation
            self.grids[pheromone_type] *= config.PHEROMONE_EVAPORATION_RATE
            
            # Apply diffusion
            if config.PHEROMONE_DIFFUSION > 0:
                # Create a diffused grid
                diffused = np.copy(self.grids[pheromone_type])
                
                # Simple diffusion kernel (average with neighbors)
                for i in range(1, self.grid_width - 1):
                    for j in range(1, self.grid_height - 1):
                        diffused[i, j] = (1 - config.PHEROMONE_DIFFUSION) * self.grids[pheromone_type][i, j] + \
                                        config.PHEROMONE_DIFFUSION * np.mean([
                                            self.grids[pheromone_type][i-1, j],
                                            self.grids[pheromone_type][i+1, j],
                                            self.grids[pheromone_type][i, j-1],
                                            self.grids[pheromone_type][i, j+1]
                                        ])
                
                # Update the grid with diffused values
                self.grids[pheromone_type] = diffused