import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Channel:
    def __init__(self, id, length, width, max_water_depth, mannings_n, slope, from_node, to_node):
        
        self.id = id
        self.length = length
        self.width = width
        self.max_water_depth = max_water_depth
        self.mannings_n = mannings_n
        self.slope = slope

        self.from_node = from_node
        self.to_node = to_node

    def area(self, water_depth):
        return self.width * water_depth

    def wetted_perimeter(self, water_depth):
        return self.width + 2 * water_depth

    def hydraulic_radius(self, water_depth):
        return self.area(water_depth) / self.wetted_perimeter(water_depth)
    
    def velocity(self, flow, water_depth):
        return flow / self.area(water_depth)

    def froude_number(self, flow, water_depth):
        velocity = self.velocity(flow, water_depth)

        return velocity / math.sqrt(G * water_depth)

    def manning_friction_slope(self, flow, water_depth):
       # Rectangular channel geometry
       velocity = self.velocity(flow, water_depth)                                  # m/s
       hydraulic_radius = self.hydraulic_radius(water_depth)                        # m

       # Manning friction slope
       return (velocity * self.mannings_n / hydraulic_radius**(2/3))**2             # dimensionless

    def critical_depth(self, flow):
        return (((flow / self.width)**2) / G) ** (1/3)
    
    def specific_energy(self, flow, water_depth):
        return ((self.velocity(flow, water_depth)**2) / (2 * G)) + water_depth
    
    def downstream_depth_from_energy(self, flow, available_energy):
        yc = self.critical_depth(flow)
        Ec = self.energy(flow, yc)

        if available_energy <= Ec:
            return yc
        
        return self.subcritical_depth(flow = flow, target_energy = available_energy, lower_bound = yc)

    def subcritical_depth(self, flow, target_energy, lower_bound, tolerance=1e-6, max_iterations=100):
        
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
                energy_low = depth_mid
            else:
                energy_high = depth_mid
        
        return 0.5 * (depth_low + depth_high)

    def gradually_varied_flow_profile(self, flow, controlled_depth=None, available_energy=None):
        # Energy available assessment
        yc = self.critical_depth(flow)

        # Downstream depth is controlled
        if controlled_depth is not None:
            initial_water_depth = controlled_depth

        # Depth is not known but energy is determined e.g. negligible loss is assumed at connections between two channels
        elif available_energy is not None:
            initial_water_depth = self.downstream_depth_from_energy(flow, available_energy)
        
        else:
            initial_water_depth = yc
            print("Warning: neither controlled depth nor available energy provided for Channel {self.id}, assumed critical depth. Check if it is actually a free discharge boundary.")

        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_y = 1e-4
        water_depth = initial_water_depth

        def direct_step_method(self, flow, water_depth, delta_y=1e-8):
            friction_slope_DS  = self.manning_friction_slope(flow, water_depth)
    
            energy_DS = self.specific_energy(flow, water_depth)
    
            water_depth += delta_y
    
            friction_slope_US  = self.manning_friction_slope(flow, water_depth)
    
            froude_number_US = self.froude_number(flow, water_depth)
    
            energy_US = self.specific_energy(flow, water_depth)
    
            mean_friction_slope = (friction_slope_DS + friction_slope_US) / 2   
    
            delta_x = -1 * (energy_US - energy_DS) / (self.slope - mean_friction_slope) 
                
            return abs(delta_x), water_depth, froude_number_US
        
        # This is iterating from the downstream end of the channel to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 
        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.
        # Finally, it prints the calculated water depth, the freeboard avaialable, and the Froude number.
        while total_x < self.length:
            delta_x, water_depth, froude_number_US = direct_step_method(flow, water_depth, delta_y)

            if delta_x == False:
                break

            if delta_x > self.length * 1e-2:
                delta_y /= 10
                total_x = 0.0
                water_depth = initial_water_depth 
                continue

            total_x += abs(delta_x)

            if abs(1 - froude_number_US**2) < 0.05:
                print("Approaching critical flow - GVF integration unstable")
                break

            if water_depth <= 0:
                print("Warning: Water depth is negative. Check input parameters.")
                break

        freeboard = self.max_water_depth - water_depth

        print(f"Flow: {flow:.3f} m³/s")
        print(f"Downstream depth: {initial_water_depth:.3f} m")
        print(f"Upstream depth:   {water_depth:.3f} m")
        print(f"Depth increase:   {water_depth - initial_water_depth:.3f} m")
        print(f"Freeboard:        {freeboard:.3f} m")
        print(f"Upstream Fr:      {froude_number_US:.3f}")
        print("-----------------------------")
        return water_depth - initial_water_depth, freeboard

    