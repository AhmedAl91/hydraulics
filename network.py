class Network:
    def __init__(self, nodes, pipes, channels):
        self.nodes = nodes
        self.pipes = pipes
        self.channels = channels

        self.links = {**pipes,**channels}

        self.incoming = {}
        self.outgoing = {}

        self.build_connectivity()

    def build_connectivity(self):
        for node_id in self.nodes:
            self.incoming[node_id] = []
            self.outgoing[node_id] = []

        for link in self.links.values():

            self.outgoing[link.from_node].append(link.id)

            self.incoming[link.to_node].append(link.id)

    def continuity_residual(self, node_id, flows, flow_case="avg"):
        connected_links = self.incoming[node_id] + self.outgoing[node_id]

        for link_id in connected_links:
            if link_id not in flows:
                raise ValueError(
                    f"No flow value provided for link '{link_id}' "
                    f"connected to node '{node_id}'."
                )
            
        inflow = sum(
            flows[link_id][flow_case]
            for link_id in self.incoming[node_id]
        )

        outflow = sum(
            flows[link_id][flow_case]
            for link_id in self.outgoing[node_id]
        )

        # Solve for flows = 0.0 m3/s
        return inflow - outflow

    def is_boundary(self, node_id):
        return len(self.incoming[node_id]) == 0 or len(self.outgoing[node_id]) == 0

    def pipe_headlosses(self, flows, flow_case="avg"):
        headlosses = {}

        for pipe_id, pipe in self.pipes.items():
            flow = flows[pipe_id][flow_case]

            headlosses[pipe_id] = pipe.headloss_full(flow)

        return headlosses

    def available_head(self, link_id):
        link = self.links[link_id]

        upstream_node = self.nodes[link.from_node]
        downstream_node = self.nodes[link.to_node]

        return upstream_node.aod - downstream_node.aod

    # assess residual head, then solve for pipe flow

# Suppose you have:

# N01 ----P01----> J01 ----P03----> N03
#                     ^
#                     |
#                    P02
#                     |
#                    N02

# with:
# P01: N01 -> J01
# P02: N02 -> J01
# P03: J01 -> N03

# This builds a merging junction:
# incoming["J01"] = ["P01", "P02"]
# outgoing["J01"] = ["P03"]

# Whereas:
#                   ----P02----> N02
#                  /
# N01 ----P01----> J01
#                  \
#                   ----P03----> N03

# builds:
# incoming["J01"] = ["P01"]
# outgoing["J01"] = ["P02", "P03"]

# Continuity equation at each node must resolve as:
# ∑Qin + Qexternal - ∑Qout = 0

# So for a merging junction:
# flows = {
#     "P01": 0.050,
#     "P02": 0.030,
#     "P03": 0.080,
# }
# 0.050 + 0.030 - 0.080 = 0

# Then for a diverging junction:
# flows = {
#     "P01": 0.080,
#     "P02": 0.050,
#     "P03": 0.030,
# }
# 0.080 - 0.050 - 0.030 = 0
