import math                                  # for basic mathematic operations
from conduit import Conduit
from constants import G, NU
from data_classes import HydraulicState, HydraulicResult, DownstreamBoundary

class Weir(Conduit):
    def __init__(self, weir_type="thin_plate", Cd=0.60, **kwargs):

        super().__init__(**kwargs)

        self.weir_type = weir_type
        self.Cd = Cd
        # Note: the weir crest level is managed as 'downstream_invert = upstream_invert' in the Conduit object
        self.crest_level = self.upstream_invert# Rectangular channel geometry
        
    def width(self, x=0.0):

        return self.downstream_width

    def area(self, depth, x=0.0):

        width = self.width(x)

        return width * depth

    def top_width(self, depth, x=0.0):

        return self.width(x)            # To ensure consistent interface with Pipes

    def wetted_perimeter(self, depth, x=0.0):

        width = self.width(x)

        return (2 * depth) + width

    def flow_over_thin_plate(self, flow, submerged=False):
        # Rectangular notch Weir formula for head of fluid above crest
        # assuming free discharge and negligible approach velocity
        # Typical Cd = 0.60. Refer to BS3680 : Part 4a : 1981

        # Q = Cd * (2/3) * sqrt(2 * G) * b * H ** (3/2)
        # H = (Q / (Cd * (2/3) * sqrt(2 * G) * b)) ** (2/3)
        H = (flow / (self.Cd * (2/3) * math.sqrt(2 * G) * self.downstream_width)) ** (2/3)

        if submerged:
            # Amend iteratively with correction factor
            pass

        energy_grade = self.specific_energy(flow, H) + self.crest_level
        hydraulic_grade = H + self.crest_level
        velocity = self.velocity(flow, H)
        head_loss = H   # rough, not sure how to determine this

        upstream_regime = self.weir_type

        if submerged:
            upstream_regime += "_submerged"

        return H, energy_grade, hydraulic_grade, velocity, upstream_regime, head_loss
    
    def solve_upstream(self, flow, downstream_state):

        # this is how the hand calc assesses it
        submerged = downstream_state.hydraulic_grade >= self.crest_level
        # but this is how HADES assesses, as it assumes the downstream velocity head is recovered as static head at the downstream face of the weir
        submerged = downstream_state.energy_grade >= self.crest_level

        if self.weir_type == "thin_plate":
            
            upstream_depth, upstream_energy_grade, upstream_hydraulic_grade, upstream_velocity, upstream_regime, head_loss = self.flow_over_thin_plate(flow, submerged)


        
        hydraulic_result = HydraulicResult(
            upstream_state=HydraulicState(
                regime=upstream_regime,
                depth=upstream_depth,
                energy_grade=upstream_energy_grade,
                hydraulic_grade=upstream_hydraulic_grade,
                velocity=upstream_velocity,
            ),
            head_loss=head_loss
        )

        return hydraulic_result