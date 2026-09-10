import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Channel:
    def __init__(self, id, position, length, width, max_depth, mannings_n, slope, flow, downstream_invert, upstream_invert):

        self.id = id
        self.position = position
        self.length = length
        self.width = width
        self.max_depth = max_depth
        self.mannings_n = mannings_n
        self.slope = slope
        self.downstream_invert = downstream_invert
        self.upstream_invert = upstream_invert

        self.flow = flow 

    def area(self, depth):
        return self.width * depth

    def wetted_perimeter(self, depth):
        return self.width + 2 * depth

    def hydraulic_radius(self, depth):
        return self.area(depth) / self.wetted_perimeter(depth)
    
    def velocity(self, flow, depth):
        return flow / self.area(depth)

    def froude_number(self, flow, depth):
        velocity = self.velocity(flow, depth)

        return velocity / math.sqrt(G * depth)

    def manning_friction_slope(self, flow, depth):
       # Rectangular channel geometry
       velocity = self.velocity(flow, depth)                                  # m/s
       hydraulic_radius = self.hydraulic_radius(depth)                        # m

       # Manning friction slope
       return (velocity * self.mannings_n / hydraulic_radius**(2/3))**2             # dimensionless

    def critical_depth(self, flow):
        return (((flow / self.width)**2) / G) ** (1/3)
    
    def specific_energy(self, flow, depth):
        return ((self.velocity(flow, depth)**2) / (2 * G)) + depth
    
    def downstream_depth_from_energy(self, flow, available_energy):
        yc = self.critical_depth(flow)
        Ec = self.energy(flow, yc)

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
        depth_change = self.gradually_varied_flow_profile(flow, downstream_specific_energy)
        
    
    def gradually_varied_flow_profile(self, flow, available_specific_energy):
        # Energy available assessment
        initial_depth = self.downstream_depth_from_energy(flow, available_specific_energy)
        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_y = 1e-4
        depth = initial_depth

        def direct_step_method(self, flow, depth, delta_y=1e-8):
            friction_slope_down  = self.manning_friction_slope(flow, depth)
    
            energy_down = self.specific_energy(flow, depth)
    
            depth += delta_y
    
            friction_slope_up  = self.manning_friction_slope(flow, depth)
    
            froude_number_up = self.froude_number(flow, depth)
    
            energy_up = self.specific_energy(flow, depth)
    
            mean_friction_slope = (friction_slope_down + friction_slope_up) / 2   
    
            delta_x = -1 * (energy_up - energy_down) / (self.slope - mean_friction_slope) 
                
            return abs(delta_x), depth, froude_number_up
        
        # This is iterating from the downstream end of the channel to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 
        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.
        # Finally, it prints the calculated water depth, the freeboard avaialable, and the Froude number.
        while total_x < self.length:
            delta_x, depth, froude_number_up = direct_step_method(flow, depth, delta_y)

            if delta_x == False:
                break

            if delta_x > self.length * 1e-2:
                delta_y /= 10
                total_x = 0.0
                depth = initial_depth 
                continue

            total_x += abs(delta_x)

            if abs(1 - froude_number_up**2) < 0.05:
                print("Approaching critical flow - GVF integration unstable")
                break

            if depth <= 0:
                print("Warning: Water depth is negative. Check input parameters.")
                break

        freeboard = self.max_depth - depth
        if freeboard <= 0:
            print(f"Warning: Freeboard of {freeboard} for component {self.id}")

        print(f"Flow: {flow:.3f} m³/s")
        print(f"Downstream depth: {initial_depth:.3f} m")
        print(f"Upstream depth:   {depth:.3f} m")
        print(f"Depth increase:   {depth - initial_depth:.3f} m")
        print(f"Freeboard:        {freeboard:.3f} m")
        print(f"Upstream Fr:      {froude_number_up:.3f}")
        print("-----------------------------")
        return depth - initial_depth

    