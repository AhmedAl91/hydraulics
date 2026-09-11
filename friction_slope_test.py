
import math
from constants import G, KINEMATIC_VISCOSITY
from channel import Channel

# def manning_friction_slope(flow, channel_width, water_depth, mannings_n):
#     # Calculate friction slope using Manning's equation
#     area = channel_width * water_depth                                      # m2
#     wetted_perimeter = channel_width + 2 * water_depth                      # m
#     hydraulic_radius = area / wetted_perimeter                              # m
#     velocity = flow / area                                                  # m/s
#     friction_slope = (velocity * mannings_n / hydraulic_radius**(2/3))**2   # dimensionless
#     froude_number = velocity / math.sqrt(G * water_depth)                    # dimensionless

#     return friction_slope, froude_number


# #####################################################################
# ########################### CASE 1 ##################################


# def flat_channel_flow(flow_case = "avg"):
#     # Fixed parameters
#     channel_length = 8.06             # m
#     channel_width = 0.600             # m
#     max_water_depth = 26.255 - 25.600 # m
#     mannings_n = 0.018                # dimensionless

#     # Input parameters
#     flow_range = {
#         "min": 0.211,                   # m3/s
#         "avg": 0.324,                   # m3/s
#         "max": 0.408                    # m3/s
#     }

#     # Evaluated parameters
#     critical_depth = (((flow_range[flow_case] / channel_width)**2)/G)**(1/3)                  # m

#     # Iterative calculation to find water depth for given flow
#     total_x = 0
#     delta_x = 0.001
#     water_depth = {
#         "min": 26.053 - 25.600,
#         "avg": 26.203 - 25.600,
#         "max": 26.303 - 25.600,
#     }
#     initial_water_depth = water_depth[flow_case]
#     # This is iterating from the downstream end of the channel to the upstream end, 
#     # calculating the water depth at each step based on the friction slope and Froude number. 
#     # The loop continues until the total distance covered equals the channel length. 
#     # If the water depth becomes negative, a warning is printed, and the loop breaks.
#     #  Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
#     while total_x < channel_length:

#         friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, water_depth[flow_case], mannings_n)

#         if abs(1 - froude_number**2) < 0.05:
#             print("Approaching critical flow - GVF integration unstable")
#             break

#         delta_y = (friction_slope / (1 - froude_number**2)) * delta_x

#         water_depth[flow_case] += delta_y

#         if water_depth[flow_case] < 0:
#             print("Warning: Water depth is negative. Check input parameters.")
#             break

#         freeboard = max_water_depth - water_depth[flow_case]
#         total_x += delta_x

#     print("Flat Channel Section:")
#     print(f"Flow case: {flow_case}, Flow: {flow_range[flow_case]:.3f} m³/s")
#     print(f"Downstream depth: {initial_water_depth:.3f} m")
#     print(f"Upstream depth:   {water_depth[flow_case]:.3f} m")
#     print(f"Depth increase:   {water_depth[flow_case] - initial_water_depth:.3f} m")
#     print(f"Freeboard:        {freeboard:.3f} m")
#     print(f"Upstream Fr:      {froude_number:.3f}")
#     print("-----------------------------")

#     return water_depth[flow_case]


# # water_level_upstream_of_flat_channel = {
# #     "min": flat_channel_flow("min"),
# #     "avg": flat_channel_flow("avg"),    
# #     "max": flat_channel_flow("max")
# # }

# def tapered_channel_flow(flow_case = "avg"):
#     # Fixed parameters
#     channel_length = 1.800             # m
#     channel_width = 4.200             # m
#     max_water_depth = 26.255 - 25.600 # m
#     mannings_n = 0.018                # dimensionless

#     # Input parameters
#     flow_range = {
#         "min": 0.211,                   # m3/s
#         "avg": 0.324,                   # m3/s
#         "max": 0.408                    # m3/s
#     }

#     # Evaluated parameters
#     critical_depth = (((flow_range[flow_case] / channel_width)**2)/G)**(1/3)                  # m

