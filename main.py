from models import Waypoint, DroneMission
from deconfliction import DeconflictionService
from visualization import visualize_scenario

def run_scenario_1_collision():
    print("\n--- Running Scenario 1: Intersecting Paths (Collision) ---")
    service = DeconflictionService(safety_radius=10.0)

    # Traffic Drone: Flies North to South
    traffic = DroneMission(
        drone_id="Traffic_01",
        waypoints=[Waypoint(50, 100, 20), Waypoint(50, 0, 20)],
        t_start=0,
        t_end=20
    )
    service.add_traffic(traffic)

    # Primary Drone: Flies West to East (Intersects at (50, 50, 20) around t=10)
    primary = DroneMission(
        drone_id="Primary_Alpha",
        waypoints=[Waypoint(0, 50, 20), Waypoint(100, 50, 20)],
        t_start=0,
        t_end=20
    )

    result = service.check_mission(primary)
    print(f"Status: {result['status']}")
    if result['status'] == "CONFLICT DETECTED":
        print(f"First Conflict: {result['details'][0]}")

    visualize_scenario(primary, [traffic], result)

def run_scenario_2_clear():
    print("\n--- Running Scenario 2: Different Altitudes (Clear) ---")
    service = DeconflictionService(safety_radius=10.0)

    # Traffic Drone: High altitude
    traffic = DroneMission(
        drone_id="Traffic_02",
        waypoints=[Waypoint(50, 100, 50), Waypoint(50, 0, 50)],
        t_start=0,
        t_end=20
    )
    service.add_traffic(traffic)

    # Primary Drone: Low altitude (Same X/Y path, but different Z)
    primary = DroneMission(
        drone_id="Primary_Beta",
        waypoints=[Waypoint(0, 50, 10), Waypoint(100, 50, 10)],
        t_start=0,
        t_end=20
    )

    result = service.check_mission(primary)
    print(f"Status: {result['status']}")
    
    visualize_scenario(primary, [traffic], result)

if __name__ == "__main__":
    run_scenario_1_collision()
    # Uncomment to run the clear scenario
    # run_scenario_2_clear()