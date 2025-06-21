"""Utility functions for Rocket Simulation"""

import numpy as np
from datetime import datetime

def validate_target(target, valid_targets):
    """Validate target planet"""
    return target in valid_targets

def format_number(num, decimals=2):
    """Format number with proper decimals and commas"""
    if isinstance(num, (int, float)):
        return f"{num:,.{decimals}f}"
    return str(num)

def calculate_orbital_period(distance_au):
    """Calculate orbital period using Kepler's 3rd law"""
    return distance_au ** 1.5 * 365.25  # days

def au_to_km(au):
    """Convert AU to kilometers"""
    return au * 149597870.7

def km_to_au(km):
    """Convert kilometers to AU"""
    return km / 149597870.7

def days_to_years(days):
    """Convert days to years"""
    return days / 365.25

def safe_divide(a, b, default=0):
    """Safe division with default value"""
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

def clamp(value, min_val, max_val):
    """Clamp value between min and max"""
    return max(min_val, min(value, max_val))

def get_timestamp():
    """Get current timestamp string"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_efficiency_score(actual, optimal):
    """Calculate efficiency score (0-100)"""
    if optimal <= 0:
        return 0
    ratio = actual / optimal
    return max(0, min(100, 100 / ratio))