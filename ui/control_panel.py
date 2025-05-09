#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Control panel UI for the AI Ant Colony Simulator
"""

import pygame
import os
import config


class Button:
    """Simple button class for the UI"""
    
    def __init__(self, rect, text, callback, color=(100, 100, 120)):
        """
        Initialize a button
        
        Args:
            rect: Button rectangle (x, y, width, height)
            text: Button text
            callback: Function to call when clicked
            color: Button color
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.color = color
        self.hover_color = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
        self.text_color = (230, 230, 230)
        self.hovered = False
        self.font = pygame.font.SysFont('Arial', 16)
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if the event was handled, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False
    
    def draw(self, surface):
        """
        Draw the button
        
        Args:
            surface: Surface to draw on
        """
        # Draw button background
        pygame.draw.rect(
            surface, 
            self.hover_color if self.hovered else self.color, 
            self.rect, 
            border_radius=5
        )
        
        # Draw button border
        pygame.draw.rect(
            surface, 
            (150, 150, 170), 
            self.rect, 
            width=2, 
            border_radius=5
        )
        
        # Draw button text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class Slider:
    """Simple slider class for the UI"""
    
    def __init__(self, rect, min_value, max_value, initial_value, callback, label=""):
        """
        Initialize a slider
        
        Args:
            rect: Slider rectangle (x, y, width, height)
            min_value: Minimum value
            max_value: Maximum value
            initial_value: Initial value
            callback: Function to call when value changes
            label: Slider label
        """
        self.rect = pygame.Rect(rect)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.callback = callback
        self.label = label
        self.dragging = False
        self.font = pygame.font.SysFont('Arial', 14)
        self.track_color = (80, 80, 100)
        self.handle_color = (150, 150, 170)
        self.handle_hover_color = (180, 180, 200)
        self.hovered = False
        
        # Calculate handle position
        self._update_handle_rect()
    
    def _update_handle_rect(self):
        """Update the handle rectangle based on the current value"""
        value_range = self.max_value - self.min_value
        if value_range == 0:
            position = 0
        else:
            position = (self.value - self.min_value) / value_range
            
        handle_x = int(self.rect.x + position * self.rect.width)
        handle_width = 10
        self.handle_rect = pygame.Rect(
            handle_x - handle_width//2, 
            self.rect.y, 
            handle_width, 
            self.rect.height
        )
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
            
        Returns:
            True if the event was handled, False otherwise
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                return True
            elif self.rect.collidepoint(event.pos):
                # Click directly on the track
                self._set_value_from_position(event.pos[0])
                self.dragging = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION:
            self.hovered = self.handle_rect.collidepoint(event.pos)
            
            if self.dragging:
                self._set_value_from_position(event.pos[0])
                return True
                
        return False
    
    def _set_value_from_position(self, x_pos):
        """
        Set the slider value based on mouse position
        
        Args:
            x_pos: Mouse x-position
        """
        position = (x_pos - self.rect.x) / self.rect.width
        position = max(0, min(1, position))
        self.value = self.min_value + position * (self.max_value - self.min_value)
        self._update_handle_rect()
        self.callback(self.value)
    
    def draw(self, surface):
        """
        Draw the slider
        
        Args:
            surface: Surface to draw on
        """
        # Draw label
        if self.label:
            label_surface = self.font.render(self.label, True, (200, 200, 200))
            label_rect = label_surface.get_rect(
                bottomleft=(self.rect.x, self.rect.y - 5)
            )
            surface.blit(label_surface, label_rect)
        
        # Draw value
        value_text = f"{self.value:.2f}"
        value_surface = self.font.render(value_text, True, (200, 200, 200))
        value_rect = value_surface.get_rect(
            bottomright=(self.rect.right, self.rect.y - 5)
        )
        surface.blit(value_surface, value_rect)
        
        # Draw track
        pygame.draw.rect(surface, self.track_color, self.rect, border_radius=3)
        
        # Draw handle
        handle_color = self.handle_hover_color if self.hovered or self.dragging else self.handle_color
        pygame.draw.rect(surface, handle_color, self.handle_rect, border_radius=3)


