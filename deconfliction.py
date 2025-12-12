import numpy as np
from typing import List, Dict, Any
from models import DroneMission
from utils import get_position_at_time

class DeconflictionService:
    def __init__(self, safety_radius: float = 5.0):
        self.safety_radius = safety_radius
        self.traffic_schedule: List[DroneMission] = []

    def add_traffic(self, mission: DroneMission):
        """Registers a background drone flight."""
        mission.calculate_trajectory()
        self.traffic_schedule.append(mission)

    def check_mission(self, primary: DroneMission, time_step: float = 0.5) -> Dict[str, Any]:
        """
        Validates the primary mission against known traffic.
        Returns status and conflict details.
        """
        primary.calculate_trajectory()
        
        conflicts = []
        
        # Discretize time to check for collisions
        # We check every 'time_step' seconds.
        current_time = primary.t_start
        while current_time <= primary.t_end:
            
            pos_primary = get_position_at_time(primary, current_time)
            
            if pos_primary is not None:
                # Check against all other drones
                for other in self.traffic_schedule:
                    # Quick Temporal Check: Is the other drone even flying right now?
                    if not (other.t_start <= current_time <= other.t_end):
                        continue
                        
                    pos_other = get_position_at_time(other, current_time)
                    
                    if pos_other is not None:
                        # Spatial Check: Euclidean Distance
                        dist = np.linalg.norm(pos_primary - pos_other)
                        
                        if dist < self.safety_radius:
                            conflicts.append({
                                "time": round(current_time, 2),
                                "location": pos_primary.tolist(),
                                "conflicting_drone": other.drone_id,
                                "distance": round(dist, 2)
                            })
            
            current_time += time_step

        if conflicts:
            return {"status": "CONFLICT DETECTED", "details": conflicts}
        else:
            return {"status": "CLEAR", "details": []}