import math                                  # for basic mathematic operations

from constants import G, KINEMATIC_VISCOSITY

class Channel:
    def __init__(self, id, length, width, max_water_depth, mannings_n, flow_range, slope, from_node, to_node):
        
        self.id = id
        self.length = length
        self.width = width
        self.max_water_depth = max_water_depth
        self.mannings_n = mannings_n
        self.flow_range = flow_range
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

    def uniform_channel_flow(self, flow_case = "avg"):
        flow = self.flow_range[flow_case]

    def non_uniform_channel_flow(self, flow_case = "avg"):
        flow = self.flow_range[flow_case]

    def gradually_varied_flow_profile(self, flow_case = "avg"):
        flow = self.flow_range[flow_case]

        # Critical depth for rectangular channel
        critical_depth = self.critical_depth(flow)

        # Assumed downstream boundary depth
        initial_water_depth = critical_depth + 0.050                               # m

        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_x = 0.001
        water_depth = initial_water_depth

        # This is iterating from the downstream end of the channel to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 
        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.
        # Finally, it prints the calculated water depth, its fraction of the maximum depth, and the Froude number.
        
        while total_x < self.length:
           friction_slope  = self.manning_friction_slope(flow, water_depth)

           froude_number = self.froude_number(flow, water_depth)

           if abs(1 - froude_number**2) < 0.05:
              print("Approaching critical flow - GVF integration unstable")
              break

           delta_y = ( (friction_slope - self.slope) / (1 - froude_number**2) ) * delta_x
           water_depth += delta_y

           if water_depth <= 0:
              print("Warning: Water depth is negative. Check input parameters.")
              break

           freeboard = self.max_water_depth - water_depth
           total_x += delta_x

        print(f"Flow case: {flow_case}, Flow: {flow:.3f} m³/s")
        print(f"Downstream depth: {initial_water_depth:.3f} m")
        print(f"Upstream depth:   {water_depth:.3f} m")
        print(f"Depth increase:   {water_depth - initial_water_depth:.3f} m")
        print(f"Freeboard:        {freeboard:.3f} m")
        print(f"Upstream Fr:      {froude_number:.3f}")
        print("-----------------------------")