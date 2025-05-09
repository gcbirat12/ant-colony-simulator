# README.md
# AI Ant Colony Simulator

![Ant Colony Simulator](https://via.placeholder.com/800x400?text=AI+Ant+Colony+Simulator)

## Description

The AI Ant Colony Simulator is a sophisticated simulation environment where each ant is powered by a machine learning agent. These ants evolve strategies for food gathering, nest building, and pheromone communication through evolutionary algorithms and emergent swarm behavior.

Unlike traditional ant colony simulations, the behavior rules in this simulator are not hardcoded. Instead, each ant learns and adapts its behavior through neural networks that evolve over time, mimicking the natural processes that lead to the emergence of complex behaviors in biological systems.

## Features

- **ML-Powered Ants**: Each ant is controlled by a neural network that evolves over time
- **Evolutionary Algorithms**: Natural selection drives the optimization of ant behavior
- **Pheromone Communication**: Ants can deposit and sense pheromones to communicate
- **Emergent Behavior**: Watch complex colony behaviors emerge without explicit programming
- **Real-time Visualization**: Modern UI with a zoomable, pannable colony view
- **Interactive Environment**: Add food sources and new ants with mouse clicks
- **Statistics Tracking**: Monitor population, food collection, efficiency, and more
- **Save & Load Models**: Save evolved models and continue training later

## Requirements

- Python 3.7+
- Pygame
- NumPy
- Matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ant-colony-simulator.git
cd ant-colony-simulator
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulator with default settings:
```bash
python main.py
```

### Command-line Options:

- `--ants <number>`: Set the initial ant population (default: 100)
- `--food <number>`: Set the initial food amount (default: 200)
- `--headless`: Run without UI for faster training
- `--load-model <file>`: Load a saved model file

### Controls:

- **Space**: Pause/Resume simulation
- **E**: Force evolution to the next generation
- **S**: Save the current model
- **P**: Toggle pheromone visibility
- **+/-**: Adjust simulation speed
- **Mouse Wheel**: Zoom in/out
- **Middle Mouse Button**: Pan the view
- **Left Click**: Add food at the clicked location
- **Right Click**: Add a new ant at the clicked location

## How It Works

### Ant Intelligence

Each ant is controlled by a neural network that accepts sensory inputs from the environment and outputs action decisions:

- **Inputs**: Distance and direction to nest, food detection, pheromone concentrations, and ant status
- **Outputs**: Turn amount, speed, pheromone emission, and food pickup/drop decisions

### Evolution

The evolution process mimics natural selection:

1. Ants perform their behaviors for a generation length
2. Fitness is calculated based on food collection efficiency
3. The best-performing ants are selected for reproduction
4. Offspring are created through crossover and mutation
5. The next generation continues with the new population

### Pheromone System

Ants can communicate through two types of pheromones:

- **Food Pheromone**: Informs other ants about food sources
- **Home Pheromone**: Helps ants find their way back to the nest

Pheromones gradually evaporate and diffuse over time, creating dynamic trails that adapt to changing conditions.

## Project Structure

The simulator is organized into modular components:

```
ant_colony_simulator/
├── main.py               # Entry point
├── config.py             # Configuration settings
├── core/                 # Core simulation components
│   ├── ant.py            # Ant behavior and logic
│   ├── colony.py         # Colony management
│   ├── environment.py    # World environment
│   ├── food.py           # Food resources
│   ├── pheromone.py      # Pheromone system
│   └── nest.py           # Nest implementation
├── ml/                   # Machine learning components
│   ├── agent.py          # ML agent implementation
│   ├── evolution.py      # Evolutionary algorithm
│   └── neural_network.py # Neural network implementation
├── ui/                   # User interface components
│   ├── app.py            # Main application window
│   ├── colony_view.py    # Colony visualization
│   ├── control_panel.py  # User controls
│   └── stats_panel.py    # Statistics display
└── utils/                # Utility functions
    ├── vector.py         # Vector mathematics
    ├── visualization.py  # Visualization helpers
    └── logger.py         # Logging utilities
```

## Extending the Project

The simulator is designed to be easily extensible:

- **Add new sensors**: Enhance ant awareness by adding new inputs in `ant.py`
- **Modify neural networks**: Change the architecture in `neural_network.py`
- **Customize evolution**: Adjust selection and reproduction in `evolution.py`
- **Add environmental features**: Implement obstacles or weather in `environment.py`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- This project was inspired by the study of swarm intelligence and emergent behavior in biological systems
- Thanks to the open-source community for libraries that made this project possible