#     # Iterative calculation to find water depth for given flow
#     total_x = 0
#     delta_x = 0.001
#     water_depth = {
#         "min": water_level_upstream_of_flat_channel["min"],
#         "avg": water_level_upstream_of_flat_channel["avg"],
#         "max": water_level_upstream_of_flat_channel["max"],
#     }
#     initial_water_depth = water_depth[flow_case]
#     # This is iterating from the downstream end of the channel to the upstream end, 
#     # calculating the water depth at each step based on the friction slope and Froude number. 
#     # The loop continues until the total distance covered equals the channel length. 
#     # If the water depth becomes negative, a warning is printed, and the loop breaks.
#     #  Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
#     while total_x < channel_length:

#         friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, water_depth[flow_case], mannings_n)

#         if abs(1 - froude_number**2) < 0.05:
#             print("Approaching critical flow - GVF integration unstable")
#             break

#         delta_y = (friction_slope / (1 - froude_number**2)) * delta_x

#         water_depth[flow_case] += delta_y

#         if water_depth[flow_case] < 0:
#             print("Warning: Water depth is negative. Check input parameters.")
#             break

#         freeboard = max_water_depth - water_depth[flow_case]
#         total_x += delta_x
#         channel_width -= 2.0 * delta_x  # Tapering the channel width by 2 per meter of length

#     print("Tapered Channel Section:")
#     print(f"Flow case: {flow_case}, Flow: {flow_range[flow_case]:.3f} m³/s")
#     print(f"Channel width: {channel_width:.3f} m at x = {total_x:.3f} m")
#     print(f"Downstream depth: {initial_water_depth:.3f} m")
#     print(f"Upstream depth:   {water_depth[flow_case]:.3f} m")
#     print(f"Depth increase:   {water_depth[flow_case] - initial_water_depth:.3f} m")
#     print(f"Freeboard:        {freeboard:.3f} m")
#     print(f"Upstream Fr:      {froude_number:.3f}")
#     print("-----------------------------")

# # water_level_upstream_of_tapered_channel = {
# #     "min": tapered_channel_flow("min"),
# #     "avg": tapered_channel_flow("avg"),
# #     "max": tapered_channel_flow("max")
# # }

# def first_flat_channel_depth(flow_case = "avg"):
#     # Fixed parameters
#     channel_length = 1.620            # m
#     channel_width = 4.200             # m
#     max_water_depth = 26.255 - 25.600 # m
#     mannings_n = 0.018                # dimensionless

#     # Input parameters
#     flow_range = {
#         "min": 0.211,                   # m3/s
#         "avg": 0.324,                   # m3/s
#         "max": 0.408                    # m3/s
#     }

#     # Evaluated parameters
#     critical_depth = (((flow_range[flow_case] / channel_width)**2)/G)**(1/3)                  # m

#     # Iterative calculation to find water depth for given flow
#     total_x = 0
#     delta_x = 0.001
#     water_depth = {
#         "min": water_level_upstream_of_tapered_channel["min"],
#         "avg": water_level_upstream_of_tapered_channel["avg"],
#         "max": water_level_upstream_of_tapered_channel["max"],
#     }
#     initial_water_depth = water_depth[flow_case]
#     # This is iterating from the downstream end of the channel to the upstream end, 
#     # calculating the water depth at each step based on the friction slope and Froude number. 
#     # The loop continues until the total distance covered equals the channel length. 
#     # If the water depth becomes negative, a warning is printed, and the loop breaks.
#     #  Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
#     while total_x < channel_length:

#         friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, water_depth[flow_case], mannings_n)

#         if abs(1 - froude_number**2) < 0.05:
#             print("Approaching critical flow - GVF integration unstable")
#             break

#         delta_y = (friction_slope / (1 - froude_number**2)) * delta_x

#         water_depth[flow_case] += delta_y

#         if water_depth[flow_case] < 0:
#             print("Warning: Water depth is negative. Check input parameters.")
#             break

#         freeboard = max_water_depth - water_depth[flow_case]
#         total_x += delta_x