class ControlPanel:
    """
    Control panel for the AI Ant Colony Simulator
    """
    
    def __init__(self, app, rect):
        """
        Initialize the control panel
        
        Args:
            app: The main application
            rect: The rectangle to draw in (x, y, width, height)
        """
        self.app = app
        self.rect = pygame.Rect(rect)
        self.surface = pygame.Surface((self.rect.width, self.rect.height))
        self.font = pygame.font.SysFont('Arial', 18)
        self.small_font = pygame.font.SysFont('Arial', 12)
        
        # Make sure app has necessary attributes
        if not hasattr(self.app, 'paused'):
            self.app.paused = False
            
        if not hasattr(self.app, 'show_pheromones'):
            self.app.show_pheromones = True
        
        # Create UI controls
        self.controls = []
        self._create_controls()
    
    def _create_controls(self):
        """Create UI controls"""
        # Fixed margins and dimensions
        panel_margin = 10  # Margin from panel edges
        button_margin = 5  # Margin between buttons
        button_width = self.rect.width - (panel_margin * 2)
        button_height = 30
        
        # Start position for first button
        button_x = panel_margin
        button_y = 60  # Leave space for title
        
        # Pause/Play button
        self.pause_button = Button(
            (button_x, button_y, button_width, button_height),
            "Pause" if not self.app.paused else "Play",
            self._toggle_pause,
            color=(120, 90, 90) if not self.app.paused else (90, 120, 90)
        )
        self.controls.append(self.pause_button)
        button_y += button_height + button_margin
        
        # Toggle pheromones button
        self.pheromone_button = Button(
            (button_x, button_y, button_width, button_height),
            "Hide Pheromones" if self.app.show_pheromones else "Show Pheromones",
            self._toggle_pheromones,
            color=(90, 90, 120)
        )
        self.controls.append(self.pheromone_button)
        button_y += button_height + button_margin
        
        # Evolution button
        self.evolve_button = Button(
            (button_x, button_y, button_width, button_height),
            "Force Evolution",
            self._force_evolution,
            color=(100, 90, 120)
        )
        self.controls.append(self.evolve_button)
        button_y += button_height + button_margin
        
        # Save button
        self.save_button = Button(
            (button_x, button_y, button_width, button_height),
            "Save Model",
            self._save_model,
            color=(90, 120, 100)
        )
        self.controls.append(self.save_button)
        button_y += button_height + button_margin
        
        # Add sliders
        slider_y = button_y + 20
        slider_height = 20
        
        # Speed slider
        self.speed_slider = Slider(
            (button_x, slider_y, button_width, slider_height),
            0.1, 10.0, self.app.speed,
            self._set_speed,
            "Simulation Speed"
        )
        self.controls.append(self.speed_slider)
        slider_y += slider_height + 30  # Extra space for labels
        
        # Mutation rate slider
        self.mutation_slider = Slider(
            (button_x, slider_y, button_width, slider_height),
            0.01, 0.5, config.MUTATION_RATE,
            self._set_mutation_rate,
            "Mutation Rate"
        )
        self.controls.append(self.mutation_slider)
        slider_y += slider_height + 30  # Extra space for labels
        
        # Crossover rate slider
        self.crossover_slider = Slider(
            (button_x, slider_y, button_width, slider_height),
            0.1, 1.0, config.CROSSOVER_RATE,
            self._set_crossover_rate,
            "Crossover Rate"
        )
        self.controls.append(self.crossover_slider)
        
        # Store the y-position after all controls for help text placement
        self.controls_end_y = slider_y + slider_height + 30
    
    def _toggle_pause(self):
        """Toggle pause state"""
        self.app.paused = not self.app.paused
        self.pause_button.text = "Pause" if not self.app.paused else "Play"
        self.pause_button.color = (120, 90, 90) if not self.app.paused else (90, 120, 90)
    
    def _toggle_pheromones(self):
        """Toggle pheromone visibility"""
        self.app.show_pheromones = not self.app.show_pheromones
        self.pheromone_button.text = "Hide Pheromones" if self.app.show_pheromones else "Show Pheromones"
    
    def _force_evolution(self):
        """Force an evolution step"""
        self.app.evolution_manager.evolve_generation()
    
    def _save_model(self):
        """Save the current model"""
        self.app.evolution_manager.save_model()
    
    def _set_speed(self, value):
        """Set simulation speed"""
        self.app.speed = value
        self.app.steps_per_frame = max(1, int(value))
    
    def _set_mutation_rate(self, value):
        """Set mutation rate"""
        config.MUTATION_RATE = value
    
    def _set_crossover_rate(self, value):
        """Set crossover rate"""
        config.CROSSOVER_RATE = value
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: Pygame event
        """
        # Adjust event position for panel coordinates
        if hasattr(event, 'pos'):
            # Only process events inside the panel
            if not self.rect.collidepoint(event.pos):
                return False
                
            # Convert global coordinates to panel-local coordinates
            local_pos = (event.pos[0] - self.rect.x, event.pos[1] - self.rect.y)
            
            # Create a modified event with local coordinates
            modified_event = pygame.event.Event(event.type, {**event.dict, 'pos': local_pos})
            
            # Pass the modified event to controls
            for control in self.controls:
                if control.handle_event(modified_event):
                    return True
        
        return False
    
    def draw(self, window):
        """
        Draw the control panel
        
        Args:
            window: Pygame window to draw on
        """
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
        title_surface = self.font.render("Control Panel", True, (220, 220, 220))
        title_rect = title_surface.get_rect(
            center=(self.rect.width // 2, 25)
        )
        self.surface.blit(title_surface, title_rect)
        
        # Draw generation info
        gen_number = getattr(self.app.evolution_manager, 'generation', 0)
        gen_text = f"Generation: {gen_number}"
        gen_surface = self.small_font.render(gen_text, True, (200, 200, 200))
        gen_rect = gen_surface.get_rect(topleft=(10, 40))
        self.surface.blit(gen_surface, gen_rect)
        
        # Draw controls
        for control in self.controls:
            control.draw(self.surface)
        
        # Draw help text section title
        help_title = self.small_font.render("Controls:", True, (200, 200, 220))
        help_title_rect = help_title.get_rect(topleft=(10, self.controls_end_y + 10))
        self.surface.blit(help_title, help_title_rect)
        
        # Draw help text in two columns to save space
        help_texts_left = [
            "Space - Pause/Resume",
            "E - Force Evolution",
            "S - Save Model",
            "P - Toggle Pheromones",
            "+/- - Adjust Speed"
        ]
        
        help_texts_right = [
            "Mouse Wheel - Zoom",
            "Middle Mouse - Pan",
            "Left Click - Add Food",
            "Right Click - Add Ant"
        ]
        
        # Position for help text
        help_y = self.controls_end_y + 30
        line_height = 18
        
        # Draw left column
        for text in help_texts_left:
            help_surface = self.small_font.render(text, True, (180, 180, 180))
            self.surface.blit(help_surface, (10, help_y))
            help_y += line_height
        
        # Reset Y position for right column
        help_y = self.controls_end_y + 30
        right_x = self.rect.width // 2 + 10
        
        # Draw right column
        for text in help_texts_right:
            help_surface = self.small_font.render(text, True, (180, 180, 180))
            self.surface.blit(help_surface, (right_x, help_y))
            help_y += line_height
        
        # Blit the surface to the window
        window.blit(self.surface, self.rect)