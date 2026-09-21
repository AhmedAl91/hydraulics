# Raw data, taken from user input API
downstream_boundary_data = {
    "kind": "known_water_level",
    "elevation": 20.0,
    "velocity": 0.0,
}

pipes_data = []

channels_data = []

weirs_data = [
  {
    "id": "storm_overflow_4",
    "Cd": 0.60,
    "weir_type": "thin_plate",
    "position": 1,
    "length" : 0.0,
    "downstream_width": 7.5,
    "upstream_width": 7.5,
    "downstream_invert" : 25.10,
    "upstream_invert": 25.10,
    "flow": 0.084,
  },
]

nodes_data = []