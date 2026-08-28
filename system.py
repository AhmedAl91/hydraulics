# Declare pipes and ducts for a given flow (split if there are merging or diverging flows)
max_flow = 501                                 # l/s
available_head = 0.05                          # m

pipes = {
  "P01": {
    # Fixed characteristics
    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe with concrete lining
    
    # Fittings and bends installed
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

ducts = {
  "D01": {
    # Fixed characteristics
    "length": 10.0,                            # m
    "diameter": 0.75,                          # m, internal diameter
    "roughness": 0.0001,                       # m = 0.1 mm, typical cast iron pipe with concrete lining
    
    # Fittings and bends installed
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
