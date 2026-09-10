import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Weir:
    def __init__(self, id, aod=None, fixed_head=None, weir_type=""):
        self.id = id
        self.aod = aod

        # For tank fill levels, bellmouths etc
        self.fixed_head = fixed_head
        # Check enums r_notch, v_notch, broad_crested
        self.weir_type = node_type
    
    def free_discharge_flow(self, head):
        pass

    def submerged_flow(self, head, downstream_energy):
        pass

    def upstream_head(self, flow, downstream_energy):
        pass

    def is_submerged(self, downstream_energy):
        pass