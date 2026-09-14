import math                                  # for basic mathematic operations
from conduit import Conduit
from constants import G, NU

class Channel(Conduit):
    def __init__(self, downstream_width, upstream_width, **kwargs):

        super().__init__(**kwargs)

        self.downstream_width = downstream_width
        self.upstream_width = upstream_width

    # Reactangular channel geometry

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
        # Python calls this before calling the Conduit (parent) method
        width = self.width(x)

        return (((flow / width) ** 2) / G) ** (1/3) 
    
    def gvf_profile_by_x(self, flow, available_specific_energy):
        # Energy available assessment
        initial_depth = self.downstream_depth_from_energy(flow, available_specific_energy)
        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_x = self.length * 1e-4
        depth = initial_depth

        def width_at_position(x):
            fraction = x / self.length
            width = self.downstream_width + fraction * (self.upstream_width - self.downstream_width)
            return width
        
        # This is iterating from the downstream end of the channel to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 
        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.
        # Finally, it prints the calculated water depth, the freeboard avaialable, and the Froude number.
        while total_x < self.length:
            width_down = width_at_position(total_x)
            x_up = total_x + delta_x
            width_up = width_at_position(x_up)
            froude_down = self.froude_number(flow, depth, width_down)
            friction_slope = self.manning_friction_slope(flow, depth, width_up)

            delta_y = ((friction_slope - self.slope) / (1 - froude_down**2)) * delta_x
            depth += delta_y
            froude_up = self.froude_number(flow, depth, width_up)

            total_x += delta_x

            if abs(1 - froude_up**2) < 0.05:
                print("Approaching critical flow - GVF integration unstable")
                break

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
        return depth - initial_depth

    def gvf_profile_by_y(self, flow, available_specific_energy):
        # Energy available assessment
        initial_depth = self.downstream_depth_from_energy(flow, available_specific_energy)
        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_y = 1e-7
        depth = initial_depth
        
        def direct_step_method(flow, depth, delta_y): 

            energy_down = self.specific_energy(flow, depth)
            friction_slope_down = self.manning_friction_slope(flow, depth,)
            froude_down = self.froude_number(flow, depth)

            gvf_gradient_upstream = (friction_slope_down - self.slope) / (1 - froude_down**2)

            if gvf_gradient_upstream > 0:
                trial_depth = depth + delta_y
            else:
                trial_depth = depth - delta_y 

            if trial_depth <= 0:
                raise ValueError(f"{self.id}: Trial depth {trial_depth:.6f} m is non-positive. Check input parameters.")

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
        return depth - initial_depth