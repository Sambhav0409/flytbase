from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Waypoint:
    """Represents a point in 3D space."""
    x: float
    y: float
    z: float  # Included for Extra Credit (4D)
    
    def to_array(self):
        return [self.x, self.y, self.z]

@dataclass
class TrajectoryPoint(Waypoint):
    """A waypoint with a specific timestamp."""
    t: float

@dataclass
class DroneMission:
    """Defines a drone's mission."""
    drone_id: str
    waypoints: List[Waypoint]
    t_start: float
    t_end: float
    trajectory: List[TrajectoryPoint] = field(default_factory=list)

    def calculate_trajectory(self):
        """
        Interpolates waypoints to create a time-stamped trajectory 
        based on constant velocity assumption over the time window.
        """
        import numpy as np
        
        total_dist = 0
        dists = []
        
        # Calculate total path distance
        for i in range(len(self.waypoints) - 1):
            p1 = np.array(self.waypoints[i].to_array())
            p2 = np.array(self.waypoints[i+1].to_array())
            d = np.linalg.norm(p2 - p1)
            dists.append(d)
            total_dist += d
            
        if total_dist == 0:
            return

        # Assign time to each waypoint based on distance portion
        total_time = self.t_end - self.t_start
        current_t = self.t_start
        
        self.trajectory.append(TrajectoryPoint(self.waypoints[0].x, self.waypoints[0].y, self.waypoints[0].z, current_t))
        
        for i, d in enumerate(dists):
            segment_time = (d / total_dist) * total_time
            current_t += segment_time
            wp = self.waypoints[i+1]
            self.trajectory.append(TrajectoryPoint(wp.x, wp.y, wp.z, current_t))