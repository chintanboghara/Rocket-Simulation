import time
import numpy as np
from datetime import datetime, timedelta

class MissionTracker:
    def __init__(self):
        self.active_missions = {}
        
    def start_mission(self, mission_id, target, trajectory_data):
        """Start tracking a new mission"""
        self.active_missions[mission_id] = {
            'target': target,
            'start_time': time.time(),
            'trajectory': trajectory_data,
            'current_position': 0,
            'status': 'active',
            'events': []
        }
        
    def get_mission_progress(self, mission_id):
        """Get current mission progress"""
        if mission_id not in self.active_missions:
            return None
            
        mission = self.active_missions[mission_id]
        elapsed = time.time() - mission['start_time']
        
        # Scale time (1 second = 10 days for demo)
        progress = min(elapsed * 10 / mission['trajectory']['transfer_time'], 1.0)
        
        # Calculate current position
        trajectory_length = len(mission['trajectory']['rocket'])
        current_index = int(progress * (trajectory_length - 1))
        
        if current_index < len(mission['trajectory']['rocket']):
            current_pos = mission['trajectory']['rocket'][current_index]
        else:
            current_pos = mission['trajectory']['rocket'][-1]
            
        return {
            'mission_id': mission_id,
            'progress': progress * 100,
            'current_position': current_pos,
            'status': 'completed' if progress >= 1.0 else 'active',
            'elapsed_days': elapsed * 10,
            'remaining_days': max(0, mission['trajectory']['transfer_time'] - elapsed * 10),
            'target': mission['target']
        }
    
    def get_all_missions(self):
        """Get status of all active missions"""
        return {mid: self.get_mission_progress(mid) 
                for mid in self.active_missions.keys()}
    
    def add_mission_event(self, mission_id, event):
        """Add event to mission log"""
        if mission_id in self.active_missions:
            self.active_missions[mission_id]['events'].append({
                'timestamp': datetime.now().isoformat(),
                'event': event
            })
    
    def get_mission_events(self, mission_id):
        """Get mission event log"""
        if mission_id not in self.active_missions:
            return []
        return self.active_missions[mission_id]['events']