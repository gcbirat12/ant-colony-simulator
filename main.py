# main.py
#!/usr/bin/env python3

"""
AI Ant Colony Simulator - Main Entry Point
"""

import sys
import argparse
from ui.app import AntColonyApp
from core.colony import Colony
from core.environment import Environment
from ml.evolution import EvolutionManager
import config

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='AI Ant Colony Simulator')
    parser.add_argument('--ants', type=int, default=config.DEFAULT_ANT_COUNT,
                        help=f'Number of ants (default: {config.DEFAULT_ANT_COUNT})')
    parser.add_argument('--food', type=int, default=config.DEFAULT_FOOD_COUNT,
                        help=f'Amount of food (default: {config.DEFAULT_FOOD_COUNT})')
    parser.add_argument('--speed', type=float, default=config.DEFAULT_SIMULATION_SPEED,
                        help=f'Simulation speed (default: {config.DEFAULT_SIMULATION_SPEED})')
    parser.add_argument('--headless', action='store_true',
                        help='Run without UI (for faster training)')
    parser.add_argument('--load-model', type=str,
                        help='Load saved model from file')
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    args = parse_args()
    
    # Set up the environment and colony
    environment = Environment(width=config.WORLD_WIDTH, height=config.WORLD_HEIGHT)
    colony = Colony(environment, initial_ants=args.ants)
    environment.generate_food(args.food)
    
    # Set up evolution manager
    evolution_manager = EvolutionManager(colony)
    
    # Load a saved model if specified
    if args.load_model:
        try:
            evolution_manager.load_model(args.load_model)
            print(f"Successfully loaded model from {args.load_model}")
        except Exception as e:
            print(f"Error loading model: {e}")
            return
    
    # Run with or without UI
    if args.headless:
        # Run without UI for faster training
        print("Running in headless mode for accelerated training...")
        evolution_manager.run_headless(generations=config.TRAINING_GENERATIONS)
        evolution_manager.save_model(config.MODEL_SAVE_PATH)
    else:
        # Launch the UI
        app = AntColonyApp(colony, evolution_manager, speed=args.speed)
        app.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting AI Ant Colony Simulator")
        sys.exit(0)