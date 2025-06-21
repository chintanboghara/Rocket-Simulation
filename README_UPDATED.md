# 🚀 Interactive Rocket Simulation Platform

A modern web-based orbital mechanics simulator with real-time trajectory visualization, fuel calculations, and launch window optimization.

## ✨ New Features

### 🌐 Web Interface
- **Interactive Controls**: Real-time parameter adjustment
- **3D Visualization**: Plotly.js powered trajectory plots
- **Responsive Design**: Works on desktop and mobile
- **Dark Space Theme**: Professional space mission aesthetic

### ⛽ Mission Planning
- **Fuel Calculations**: Realistic delta-v and mass requirements
- **Launch Windows**: Optimal timing based on planetary alignment
- **Mission Metrics**: Comprehensive performance analysis
- **Efficiency Analysis**: Fuel penalties for sub-optimal launches

## 🚀 Quick Start

### Option 1: Auto-Setup (Recommended)
```bash
python start.py
```

### Option 2: Manual Setup
```bash
pip install flask numpy
python app.py
```

### Option 3: Original CLI
```bash
python main.py --target mars
```

## 🌐 Web Interface Usage

1. **Start Server**: Run `python start.py`
2. **Open Browser**: Go to `http://localhost:5000`
3. **Select Target**: Choose Venus, Mars, or Jupiter
4. **Adjust Quality**: Use slider for animation smoothness
5. **Launch Mission**: Click to calculate trajectory
6. **View Windows**: Check optimal launch dates

## 📊 Mission Data

| Planet  | Distance | Transfer Time | Delta-V | Difficulty |
|---------|----------|---------------|---------|------------|
| Venus   | 0.72 AU  | ~146 days     | ~5.5 km/s | Easy      |
| Mars    | 1.52 AU  | ~259 days     | ~6.3 km/s | Medium    |
| Jupiter | 5.20 AU  | ~997 days     | ~8.8 km/s | Hard      |

## 🔧 Technical Features

- **Error Handling**: Graceful failure recovery
- **Input Validation**: Safe parameter ranges
- **Performance**: Optimized calculations
- **Cross-Platform**: Windows, macOS, Linux support
- **Modular Design**: Extensible architecture

## 🐛 Troubleshooting

### Common Issues
- **Import Errors**: Run `python start.py` for auto-install
- **Port Conflicts**: Server uses port 5000
- **Browser Issues**: Try Chrome/Firefox for best experience

### Performance Tips
- Lower animation steps (50-100) for faster rendering
- Close other browser tabs for better performance
- Use latest browser version for WebGL support

## 🔮 Upcoming Features

- Multi-gravity assist trajectories
- Historical mission database
- Spacecraft design module
- Real-time mission tracking
- Educational tutorials

## 📁 Project Structure

```
Rocket-Simulation/
├── app.py              # Web application
├── start.py            # Auto-setup launcher
├── main.py             # Original CLI version
├── fuel_calculator.py  # Mission planning
├── launch_optimizer.py # Window calculations
├── templates/          # Web interface
└── requirements.txt    # Dependencies
```