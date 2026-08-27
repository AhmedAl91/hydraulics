#  Libraries & packages
import math

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
    "length": 10.0,               # m
    "diameter": 0.75,             # m, internal diameter
    "roughness": 0.0001,          # m = 0.1 mm, typical cast iron pipe
    "resistance": 0.0,            # to be determined from sum of fittings
  }
}

