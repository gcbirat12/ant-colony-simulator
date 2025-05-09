# logger.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Logging utility for the AI Ant Colony Simulator
"""

import logging
import os
import time
import config


class SimulationLogger:
    """
    Logger for simulation events and statistics
    """
    
    def __init__(self, log_to_console=True, log_to_file=True):
        """
        Initialize the logger
        
        Args:
            log_to_console: Whether to log to console
            log_to_file: Whether to log to file
        """
        # Create logger
        self.logger = logging.getLogger('AntColonySimulator')
        self.logger.setLevel(logging.INFO)
        
        # Create formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Set up console handler
        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # Set up file handler
        if log_to_file:
            # Create logs directory if it doesn't exist
            os.makedirs(os.path.dirname(config.LOG_FILE_PATH), exist_ok=True)
            
            # Generate log filename with timestamp
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            log_filename = config.LOG_FILE_PATH.replace(
                '.log', f'_{timestamp}.log'
            )
            
            file_handler = logging.FileHandler(log_filename)
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
    
    def info(self, message):
        """Log an info message"""
        self.logger.info(message)
    
    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log a critical message"""
        self.logger.critical(message)
    
    def log_colony_stats(self, colony):
        """
        Log colony statistics
        
        Args:
            colony: The ant colony
        """
        stats = colony.get_colony_stats()
        
        self.info(
            f"Colony Stats: Gen={stats['generation']}, "
            f"Pop={stats['population']}, "
            f"Food={stats['food_delivered']}, "
            f"Efficiency={(stats['food_delivered'] / max(1, stats['total_steps'])):.5f}"
        )
    
    def log_evolution(self, generation, max_fitness, avg_fitness, population_size):
        """
        Log evolution information
        
        Args:
            generation: Current generation
            max_fitness: Maximum fitness
            avg_fitness: Average fitness
            population_size: Population size
        """
        self.info(
            f"Evolution: Gen={generation}, "
            f"MaxFit={max_fitness:.2f}, "
            f"AvgFit={avg_fitness:.2f}, "
            f"Pop={population_size}"
        )