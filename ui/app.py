#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main application window for the AI Ant Colony Simulator
"""

import pygame
import sys
import time
from ui.colony_view import ColonyView
from ui.control_panel import ControlPanel
from ui.stats_panel import StatsPanel
from core.ant import Ant
from utils.vector import Vector2D
import config


class AntColonyApp:
    """
    Main application class for the AI Ant Colony Simulator
    """
    
    def __init__(self, colony, evolution_manager, speed=1.0):
        """
        Initialize the application
        
        Args:
            colony: The ant colony to visualize
            evolution_manager: The evolution manager
            speed: Simulation speed multiplier
        """
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("AI Ant Colony Simulator")
        
        # Store references
        self.colony = colony
        self.evolution_manager = evolution_manager
        self.speed = speed
        
        # Explicitly set simulation state variables BEFORE creating UI components
        self.running = False
        self.paused = False  # This is critical - UI references this
        self.show_pheromones = True
        self.steps_per_frame = max(1, int(speed))
        self.generation_timer = 0
        
        # Set up the window
        self.window_width = config.WORLD_WIDTH + 300  # Main view + side panel
        self.window_height = config.WORLD_HEIGHT
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        
        # NOW create the UI components (after all attributes are initialized)
        self.colony_view = ColonyView(self.colony, (0, 0, config.WORLD_WIDTH, config.WORLD_HEIGHT))
        self.control_panel = ControlPanel(
            self, 
            (config.WORLD_WIDTH, 0, 300, config.WORLD_HEIGHT // 2)
        )
        self.stats_panel = StatsPanel(
            self.colony, 
            (config.WORLD_WIDTH, config.WORLD_HEIGHT // 2, 300, config.WORLD_HEIGHT // 2)
        )
        
        # Timing
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.last_update = time.time()
    
    def run(self):
        """
        Main application loop
        """
        self.running = True
        
        while self.running:
            # Process events
            self.handle_events()
            
            # Update simulation if not paused
            if not self.paused:
                for _ in range(self.steps_per_frame):
                    self.update()
            
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(self.fps)
    
    def handle_events(self):
        """
        Process pygame events
        """
        for event in pygame.event.get():
            # Check for quit event
            if event.type == pygame.QUIT:
                self.quit()
            # Handle keypress events
            elif event.type == pygame.KEYDOWN:
                self.handle_keypress(event.key)
            # Handle mouse events
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_event(event)
                
            # Forward events to UI components
            self.control_panel.handle_event(event)
            self.colony_view.handle_event(event)
    
    def handle_keypress(self, key):
        """
        Handle keyboard input
        
        Args:
            key: Pygame key constant
        """
        if key == pygame.K_ESCAPE:
            self.quit()
        elif key == pygame.K_SPACE:
            self.paused = not self.paused
            print(f"Simulation {'paused' if self.paused else 'resumed'}")
        elif key == pygame.K_p:
            self.show_pheromones = not self.show_pheromones
        elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
            self.speed = min(10.0, self.speed * 1.2)
            self.steps_per_frame = max(1, int(self.speed))
        elif key == pygame.K_MINUS:
            self.speed = max(0.1, self.speed / 1.2)
            self.steps_per_frame = max(1, int(self.speed))
        elif key == pygame.K_e:
            # Force evolution
            self.evolution_manager.evolve_generation()
        elif key == pygame.K_s:
            # Save model
            self.evolution_manager.save_model()
    
    def handle_mouse_event(self, event):
        """
        Handle mouse input
        
        Args:
            event: Pygame event
        """
        # Check if the event is in the colony view area
        if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] < config.WORLD_WIDTH:
            # Left click: Add food
            if event.button == 1:
                x, y = self.colony_view.screen_to_world(event.pos)
                self.colony.environment.generate_food(1)
            # Right click: Add ants
            elif event.button == 3:
                x, y = self.colony_view.screen_to_world(event.pos)
                new_ant = Ant(self.colony, Vector2D(x, y))
                self.colony.ants.append(new_ant)
    
    def update(self):
        """
        Update the simulation state
        """
        # Update the environment
        self.colony.environment.update()
        
        # Update the colony
        self.colony.update()
        
        # Update generation timer
        self.generation_timer += 1
        if self.generation_timer >= config.GENERATION_LENGTH:
            self.generation_timer = 0
            self.evolution_manager.evolve_generation()
    
    def draw(self):
        """
        Draw the application
        """
        # Clear the window
        self.window.fill((20, 20, 30))
        
        # Draw the colony view
        self.colony_view.draw(self.window, show_pheromones=self.show_pheromones)
        
        # Draw UI panels
        self.control_panel.draw(self.window)
        self.stats_panel.draw(self.window)
        
        # Draw simulation speed indicator
        font = pygame.font.SysFont('Arial', 16)
        speed_text = font.render(f"Speed: {self.speed:.1f}x", True, (200, 200, 200))
        self.window.blit(speed_text, (config.WORLD_WIDTH + 10, 10))
        
        # Update the display
        pygame.display.flip()
    
    def quit(self):
        """
        Quit the application
        """
        # Save the model before quitting
        self.evolution_manager.save_model()
        
        # Quit pygame and exit
        pygame.quit()
        self.running = False
        print("Exiting AI Ant Colony Simulator")
        sys.exit(0)