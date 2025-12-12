import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from utils import get_position_at_time

def visualize_scenario(primary_mission, traffic_missions, conflicts):
    """
    Generates a 3D animation of the scenario.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Altitude (Z)')
    ax.set_title(f'4D Strategic Deconfliction: {primary_mission.drone_id}')

    # Set plot limits
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 50)

    # Plot paths (static lines)
    def plot_path(mission, color, label):
        xs = [p.x for p in mission.waypoints]
        ys = [p.y for p in mission.waypoints]
        zs = [p.z for p in mission.waypoints]
        ax.plot(xs, ys, zs, color=color, alpha=0.3, label=f"{label} Path")

    plot_path(primary_mission, 'blue', 'Primary')
    for t in traffic_missions:
        plot_path(t, 'red', f'Traffic {t.drone_id}')

    # Dynamic elements (dots moving)
    primary_dot, = ax.plot([], [], [], 'bo', ms=8, label='Primary Drone')
    traffic_dots = [ax.plot([], [], [], 'ro', ms=5)[0] for _ in traffic_missions]
    
    # Conflict markers
    conflict_scatter = ax.scatter([], [], [], c='orange', s=100, marker='x', label='Conflict')

    t_min = min(primary_mission.t_start, min([d.t_start for d in traffic_missions]))
    t_max = max(primary_mission.t_end, max([d.t_end for d in traffic_missions]))
    
    frames = np.linspace(t_min, t_max, 200)

    def update(t):
        # Update Primary
        pos = get_position_at_time(primary_mission, t)
        if pos is not None:
            primary_dot.set_data([pos[0]], [pos[1]])
            primary_dot.set_3d_properties([pos[2]])
        else:
            primary_dot.set_data([], [])
            primary_dot.set_3d_properties([])

        # Update Traffic
        for i, mission in enumerate(traffic_missions):
            pos = get_position_at_time(mission, t)
            if pos is not None:
                traffic_dots[i].set_data([pos[0]], [pos[1]])
                traffic_dots[i].set_3d_properties([pos[2]])
            else:
                traffic_dots[i].set_data([], [])
                traffic_dots[i].set_3d_properties([])
        
        # Flash conflict if current time matches a conflict time (+/- buffer)
        cx, cy, cz = [], [], []
        if conflicts['status'] == "CONFLICT DETECTED":
            for c in conflicts['details']:
                if abs(c['time'] - t) < 0.5:
                    cx.append(c['location'][0])
                    cy.append(c['location'][1])
                    cz.append(c['location'][2])
        
        conflict_scatter._offsets3d = (cx, cy, cz)
        
        return [primary_dot] + traffic_dots + [conflict_scatter]

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, blit=False)
    plt.legend()
    plt.show()