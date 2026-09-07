
import math
from constants import G, KINEMATIC_VISCOSITY

def manning_friction_slope(flow, channel_width, water_depth, mannings_n):
    # Calculate friction slope using Manning's equation
    area = channel_width * water_depth                                      # m2
    wetted_perimeter = channel_width + 2 * water_depth                      # m
    hydraulic_radius = area / wetted_perimeter                              # m
    velocity = flow / area                                                  # m/s
    friction_slope = (velocity * mannings_n / hydraulic_radius**(2/3))**2   # dimensionless
    froude_number = velocity / math.sqrt(G * water_depth)                    # dimensionless

    return friction_slope, froude_number

def open_channel_flow_check(flow_case = "avg"):
    # Fixed parameters
    G = 9.81                          # m/s2
    channel_length = 8.06             # m
    channel_width = 0.600             # m
    max_water_depth = 26.175 - 25.600 # m
    mannings_n = 0.018                # dimensionless

    # Input parameters
    flow_range = {
        "min": 0.211,                   # m3/s
        "avg": 0.324,                   # m3/s
        "max": 0.408                    # m3/s
    }

    # Evaluated parameters
    critical_depth = (((flow_range[flow_case] / channel_width)**2)/G)**(1/3)                  # m
    initial_water_depth = critical_depth + 0.050                                              # m, assumed starting value, to avoid Fr = 1 at the start of the calculation

    # Iterative calculation to find water depth for given flow
    total_x = 0
    delta_x = 0.001
    water_depth = initial_water_depth
    # This is iterating from the downstream end of the channel to the upstream end, 
    # calculating the water depth at each step based on the friction slope and Froude number. 
    # The loop continues until the total distance covered equals the channel length. 
    # If the water depth becomes negative, a warning is printed, and the loop breaks.
    #  Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
    while total_x < channel_length:

        friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, water_depth, mannings_n)

        if abs(1 - froude_number**2) < 0.05:
            print("Approaching critical flow - GVF integration unstable")
            break

        delta_y = (friction_slope / (1 - froude_number**2)) * delta_x

        water_depth += delta_y

        if water_depth < 0:
            print("Warning: Water depth is negative. Check input parameters.")
            break

        freeboard = max_water_depth - water_depth
        total_x += delta_x

    print(f"Flow case: {flow_case}, Flow: {flow_range[flow_case]:.3f} m³/s")
    print(f"Downstream depth: {initial_water_depth:.3f} m")
    print(f"Upstream depth:   {water_depth:.3f} m")
    print(f"Depth increase:   {water_depth - initial_water_depth:.3f} m")
    print(f"Freeboard:        {freeboard:.3f} m")
    print(f"Upstream Fr:      {froude_number:.3f}")
    print("-----------------------------")

open_channel_flow_check("min")
open_channel_flow_check("avg")
open_channel_flow_check("max")
