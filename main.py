#  Libraries & packages
import math      # for basic mathematic operations

# Constants
G = 9.81         # m2/s

# Water parameters @ 20 C
NU = 1.0e-6      # m2/s, approximate kinematic viscosity
RHO = 998        # kg/m3, approximate density

# Declare nodes
nodes = {}

# Declare pipes and ducts
pipes = {
  # Give Id to pipe
  "P01": {
    # Fixed characteristics
    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe
    "k_values_fittings": 0.0,                  # i.e. resistance coefficients, to be determined from sum of fittings
  }
}


# Utility methods
def area(diameter):
  return math.pi * diameter**2 / 4

def velocity(flow, diameter):
  return flow / area(diameter)

def reynolds_number(flow, diameter):
  v = velocity(flow, diameter)
  return v * diameter / NU

