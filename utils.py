import numpy as np
from models import TrajectoryPoint

def interpolate_position(p1: TrajectoryPoint, p2: TrajectoryPoint, t: float) -> np.ndarray:
    """
    Linearly interpolates position between two trajectory points at time t.
    """
    if t <= p1.t:
        return np.array([p1.x, p1.y, p1.z])
    if t >= p2.t:
        return np.array([p2.x, p2.y, p2.z])
        
    fraction = (t - p1.t) / (p2.t - p1.t)
    
    pos1 = np.array([p1.x, p1.y, p1.z])
    pos2 = np.array([p2.x, p2.y, p2.z])
    
    return pos1 + (pos2 - pos1) * fraction

def get_position_at_time(mission, t: float):
    """Finds the drone's position at a specific time t."""
    if t < mission.t_start or t > mission.t_end:
        return None # Drone is not in the air
        
    # Find the segment that contains t
    for i in range(len(mission.trajectory) - 1):
        p1 = mission.trajectory[i]
        p2 = mission.trajectory[i+1]
        
        if p1.t <= t <= p2.t:
            return interpolate_position(p1, p2, t)
            
    return None