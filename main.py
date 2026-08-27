#  Libraries & packages
import math                                  # for basic mathematic operations
import matplotlib.pyplot as plt              # for plotting system curve
from fittings import K_VALUES                # resistance coefficient library

# Constants
G = 9.81                                     # m2/s

# Water parameters @ 20 C
NU = 1.0e-6                                  # m2/s, approximate kinematic viscosity
RHO = 998                                    # kg/m3, approximate density

# Boundary
boundary = "upper"                            # for conservatism in k values

# Declare pipes and ducts for a given flow (split if there are merging or diverging flows)
pipes = {
  # Give Id to pipe
  "P01": {
    # Fixed characteristics
    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe with concrete lining
    
    # Fittings installed in this pipe
    "fittings": [
      "pipe_bend_45_degrees", 
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_short",
      "pipe_bend_90_degrees_short",
      "pipe_bend_90_degrees_short",
      "pipe_bend_90_degrees_short",
    ]
  }
}

# Utility functions    
def area(diameter):
  return math.pi * diameter**2 / 4

def velocity(flow, diameter):
  return flow / area(diameter)

def reynolds_number(flow, diameter):
  v = velocity(flow, diameter)
  return v * diameter / NU

def friction_factor(flow, diameter, roughness):
  # Darcy friction factor using Swamee-Jain approximation
  re = reynolds_number(flow, diameter)

  # Laminar flow
  if re < 2_300:
    return 64 / re
  
  return 0.25 / ( math.log10( roughness / (3.7 * diameter) + 5.74 / re**0.9 ) ** 2 )

# Head loss calculation

def determine_k_values(pipe, boundary):
  # if upper or lower bound of K values
  total_k = 0.0
  
  for fitting in fittings:
    total_k += K_VALUES[fitting][boundary] 
    
  return total k
    
def pipe_headloss(flow, pipe):
# Return friction, fitting and total headloss for one pipe
  diameter = pipe["diameter"]
  length = pipe["length"]
  roughness = pipe["roughness"]
  k = determine_k_values(pipe, boundary)
  
  v = velocity(flow, pipe["diameter"])
  
  f = friction_factor(flow, pipe["diameter"], pipe["roughness"])
  
  friction_loss = ( f * length / d * v**2 / (2 * G) )          # f (L/D) * (v^2/2g)
  fittings_loss = pipe.k_values_fittings * v**2 / (2 * G)      # K * (v^2/2g)   

def total_headloss(flow, pipes):
# Return total headloss through pipes arranged in series
  for pipe_id, pipe in pipes.items():
    result = pipe_headloss(flow, pipe)
    total_loss += result
    
  return total_loss    

def plot_system_curves(pipes):

  flows = [ q / 1000 for q in range(1, 1001)  ]                # assign m3/s from a range of l/s

  losses = [ total_headloss(q, pipes) for q in flows ]

  plt.plot(flows, losses)

  plt.xlabel("Flow (m³/s)")
  plt.ylabel("Headloss (m)")
  plt.title("System Resistance Curve")
  plt.grid()

  plt.show()
