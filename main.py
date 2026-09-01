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
flow_cases = system.flow_cases                # m3/s

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

def total_headloss(flow, pipe, boundary):
  # Return total headloss through pipe
  return pipe_headloss(flow, pipe, boundary)    

def plot_system_curves(pipes, case="average"):
  # plot head losses against a range of flows  
  for pipe_id, pipe in pipes.items():

    available_head = nodes[pipe["from_node"]]["aod"] - nodes[pipe["to_node"]]["aod"]  # m

    max_flow = flow_cases[case][pipe_id] + 1                      # m3/s

    flows = [q for q in range(1, max_flow)]                       # m3/s
    
    lower_losses = [total_headloss(q, pipe, "lower") for q in flows]
    
    upper_losses = [total_headloss(q, pipe, "upper") for q in flows]
  
    plt.plot(flows, lower_losses, label="Lower resistance")
    
    plt.plot(flows, upper_losses, label="Upper resistance")
  
    plt.xlabel("Flow (m³/s)")
    plt.ylabel("Headloss (m)")
    # Intersect system curve with available head
    plt.axhline(
        y=available_head,
        label="Available head (m)"
    )
    plt.title("System Resistance Curves")
    plt.fill_between(
      flows,
      lower_losses,
      upper_losses,
      alpha=0.2,
      label="Resistance uncertainty"
    )
    plt.grid()
    plt.legend()
  
    plt.savefig(
      "outputs/system_curve.png",
      dpi=150,
      bbox_inches="tight"
    )
  
    plt.show()
  
  

# Call function
plot_system_curves(pipes, "average")
