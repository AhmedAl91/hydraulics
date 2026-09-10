import math                                  # for basic mathematic operations
import matplotlib.pyplot as plt              # for plotting system curve

from pipe import Pipe 
from channel import Channel
from weir import Weir 
from node import Node 
from network import Network 
import system                                # input data


# Lookup dictionaries of all objects
pipes = {}

for pipe_data in system.pipes_data:
    pipe = Pipe(**pipe_data)
    pipes[pipe.id] = pipe

channels = {}

for channel_data in system.channels_data:
    channel = Channel(**channel_data)
    channels[channel.id] = channel

weirs = {}

for weir_data in system.weirs_data:
    weir = Weir(**weir_data)
    weirs[weir.id] = weir

nodes = {}

for node_data in system.nodes_data:
    node = Node(**node_data)
    nodes[node.id] = node

components = ... # how to order based on .position property in each system object counting from 1 to N ?

network = Network(nodes, components)

flow_case = "avg"

flows = {
    "P01": {
        "min": 0.200,
        "avg": 0.300,
        "max": 0.400,
	},
    "P02":  {
        "min": 0.100,
        "avg": 0.100,
        "max": 0.400,
	},
    "C01":  {
        "min": 0.100,
        "avg": 0.200,
        "max": 0.400,
	},
}

for node_id, node in network.nodes.items():
    if network.is_boundary(node_id):
          continue
    
    residual = network.continuity_residual(node_id, flows, flow_case)
    
    print(f"Node {node_id}: {residual:.6f}")

headlosses = network.pipe_headlosses(
    flows,
    flow_case="avg",
)

print(headlosses)
