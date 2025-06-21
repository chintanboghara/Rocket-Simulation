import numpy as np
from datetime import datetime, timedelta

class LaunchOptimizer:
    def __init__(self):
        self.planets = {
            'venus': {'period': 224.7, 'distance': 0.723},
            'mars': {'period': 687.0, 'distance': 1.524}, 
            'jupiter': {'period': 4333.0, 'distance': 5.204}
        }
        
    def synodic_period(self, target):
        """Calculate synodic period between Earth and target planet"""
        earth_period = 365.25
        target_period = self.planets[target]['period']
        
        if target_period > earth_period:
            synodic = 1 / (1/earth_period - 1/target_period)
        else:
            synodic = 1 / (1/target_period - 1/earth_period)
            
        return abs(synodic)
    
    def next_launch_windows(self, target, num_windows=3):
        """Calculate next optimal launch windows"""
        synodic = self.synodic_period(target)
        base_date = datetime.now()
        
        windows = []
        for i in range(num_windows):
            launch_date = base_date + timedelta(days=i * synodic)
            
            # Calculate transfer time
            a_earth = 1.0
            a_target = self.planets[target]['distance']
            a_transfer = (a_earth + a_target) / 2
            transfer_time = a_transfer**1.5 / 2 * 365.25
            
            arrival_date = launch_date + timedelta(days=transfer_time)
            
            windows.append({
                'launch_date': launch_date.strftime('%Y-%m-%d'),
                'arrival_date': arrival_date.strftime('%Y-%m-%d'),
                'transfer_days': int(transfer_time),
                'window_number': i + 1
            })
            
        return windows
    
    def launch_efficiency(self, target, days_from_optimal=0):
        """Calculate launch efficiency based on timing"""
        # Efficiency decreases as we move away from optimal window
        max_deviation = 30  # days
        efficiency = max(0, 1 - abs(days_from_optimal) / max_deviation)
        
        # Convert to fuel penalty
        fuel_penalty = (1 - efficiency) * 0.2  # Up to 20% fuel penalty
        
        return {
            'efficiency': efficiency * 100,
            'fuel_penalty': fuel_penalty * 100,
            'recommended': efficiency > 0.8
        }