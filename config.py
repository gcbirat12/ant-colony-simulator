# config.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for the AI Ant Colony Simulator
"""

# World settings
WORLD_WIDTH = 1200
WORLD_HEIGHT = 800
WRAP_WORLD = True  # Whether ants can wrap around the edges of the world

# Default simulation parameters
DEFAULT_ANT_COUNT = 20
DEFAULT_FOOD_COUNT = 200
DEFAULT_SIMULATION_SPEED = 1.0

# Colony settings
NEST_RADIUS = 50
INITIAL_ENERGY = 500
MAX_COLONY_SIZE = 500

# Ant parameters
ANT_SIZE = 8
ANT_VISION_RANGE = 50
ANT_SPEED = 3
ANT_ENERGY_CONSUMPTION = 0.05
ANT_ENERGY_FROM_FOOD = 100
ANT_LIFESPAN = 3000  # in simulation steps

# Food settings
FOOD_SIZE = 5
FOOD_ENERGY = 50
FOOD_SPAWN_RATE = 0.02  # Probability of new food appearing per step

# Pheromone settings
PHEROMONE_DEPOSIT = 10
PHEROMONE_EVAPORATION_RATE = 0.995  # Multiplier applied each step (< 1)
PHEROMONE_DIFFUSION = 0.05

# Machine Learning parameters
NEURAL_NETWORK_LAYERS = [16, 32, 16]  # Hidden layer sizes
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
SELECTION_PRESSURE = 0.8
GENERATION_LENGTH = 5000  # Steps before evolutionary update
TRAINING_GENERATIONS = 100

# UI settings
UI_UPDATE_INTERVAL = 20  # milliseconds between UI updates
ZOOM_MIN = 0.5
ZOOM_MAX = 5.0
ZOOM_STEP = 0.1

# File paths
MODEL_SAVE_PATH = "models/ant_model.pkl"
LOG_FILE_PATH = "logs/simulation.log"

# Colors
COLOR_BACKGROUND = (20, 20, 30)
COLOR_NEST = (150, 100, 50)
COLOR_FOOD = (50, 200, 50)
COLOR_ANT = (200, 200, 200)
COLOR_PHEROMONE_FOOD = (50, 200, 50, 128)
COLOR_PHEROMONE_HOME = (50, 50, 200, 128)

# Debug
DEBUG_MODE = False
SHOW_ANT_VISION = False
SHOW_NEURAL_OUTPUTS = False