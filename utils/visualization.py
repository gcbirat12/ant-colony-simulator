# visualization.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Visualization utilities for the AI Ant Colony Simulator
"""

import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
import config


def get_color_gradient(color1, color2, steps):
    """
    Generate a gradient between two colors
    
    Args:
        color1: First color (r, g, b)
        color2: Second color (r, g, b)
        steps: Number of gradient steps
        
    Returns:
        List of gradient colors
    """
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    r_step = (r2 - r1) / steps
    g_step = (g2 - g1) / steps
    b_step = (b2 - b1) / steps
    
    gradient = []
    for i in range(steps):
        r = int(r1 + r_step * i)
        g = int(g1 + g_step * i)
        b = int(b1 + b_step * i)
        gradient.append((r, g, b))
    
    return gradient


def create_heatmap_surface(width, height, data, colormap='viridis'):
    """
    Create a surface with a heatmap visualization
    
    Args:
        width: Surface width
        height: Surface height
        data: 2D numpy array of data values
        colormap: Matplotlib colormap name
        
    Returns:
        Pygame surface with the heatmap
    """
    # Create a figure with the exact size we need
    dpi = 100
    fig_width = width / dpi
    fig_height = height / dpi
    
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    ax = fig.add_subplot(111)
    
    # Create the heatmap
    im = ax.imshow(data, cmap=colormap)
    
    # Remove axes and margins
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    
    # Render to a numpy array
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = io.BytesIO()
    plt.savefig(buf, format='raw', dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    img_arr = img_arr.reshape((height, width, -1))
    
    # Close the figure to avoid memory leaks
    plt.close(fig)
    
    # Convert to a pygame surface
    surface = pygame.Surface((width, height))
    pygame.surfarray.blit_array(surface, img_arr[:, :, :3])
    
    return surface


def create_plot_surface(width, height, x_data, y_data, title='', xlabel='', ylabel=''):
    """
    Create a surface with a line plot visualization
    
    Args:
        width: Surface width
        height: Surface height
        x_data: X-axis data
        y_data: Y-axis data
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        
    Returns:
        Pygame surface with the plot
    """
    # Create a figure with the exact size we need
    dpi = 100
    fig_width = width / dpi
    fig_height = height / dpi
    
    fig = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
    ax = fig.add_subplot(111)
    
    # Create the plot
    ax.plot(x_data, y_data, color='#66c2a5', linewidth=2)
    
    # Set labels and title
    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    
    # Adjust style for better visibility
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Set background color
    fig.patch.set_facecolor('#2a2a3a')
    ax.set_facecolor('#3a3a4a')
    
    # Set text colors
    title_color = '#ffffff'
    ax.title.set_color(title_color)
    ax.xaxis.label.set_color(title_color)
    ax.yaxis.label.set_color(title_color)
    
    # Set tick colors
    ax.tick_params(axis='x', colors=title_color)
    ax.tick_params(axis='y', colors=title_color)
    
    # Set spine colors
    for spine in ax.spines.values():
        spine.set_color('#555555')
    
    # Add some padding
    plt.tight_layout(pad=0.5)
    
    # Render to a numpy array
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    buf = io.BytesIO()
    plt.savefig(buf, format='raw', dpi=dpi)
    buf.seek(0)
    img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
    img_arr = img_arr.reshape((height, width, -1))
    
    # Close the figure to avoid memory leaks
    plt.close(fig)
    
    # Convert to a pygame surface
    surface = pygame.Surface((width, height))
    pygame.surfarray.blit_array(surface, img_arr[:, :, :3])
    
    return surface


def render_text_multiline(text, font, color, max_width, line_spacing=2):
    """
    Render multi-line text to a surface
    
    Args:
        text: Text to render
        font: Pygame font
        color: Text color
        max_width: Maximum width
        line_spacing: Space between lines
        
    Returns:
        Surface with the rendered text
    """
    # Split the text into words
    words = text.split(' ')
    lines = []
    current_line = []
    
    # Group words into lines that fit the max width
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_width, _ = font.size(test_line)
        
        if test_width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    # Render each line
    line_surfaces = []
    max_line_width = 0
    total_height = 0
    
    for line in lines:
        line_surface = font.render(line, True, color)
        line_surfaces.append(line_surface)
        max_line_width = max(max_line_width, line_surface.get_width())
        total_height += line_surface.get_height() + line_spacing
    
    # Create a surface to hold all the lines
    result_surface = pygame.Surface((max_line_width, total_height), pygame.SRCALPHA)
    
    # Blit each line onto the result surface
    y_offset = 0
    for line_surface in line_surfaces:
        result_surface.blit(line_surface, (0, y_offset))
        y_offset += line_surface.get_height() + line_spacing
    
    return result_surface