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

network = Network(nodes = nodes, pipes = pipes, channels = channels, weirs = weirs, downstream_boundary = system.downstream_boundary)

network.solve()
network.check_continuity()
