#  Libraries & packages
import math                                  # for basic mathematic operations
import matplotlib.pyplot as plt              # for plotting system curve
from fittings import K_VALUES                # resistance coefficient library
import hydraulics                            # fluid mechanic equations
import system_design                         # input data: pipes and ducts 

# Constants
G = 9.81                                     # m2/s

# Water parameters @ 20 C
NU = 1.0e-6                                  # m2/s, approximate kinematic viscosity

pipes = system_design.pipes
ducts = system_design.ducts

def pipe_headloss(flow, pipe, boundary):
  # Return friction, fitting and total headloss for one pipe
  diameter = pipe["diameter"]
  length = pipe["length"]
  roughness = pipe["roughness"]
  k = hydraulics.determine_k_values(pipe, boundary)
  
  v = hydraulics.velocity(flow, diameter)
  
  f = hydraulics.friction_factor(flow, diameter, roughness)
  
  friction_loss = ( f * length / diameter * v**2 / (2 * G) )          # f (L/D) * (v^2/2g)
  fittings_loss = k * v**2 / (2 * G)                                  # K * (v^2/2g)   
  
  return friction_loss + fittings_loss

def total_headloss(flow, pipes, boundary):
  # Return total headloss through pipes arranged in series
  total_loss = 0.0
  
  for pipe_id, pipe in pipes.items():
    result = hydraulics.pipe_headloss(flow, pipe, boundary)
    total_loss += result
    
  return total_loss    

def plot_system_curves(pipes):
  # plot head losses against a range of 1 to 1000 l/s
  available_head = 0.05                                     # m
  
  flows = [q / 1000 for q in range(1, 501)]                # assign m3/s

  lower_losses = [hydraulics.total_headloss(q, pipes, "lower") for q in flows]
  
  upper_losses = [hydraulics.total_headloss(q, pipes, "upper") for q in flows]

  plt.plot(flows, lower_losses, label="Lower resistance")
  
  plt.plot(flows, upper_losses, label="Upper resistance")

  plt.xlabel("Flow (m³/s)")
  plt.ylabel("Headloss (m)")
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

  plt.show()

# Call function
plot_system_curves(pipes)
