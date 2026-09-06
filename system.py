# Raw data, taken from user input API
pipes_data = [
  {
    "id": "P01",
    "length": 100,
    "diameter": 0.6,
    "roughness": 0.03,
    "from_node": "N01",
    "to_node": "N02",
    "fittings": ["pipe_bend_90_degrees_short", "pipe_entry_into_manhole", "pipe_exit_into_manhole"]
  },
  {
    "id": "P02",
    "length": 100,
    "diameter": 0.6,
    "roughness": 0.03,
    "from_node": "N02",
    "to_node": "N03",
    "fittings": ["pipe_bend_90_degrees_short", "pipe_entry_into_manhole", "pipe_exit_into_manhole"]
  },
]

channels_data = [
  {
    "id": "C01",
    "length": 8.06,						# m
    "width": 0.600,						# m
    "mannings_n": 0.018,				# dimensionless
    "max_water_depth": 26.175 - 25.600,	# m
    "slope": 0.0,						# m/m
    "from_node": "N02",
    "to_node": "N04",
  },
]

nodes_data = [
    {
        "id": "N01",
        "aod": 26.175,
    },
    {
        "id": "N02",
        "aod": 25.600
    },
    {
        "id": "N03",
        "aod": 25.100
    },
    {
        "id": "N04",
        "aod": 24.800
    },
]