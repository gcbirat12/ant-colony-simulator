#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2D Vector class for the AI Ant Colony Simulator
"""

import numpy as np


class Vector2D:
    """
    2D vector implementation for positions, velocities, and directions
    """
    
    def __init__(self, x=0.0, y=0.0):
        """
        Initialize a 2D vector
        
        Args:
            x: X component
            y: Y component
        """
        self.x = float(x)
        self.y = float(y)
    
    def __add__(self, other):
        """Vector addition"""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    @staticmethod
    def random_unit_vector():
        """
        Create a random unit vector (normalized)
        
        Returns:
            Random unit vector
        """
        angle = np.random.uniform(0, 2 * np.pi)
        return Vector2D(np.cos(angle), np.sin(angle))
    
    def __sub__(self, other):
        """Vector subtraction"""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        """Scalar multiplication"""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        """Scalar division"""
        if scalar == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __repr__(self):
        """String representation"""
        return f"Vector2D({self.x:.2f}, {self.y:.2f})"
    
    def magnitude(self):
        """Calculate the magnitude (length) of the vector"""
        return np.sqrt(self.x * self.x + self.y * self.y)
    
    def magnitude_squared(self):
        """Calculate the squared magnitude (faster for comparisons)"""
        return self.x * self.x + self.y * self.y
    
    def normalized(self):
        """Return a normalized (unit) vector in the same direction"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def dot(self, other):
        """Calculate the dot product with another vector"""
        return self.x * other.x + self.y * other.y
    
    def distance_to(self, other):
        """Calculate the distance to another vector"""
        return (other - self).magnitude()
    
    def angle(self):
        """Calculate the angle of this vector in radians"""
        return np.arctan2(self.y, self.x)
    
    def rotate(self, angle):
        """
        Rotate the vector by the given angle in radians
        
        Args:
            angle: Angle in radians
            
        Returns:
            New rotated vector
        """
        cos_theta = np.cos(angle)
        sin_theta = np.sin(angle)
        
        new_x = self.x * cos_theta - self.y * sin_theta
        new_y = self.x * sin_theta + self.y * cos_theta
        
        return Vector2D(new_x, new_y)
    
    def perp(self):
        """
        Return a perpendicular vector (rotated 90 degrees counterclockwise)
        
        Returns:
            Perpendicular vector
        """
        return Vector2D(-self.y, self.x)
    
    @staticmethod
    def random(max_x, max_y):
        """
        Create a random vector within the given bounds
        
        Args:
            max_x: Maximum x value
            max_y: Maximum y value
            
        Returns:
            Random vector
        """
        return Vector2D