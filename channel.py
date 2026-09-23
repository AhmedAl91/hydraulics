import math                                  # for basic mathematic operations
from conduit import Conduit
from constants import G, NU
from data_classes import HydraulicState, HydraulicResult, DownstreamBoundary

class Channel(Conduit):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)

    # Rectangular channel geometry

    def width(self, x=0.0):

        fraction = x / self.length

        return self.downstream_width + fraction * (self.upstream_width - self.downstream_width)

    def area(self, depth, x=0.0):

        width = self.width(x)

        return width * depth

    def top_width(self, depth, x=0.0):

        return self.width(x)            # To ensure consistent interface with Pipes

    def wetted_perimeter(self, depth, x=0.0):

        width = self.width(x)

        return (2 * depth) + width

    def critical_depth(self, flow, x=0.0):
        # yc = (((Q / W) ** 2) / G) ** (1/3)
        # Note on abstraction: python calls this before calling the Conduit (parent) method
        width = self.width(x)

        return (((flow / width) ** 2) / G) ** (1/3) 

    def solve_upstream(self, flow, downstream_state):
        # Assess the available energy
        downstream_specific_energy = downstream_state.energy_grade - self.downstream_invert

        if self.downstream_width == self.upstream_width:
            # Δy is set → solve Δx
            upstream_depth, upstream_energy_grade, upstream_hydraulic_grade, upstream_velocity, head_loss = self.gvf_profile_by_y(flow, downstream_specific_energy)
        else:
            # Δx known → geometry known → solve y_up
            upstream_depth, upstream_energy_grade, upstream_hydraulic_grade, upstream_velocity, head_loss = self.gvf_profile_by_x(flow, downstream_specific_energy)

        hydraulic_result = HydraulicResult(
            upstream_state=HydraulicState(
                regime="open_channel",
                depth=upstream_depth,
                energy_grade=upstream_energy_grade,
                hydraulic_grade=upstream_hydraulic_grade,
                velocity=upstream_velocity,
            ),
            head_loss=head_loss
        )

        return hydraulic_result
    
    def gvf_profile_by_x(self, flow, available_specific_energy, tolerance=1e-6):
        # dy/dx = (Sf - S0) / (1 - Fr**2)
        # The head (and therefore depth) of free flowing water is proportional to the friction slope (Sf)
        # which is a measure of head loss per unit distance. It is eased by the physical slope (S0)
        # and the velocity (inferred through Fr).

        # This method plugs in a small change in length (Δx) to estimate the new upstream depth (y).
        # It works for rectangular channels and has allowance for tapered widths by re-estimating width, Sf and Fr.
        # Fixed-point iteration is used to estimate a mean gradient across the downstream and upstream 
        # hydraulic states to determine the upstream state.

        # Determine downstream depth from specific energy at boundary
        initial_depth = self._from_energy(flow, available_specific_energy)
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

    def gvf_profile_by_y(self, flow, available_specific_energy):
        # dy/dx = (Sf - S0) / (1 - Fr**2)
        # The head (and therefore depth) of free flowing water is proportional to the friction slope (Sf)
        # which is a measure of head loss per unit distance. It is eased by the physical slope (S0)
        # and the velocity (inferred through Fr)

        # This method plugs in a small change in depth (Δy) to determine the change in length (Δx).
        # It only works for straight lengths of channels, i.e. does not work for pipes nor tapered channels 
        # as they have intermittent / variable losses as a function of x (fittings, or change in width).

        # The direct step method is derived from literature, where the downstream hydraulic state is defined,
        # the gradient backing upstream is estimated, and then the upstream hydraulic state is derived.
        # Interpolation is required afterwards, as small changes in y can result in large x changes, 
        # and can overshoot. 

        # Determine downstream depth from specific energy at boundary
        initial_depth = self.downstream_depth_from_energy(flow, available_specific_energy)
        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_y = 1e-7
        depth = initial_depth
        
        def direct_step_method(flow, depth, delta_y): 
            # Define the downstream hydraulic state
            energy_down = self.specific_energy(flow, depth)
            friction_slope_down = self.manning_friction_slope(flow, depth,)
            froude_down = self.froude_number(flow, depth)

            # Estimate the upstream hydraulic state
            gradient_down = (friction_slope_down - self.slope) / (1 - froude_down**2)

            if gradient_down > 0:
                trial_depth = depth + delta_y
            else:
                trial_depth = depth - delta_y 

            if trial_depth <= 0:
                raise ValueError(f"{self.id}: Trial depth {trial_depth:.6f} m is non-positive. Check input parameters.")

            # Determine the upstream hydraulic sate
            energy_up = self.specific_energy(flow, trial_depth)
            friction_slope_up = self.manning_friction_slope(flow, trial_depth)
            mean_friction_slope = (friction_slope_down + friction_slope_up) / 2

            delta_x = (energy_up - energy_down) / (mean_friction_slope - self.slope)

            froude_up = self.froude_number(flow, trial_depth)
                
            return delta_x, trial_depth, froude_up
        
        # This is iterating from the downstream end of the channel to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 
        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.
        # Finally, it prints the calculated water depth, the freeboard avaialable, and the Froude number.
        while total_x < self.length:
            delta_x, new_depth, froude_up = direct_step_method(flow, depth, delta_y)

            if delta_x <= 0:
                raise ValueError(f"{self.id}: Direct-step calculation produced dx={delta_x:.6f} m, which is non-positive. Check input parameters.")

            # As delta_x could be very large: Interpolate to ensure we do not exceed the channel length
            if total_x + delta_x > self.length:
                remaining_x = self.length - total_x
                fraction = remaining_x / delta_x

                new_depth = depth + fraction * (new_depth - depth)
                delta_x = remaining_x

                froude_up = self.froude_number(flow, new_depth)

            total_x += delta_x
            depth = new_depth

            if abs(1 - froude_up**2) < 0.05:
                print("Approaching critical flow - GVF integration unstable")
                break

            if depth <= 0:
                print("Warning: Water depth is negative. Check input parameters.")
                break

        freeboard = self.max_depth - depth
        
        if freeboard <= 0:
            print(f"Warning: Freeboard of {freeboard:.3f} for component {self.id}")


        print(f"Solving GVF by Δy for {self.id}:")
        print(f"Flow: {flow:.3f} m³/s")
        print(f"Downstream depth: {initial_depth:.3f} m")
        print(f"Upstream depth:   {depth:.3f} m")
        print(f"Depth increase:   {depth - initial_depth:.4f} m")
        print(f"Freeboard:        {freeboard:.3f} m")
        print(f"Upstream Fr:      {froude_up:.3f}")
        print("-----------------------------")

        energy_grade = self.specific_energy(flow, depth) + self.upstream_invert
        hydraulic_grade = depth + self.upstream_invert
        velocity = self.velocity(flow, depth)
        head_loss = self.specific_energy(flow, depth) + self.upstream_invert - self.specific_energy(flow, initial_depth) - self.downstream_invert 

        return depth, energy_grade, velocity, hydraulic_grade, head_loss