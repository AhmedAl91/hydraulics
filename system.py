# Raw data, taken from user input API
pipes_data = [
  {
    "id": "P01",
    "length": 100,
    "diameter": 0.3,
    "roughness": 0.02,
    "from_node": "N03",
    "to_node": "N04",
    "fittings": ["pipe_bend_90_degrees_short", "pipe_entry_into_manhole", "pipe_exit_into_manhole"],
	"flow_range": {
		"min": 0.211,                   # m3/s
		"avg": 0.324,                   # m3/s
		"max": 0.408                    # m3/s
	}
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
    "from_node": "N01",
    "to_node": "N02",
	"flow_range": {
		"min": 0.211,                   # m3/s
		"avg": 0.324,                   # m3/s
		"max": 0.408                    # m3/s
	}
  },
]

nodes_data = [
    {
        "id": "N01",
        "aod": 26.175,
    },
    {
        "id": "N02",
        "aod": 25.600,
    },
]