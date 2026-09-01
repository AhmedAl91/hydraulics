# Declare nodes, junctions, pipes and ducts

nodes = {
    # Nxx for nodes, Jxx for tee / junctions  # aod: mm
    "N01": {"aod": 100.0},                    
    "N02": {"aod": 95.0},
    "J01": {"aod": 85.0},
    "N03": {"aod": 80.0},
}

# Example merging flows: Q3 = Q1 + Q2         # m3/s
# Requires a manual check for continuity of flow at junctions, i.e. Q1 + Q2 = Q3
flow_cases = {
    "average": {
      "P01": 0.050,
      "P02": 0.030, 
      "P03": 0.080, 
    },   

    "peak": {
      "P01": 0.050,
      "P02": 0.030, 
      "P03": 0.080, 
    },                                  
}
# Example diverging flows: Q1 = Q2 + Q3 
# This needs rework as in reality the Q2 is an output from the head evaluated at the junction
# q_in = 0.100

# split = {
#     "P02": 0.40,
#     "P03": 0.60
# }

# flow_case_2 = {
#     # can create multiple flow cases e.g. peak, average, min
#     "P01": q_in,                              # m3/s
#     "P02": q_in * split["P02"], 
#     "P03": q_in * split["P03"],                         
# }

pipes = {
  "P01": {
    # Fixed characteristics
    "from_node": "N01",
    "to_node": "J01",

    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe with concrete lining
    
    # Fittings and bends installed
    "fittings": [
      "pipe_bend_45_degrees", 
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_short",
    ]
  },
  "P02": {
    # Fixed characteristics
    "from_node": "N02",
    "to_node": "J01",

    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe with concrete lining
    
    # Fittings and bends installed
    "fittings": [
      "pipe_bend_45_degrees", 
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_short",
    ]
  },
  "P03": {
    # Fixed characteristics
    "from_node": "J01",
    "to_node": "N03",

    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe with concrete lining
    
    # Fittings and bends installed
    "fittings": [
      "pipe_bend_45_degrees", 
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_long",
      "pipe_bend_90_degrees_short",
    ]
  },
}

ducts = {
  "D01": {
    # Fixed characteristics
    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe with concrete lining
    
    # Fittings and bends installed
    "fittings": [
      "pipe_bend_45_degrees", 
    ]
  }
}
