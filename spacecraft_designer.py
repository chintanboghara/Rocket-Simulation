class SpacecraftDesigner:
    def __init__(self):
        self.components = {
            'engines': {
                'chemical': {'isp': 450, 'thrust': 500, 'mass': 200, 'cost': 1000000},
                'ion': {'isp': 3000, 'thrust': 0.1, 'mass': 50, 'cost': 5000000},
                'nuclear': {'isp': 900, 'thrust': 250, 'mass': 800, 'cost': 10000000}
            },
            'fuel_tanks': {
                'small': {'capacity': 1000, 'mass': 100, 'cost': 100000},
                'medium': {'capacity': 5000, 'mass': 400, 'cost': 400000},
                'large': {'capacity': 15000, 'mass': 1000, 'cost': 1000000}
            },
            'power': {
                'solar': {'power': 5000, 'mass': 200, 'cost': 500000},
                'rtg': {'power': 300, 'mass': 50, 'cost': 2000000},
                'nuclear': {'power': 50000, 'mass': 2000, 'cost': 20000000}
            },
            'payload': {
                'science': {'mass': 500, 'cost': 3000000},
                'communication': {'mass': 100, 'cost': 1000000},
                'lander': {'mass': 2000, 'cost': 10000000}
            }
        }
    
    def design_spacecraft(self, config):
        """Design spacecraft based on configuration"""
        total_mass = 100  # Base structure
        total_cost = 500000  # Base cost
        capabilities = []
        
        # Engine
        engine = config.get('engine', 'chemical')
        if engine in self.components['engines']:
            engine_data = self.components['engines'][engine]
            total_mass += engine_data['mass']
            total_cost += engine_data['cost']
            capabilities.append(f"Engine: {engine} (ISP: {engine_data['isp']}s)")
        
        # Fuel tank
        tank = config.get('fuel_tank', 'medium')
        if tank in self.components['fuel_tanks']:
            tank_data = self.components['fuel_tanks'][tank]
            total_mass += tank_data['mass']
            total_cost += tank_data['cost']
            fuel_capacity = tank_data['capacity']
            capabilities.append(f"Fuel: {fuel_capacity}kg capacity")
        
        # Power system
        power = config.get('power', 'solar')
        if power in self.components['power']:
            power_data = self.components['power'][power]
            total_mass += power_data['mass']
            total_cost += power_data['cost']
            capabilities.append(f"Power: {power_data['power']}W")
        
        # Payload
        payload = config.get('payload', 'science')
        if payload in self.components['payload']:
            payload_data = self.components['payload'][payload]
            total_mass += payload_data['mass']
            total_cost += payload_data['cost']
            capabilities.append(f"Payload: {payload}")
        
        return {
            'total_mass': total_mass,
            'total_cost': total_cost,
            'capabilities': capabilities,
            'config': config,
            'performance_rating': self.calculate_performance(config, total_mass)
        }
    
    def calculate_performance(self, config, total_mass):
        """Calculate spacecraft performance rating"""
        base_score = 50
        
        # Engine efficiency
        engine = config.get('engine', 'chemical')
        if engine == 'ion':
            base_score += 30
        elif engine == 'nuclear':
            base_score += 20
        
        # Mass efficiency
        if total_mass < 2000:
            base_score += 20
        elif total_mass > 5000:
            base_score -= 10
        
        # Power system
        power = config.get('power', 'solar')
        if power == 'nuclear':
            base_score += 15
        elif power == 'rtg':
            base_score += 10
        
        return min(100, max(0, base_score))
    
    def get_presets(self):
        """Get predefined spacecraft configurations"""
        return {
            'budget': {
                'engine': 'chemical',
                'fuel_tank': 'small',
                'power': 'solar',
                'payload': 'science'
            },
            'standard': {
                'engine': 'chemical',
                'fuel_tank': 'medium',
                'power': 'solar',
                'payload': 'science'
            },
            'advanced': {
                'engine': 'ion',
                'fuel_tank': 'large',
                'power': 'rtg',
                'payload': 'science'
            },
            'deep_space': {
                'engine': 'nuclear',
                'fuel_tank': 'large',
                'power': 'nuclear',
                'payload': 'science'
            }
        }