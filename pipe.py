
from fittings import K_VALUES                # resistance coefficient library
import math                                  # for basic mathematic operations
# import matplotlib.pyplot as plt              # for plotting system curve
from conduit import Conduit
from data_classes import HydraulicState, HydraulicResult, DownstreamBoundary

from constants import G, NU

class Pipe(Conduit):
    def __init__(self, diameter, roughness=0.0, fittings=None, **kwargs):
        
        super().__init__(**kwargs)

        self.diameter = diameter
        self.radius = diameter / 2
        self.roughness = roughness

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

    def gvf_profile_by_x(self, flow, available_specific_energy, tolerance=1e-6):
        # dy/dx = (Sf - S0) / (1 - Fr**2)
        # The head (and therefore depth) of free flowing water is proportional to the friction slope (Sf)
        # which is a measure of head loss per unit distance. It is eased by the physical slope (S0)
        # and the velocity (inferred through Fr).

        # This method plugs in a small change in length (Δx) to estimate the new upstream depth (y).
        # Fixed-point iteration is used to estimate a mean gradient across the downstream and upstream 
        # hydraulic states to determine the upstream state.

        # Determine downstream depth from specific energy at boundary
        initial_depth = self.downstream_depth_from_energy(flow, available_specific_energy)
        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_x = self.length * 1e-4
        depth = initial_depth
        
        # This is iterating from the downstream end of the channel to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 
        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.
        # Finally, it prints the calculated water depth, the freeboard avaialable, and the Froude number.
        while total_x < self.length:
            x_down = total_x
            # Prevent overshooting
            x_up = min(total_x + delta_x, self.length)
            dx = x_up - x_down  

            # Define the downstream hydraulic state
            froude_down = self.froude_number(flow, depth, x_down)
            friction_slope_down = self.manning_friction_slope(flow, depth, x_down)

            if abs(1 - froude_down**2) < 0.05:
                print("Approaching critical flow - GVF integration unstable")
                break

            # Estimate the upstream hydraulic state
            gradient_down = (friction_slope_down - self.slope) / (1 - froude_down**2)
            trial_depth = depth + gradient_down * dx

            for _ in range(20):
                froude_up = self.froude_number(flow, depth, x_up)
                friction_slope_up = self.manning_friction_slope(flow, trial_depth, x_up)

                if abs(1 - froude_up**2) < 0.05:
                    print("Approaching critical flow - GVF integration unstable")
                    break
                
                gradient_up = (friction_slope_up - self.slope) / (1 - froude_up**2)
                mean_gradient = (gradient_down + gradient_up) / 2
                corrected_depth = depth + mean_gradient * dx

                if abs(corrected_depth - trial_depth) < tolerance:
                    trial_depth = corrected_depth
                    break 
                
                trial_depth = corrected_depth
            
            depth = trial_depth
            total_x = x_up

            if depth <= 0:
                print("Warning: Water depth is negative. Check input parameters.")
                break

        freeboard = self.max_depth - depth
        
        if freeboard <= 0:
            print(f"Warning: Freeboard of {freeboard:.3f} for component {self.id}")

        print(f"Solving GVF by Δx for {self.id}:")
        print(f"Flow: {flow:.3f} m³/s")
        print(f"Downstream depth: {initial_depth:.3f} m")
        print(f"Upstream depth:   {depth:.3f} m")
        print(f"Depth increase:   {depth - initial_depth:.4f} m")
        print(f"Freeboard:        {freeboard:.3f} m")
        print(f"Upstream Fr:      {froude_up:.3f}")
        print("-----------------------------")

        energy_grade = self.specific_energy(flow, depth, self.length) + self.upstream_invert
        hydraulic_grade = depth + self.upstream_invert
        velocity = self.velocity(flow, depth, self.length)
        head_loss = self.specific_energy(flow, depth, self.length) + self.upstream_invert - self.specific_energy(flow, initial_depth, 0.0) - self.downstream_invert 

        return depth, energy_grade, velocity, hydraulic_grade, head_loss

    
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