
from constants import G, NU
import math                                  # for basic mathematic operations
# import matplotlib.pyplot as plt              # for plotting system curve
from data_classes import HydraulicState, HydraulicResult, DownstreamBoundary

from conduit import Conduit
from pipe import Pipe 
from channel import Channel
from weir import Weir 
from node import Node 
from network import Network 
import system                                # input data


def RAS_outlet_flat_channel_flow():
    # Fixed parameters
    channel_length = 8.06               # m
    downstream_width = 0.600            # m
    upstream_width = 0.600              # m
    max_water_depth = 26.255 - 25.600   # m
    mannings_n = 0.018                  # dimensionless
    downstream_invert = 25.60           # m 
    upstream_invert = 25.60             # m 
    slope = 0.0                         # m/m

    # Input parameters
    flow_range = {
        "min": 0.211,                   # m3/s
        "avg": 0.324,                   # m3/s
        "max": 0.408                    # m3/s
    }

    water_depth = {
        "min": 26.053 - 25.600,
        "avg": 26.203 - 25.600,
        "max": 26.303 - 25.600,
    }

    for flow_case in flow_range:
        flow = flow_range[flow_case]
        channel = Channel(id="RAS_outlet_flat_channel", position=1, length=channel_length, downstream_width=downstream_width, upstream_width=upstream_width,
                          max_depth=max_water_depth, mannings_n=mannings_n, slope=slope,
                          downstream_invert=downstream_invert, upstream_invert=upstream_invert)

        initial_depth = water_depth[flow_case]
        available_specific_energy = channel.specific_energy(flow, initial_depth)
        channel.gvf_profile_by_x(flow, available_specific_energy)


def RAS_outlet_tapered_channel_flow():
    # Fixed parameters
    channel_length = 1.800              # m
    downstream_width = 0.600            # m
    upstream_width = 4.200              # m
    max_water_depth = 26.255 - 25.600   # m
    mannings_n = 0.018                  # dimensionless
    downstream_invert = 25.60           # m 
    upstream_invert = 25.60             # m 
    slope = 0.0                         # m/m

    # Input parameters
    flow_range = {
        "min": 0.211,                   # m3/s
        "avg": 0.324,                   # m3/s
        "max": 0.408                    # m3/s
    }

    water_depth = {
        "min": 26.070 - 25.600,
        "avg": 26.223 - 25.600,
        "max": 26.325 - 25.600,
    }

    for flow_case in flow_range:
        flow = flow_range[flow_case]
        channel = Channel(id="RAS_outlet_tapered_channel", position=1, length=channel_length, downstream_width=downstream_width, upstream_width=upstream_width,
                          max_depth=max_water_depth, mannings_n=mannings_n, slope=slope, 
                          downstream_invert=downstream_invert, upstream_invert=upstream_invert)

        initial_depth = water_depth[flow_case]
        available_specific_energy = channel.specific_energy(flow, initial_depth)

        channel.gvf_profile_by_x(flow, available_specific_energy)

# RAS_outlet_flat_channel_flow()
# RAS_outlet_tapered_channel_flow()

def partially_filled_pipe_test():
    downstream_boundary = DownstreamBoundary(**system.downstream_boundary_data)
    downstream_state = downstream_boundary.hydraulic_state()

    diameter = 0.600
    downstream_invert = 19.95
    upstream_invert = 26.00
    slope = 0.015
    roughness = 0.003
    mannings_n = 0.018
    fittings = None
    
    pipe_data = {
        "id": "test_pipe",
        "position": 1,
        "length": 100.0,
        "diameter": diameter,
        "downstream_width": diameter,
        "upstream_width": diameter,
        "downstream_invert": downstream_invert,
        "upstream_invert": upstream_invert,
        "slope": slope,
        "roughness": roughness,
        "mannings_n": mannings_n,
        "fittings": fittings
    }
    pipe = Pipe(**pipe_data)

    pipe.solve_upstream(downstream_state=downstream_state)

partially_filled_pipe_test()