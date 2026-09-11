import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Channel:
    def __init__(self, id, position, length, downstream_width, upstream_width, max_depth, mannings_n, flow, downstream_invert, upstream_invert, slope=0.0):

        self.id = id
        self.position = position
        self.length = length
        self.downstream_width = downstream_width 
        self.upstream_width  = upstream_width  
        self.max_depth = max_depth
        self.mannings_n = mannings_n
        self.slope = slope
        self.downstream_invert = downstream_invert
        self.upstream_invert = upstream_invert

        self.flow = flow 

    def area(self, depth, width=None):
        if width is None:
            width = self.downstream_width
        return width * depth

    def wetted_perimeter(self, depth, width=None):
        if width is None:
            width = self.downstream_width
        return width + 2 * depth

    def hydraulic_radius(self, depth, width=None):
        if width is None:
            width = self.downstream_width
        return self.area(depth, width) / self.wetted_perimeter(depth, width)

    def velocity(self, flow, depth, width=None):
        return flow / self.area(depth, width)

    def froude_number(self, flow, depth, width=None):
        velocity = self.velocity(flow, depth, width)

        return velocity / math.sqrt(G * depth)

    def manning_friction_slope(self, flow, depth, width=None):
       # Rectangular channel geometry
       velocity = self.velocity(flow, depth, width)                          # m/s
       hydraulic_radius = self.hydraulic_radius(depth, width)                 # m

       # Manning friction slope
       return (velocity * self.mannings_n / hydraulic_radius**(2/3))**2             # dimensionless

    def critical_depth(self, flow, width=None):
        if width is None:
            width = self.downstream_width
        return (((flow / width)**2) / G) ** (1/3)
    
    def specific_energy(self, flow, depth, width=None):
        if width is None:
            width = self.downstream_width
        return ((self.velocity(flow, depth, width)**2) / (2 * G)) + depth
    
    def downstream_depth_from_energy(self, flow, available_energy):
        yc = self.critical_depth(flow)
        Ec = self.specific_energy(flow, yc)

        if available_energy <= Ec:
            return yc
        return self.solve_depth_from_energy(flow = flow, target_energy = available_energy, lower_bound = yc)

    def solve_depth_from_energy(self, flow, target_energy, lower_bound, tolerance=1e-6, max_iterations=100):
        
        def residual_energy(depth):
            return self.specific_energy(flow, depth) - target_energy
        
        depth_low = lower_bound    # minimum energy = critical depth 
        depth_high = target_energy # large depth energy ~= depth

        while residual_energy(depth_high) < 0:
            depth_high *= 2

        # Iterative bisection 
        for _ in range(max_iterations):
            depth_mid = 0.5 * (depth_low + depth_high)
            error_mid = residual_energy(depth_mid)

            if abs(error_mid) < tolerance:
                return depth_mid
            
            if error_mid < 0:
                depth_low = depth_mid
            else:
                depth_high = depth_mid

        return 0.5 * (depth_low + depth_high)

    def solve_upstream(self, flow, downstream_state):
        # Energy available assessment
        downstream_specific_energy = downstream_state.energy_level - self.downstream_invert
        depth_critical = self.critical_depth(flow)

        if self.downstream_width == self.upstream_width:
            # Δy is set → solve Δx
            depth_change = self.gvf_profile_by_y(flow, downstream_specific_energy)
        else:
            # Δx known → geometry known → solve y_up
            depth_change = self.gvf_profile_by_x(flow, downstream_specific_energy)

        return depth_change, depth_critical

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
                actual_delta_y  = min(delta_y, depth * 0.5)
                trial_depth = depth - actual_delta_y 

            if trial_depth <= 0:
                # this error pings on first loop, and the self. properties are not passing
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

            # Interpolate to ensure we do not exceed the channel length
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

    