import numpy as np

class FuelCalculator:
    def __init__(self):
        # Spacecraft parameters
        self.dry_mass = 1000  # kg
        self.isp = 450  # specific impulse (seconds)
        self.g0 = 9.81  # standard gravity
        
    def delta_v_hohmann(self, r1, r2, mu=1.327e11):  # mu for Sun in km³/s²
        """Calculate delta-v for Hohmann transfer"""
        # Convert AU to km
        r1_km = r1 * 149.6e6
        r2_km = r2 * 149.6e6
        
        # Velocities
        v1 = np.sqrt(mu / r1_km)
        v2 = np.sqrt(mu / r2_km)
        
        # Transfer orbit
        a_transfer = (r1_km + r2_km) / 2
        v_transfer_1 = np.sqrt(mu * (2/r1_km - 1/a_transfer))
        v_transfer_2 = np.sqrt(mu * (2/r2_km - 1/a_transfer))
        
        # Delta-v requirements
        dv1 = abs(v_transfer_1 - v1)  # Departure burn
        dv2 = abs(v2 - v_transfer_2)  # Arrival burn
        
        return dv1/1000, dv2/1000  # Convert to km/s
    
    def fuel_mass(self, delta_v):
        """Calculate fuel mass using rocket equation"""
        mass_ratio = np.exp(delta_v * 1000 / (self.isp * self.g0))
        total_mass = self.dry_mass * mass_ratio
        fuel_mass = total_mass - self.dry_mass
        return fuel_mass
    
    def mission_fuel(self, target_distance):
        """Calculate total mission fuel requirements"""
        dv1, dv2 = self.delta_v_hohmann(1.0, target_distance)
        total_dv = dv1 + dv2
        
        fuel_needed = self.fuel_mass(total_dv)
        
        return {
            'departure_dv': dv1,
            'arrival_dv': dv2,
            'total_dv': total_dv,
            'fuel_mass': fuel_needed,
            'total_mass': self.dry_mass + fuel_needed,
            'fuel_ratio': fuel_needed / (self.dry_mass + fuel_needed)
        }