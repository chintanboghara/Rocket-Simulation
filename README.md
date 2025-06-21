# 🚀 Interactive Rocket Simulation Platform

A comprehensive web-based orbital mechanics simulator with advanced mission planning, real-time tracking, and educational features.

## Features

### Web Interface
- **Interactive Controls**: Real-time parameter adjustment
- **3D Visualization**: Plotly.js powered trajectory plots
- **Mission Planning**: Fuel calculations and launch windows
- **Live Tracking**: Real-time mission progress monitoring

### Educational System
- **Interactive Tutorials**: Learn orbital mechanics step-by-step
- **Knowledge Quizzes**: Test understanding with instant feedback
- **Performance Analytics**: Track learning progress and efficiency

### Advanced Features
- **Gravity Assist Calculator**: Multi-planet flyby optimization
- **Spacecraft Designer**: Custom mission configurations
- **Historical Missions**: Compare with real NASA missions
- **Launch Window Optimizer**: Optimal timing calculations

## Quick Start

### Web Interface (Recommended)
```bash
python start.py
# Open browser to: http://localhost:5000
```

### Docker
```bash
# Web interface
docker-compose up web

# CLI mode
docker-compose --profile cli up cli
```

### Manual Setup
```bash
pip install flask numpy
python app.py
```

## Mission Data

| Planet  | Distance | Transfer Time | Delta-V | Difficulty |
|---------|----------|---------------|---------|------------|
| Venus   | 0.72 AU  | ~146 days     | ~5.5 km/s | Easy      |
| Mars    | 1.52 AU  | ~259 days     | ~6.3 km/s | Medium    |
| Jupiter | 5.20 AU  | ~997 days     | ~8.8 km/s | Hard      |

## Usage Examples

### Web Interface
1. **Launch Mission**: Select target and run simulation
2. **Design Spacecraft**: Choose components and calculate performance
3. **Learn Orbital Mechanics**: Take interactive tutorials
4. **Track Performance**: View analytics and recommendations
5. **Optimize Routes**: Compare gravity assist trajectories

### CLI Mode
```bash
# Basic simulation
python main.py --target mars

# Advanced options
python main.py --target jupiter --steps 500 --speed 30
```

## Technical Details

### Requirements
- Python 3.9+
- Flask, NumPy
- Modern web browser
- 2GB+ RAM

### Architecture
- **Backend**: Flask REST API
- **Frontend**: Interactive HTML/JavaScript
- **Visualization**: Plotly.js
- **Physics**: NumPy calculations
- **Storage**: JSON data export

## 🐳 Docker Usage

```bash
# Web interface on port 5000
docker-compose up web

# CLI simulation
docker-compose --profile cli up cli

# Custom parameters
docker run -v $(pwd)/results:/app/results rocket-sim python main.py --target venus
```

## Performance

- **Web Response**: <100ms for calculations
- **Simulation Time**: 1-5 seconds
- **Memory Usage**: ~200MB base, ~500MB during animation
- **Browser Support**: Chrome, Firefox, Safari, Edge

## Development

```bash
git clone <repository>
cd Rocket-Simulation
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python start.py
```

## Educational Content

- **Basics**: Orbits, Hohmann transfers, Delta-V
- **Advanced**: Gravity assists, Launch windows
- **Missions**: Historical NASA missions analysis
- **Quizzes**: Interactive knowledge testing

## Interactive Features

- Real-time trajectory visualization
- Mission progress tracking
- Performance analytics dashboard
- Spacecraft component selection
- Multi-planet route optimization
- Educational tutorial system

## Physics Accuracy

- Kepler's laws implementation
- Hohmann transfer calculations
- Gravity assist physics
- Real planetary data
- Historical mission validation