from data_classes import dataclass

class Network:
    def __init__(self, nodes, pipes, channels, weirs, downstream_boundary):
        self.nodes = nodes
        self.pipes = pipes
        self.channels = channels
        self.weirs = weirs
        self.downstream_boundary = downstream_boundary

        self.incoming = {}
        self.outgoing = {}

        self.build_connectivity()
        self.components = {**pipes,**channels, **weirs}
        self.components = self.order_components()

    def build_connectivity(self):
        for node_id in self.nodes:
            self.incoming[node_id] = []
            self.outgoing[node_id] = []

        for component in self.components.values():
            self.outgoing[component.from_node].append(component.id)
            self.incoming[component.to_node].append(component.id)
    
    def order_components(self):
        positions = [component.position for component in self.components]

        expected = list(range(1, len(self.components) + 1))

        if sorted(positions) != expected:
            raise ValueError(
                f"Component positions must be unique and consecutive "
                f"from 1 to {len(self.components)}. "
                f"Received: {positions}"
            )

        return sorted(
            self.components,
            key=lambda component: component.position
        )
    
    def solve(self):

        state = self.downstream_boundary.hydraulic_state()

        results = {}

        for component in self.components:

            upstream_state = component.solve_upstream(flow = component.flow, downstream_state = state)

            results[component.id] = upstream_state

            downstream_state = upstream_state

        return results
    
    def check_continuity(self, node_id):

        q_in = sum(self.components[c_id].flow for c_id in self.incoming[node_id])
        q_out = sum(self.components[c_id].flow for c_id in self.outgoing[node_id])

        return q_in - q_out


