import numpy as np

class GravityAssist:
    def __init__(self):
        self.planets = {
            'venus': {'distance': 0.723, 'mass': 4.87e24, 'radius': 6052},
            'earth': {'distance': 1.0, 'mass': 5.97e24, 'radius': 6371},
            'mars': {'distance': 1.524, 'mass': 6.42e23, 'radius': 3390},
            'jupiter': {'distance': 5.204, 'mass': 1.90e27, 'radius': 69911}
        }
        
    def flyby_velocity_change(self, planet, approach_velocity, flyby_altitude=1000):
        """Calculate velocity change from gravity assist"""
        planet_data = self.planets[planet]
        mu = 6.674e-11 * planet_data['mass']  # GM
        r_p = (planet_data['radius'] + flyby_altitude) * 1000  # m
        
        # Hyperbolic excess velocity
        v_inf = approach_velocity * 1000  # m/s
        
        # Deflection angle
        delta = 2 * np.arcsin(1 / (1 + r_p * v_inf**2 / mu))
        
        # Velocity change magnitude
        dv = 2 * v_inf * np.sin(delta / 2)
        
        return dv / 1000  # km/s
    
    def multi_flyby_trajectory(self, route):
        """Calculate multi-planet flyby trajectory"""
        total_dv = 0
        trajectory = []
        
        for i, planet in enumerate(route):
            if i == 0:  # Launch from Earth
                v_launch = np.sqrt(2 * 6.674e-11 * 1.327e20 / (1.496e11))  # Escape velocity
                total_dv += v_launch / 1000
                trajectory.append({
                    'planet': planet,
                    'action': 'launch',
                    'velocity': v_launch / 1000,
                    'cumulative_dv': total_dv
                })
            else:
                # Calculate flyby
                approach_v = 15 + i * 5  # Simplified approach velocity
                dv_gain = self.flyby_velocity_change(planet, approach_v)
                total_dv -= dv_gain  # Gravity assist reduces total dv needed
                
                trajectory.append({
                    'planet': planet,
                    'action': 'flyby',
                    'velocity_gain': dv_gain,
                    'cumulative_dv': total_dv
                })
        
        return {
            'route': route,
            'total_dv': max(0, total_dv),  # Ensure non-negative
            'trajectory': trajectory,
            'efficiency': min(100, max(0, 100 - total_dv * 3))  # Efficiency score
        }
    
    def suggest_routes(self, destination):
        """Suggest optimal flyby routes"""
        routes = {
            'jupiter': [
                ['earth', 'venus', 'jupiter'],
                ['earth', 'mars', 'jupiter'],
                ['earth', 'venus', 'mars', 'jupiter']
            ],
            'mars': [
                ['earth', 'venus', 'mars'],
                ['earth', 'mars']
            ],
            'venus': [
                ['earth', 'venus']
            ]
        }
        
        suggested = []
        for route in routes.get(destination, []):
            trajectory = self.multi_flyby_trajectory(route)
            suggested.append(trajectory)
        
        return sorted(suggested, key=lambda x: x['total_dv'])