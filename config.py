"""Configuration settings for Rocket Simulation"""

# Server settings
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

# Simulation limits
MAX_STEPS = 1000
MIN_STEPS = 50
DEFAULT_STEPS = 200

# Mission tracking settings
TRACKING_UPDATE_INTERVAL = 1000  # milliseconds
TIME_SCALE = 10  # 1 second = 10 days

# Spacecraft design limits
MAX_MASS = 50000  # kg
MAX_COST = 100000000  # $100M

# Planet data
PLANETS = {
    'venus': {'distance': 0.723, 'name': 'Venus'},
    'mars': {'distance': 1.524, 'name': 'Mars'},
    'jupiter': {'distance': 5.204, 'name': 'Jupiter'}
}

# Feature flags
FEATURES = {
    'fuel_calculator': True,
    'launch_optimizer': True,
    'gravity_assist': True,
    'mission_database': True,
    'mission_tracker': True,
    'spacecraft_designer': True
}