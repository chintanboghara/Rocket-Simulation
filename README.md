# 🚀 Rocket Simulation: Interplanetary Missions

A Python-based orbital mechanics simulator that visualizes rocket trajectories from Earth to Venus, Mars, and Jupiter using Hohmann transfer orbits.

## Overview

This simulation implements real orbital dynamics to calculate and animate spacecraft trajectories between planets. It uses Kepler's laws and elliptical orbit mathematics to provide accurate transfer times and energy requirements.

### Key Physics
- **Hohmann Transfer Orbits**: Most energy-efficient path between circular orbits
- **Kepler's Laws**: Planetary motion and orbital periods
- **Astronomical Units (AU)**: Earth-Sun distance as reference (1 AU = 149.6M km)

## Requirements

- Python 3.9+
- FFmpeg (for video generation)
- 2GB+ RAM (for animation rendering)

## Installation

### Local Setup
```bash
git clone https://github.com/chintanboghara/Rocket-Simulation.git
cd Rocket-Simulation
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Docker Setup
```bash
docker-compose up
```

## Usage

### Basic Commands
```bash
# Mars mission (default)
python main.py

# Venus mission
python main.py --target venus

# Jupiter mission with custom settings
python main.py --target jupiter --speed 30 --steps 500
```

### Command Line Options
| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--target` | venus, mars, jupiter | mars | Destination planet |
| `--speed` | 10-200 | 50 | Animation speed (ms per frame) |
| `--steps` | 50-1000 | 200 | Animation quality (more = smoother) |
| `--format` | mp4 | mp4 | Output format |

## Mission Data

### Planetary Parameters
| Planet | Distance (AU) | Transfer Time | Difficulty |
|--------|---------------|---------------|------------|
| Venus | 0.723 | ~146 days | Easy |
| Mars | 1.524 | ~259 days | Medium |
| Jupiter | 5.204 | ~997 days | Hard |

### Output Files
- `results/animation.mp4` - 3D visualization
- `results/mission_data.json` - Trajectory coordinates

## Features

### Simulation Capabilities
- **Real Orbital Mechanics**: Accurate physics calculations
- **Multiple Targets**: Venus, Mars, Jupiter missions
- **Dynamic Scaling**: Auto-adjusts view based on target distance
- **Progress Tracking**: Real-time completion percentage

### Technical Features
- **Configurable Quality**: Adjust animation smoothness
- **Data Export**: JSON format for analysis
- **Docker Support**: Containerized execution
- **Cross-Platform**: Windows, macOS, Linux

## Science Behind the Simulation

### Transfer Orbit Calculations
```
Semi-major axis: a = (r₁ + r₂) / 2
Eccentricity: e = |r₂ - r₁| / (r₁ + r₂)
Transfer time: t = π√(a³/μ)
```

### Planetary Motion
- Earth orbital period: 1 year
- Angular velocities calculated from Kepler's 3rd law
- Launch windows determined by planetary alignment

## Docker Usage

### Quick Start
```bash
# Run simulation
docker-compose up

# Custom parameters
docker run -v $(pwd)/results:/app/results rocket-sim python main.py --target venus
```

### Build Custom Image
```bash
docker build -t rocket-sim .
docker run -v $(pwd)/results:/app/results rocket-sim
```

## Performance

- **Rendering Time**: 30-120 seconds (depends on steps)
- **Memory Usage**: ~500MB during animation
- **Output Size**: 2-10MB MP4 files

## Troubleshooting

### Common Issues
```bash
# FFmpeg not found
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS

# Memory errors with high steps
python main.py --steps 100  # Reduce quality

# Docker permission issues
sudo docker-compose up     # Linux
```