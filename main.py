import math                                  # for basic mathematic operations
import matplotlib.pyplot as plt              # for plotting system curve

from pipe import Pipe 
from channel import Channel 
from node import Node 
from network import Network 
import system                                # input data


# Lookup dictionaries of all objects
pipes = {}

for pipe_data in system.pipes_data:
    pipe = Pipe(**pipe_data)
    pipes[pipe.id] = pipe

channels = {}

for channel_data in system.channels_data:
    channel = Channel(**channel_data)
    channels[channel.id] = channel

nodes = {}

for node_data in system.nodes_data:
    node = Node(**node_data)
    nodes[node.id] = node

network = Network(nodes = nodes, pipes = pipes, channels = channels)

flow_case = "avg"

flows = {
    "P01": {
        "min": 0.200,
        "avg": 0.300,
        "max": 0.400,
	},
    "P02":  {
        "min": 0.100,
        "avg": 0.100,
        "max": 0.400,
	},
    "C01":  {
        "min": 0.100,
        "avg": 0.200,
        "max": 0.400,
	},
}

for node_id, node in network.nodes.items():
    if network.is_boundary(node_id):
          continue
    
    residual = network.continuity_residual(node_id, flows, flow_case)
    
    print(f"Node {node_id}: {residual:.6f}")

headlosses = network.pipe_headlosses(
    flows,
    flow_case="avg",
)

print(headlosses)

#############################################################################

# def manning_friction_slope(flow, channel_width, water_depth, mannings_n):
#   # Calculate friction slope using Manning's equation
#   area = channel_width * water_depth                                      # m2
#   wetted_perimeter = channel_width + 2 * water_depth                      # m
#   hydraulic_radius = area / wetted_perimeter                              # m
#   velocity = flow / area                                                  # m/s
#   friction_slope = (velocity * mannings_n / hydraulic_radius**(2/3))**2   # dimensionless
#   froude_number = velocity / (9.81 * water_depth)**0.5                    # dimensionless

#   return friction_slope, froude_number

# def open_channel_flow_check(flow_case = "avg"):
#   # Fixed parameters
#   G = 9.81                          # m/s2
#   channel_length = 8.06             # m
#   channel_width = 0.600             # m
#   max_water_depth = 26.175 - 25.600 # m
#   mannings_n = 0.018                # dimensionless

#   # Input parameters
#   flow_range = {
#     "min": 0.211,                   # m3/s
#     "avg": 0.324,                   # m3/s
#     "max": 0.408                    # m3/s
#   }

#   # Evaluated parameters
#   critical_depth = (((flow_range[flow_case] / channel_width)**2)/G)**(1/3)                  # m
#   initial_water_depth = critical_depth + 0.050                                                      # m, assumed starting value, to avoid Fr = 1 at the start of the calculation
#   friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, initial_water_depth, mannings_n)

#   # Iterative calculation to find water depth for given flow
#   total_x = 0
#   delta_x = 0.001
#   water_depth = initial_water_depth
#   # This is iterating from the downstream end of the channel to the upstream end, 
#   # calculating the water depth at each step based on the friction slope and Froude number. 
#   # The loop continues until the total distance covered equals the channel length. 
#   # If the water depth becomes negative, a warning is printed, and the loop breaks.
#   #  Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
#   while total_x < channel_length:

#     friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, water_depth, mannings_n)

#     if abs(1 - froude_number**2) < 0.05:
#       print("Approaching critical flow - GVF integration unstable")
#       break

#     delta_y = (friction_slope / (1 - froude_number**2)) * delta_x

#     water_depth += delta_y

#     if water_depth < 0:
#       print("Warning: Water depth is negative. Check input parameters.")
#       break

#     freeboard = max_water_depth - water_depth
#     total_x += delta_x

#   print(f"Flow case: {flow_case}, Flow: {flow_range[flow_case]:.3f} m³/s")
#   print(f"Downstream depth: {initial_water_depth:.3f} m")
#   print(f"Upstream depth:   {water_depth:.3f} m")
#   print(f"Depth increase:   {water_depth - initial_water_depth:.3f} m")
#   print(f"Freeboard:        {freeboard:.3f} m")
#   print(f"Upstream Fr:      {froude_number:.3f}")
#   print("-----------------------------")

# open_channel_flow_check("min")
# open_channel_flow_check("avg")
# open_channel_flow_check("max")
