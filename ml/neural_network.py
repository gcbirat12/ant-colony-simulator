# neural_network.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neural Network implementation for the AI Ant Colony Simulator
"""

import numpy as np
import pickle


class NeuralNetwork:
    """
    Simple neural network with feedforward and backpropagation
    """
    
    def __init__(self, input_size, hidden_sizes, output_size):
        """
        Initialize a neural network
        
        Args:
            input_size: Number of input neurons
            hidden_sizes: List of hidden layer sizes
            output_size: Number of output neurons
        """
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size
        
        # Create list of layer sizes including input and output
        layer_sizes = [input_size] + hidden_sizes + [output_size]
        
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        
        for i in range(len(layer_sizes) - 1):
            # Xavier/Glorot initialization for better convergence
            scale = np.sqrt(2.0 / (layer_sizes[i] + layer_sizes[i+1]))
            self.weights.append(np.random.normal(0, scale, (layer_sizes[i], layer_sizes[i+1])))
            self.biases.append(np.zeros(layer_sizes[i+1]))
            
        # For caching activations during forward pass (used in backprop)
        self.activations = []
    
    def forward(self, inputs):
        """
        Forward pass through the network
        
        Args:
            inputs: Input array
            
        Returns:
            Output array
        """
        # Convert inputs to numpy array
        x = np.array(inputs, dtype=float)
        
        # Reset activations
        self.activations = [x]
        
        # Forward pass through each layer
        for i in range(len(self.weights)):
            # Linear transformation: z = x * W + b
            z = np.dot(x, self.weights[i]) + self.biases[i]
            
            # Apply activation function
            if i < len(self.weights) - 1:
                # ReLU for hidden layers
                x = np.maximum(0, z)
            else:
                # Linear output for output layer
                x = z
                
            # Store activation for backpropagation
            self.activations.append(x)
            
        return x
    
    def backprop(self, inputs, targets, learning_rate):
        """
        Update weights using backpropagation
        
        Args:
            inputs: Input array
            targets: Target output array
            learning_rate: Learning rate
        """
        # Forward pass to ensure activations are up to date
        outputs = self.forward(inputs)
        
        # Initialize gradients
        deltas = [None] * len(self.weights)
        
        # Output layer error
        error = outputs - targets
        deltas[-1] = error
        
        # Backpropagate the error through the hidden layers
        for i in range(len(self.weights) - 2, -1, -1):
            # Compute error for hidden layer
            error = np.dot(deltas[i + 1], self.weights[i + 1].T)
            
            # Apply derivative of ReLU activation
            activation = self.activations[i + 1]
            error = error * (activation > 0).astype(float)
            
            deltas[i] = error
        
        # Update weights and biases
        for i in range(len(self.weights)):
            # Gradient for weights: input_activation * delta
            dW = np.outer(self.activations[i], deltas[i])
            
            # Gradient for biases: delta
            db = deltas[i]
            
            # Update weights and biases
            self.weights[i] -= learning_rate * dW
            self.biases[i] -= learning_rate * db
    
    def mutate(self, mutation_rate):
        """
        Randomly mutate weights and biases
        
        Args:
            mutation_rate: Probability of mutation for each parameter
        """
        for i in range(len(self.weights)):
            # Mutate weights
            mask = np.random.random(self.weights[i].shape) < mutation_rate
            mutations = np.random.normal(0, 0.1, self.weights[i].shape)
            self.weights[i] += mask * mutations
            
            # Mutate biases
            mask = np.random.random(self.biases[i].shape) < mutation_rate
            mutations = np.random.normal(0, 0.1, self.biases[i].shape)
            self.biases[i] += mask * mutations
    
    def crossover(self, other, crossover_rate):
        """
        Perform crossover with another neural network
        
        Args:
            other: The other neural network
            crossover_rate: Rate of gene crossover
            
        Returns:
            A new neural network with mixed weights
        """
        # Create a new network with the same architecture
        child = NeuralNetwork(self.input_size, self.hidden_sizes, self.output_size)
        
        # Crossover weights and biases
        for i in range(len(self.weights)):
            # Crossover mask (True: use self, False: use other)
            mask = np.random.random(self.weights[i].shape) < crossover_rate
            
            # Apply crossover to weights
            child.weights[i] = np.where(mask, self.weights[i], other.weights[i])
            
            # Crossover mask for biases
            mask = np.random.random(self.biases[i].shape) < crossover_rate
            
            # Apply crossover to biases
            child.biases[i] = np.where(mask, self.biases[i], other.biases[i])
            
        return child
    
    def get_weights(self):
        """
        Get weights and biases for serialization
        
        Returns:
            Dictionary with weights and biases
        """
        return {
            'weights': [w.tolist() for w in self.weights],
            'biases': [b.tolist() for b in self.biases]
        }
    
    def set_weights(self, weights_dict):
        """
        Set weights and biases from serialization
        
        Args:
            weights_dict: Dictionary with weights and biases
        """
        self.weights = [np.array(w) for w in weights_dict['weights']]
        self.biases = [np.array(b) for b in weights_dict['biases']]
    
    def save(self, filename):
        """
        Save the neural network to a file
        
        Args:
            filename: Path to save the file
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.get_weights(), f)
    
    @classmethod
    def load(cls, filename, input_size, hidden_sizes, output_size):
        """
        Load a neural network from a file
        
        Args:
            filename: Path to the file
            input_size: Number of input neurons
            hidden_sizes: List of hidden layer sizes
            output_size: Number of output neurons
            
        Returns:
            Loaded neural network
        """
        network = cls(input_size, hidden_sizes, output_size)
        
        with open(filename, 'rb') as f:
            weights_dict = pickle.load(f)
            
        network.set_weights(weights_dict)
        return network