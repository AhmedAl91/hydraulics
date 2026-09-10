from data_classes import dataclass

class Network:
    def __init__(self, nodes, pipes, channels, weirs, downstream_boundary):
        self.nodes = nodes
        self.pipes = pipes
        self.channels = channels
        self.weirs = weirs
        self.downstream_boundary = downstream_boundary
        # need to check object data class as DownstreamBoundary somehow

        self.components = {**pipes,**channels, **weirs}

        self.incoming = {}
        self.outgoing = {}

        self.build_connectivity()

    def build_connectivity(self):
        for node_id in self.nodes:
            self.incoming[node_id] = []
            self.outgoing[node_id] = []

        for component in self.components.values():
            self.outgoing[component.from_node].append(component.id)
            self.incoming[component.to_node].append(component.id)
    
    def solve(self):

        state = self.downstream_boundary.hydraulic_state()

        ordered_components = self.get_solution_order()

        results = {}

        for component in self.ordered_components:

            upstream_state = component.solve_upstream(flow = component.flow, downstream_state = state)

            results[component.id] = upstream_state

            downstream_state = upstream_state

        return results
    
    def check_continuity(self, node_id):

        q_in = sum(self.components[c_id].flow for c_id in self.incoming[node_id])
        q_out = sum(self.components[c_id].flow for c_id in self.outgoing[node_id])

        return q_in - q_out


