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
    
    def energy(self, flow, water_depth):
        return ((self.velocity(flow, water_depth)**2) / (2 * G)) + water_depth

    def uniform_channel_flow(self, flow):
        pass

    def non_uniform_channel_flow(self, flow):
        pass

    def gradually_varied_flow_profile(self, flow, controlled_depth=False):
        # Critical depth for rectangular channel
        critical_depth = self.critical_depth(flow)

        # Assumed downstream boundary depth
        if controlled_depth:
            initial_water_depth = controlled_depth
        else:
            initial_water_depth = critical_depth + 0.010                                # m

        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_y = 0.001
        water_depth = initial_water_depth

        # This is iterating from the downstream end of the channel to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 
        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.
        # Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
        
        while total_x < self.length:
           friction_slope_1  = self.manning_friction_slope(flow, water_depth)

           froude_number_1 = self.froude_number(flow, water_depth)

           energy_1 = self.energy(flow, water_depth)

           if abs(1 - froude_number_1**2) < 0.05:
              print("Approaching critical flow - GVF integration unstable")
              break

           water_depth += delta_y

           friction_slope_2  = self.manning_friction_slope(flow, water_depth)

           froude_number_2 = self.froude_number(flow, water_depth)

           energy_2 = self.energy(flow, water_depth)

           if abs(1 - froude_number_2**2) < 0.05:
              print("Approaching critical flow - GVF integration unstable")
              break

           if water_depth <= 0:
              print("Warning: Water depth is negative. Check input parameters.")
              break

           mean_friction_slope = (friction_slope_1 + friction_slope_2) / 2   

           delta_x = -1 * (energy_2 - energy_1) / (self.slope - mean_friction_slope)  

           freeboard = self.max_water_depth - water_depth

           total_x += delta_x

        print(f"Flow: {flow:.3f} m³/s")
        print(f"Downstream depth: {initial_water_depth:.3f} m")
        print(f"Upstream depth:   {water_depth:.3f} m")
        print(f"Depth increase:   {water_depth - initial_water_depth:.3f} m")
        print(f"Freeboard:        {freeboard:.3f} m")
        print(f"Upstream Fr:      {froude_number_2:.3f}")
        print("-----------------------------")