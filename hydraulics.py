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
  
  return 0.25 / (math.log10( roughness / (3.7 * diameter) + 5.74 / re**0.9 ) ** 2)

def determine_k_values(pipe, boundary):
  # Sums K values depending for either upper or lower bound
  total_k = 0.0
  
  for fitting in pipe["fittings"]:
    total_k += K_VALUES[fitting][boundary] 
    
  return total_k