#     print("Tapered Channel Section:")
#     print(f"Flow case: {flow_case}, Flow: {flow_range[flow_case]:.3f} m³/s")
#     print(f"Channel width: {channel_width:.3f} m at x = {total_x:.3f} m")
#     print(f"Downstream depth: {initial_water_depth:.3f} m")
#     print(f"Upstream depth:   {water_depth[flow_case]:.3f} m")
#     print(f"Depth increase:   {water_depth[flow_case] - initial_water_depth:.3f} m")
#     print(f"Freeboard:        {freeboard:.3f} m")
#     print(f"Upstream Fr:      {froude_number:.3f}")
#     print("-----------------------------")


# #####################################################################
# ########################### CASE 2 ##################################


# def screw_suction(flow_case = "avg"):
#     # Fixed parameters
#     channel_length = 3.300             # m
#     channel_width = 1.200             # m
#     max_water_depth = 20.40 - 19.70              # m
#     mannings_n = 0.018                # dimensionless

#     # Input parameters
#     flow_range = {
#         "min": 0.084,                   # m3/s
#         "avg": 0.095,                   # m3/s
#         "max": 0.106                    # m3/s
#     }

#     # Evaluated parameters
#     critical_depth = (((flow_range[flow_case] / channel_width)**2)/G)**(1/3)                  # m

#     # Iterative calculation to find water depth for given flow
#     total_x = 0
#     delta_x = 0.001
#     water_depth = {
#         "min": critical_depth + 0.050,
#         "avg": critical_depth + 0.050,
#         "max": critical_depth + 0.050,
#     }
#     initial_water_depth = water_depth[flow_case]
#     # This is iterating from the downstream end of the channel to the upstream end, 
#     # calculating the water depth at each step based on the friction slope and Froude number. 
#     # The loop continues until the total distance covered equals the channel length. 
#     # If the water depth becomes negative, a warning is printed, and the loop breaks.
#     #  Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
#     while total_x < channel_length:

#         friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, water_depth[flow_case], mannings_n)

#         if abs(1 - froude_number**2) < 0.05:
#             print("Approaching critical flow - GVF integration unstable")
#             break

#         delta_y = (friction_slope / (1 - froude_number**2)) * delta_x

#         water_depth[flow_case] += delta_y

#         if water_depth[flow_case] < 0:
#             print("Warning: Water depth is negative. Check input parameters.")
#             break

#         freeboard = max_water_depth - water_depth[flow_case]
#         total_x += delta_x

#     print("Flat Channel Section:")
#     print(f"Flow case: {flow_case}, Flow: {flow_range[flow_case]:.3f} m³/s")
#     print(f"Downstream depth: {initial_water_depth:.3f} m")
#     print(f"Upstream depth:   {water_depth[flow_case]:.3f} m")
#     print(f"Depth increase:   {water_depth[flow_case] - initial_water_depth:.3f} m")
#     print(f"Freeboard:        {freeboard:.3f} m")
#     print(f"Upstream Fr:      {froude_number:.3f}")
#     print("-----------------------------")

#     return water_depth[flow_case]


# # water_level_upstream_of_flat_channel = {
# #     "min": screw_suction("min"),
# #     "avg": screw_suction("avg"),    
# #     "max": screw_suction("max")
# # }


# #####################################################################
# ########################### NEW METHOD ##############################

# # flow_range = {
# #     "min": 0.084,                   # m3/s
# #     "avg": 0.095,                   # m3/s
# #     "max": 0.106                    # m3/s
# # }

# # print("Screw Suction Results:")
# # screw_suction_results = {
# #     "min": Channel("screw_suction", 1.2, 3.3, 20.40 - 19.70, 0.018, 0.0, "None", "None").gradually_varied_flow_profile(flow_range["min"], controlled_depth=20.40 - 19.70),
# #     "avg": Channel("screw_suction", 1.2, 3.3, 20.40 - 19.70, 0.018, 0.0, "None", "None").gradually_varied_flow_profile(flow_range["avg"], controlled_depth=20.40 - 19.70),
# #     "max": Channel("screw_suction", 1.2, 3.3, 20.40 - 19.70, 0.018, 0.0, "None", "None").gradually_varied_flow_profile(flow_range["max"], controlled_depth=20.40 - 19.70),
# # }

