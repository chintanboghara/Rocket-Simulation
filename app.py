from flask import Flask, render_template, request, jsonify
import numpy as np
import os
import time
from config import HOST, PORT, DEBUG, MAX_STEPS, MIN_STEPS, PLANETS
try:
    from fuel_calculator import FuelCalculator
    from launch_optimizer import LaunchOptimizer
    from gravity_assist import GravityAssist
    from mission_database import MissionDatabase
    from mission_tracker import MissionTracker
    from spacecraft_designer import SpacecraftDesigner
    from tutorial_system import TutorialSystem
    from analytics import PerformanceAnalytics
except ImportError as e:
    print(f"Warning: {e}. Some features may not work.")
    FuelCalculator = None
    LaunchOptimizer = None
    GravityAssist = None
    MissionDatabase = None
    MissionTracker = None
    SpacecraftDesigner = None
    TutorialSystem = None
    PerformanceAnalytics = None

app = Flask(__name__)

class RocketSimulator:
    def __init__(self):
        self.planets = {k: v['distance'] for k, v in PLANETS.items()}
        self.fuel_calc = FuelCalculator() if FuelCalculator else None
        self.launch_opt = LaunchOptimizer() if LaunchOptimizer else None
        self.gravity_assist = GravityAssist() if GravityAssist else None
        self.mission_db = MissionDatabase() if MissionDatabase else None
        self.tracker = MissionTracker() if MissionTracker else None
        self.designer = SpacecraftDesigner() if SpacecraftDesigner else None
        self.tutorial = TutorialSystem() if TutorialSystem else None
        self.analytics = PerformanceAnalytics() if PerformanceAnalytics else None
        
    def calculate_mission(self, target, steps=200):
        a_earth = 1.0
        a_target = self.planets[target]
        omega_earth, omega_target = 2*np.pi, 2*np.pi/a_target**1.5
        a_transfer = (a_earth + a_target) / 2
        e = abs(a_target - a_earth) / (a_earth + a_target)
        t_transfer = a_transfer**1.5 / 2
        
        t = np.linspace(0, t_transfer, steps)
        theta_target0 = np.pi - omega_target * t_transfer
        
        # Earth positions
        theta_earth = omega_earth * t
        x_earth = a_earth * np.cos(theta_earth)
        y_earth = a_earth * np.sin(theta_earth)
        
        # Target positions
        theta_target = theta_target0 + omega_target * t
        x_target = a_target * np.cos(theta_target)
        y_target = a_target * np.sin(theta_target)
        
        # Rocket trajectory
        theta_rocket = np.pi * t / t_transfer
        r_rocket = a_transfer * (1 - e**2) / (1 + e * np.cos(theta_rocket))
        x_rocket = r_rocket * np.cos(theta_rocket)
        y_rocket = r_rocket * np.sin(theta_rocket)
        
        # Calculate fuel requirements if available
        fuel_data = self.fuel_calc.mission_fuel(a_target) if self.fuel_calc else {
            'departure_dv': 0, 'arrival_dv': 0, 'total_dv': 0,
            'fuel_mass': 0, 'total_mass': 1000, 'fuel_ratio': 0
        }
        
        # Compare with historical missions
        historical_comparison = self.mission_db.compare_with_simulation(target, t_transfer * 365.25) if self.mission_db else None
        
        return {
            'earth': list(zip(x_earth.tolist(), y_earth.tolist())),
            'target': list(zip(x_target.tolist(), y_target.tolist())),
            'rocket': list(zip(x_rocket.tolist(), y_rocket.tolist())),
            'transfer_time': t_transfer * 365.25,
            'max_distance': float(np.max(np.sqrt(x_rocket**2 + y_rocket**2))),
            'fuel': fuel_data,
            'historical': historical_comparison
        }

