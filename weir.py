import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Weir:
    def __init__(self, id,position, width, crest_level, downstream_invert, upstream_invert, weir_type=""):
        self.id = id
        self.position = position
        self.width = width
        self.crest_level = crest_level
        self.downstream_invert = downstream_invert
        self.upstream_invert = upstream_invert
        self.weir_type = weir_type
    
    def free_discharge_flow(self, head):
        pass

    def submerged_flow(self, head, downstream_energy):
        pass

    def upstream_head(self, flow, downstream_energy):
        pass

    def is_submerged(self, downstream_energy):
        pass