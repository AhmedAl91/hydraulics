from data_classes import HydraulicState, HydraulicResult, DownstreamBoundary

class Network:
    def __init__(self, nodes, pipes, channels, weirs, downstream_boundary):
        self.nodes = nodes
        self.pipes = pipes
        self.channels = channels
        self.weirs = weirs
        self.downstream_boundary = downstream_boundary

        self.components = {**pipes,**channels, **weirs}

        self.incoming = {}
        self.outgoing = {}

        # self.build_connectivity()

        self.ordered_components = self.order_components()

    # For junction based network evaluation
    def build_connectivity(self):
        for node_id in self.nodes:
            self.incoming[node_id] = []
            self.outgoing[node_id] = []

        for component in self.components.values():
            self.outgoing[component.from_node].append(component.id)
            self.incoming[component.to_node].append(component.id)
    
    # For serial network evaluation
    def order_components(self):
        components = list(self.components.values())

        positions = [component.position for component in components]

        expected = list(range(1, len(self.components) + 1))

        if sorted(positions) != expected:
            raise ValueError(
                f"Component positions must be unique and consecutive "
                f"from 1 to {len(components)}. "
                f"Received: {positions}"
            )

        return sorted(
            components,
            key=lambda component: component.position
        )
    
    def solve(self):

        downstream_state = self.downstream_boundary.hydraulic_state()

        results = {}

        # A serial hydraulic model:

        # UPSTREAM                                      DOWNSTREAM

        #  A -------- B -------- C -------- D -------- Boundary
        #                                          ← solver starts

        # The loop is doing: Boundary ← D ← C ← B ← A

        # However when the solver arrives at a hydraulic control:

        #  A -------- B -------- C -------- D -------- Boundary
        #      ↑
        #    control

        #      → supercritical →
        #                       jump
        #                       ← subcritical ←

        # It must now segment the loop by solving B → C → D again

        for i, component in enumerate(self.ordered_components):

            result = component.solve_upstream(flow = component.flow, downstream_state = downstream_state)
                
            if result.is_hydraulic_control:

                # We have reached a hydraulic control, e.g. a flume
                # Solve the hydraulic domain downstream of the control.
                # This may contain:
                # critical → supercritical → hydraulic jump → subcritical

                # ordered_components:
                
                # [D, C, B, A]
                #        ^
                #        i = 2
                
                # Components downstream of B:
                # [D, C]
                
                # Reverse them for downstream marching:
                # [C, D]

                downstream_components = self.components_downstream_of(i)
                downstream_results = self.solve_downstream_domain(
                    components=downstream_components, 
                    upstream_state=result.upstream_state,
                    downstream_state=downstream_state
                )
                results.update(downstream_results)

                # Continue upstream using the state established at the control.
                downstream_state = result.upstream_state

            else:

                results[component.id] = result
                downstream_state = result.upstream_state

        return results

    def solve_downstream_domain(self, components, upstream_state, downstream_state):
        pass


    def components_downstream_of(self, index):
        return list(reversed(self.ordered_components[:index]))

    
    def check_continuity(self, node_id):

        q_in = sum(self.components[c_id].flow for c_id in self.incoming[node_id])
        q_out = sum(self.components[c_id].flow for c_id in self.outgoing[node_id])

        return q_in - q_out


