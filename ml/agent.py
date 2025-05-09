#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ML Agent implementation for the AI Ant Colony Simulator
"""

import numpy as np
from ml.neural_network import NeuralNetwork
import config


class MLAgent:
    """
    Machine Learning agent that controls an ant's behavior
    """
    
    def __init__(self, network=None):
        """
        Initialize a new ML agent
        
        Args:
            network: Optional pre-trained neural network
        """
        # Input size: sensory inputs from the ant
        # IMPORTANT: Must match the actual input vector length in ant.py
        input_size = 15  # Updated to match what ant.py is providing
        
        # Output size: [turn_amount, speed, drop_pheromone, pickup_food]
        output_size = 4
        
        # Create or use a neural network
        if network is None:
            self.network = NeuralNetwork(
                input_size=input_size,
                hidden_sizes=config.NEURAL_NETWORK_LAYERS,
                output_size=output_size
            )
        else:
            self.network = network
            
        # Initialize learning parameters
        self.learning_rate = 0.01
        self.discount_factor = 0.95
        self.last_state = None
        self.last_action = None
        
    def process(self, inputs):
        """
        Process sensory inputs and decide on actions
        
        Args:
            inputs: Numpy array of sensory inputs
            
        Returns:
            Numpy array of action outputs
        """
        # Store for learning
        self.last_state = inputs
        
        # Make sure input dimensions match what the network expects
        if len(inputs) != self.network.input_size:
            # Adjust the input size by either padding or truncating
            if len(inputs) < self.network.input_size:
                # Pad with zeros
                pad_size = self.network.input_size - len(inputs)
                inputs = np.pad(inputs, (0, pad_size), 'constant')
            else:
                # Truncate
                inputs = inputs[:self.network.input_size]
                
        # Forward pass through the neural network
        outputs = self.network.forward(inputs)
        
        # Apply activation function to keep outputs in appropriate ranges
        processed_outputs = self._activate_outputs(outputs)
        
        # Store for learning
        self.last_action = processed_outputs
        
        return processed_outputs
    
    def _activate_outputs(self, outputs):
        """Apply appropriate activation functions to outputs"""
        # Use sigmoid activation for all outputs to keep them in [0,1]
        return 1.0 / (1.0 + np.exp(-outputs))
    
    def learn_from_experience(self, experiences):
        """
        Learn from a batch of experience tuples
        
        Args:
            experiences: List of (state, action, reward) tuples
        """
        if not experiences:
            return
            
        # Simple reward-based learning
        for state, action, reward in experiences:
            # Adjust weights based on reward signal
            target = action.copy() 
            
            # If reward is positive, reinforce the action
            # If reward is negative, discourage the action
            if reward > 0:
                # For positive reward, move towards the action
                pass  # No change needed as we're reinforcing
            else:
                # For negative reward, move away from the action
                target = 1 - target
                
            # Scale the learning by the magnitude of the reward
            scale = min(abs(reward), 1.0) * self.learning_rate
            
            # Update weights through backpropagation
            self.network.backprop(state, target, scale)
    
    def mutate(self, mutation_rate=config.MUTATION_RATE):
        """
        Randomly mutate the neural network weights
        
        Args:
            mutation_rate: Probability of each weight being mutated
        """
        self.network.mutate(mutation_rate)
    
    def crossover(self, other_agent, crossover_rate=config.CROSSOVER_RATE):
        """
        Create a new agent by crossing over with another agent
        
        Args:
            other_agent: The other agent to crossover with
            crossover_rate: Rate of gene crossover
            
        Returns:
            A new agent with a mixed neural network
        """
        # Create a new network by crossing over weights
        new_network = self.network.crossover(
            other_agent.network, 
            crossover_rate
        )
        
        # Return a new agent with the crossed-over network
        return MLAgent(network=new_network)
    
    def get_weights(self):
        """Get neural network weights for serialization"""
        return self.network.get_weights()
    
    def set_weights(self, weights):
        """Set neural network weights from serialization"""
        self.network.set_weights(weights)