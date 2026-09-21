
from fittings import K_VALUES                # resistance coefficient library
import math                                  # for basic mathematic operations
# import matplotlib.pyplot as plt              # for plotting system curve
from conduit import Conduit
from data_classes import HydraulicState, HydraulicResult, DownstreamBoundary

from constants import G, NU

class Pipe(Conduit):
    def __init__(self, diameter, fittings=None, **kwargs):
        
        super().__init__(**kwargs)

        self.diameter = diameter
        self.radius = diameter / 2

        self.fittings = fittings or []

    def theta(self, depth):
        if depth <= 0:
            return 0.0
        
        if depth >= self.diameter:
            return 2 * math.pi
        
        return 2 * math.acos((self.radius - depth) / self.radius)

    def area(self, depth, x=0.0):
        theta = self.theta(depth)

        return self.radius**2 / 2 * (theta - math.sin(theta))

    def wetted_perimeter(self, depth, x=0.0):
        theta = self.theta(depth)

        return self.radius * theta

    def top_width(self, depth, x=0.0):
        theta = self.theta(depth)

        return 2 * self.radius * math.sin(theta / 2)

    def hydraulic_diameter(self, depth, x=0.0):
        return 4 * self.hydraulic_radius(depth, x)

    def friction_factor_filled(self, flow, x=0.0):
        if flow == 0:
            return 0.0

        V = self.velocity(flow, depth, x)

        Re = V * self.diameter / NU

		# Darcy friction factor using Swamee-Jain approximation

		# Laminar flow
        if Re < 2_300:
            return 64 / Re

        # Turbulent
        return 0.25 / (math.log10(self.roughness / (3.7 * self.diameter) + 5.74 / Re**0.9 ) ** 2)

    def total_k_values(self):
        return sum(K_VALUES[fitting] for fitting in self.fittings)

    def headloss_filled(self, flow):
        depth = self.diameter

        V = self.velocity(flow, depth)
        f = self.friction_factor_filled(flow, depth)
        K = self.total_k_values()

        friction_loss = f * self.length / self.diameter * V**2 / (2 * G)

        fittings_loss = K * V**2 / (2 * G)

        return friction_loss + fittings_loss

    def gvf_profile_by_x(self, flow):
        # GVF solver by dx with intermittent estimates of fittings??
        pass

    
    def solve_upstream(self, flow, downstream_state):
        # Downstream hydraulic condition
        crown = self.downstream_invert + self.diameter
        velocity_head = downstream_state.velocity ** 2 / (2 * G)
        hydraulic_grade = downstream_state.energy_grade - velocity_head
        depth_critical = self.critical_depth(flow)

        if hydraulic_grade >= crown:
            # Pipe is surcharged/pressurised
            head_loss = self.headloss_filled(flow)
            hydraulic_result = HydraulicResult(
                upstream_state=HydraulicState(
                    regime="pressurised",
                    depth=self.diameter,
                    energy_grade=downstream_state.energy_grade + head_loss,
                    hydraulic_grade=self.diameter + self.upstream_invert,
                    velocity=self.velocity(flow, self.diameter),
                ),
                head_loss=head_loss,
            )
        else:
            # Solve GVF by Δx
            # Assess the available energy
            downstream_specific_energy = downstream_state.energy_grade - self.downstream_invert
            upstream_depth, upstream_energy_grade, upstream_hydraulic_grade, upstream_velocity, head_loss = self.gvf_profile_by_x(flow, downstream_specific_energy)
            hydraulic_result = HydraulicResult(
                upstream_state=HydraulicState(
                    regime="open_channel",
                    depth=upstream_depth,
                    energy_grade=upstream_energy_grade,
                    hydraulic_grade=upstream_hydraulic_grade,
                    velocity=upstream_velocity,
                ),
                head_loss=head_loss,
            )

        return hydraulic_result