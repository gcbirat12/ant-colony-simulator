# colony_view.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Colony visualization for the AI Ant Colony Simulator
"""

import pygame
import numpy as np
from utils.vector import Vector2D
import config


class ColonyView:
    """
    Visualizes the ant colony and environment
    """
    
    def __init__(self, colony, rect):
        """
        Initialize the colony view
        
        Args:
            colony: The ant colony to visualize
            rect: The rectangle to draw in (x, y, width, height)
        """
        self.colony = colony
        self.rect = pygame.Rect(rect)
        
        # View state
        self.offset_x = 0
        self.offset_y = 0
        self.zoom = 1.0
        self.dragging = False
        self.last_mouse_pos = None
        
        # Setup surfaces
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.pheromone_surface = pygame.Surface(
            (self.rect.width, self.rect.height), 
            pygame.SRCALPHA
        )
        
        # Generate nest background texture
        self.nest_texture = self._generate_nest_texture()
    
    def _generate_nest_texture(self):
        """Generate a texture for the nest"""
        size = config.NEST_RADIUS * 2
        texture = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Fill with base color
        pygame.draw.circle(
            texture, 
            config.COLOR_NEST, 
            (size//2, size//2), 
            config.NEST_RADIUS
        )
        
        # Add some random noise for texture
        for _ in range(100):
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, config.NEST_RADIUS)
            x = int(size//2 + radius * np.cos(angle))
            y = int(size//2 + radius * np.sin(angle))
            
            # Draw small darker spots
            spot_color = (
                max(0, config.COLOR_NEST[0] - 30),
                max(0, config.COLOR_NEST[1] - 30),
                max(0, config.COLOR_NEST[2] - 30)
            )
            spot_size = np.random.randint(2, 6)
            pygame.draw.circle(texture, spot_color, (x, y), spot_size)
        
        return texture
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        # Handle zooming
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                zoom_factor = 1.1 if event.y > 0 else 1/1.1
                self.zoom = max(config.ZOOM_MIN, min(config.ZOOM_MAX, self.zoom * zoom_factor))
        
        # Handle dragging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2 and self.rect.collidepoint(event.pos):  # Middle button
                self.dragging = True
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:  # Middle button
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and self.last_mouse_pos is not None:
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                self.offset_x += dx
                self.offset_y += dy
                self.last_mouse_pos = event.pos
    
    def screen_to_world(self, pos):
        """
        Convert screen coordinates to world coordinates
        
        Args:
            pos: Screen position (x, y)
            
        Returns:
            World position (x, y)
        """
        # Adjust for view position
        x = (pos[0] - self.rect.x - self.offset_x) / self.zoom
        y = (pos[1] - self.rect.y - self.offset_y) / self.zoom
        
        return x, y
    
    def world_to_screen(self, x, y):
        """
        Convert world coordinates to screen coordinates
        
        Args:
            x: World x-coordinate
            y: World y-coordinate
            
        Returns:
            Screen position (x, y)
        """
        # Apply zoom and offset
        screen_x = int(x * self.zoom + self.offset_x + self.rect.x)
        screen_y = int(y * self.zoom + self.offset_y + self.rect.y)
        
        return screen_x, screen_y
    
    def draw(self, window, show_pheromones=True):
        """
        Draw the colony and environment
        
        Args:
            window: Pygame window to draw on
            show_pheromones: Whether to show pheromone trails
        """
        # Clear the surface
        self.surface.fill(config.COLOR_BACKGROUND)
        
        # Draw pheromones if enabled
        if show_pheromones:
            self._draw_pheromones()
            self.surface.blit(self.pheromone_surface, (0, 0))
        
        # Draw the nest
        self._draw_nest()
        
        # Draw food sources
        self._draw_food()
        
        # Draw ants
        self._draw_ants()
        
        # Draw debug information if enabled
        if config.DEBUG_MODE:
            self._draw_debug()
        
        # Blit the surface to the window
        window.blit(self.surface, self.rect)
    
    def _draw_pheromones(self):
        """Draw pheromone trails"""
        # Clear the pheromone surface
        self.pheromone_surface.fill((0, 0, 0, 0))
        
        # Get pheromone system from environment
        pheromone_system = self.colony.environment.pheromone_system
        
        # Draw each type of pheromone
        for pheromone_type, grid in pheromone_system.grids.items():
            color = pheromone_system.colors[pheromone_type]
            
            # Loop through the grid
            for i in range(pheromone_system.grid_width):
                for j in range(pheromone_system.grid_height):
                    intensity = grid[i, j]
                    if intensity > 0.1:  # Only draw visible amounts
                        # Calculate world position
                        x = i * pheromone_system.resolution
                        y = j * pheromone_system.resolution
                        
                        # Convert to screen position
                        screen_x, screen_y = self.world_to_screen(x, y)
                        
                        # Only draw if on screen
                        if (0 <= screen_x < self.rect.width and 
                                0 <= screen_y < self.rect.height):
                            # Adjust size based on intensity
                            size = max(1, int(min(intensity, 10) * self.zoom))
                            
                            # Adjust alpha based on intensity
                            alpha = min(255, int(intensity * 200))
                            pheromone_color = (color[0], color[1], color[2], alpha)
                            
                            # Draw the pheromone
                            pygame.draw.circle(
                                self.pheromone_surface, 
                                pheromone_color, 
                                (screen_x, screen_y), 
                                size
                            )
    
    def _draw_nest(self):
        """Draw the colony nest"""
        # Get nest position
        nest_pos = self.colony.nest.position
        
        # Convert to screen position
        screen_x, screen_y = self.world_to_screen(nest_pos.x, nest_pos.y)
        
        # Scale the nest texture
        scaled_size = int(self.colony.nest.radius * 2 * self.zoom)
        if scaled_size > 0:
            scaled_texture = pygame.transform.scale(
                self.nest_texture, 
                (scaled_size, scaled_size)
            )
            
            # Draw the scaled texture
            texture_rect = scaled_texture.get_rect(
                center=(screen_x, screen_y)
            )
            self.surface.blit(scaled_texture, texture_rect)
            
            # Draw a border
            pygame.draw.circle(
                self.surface, 
                (100, 70, 40), 
                (screen_x, screen_y), 
                int(self.colony.nest.radius * self.zoom),
                max(1, int(2 * self.zoom))
            )
    
    def _draw_food(self):
        """Draw food sources"""
        for food in self.colony.environment.food_sources:
            # Convert to screen position
            screen_x, screen_y = self.world_to_screen(food.position.x, food.position.y)
            
            # Calculate screen size
            size = max(1, int(food.size * self.zoom))
            
            # Draw the food
            pygame.draw.circle(
                self.surface, 
                food.color, 
                (screen_x, screen_y), 
                size
            )
    
    def _draw_ants(self):
        """Draw all ants"""
        for ant in self.colony.ants:
            if not ant.alive:
                continue
                
            # Convert to screen position
            screen_x, screen_y = self.world_to_screen(ant.position.x, ant.position.y)
            
            # Check if on screen
            if (screen_x < -20 or screen_x > self.rect.width + 20 or
                    screen_y < -20 or screen_y > self.rect.height + 20):
                continue
                
            # Calculate screen size
            size = max(1, int(config.ANT_SIZE * self.zoom))
            
            # Determine ant color (carrying food or not)
            color = (220, 170, 50) if ant.carrying_food else config.COLOR_ANT
            
            # Draw the ant body
            pygame.draw.circle(
                self.surface, 
                color, 
                (screen_x, screen_y), 
                size
            )
            
            # Draw direction indicator
            direction_x = ant.position.x + ant.direction.x * config.ANT_SIZE * 1.5
            direction_y = ant.position.y + ant.direction.y * config.ANT_SIZE * 1.5
            head_x, head_y = self.world_to_screen(direction_x, direction_y)
            
            pygame.draw.line(
                self.surface, 
                (50, 50, 50), 
                (screen_x, screen_y), 
                (head_x, head_y), 
                max(1, int(self.zoom))
            )
    
    def _draw_debug(self):
        """Draw debug information"""
        # Draw coordinate grid
        grid_spacing = 100
        for x in range(0, config.WORLD_WIDTH, grid_spacing):
            start_x, start_y = self.world_to_screen(x, 0)
            end_x, end_y = self.world_to_screen(x, config.WORLD_HEIGHT)
            pygame.draw.line(
                self.surface, 
                (50, 50, 60), 
                (start_x, start_y), 
                (end_x, end_y), 
                1
            )
            
        for y in range(0, config.WORLD_HEIGHT, grid_spacing):
            start_x, start_y = self.world_to_screen(0, y)
            end_x, end_y = self.world_to_screen(config.WORLD_WIDTH, y)
            pygame.draw.line(
                self.surface, 
                (50, 50, 60), 
                (start_x, start_y), 
                (end_x, end_y), 
                1
            )
            
        # Draw ant vision ranges if enabled
        if config.SHOW_ANT_VISION:
            for ant in self.colony.ants:
                if not ant.alive:
                    continue
                    
                screen_x, screen_y = self.world_to_screen(ant.position.x, ant.position.y)
                vision_radius = int(config.ANT_VISION_RANGE * self.zoom)
                
                pygame.draw.circle(
                    self.surface, 
                    (100, 100, 150, 128), 
                    (screen_x, screen_y), 
                    vision_radius, 
                    1
                )