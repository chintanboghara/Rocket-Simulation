import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os
import matplotlib
import argparse
import json
matplotlib.use('Agg')  # Use non-interactive backend for Docker

# Parse arguments
parser = argparse.ArgumentParser(description='Rocket Simulation')
parser.add_argument('--target', choices=['venus', 'mars', 'jupiter'], default='mars')
parser.add_argument('--speed', type=int, default=50, help='Animation speed (ms)')
parser.add_argument('--steps', type=int, default=200, help='Animation steps')
parser.add_argument('--format', choices=['mp4'], default='mp4')
args = parser.parse_args()

# Planet data
planets = {'venus': 0.723, 'mars': 1.524, 'jupiter': 5.204}
a_earth = 1.0
a_target = planets[args.target]
omega_earth, omega_target = 2*np.pi, 2*np.pi/a_target**1.5
a_transfer = (a_earth + a_target) / 2
e = abs(a_target - a_earth) / (a_earth + a_target)
t_transfer = a_transfer**1.5 / 2

# Calculate positions
num_steps = args.steps
t = np.linspace(0, t_transfer, num_steps)
theta_target0 = np.pi - omega_target * t_transfer

theta_earth = omega_earth * t
x_earth, y_earth = a_earth * np.cos(theta_earth), a_earth * np.sin(theta_earth)

theta_target = theta_target0 + omega_target * t
x_target, y_target = a_target * np.cos(theta_target), a_target * np.sin(theta_target)

theta_rocket = np.pi * t / t_transfer
r_rocket = a_transfer * (1 - e**2) / (1 + e * np.cos(theta_rocket))
x_rocket, y_rocket = r_rocket * np.cos(theta_rocket), r_rocket * np.sin(theta_rocket)

# Setup plot
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})

# Plot orbits and trajectory
theta = np.linspace(0, 2*np.pi, 100)
ax.plot(a_earth*np.cos(theta), a_earth*np.sin(theta), 0, 'b--', label='Earth Orbit')
colors = {'venus': 'orange', 'mars': 'r', 'jupiter': 'brown'}
color = colors[args.target]
ax.plot(a_target*np.cos(theta), a_target*np.sin(theta), 0, f'{color}--', label=f'{args.target.title()} Orbit')
ax.plot(x_rocket, y_rocket, 0, 'g-', label='Rocket Trajectory')
ax.scatter(0, 0, 0, color='yellow', s=100, label='Sun')

earth_dot, = ax.plot([], [], [], 'bo', markersize=8)
target_dot, = ax.plot([], [], [], f'{color}o', markersize=8)
rocket_dot, = ax.plot([], [], [], 'go', markersize=6)

def animate(i):
    earth_dot.set_data([x_earth[i]], [y_earth[i]])
    earth_dot.set_3d_properties([0])
    target_dot.set_data([x_target[i]], [y_target[i]])
    target_dot.set_3d_properties([0])
    rocket_dot.set_data([x_rocket[i]], [y_rocket[i]])
    rocket_dot.set_3d_properties([0])
    
    # Update title with progress
    progress = (i / num_steps) * 100
    ax.set_title(f'Rocket Journey - Progress: {progress:.1f}%')
    return earth_dot, target_dot, rocket_dot

# Create animation
anim = FuncAnimation(fig, animate, frames=num_steps, interval=args.speed, blit=False)

ax.set_xlabel('X (AU)')
ax.set_ylabel('Y (AU)')
ax.set_title(f'Rocket Journey from Earth to {args.target.title()}')
max_dist = max(a_earth, a_target) * 1.2
ax.set_xlim(-max_dist, max_dist)
ax.set_ylim(-max_dist, max_dist)
ax.set_zlim(-0.1, 0.1)
ax.legend()

# Calculate metrics
distance = np.sqrt(x_rocket**2 + y_rocket**2)
print(f"Mission Metrics:")
print(f"Transfer time: {t_transfer * 365.25:.0f} days")
print(f"Max distance: {np.max(distance):.2f} AU")

try:
    os.makedirs('results', exist_ok=True)
    filename = f'results/animation.{args.format}'
    writer = 'ffmpeg'
    anim.save(filename, writer=writer)
    
    # Export data
    data = {
        'mission': f'Earth to {args.target}',
        'positions': {
            'earth': [[float(x), float(y)] for x, y in zip(x_earth, y_earth)],
            'target': [[float(x), float(y)] for x, y in zip(x_target, y_target)],
            'rocket': [[float(x), float(y)] for x, y in zip(x_rocket, y_rocket)]
        }
    }
    with open('results/mission_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Animation saved to {filename}")
    print("Data exported to results/mission_data.json")
except Exception as e:
    print(f"Error: {e}")

# plt.show()  # Disabled for Docker     