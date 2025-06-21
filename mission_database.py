from datetime import datetime

class MissionDatabase:
    def __init__(self):
        self.missions = {
            'voyager_1': {
                'name': 'Voyager 1',
                'launch_date': '1977-09-05',
                'target': 'jupiter',
                'route': ['earth', 'jupiter'],
                'status': 'active',
                'achievements': ['First Jupiter flyby', 'Interstellar space'],
                'duration_days': 16800,
                'distance_au': 159.0
            },
            'voyager_2': {
                'name': 'Voyager 2',
                'launch_date': '1977-08-20',
                'target': 'jupiter',
                'route': ['earth', 'jupiter', 'saturn', 'uranus', 'neptune'],
                'status': 'active',
                'achievements': ['Grand Tour', 'Only Uranus/Neptune visitor'],
                'duration_days': 16900,
                'distance_au': 132.0
            },
            'cassini': {
                'name': 'Cassini-Huygens',
                'launch_date': '1997-10-15',
                'target': 'saturn',
                'route': ['earth', 'venus', 'venus', 'earth', 'jupiter', 'saturn'],
                'status': 'completed',
                'achievements': ['Saturn orbit', 'Titan landing'],
                'duration_days': 7300,
                'distance_au': 9.5
            },
            'new_horizons': {
                'name': 'New Horizons',
                'launch_date': '2006-01-19',
                'target': 'pluto',
                'route': ['earth', 'jupiter', 'pluto'],
                'status': 'active',
                'achievements': ['First Pluto flyby', 'Kuiper Belt exploration'],
                'duration_days': 6500,
                'distance_au': 50.0
            },
            'mars_2020': {
                'name': 'Perseverance',
                'launch_date': '2020-07-30',
                'target': 'mars',
                'route': ['earth', 'mars'],
                'status': 'active',
                'achievements': ['Mars samples', 'Helicopter flight'],
                'duration_days': 1200,
                'distance_au': 1.5
            }
        }
    
    def get_missions_by_target(self, target):
        """Get all missions to a specific target"""
        return [mission for mission in self.missions.values() 
                if mission['target'] == target]
    
    def get_active_missions(self):
        """Get currently active missions"""
        return [mission for mission in self.missions.values() 
                if mission['status'] == 'active']
    
    def get_mission_stats(self):
        """Get database statistics"""
        total = len(self.missions)
        active = len(self.get_active_missions())
        completed = total - active
        
        targets = {}
        for mission in self.missions.values():
            target = mission['target']
            targets[target] = targets.get(target, 0) + 1
        
        return {
            'total_missions': total,
            'active_missions': active,
            'completed_missions': completed,
            'targets': targets,
            'oldest_active': min([m for m in self.missions.values() if m['status'] == 'active'], 
                               key=lambda x: x['launch_date'])['name']
        }
    
    def compare_with_simulation(self, target, sim_transfer_time):
        """Compare simulation with historical missions"""
        historical = self.get_missions_by_target(target)
        if not historical:
            return None
        
        comparisons = []
        for mission in historical:
            comparison = {
                'mission_name': mission['name'],
                'actual_duration': mission['duration_days'],
                'simulated_duration': sim_transfer_time,
                'difference': abs(mission['duration_days'] - sim_transfer_time),
                'accuracy': max(0, 100 - abs(mission['duration_days'] - sim_transfer_time) / mission['duration_days'] * 100)
            }
            comparisons.append(comparison)
        
        return comparisons