import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Node:
    def __init__(self, id, aod=None, fixed_head=None, node_type="junction",):
        self.id = id
        self.aod = aod

        # For tank fill levels, bellmouths etc
        self.fixed_head = fixed_head
        # To be determined later
        self.node_type = node_type