# flow_range = {
#     "min": 0.168,                   # m3/s
#     "avg": 0.189,                   # m3/s
#     "max": 0.211                    # m3/s
# }

# print("Inlet Chamber Results:")
# inlet_chamber_results = {
#     "min": Channel("inlet_chamber", 1.5, 4.2, 22.40 - 19.70, 0.018, 0.0, "None", "None").gradually_varied_flow_profile(flow_range["min"], controlled_depth=20.412 - 19.70),
#     "avg": Channel("inlet_chamber", 1.5, 4.2, 22.40 - 19.70, 0.018, 0.0, "None", "None").gradually_varied_flow_profile(flow_range["avg"], controlled_depth=20.412 - 19.70),
#     "max": Channel("inlet_chamber", 1.5, 4.2, 22.40 - 19.70, 0.018, 0.0, "None", "None").gradually_varied_flow_profile(flow_range["max"], controlled_depth=20.414 - 19.70),
# }

def RAS_outlet_flat_channel_flow():
    # Fixed parameters
    channel_length = 8.06               # m
    downstream_width = 0.600            # m
    upstream_width = 0.600              # m
    max_water_depth = 26.255 - 25.600   # m
    mannings_n = 0.018                  # dimensionless
    downstream_invert = 25.60           # m 
    upstream_invert = 25.60             # m 
    slope = 0.0                         # m/m

    # Input parameters
    flow_range = {
        "min": 0.211,                   # m3/s
        "avg": 0.324,                   # m3/s
        "max": 0.408                    # m3/s
    }

    water_depth = {
        "min": 26.053 - 25.600,
        "avg": 26.203 - 25.600,
        "max": 26.303 - 25.600,
    }

    for flow_case in flow_range:
        flow = flow_range[flow_case]
        channel = Channel(id="RAS_outlet_flat_channel", position=1, length=channel_length, downstream_width=downstream_width, upstream_width=upstream_width,
                          max_depth=max_water_depth, mannings_n=mannings_n, slope=slope, flow=flow,
                          downstream_invert=downstream_invert, upstream_invert=upstream_invert)

        initial_depth = water_depth[flow_case]
        available_specific_energy = channel.specific_energy(flow, initial_depth)
        channel.gvf_profile_by_y(flow, available_specific_energy)


def RAS_outlet_tapered_channel_flow():
    # Fixed parameters
    channel_length = 1.800              # m
    downstream_width = 0.600            # m
    upstream_width = 4.200              # m
    max_water_depth = 26.255 - 25.600   # m
    mannings_n = 0.018                  # dimensionless
    downstream_invert = 25.60           # m 
    upstream_invert = 25.60             # m 
    slope = 0.0                         # m/m

    # Input parameters
    flow_range = {
        "min": 0.211,                   # m3/s
        "avg": 0.324,                   # m3/s
        "max": 0.408                    # m3/s
    }

    water_depth = {
        "min": 26.070 - 25.600,
        "avg": 26.223 - 25.600,
        "max": 26.325 - 25.600,
    }

    for flow_case in flow_range:
        flow = flow_range[flow_case]
        channel = Channel(id="RAS_outlet_tapered_channel", position=1, length=channel_length, downstream_width=downstream_width, upstream_width=upstream_width,
                          max_depth=max_water_depth, mannings_n=mannings_n, slope=slope, flow=flow, 
                          downstream_invert=downstream_invert, upstream_invert=upstream_invert)

        initial_depth = water_depth[flow_case]
        available_specific_energy = channel.specific_energy(flow, initial_depth)

        channel.gvf_profile_by_x(flow, available_specific_energy)

RAS_outlet_flat_channel_flow()
RAS_outlet_tapered_channel_flow()