import time
from collections import defaultdict
import json

class PerformanceAnalytics:
    def __init__(self):
        self.mission_history = []
        self.performance_metrics = defaultdict(list)
        self.user_stats = {
            'total_simulations': 0,
            'favorite_target': None,
            'avg_efficiency': 0,
            'learning_progress': {}
        }
    
    def log_simulation(self, target, result, user_config=None):
        """Log simulation for analytics"""
        timestamp = time.time()
        
        mission_data = {
            'timestamp': timestamp,
            'target': target,
            'transfer_time': result.get('transfer_time', 0),
            'fuel_dv': result.get('fuel', {}).get('total_dv', 0),
            'fuel_mass': result.get('fuel', {}).get('fuel_mass', 0),
            'efficiency_score': self.calculate_efficiency_score(target, result),
            'config': user_config or {}
        }
        
        self.mission_history.append(mission_data)
        self.update_user_stats()
        
        # Keep only last 100 missions
        if len(self.mission_history) > 100:
            self.mission_history = self.mission_history[-100:]
    
    def calculate_efficiency_score(self, target, result):
        """Calculate mission efficiency score (0-100)"""
        fuel_dv = result.get('fuel', {}).get('total_dv', 0)
        
        # Optimal delta-v values for comparison
        optimal_dv = {'venus': 5.5, 'mars': 6.3, 'jupiter': 8.8}
        
        if fuel_dv <= 0 or target not in optimal_dv:
            return 50
        
        efficiency = (optimal_dv[target] / fuel_dv) * 100
        return min(100, max(0, efficiency))
    
    def update_user_stats(self):
        """Update user statistics"""
        if not self.mission_history:
            return
        
        self.user_stats['total_simulations'] = len(self.mission_history)
        
        # Find favorite target
        target_counts = defaultdict(int)
        efficiency_sum = 0
        
        for mission in self.mission_history:
            target_counts[mission['target']] += 1
            efficiency_sum += mission['efficiency_score']
        
        self.user_stats['favorite_target'] = max(target_counts, key=target_counts.get)
        self.user_stats['avg_efficiency'] = efficiency_sum / len(self.mission_history)
    
    def get_performance_trends(self):
        """Get performance trends over time"""
        if len(self.mission_history) < 2:
            return {'trend': 'insufficient_data'}
        
        recent = self.mission_history[-10:]  # Last 10 missions
        older = self.mission_history[-20:-10] if len(self.mission_history) >= 20 else []
        
        recent_avg = sum(m['efficiency_score'] for m in recent) / len(recent)
        older_avg = sum(m['efficiency_score'] for m in older) / len(older) if older else recent_avg
        
        trend = 'improving' if recent_avg > older_avg + 5 else 'declining' if recent_avg < older_avg - 5 else 'stable'
        
        return {
            'trend': trend,
            'recent_efficiency': recent_avg,
            'improvement': recent_avg - older_avg,
            'total_missions': len(self.mission_history)
        }
    
    def get_target_analytics(self):
        """Get analytics by target planet"""
        target_stats = defaultdict(lambda: {'count': 0, 'avg_efficiency': 0, 'best_efficiency': 0})
        
        for mission in self.mission_history:
            target = mission['target']
            target_stats[target]['count'] += 1
            target_stats[target]['avg_efficiency'] += mission['efficiency_score']
            target_stats[target]['best_efficiency'] = max(
                target_stats[target]['best_efficiency'], 
                mission['efficiency_score']
            )
        
        # Calculate averages
        for target in target_stats:
            if target_stats[target]['count'] > 0:
                target_stats[target]['avg_efficiency'] /= target_stats[target]['count']
        
        return dict(target_stats)
    
    def get_recommendations(self):
        """Get personalized recommendations"""
        recommendations = []
        
        if len(self.mission_history) < 5:
            recommendations.append({
                'type': 'tutorial',
                'message': 'Try the interactive tutorials to learn orbital mechanics basics!',
                'action': 'open_tutorials'
            })
        
        trends = self.get_performance_trends()
        if trends['trend'] == 'declining':
            recommendations.append({
                'type': 'improvement',
                'message': 'Your efficiency has decreased. Try using gravity assists for better performance.',
                'action': 'show_gravity_assist'
            })
        
        target_stats = self.get_target_analytics()
        if 'jupiter' not in target_stats and len(self.mission_history) > 10:
            recommendations.append({
                'type': 'challenge',
                'message': 'Ready for a challenge? Try a mission to Jupiter!',
                'action': 'set_target_jupiter'
            })
        
        return recommendations
    
    def export_data(self):
        """Export analytics data"""
        return {
            'user_stats': self.user_stats,
            'performance_trends': self.get_performance_trends(),
            'target_analytics': self.get_target_analytics(),
            'recommendations': self.get_recommendations(),
            'recent_missions': self.mission_history[-10:] if self.mission_history else []
        }