# stats_panel.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics panel UI for the AI Ant Colony Simulator
"""

import pygame
import numpy as np
import time
from collections import deque
import config


class Graph:
    """Simple graph widget for the stats panel"""
    
    def __init__(self, rect, title, color=(100, 200, 100), max_points=100):
        """
        Initialize a graph
        
        Args:
            rect: Graph rectangle (x, y, width, height)
            title: Graph title
            color: Line color
            max_points: Maximum number of data points to display
        """
        self.rect = pygame.Rect(rect)
        self.title = title
        self.color = color
        self.max_points = max_points
        self.data = deque(maxlen=max_points)
        self.min_value = 0
        self.max_value = 1
        self.auto_scale = True
        self.font = pygame.font.SysFont('Arial', 14)
    
    def add_point(self, value):
        """
        Add a data point to the graph
        
        Args:
            value: Value to add
        """
        self.data.append(value)
        
        # Update min and max values if auto-scaling
        if self.auto_scale and len(self.data) > 0:
            self.min_value = min(self.data)
            self.max_value = max(self.data)
            
            # Add a 10% margin
            value_range = self.max_value - self.min_value
            if value_range == 0:
                value_range = 1
                
            self.min_value -= value_range * 0.1
            self.max_value += value_range * 0.1
    
    def draw(self, surface):
        """
        Draw the graph
        
        Args:
            surface: Surface to draw on
        """
        # Draw background
        pygame.draw.rect(surface, (50, 50, 60), self.rect, border_radius=5)
        pygame.draw.rect(surface, (70, 70, 80), self.rect, width=1, border_radius=5)
        
        # Draw title
        title_surface = self.font.render(self.title, True, (200, 200, 200))
        title_rect = title_surface.get_rect(topleft=(self.rect.x + 5, self.rect.y + 5))
        surface.blit(title_surface, title_rect)
        
        # Draw y-axis labels
        if len(self.data) > 0:
            min_label = self.font.render(f"{self.min_value:.1f}", True, (180, 180, 180))
            max_label = self.font.render(f"{self.max_value:.1f}", True, (180, 180, 180))
            
            surface.blit(min_label, (self.rect.x + 5, self.rect.bottom - 20))
            surface.blit(max_label, (self.rect.x + 5, self.rect.y + 25))
        
        # Draw data points
        if len(self.data) > 1:
            # Calculate scale factors
            x_scale = self.rect.width / (self.max_points - 1 if self.max_points > 1 else 1)
            
            value_range = self.max_value - self.min_value
            if value_range == 0:
                value_range = 1
            y_scale = (self.rect.height - 40) / value_range
            
            # Draw connecting lines
            points = []
            for i, value in enumerate(self.data):
                x = self.rect.x + i * x_scale
                y = self.rect.bottom - 20 - (value - self.min_value) * y_scale
                points.append((x, y))
            
            if len(points) > 1:
                pygame.draw.lines(surface, self.color, False, points, width=2)


class StatsPanel:
    """
    Statistics panel for the AI Ant Colony Simulator
    """
    
    def __init__(self, colony, rect):
        """
        Initialize the stats panel
        
        Args:
            colony: The ant colony
            rect: The rectangle to draw in (x, y, width, height)
        """
        self.colony = colony
        self.rect = pygame.Rect(rect)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.font = pygame.font.SysFont('Arial', 18)
        self.small_font = pygame.font.SysFont('Arial', 14)
        
        # Performance tracking
        self.fps_history = deque(maxlen=60)
        self.last_update_time = time.time()
        
        # Statistics
        self.stats = {
            'population': 0,
            'food_collected': 0,
            'food_delivered': 0,
            'efficiency': 0
        }
        
        # Create graphs
        self._create_graphs()
        
        # Update timer
        self.last_graph_update = 0
        self.graph_update_interval = 30  # Update every 30 frames
    
    def _create_graphs(self):
        """Create statistics graphs"""
        graph_width = self.rect.width - 20
        graph_height = 100
        graph_x = self.rect.x + 10
        graph_y = self.rect.y + 50
        
        # Population graph
        self.population_graph = Graph(
            (10, graph_y - self.rect.y, graph_width, graph_height),
            "Population",
            color=(100, 180, 220)
        )
        graph_y += graph_height + 20
        
        # Food delivery graph
        self.food_graph = Graph(
            (10, graph_y - self.rect.y, graph_width, graph_height),
            "Food Delivered",
            color=(100, 220, 100)
        )
        graph_y += graph_height + 20
        
        # Efficiency graph
        self.efficiency_graph = Graph(
            (10, graph_y - self.rect.y, graph_width, graph_height),
            "Efficiency",
            color=(220, 180, 100)
        )
    
    def update(self):
        """Update statistics"""
        # Calculate FPS
        current_time = time.time()
        frame_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        if frame_time > 0:
            fps = 1.0 / frame_time
            self.fps_history.append(fps)
        
        # Get colony stats
        self.stats = self.colony.get_colony_stats()
        
        # Update graphs (not every frame for performance)
        self.last_graph_update += 1
        if self.last_graph_update >= self.graph_update_interval:
            self.last_graph_update = 0
            
            self.population_graph.add_point(self.stats['population'])
            self.food_graph.add_point(self.stats['food_delivered'])
            self.efficiency_graph.add_point(self.stats['efficiency'] * 1000)  # Scale for better visibility
    
    def draw(self, window):
        """
        Draw the stats panel
        
        Args:
            window: Pygame window to draw on
        """
        # Update stats before drawing
        self.update()
        
        # Clear the surface
        self.surface.fill((40, 40, 50))
        
        # Draw panel border
        pygame.draw.rect(
            self.surface, 
            (70, 70, 80), 
            (0, 0, self.rect.width, self.rect.height), 
            width=2
        )
        
        # Draw panel title
        title_surface = self.font.render("Statistics", True, (220, 220, 220))
        title_rect = title_surface.get_rect(
            center=(self.rect.width // 2, 25)
        )
        self.surface.blit(title_surface, title_rect)
        
        # Draw FPS counter
        if len(self.fps_history) > 0:
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            fps_text = f"FPS: {avg_fps:.1f}"
            fps_surface = self.small_font.render(fps_text, True, (180, 180, 180))
            fps_rect = fps_surface.get_rect(topright=(self.rect.width - 10, 10))
            self.surface.blit(fps_surface, fps_rect)
        
        # Draw graphs
        self.population_graph.draw(self.surface)
        self.food_graph.draw(self.surface)
        self.efficiency_graph.draw(self.surface)
        
        # Draw additional stats at the bottom
        stats_y = self.rect.height - 100
        stats_texts = [
            f"Population: {self.stats['population']}",
            f"Food Collected: {self.stats['food_collected']:.0f}",
            f"Food Delivered: {self.stats['food_delivered']}",
            f"Ants Born: {self.stats['ants_born']}",
            f"Ants Died: {self.stats['ants_died']}",
            f"Total Steps: {self.stats['total_steps']}"
        ]
        
        for text in stats_texts:
            stat_surface = self.small_font.render(text, True, (200, 200, 200))
            stat_rect = stat_surface.get_rect(topleft=(10, stats_y))
            self.surface.blit(stat_surface, stat_rect)
            stats_y += 20
        
        # Blit the surface to the window
        window.blit(self.surface, self.rect)