simulator = RocketSimulator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json or {}
        target = data.get('target', 'mars')
        steps = min(max(int(data.get('steps', 200)), MIN_STEPS), MAX_STEPS)  # Limit range
        
        if target not in simulator.planets:
            return jsonify({'error': 'Invalid target planet'}), 400
            
        result = simulator.calculate_mission(target, steps)
        
        # Log simulation for analytics
        if simulator.analytics:
            simulator.analytics.log_simulation(target, result, {'steps': steps})
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/launch-windows/<target>')
def launch_windows(target):
    try:
        if target not in simulator.planets:
            return jsonify({'error': 'Invalid target planet'}), 400
            
        if not simulator.launch_opt:
            return jsonify({'error': 'Launch optimizer not available'}), 503
            
        windows = simulator.launch_opt.next_launch_windows(target)
        return jsonify(windows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/gravity-assist/<target>')
def gravity_assist_routes(target):
    try:
        if target not in simulator.planets:
            return jsonify({'error': 'Invalid target planet'}), 400
            
        if not simulator.gravity_assist:
            return jsonify({'error': 'Gravity assist calculator not available'}), 503
            
        routes = simulator.gravity_assist.suggest_routes(target)
        return jsonify(routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start-tracking', methods=['POST'])
def start_tracking():
    try:
        data = request.json or {}
        mission_id = data.get('mission_id', f"mission_{int(time.time())}")
        target = data.get('target', 'mars')
        
        if not simulator.tracker:
            return jsonify({'error': 'Mission tracker not available'}), 503
            
        # Get trajectory data
        trajectory = simulator.calculate_mission(target, 100)
        simulator.tracker.start_mission(mission_id, target, trajectory)
        
        return jsonify({'mission_id': mission_id, 'status': 'started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/mission-status/<mission_id>')
def mission_status(mission_id):
    try:
        if not simulator.tracker:
            return jsonify({'error': 'Mission tracker not available'}), 503
            
        status = simulator.tracker.get_mission_progress(mission_id)
        if not status:
            return jsonify({'error': 'Mission not found'}), 404
            
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/active-missions')
def active_missions():
    try:
        if not simulator.tracker:
            return jsonify({'error': 'Mission tracker not available'}), 503
            
        missions = simulator.tracker.get_all_missions()
        return jsonify(missions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/design-spacecraft', methods=['POST'])
def design_spacecraft():
    try:
        if not simulator.designer:
            return jsonify({'error': 'Spacecraft designer not available'}), 503
            
        config = request.json or {}
        design = simulator.designer.design_spacecraft(config)
        return jsonify(design)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/spacecraft-presets')
def spacecraft_presets():
    try:
        if not simulator.designer:
            return jsonify({'error': 'Spacecraft designer not available'}), 503
            
        presets = simulator.designer.get_presets()
        return jsonify(presets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tutorials')
def get_tutorials():
    try:
        if not simulator.tutorial:
            return jsonify({'error': 'Tutorial system not available'}), 503
        tutorials = simulator.tutorial.get_all_tutorials()
        return jsonify(tutorials)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tutorial/<tutorial_id>/<int:step>')
def get_tutorial_step(tutorial_id, step):
    try:
        if not simulator.tutorial:
            return jsonify({'error': 'Tutorial system not available'}), 503
        step_data = simulator.tutorial.get_step(tutorial_id, step)
        if not step_data:
            return jsonify({'error': 'Tutorial step not found'}), 404
        return jsonify(step_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quiz/<tutorial_id>')
def get_quiz(tutorial_id):
    try:
        if not simulator.tutorial:
            return jsonify({'error': 'Tutorial system not available'}), 503
        quiz = simulator.tutorial.generate_quiz(tutorial_id)
        return jsonify(quiz)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics')
def get_analytics():
    try:
        if not simulator.analytics:
            return jsonify({'error': 'Analytics not available'}), 503
        data = simulator.analytics.export_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    print("🚀 Starting Rocket Simulation Server...")
    print("📡 Open your browser to: http://localhost:5000")
    try:
        app.run(debug=DEBUG, host=HOST, port=PORT)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        input("Press Enter to exit...")