#  Libraries & packages
import math                                  # for basic mathematic operations
import matplotlib.pyplot as plt              # for plotting system curve
import hydraulics                            # fluid mechanic equations
import system                                # input data: pipes and ducts 

# Constants
G = 9.81                                     # m2/s

# Declare system design inputs
nodes = system.nodes
pipes = system.pipes
ducts = system.ducts
design_flows = system.design_flows                # m3/s

def pipe_headloss(flow, pipe, boundary):
  # Return friction, fitting and total headloss for one pipe
  diameter = pipe["diameter"]
  length = pipe["length"]
  roughness = pipe["roughness"]
  k = hydraulics.determine_k_values(pipe, boundary)
  
  v = hydraulics.velocity(flow, diameter)
  
  f = hydraulics.friction_factor(flow, diameter, roughness)
  
  friction_loss = (f * length / diameter * v**2 / (2 * G))          # f (L/D) * (v^2/2g)
  fittings_loss = k * v**2 / (2 * G)                                  # K * (v^2/2g)   
  
  return friction_loss + fittings_loss

def plot_system_curves(pipes, case="average"):
  # plot head losses against a range of flows  
  for pipe_id, pipe in pipes.items():

    available_head = (nodes[pipe["from_node"]]["aod"] - nodes[pipe["to_node"]]["aod"]) / 1000  # m

    max_flow = design_flows[case][pipe_id] + 1                      # l/s

    flows = [q / 1000 for q in range(1, max_flow, 1)]                       # m3/s
    
    # lower_losses = [pipe_headloss(q, pipe, "lower") for q in flows]
    
    upper_losses = [pipe_headloss(q, pipe, "upper") for q in flows]
  
    # plt.plot(flows, lower_losses, label="Lower resistance")
    
    plt.plot(flows, upper_losses, label="System resistance")
  
    plt.xlabel("Flow (m³/s)")
    plt.ylabel("Headloss (m)")
    # Intersect system curve with available head
    plt.axhline(
        y=available_head,
        label="Available head (m)"
    )
    plt.title("System Resistance Curves")
    # plt.fill_between(
    #   flows,
    #   lower_losses,
    #   upper_losses,
    #   alpha=0.2,
    #   label="Resistance uncertainty"
    # )
    plt.grid()
    plt.legend()
  
    plt.savefig(
      f"outputs/system_curve_{pipe_id}_{case}.png",
      dpi=150,
      bbox_inches="tight"
    )
  
    plt.show()
  
  

# # Call function
# plot_system_curves(pipes, "average")


# # Call function
# plot_system_curves(pipes, "peak")

def manning_friction_slope(flow, channel_width, water_depth, mannings_n):
  # Calculate friction slope using Manning's equation
  area = channel_width * water_depth                                      # m2
  wetted_perimeter = channel_width + 2 * water_depth                      # m
  hydraulic_radius = area / wetted_perimeter                              # m
  velocity = flow / area                                                  # m/s
  friction_slope = (velocity * mannings_n / hydraulic_radius**(2/3))**2   # dimensionless
  froude_number = velocity / (9.81 * water_depth)**0.5                    # dimensionless

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
  water_depth = critical_depth + 0.050                                                      # m, assumed starting value, to avoid Fr = 1 at the start of the calculation
  friction_slope, froude_number = manning_friction_slope(flow_range[flow_case], channel_width, water_depth, mannings_n)

  # Iterative calculation to find water depth for given flow
  total_x = 0
  delta_x = 0.001
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

    total_x += delta_x

  print(f"Flow case: {flow_case}, Flow: {flow_range[flow_case]:.3f} m³/s")
  print(f"Water depth: {water_depth:.3f} m, Fraction of max depth: {water_depth / max_water_depth:.3f}, Froude number: {froude_number:.3f}", flush=True)

open_channel_flow_check("min")
open_channel_flow_check("avg")
open_channel_flow_check("max")