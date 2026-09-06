import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Node:
    def __init__(self, id, aod=None, fixed_head=None, external_flow=0.0, node_type="junction",):
        self.id = id
        self.aod = aod

        # For tank fill levels, bellmouths etc
        self.fixed_head = fixed_head
        # For flows that do not need resolving, flow entering if > 0, flow leaving if < 0
        self.external_flow = external_flow
        # To be determined later
        self.node_type = node_type