import math                                  # for basic mathematic operations
from constants import G, NU
from data_classes import HydraulicState, HydraulicResult, DownstreamBoundary

class Conduit:
    def __init__(self, id, position, downstream_width, upstream_width, flow, downstream_invert, upstream_invert, max_depth=0.0, mannings_n=0.0, length=0.0, slope=0.0):

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

    # Absracted methods for child classes - agnostic of geometry

    # def area(self, depth, x=0.0)
    # def wetted_perimeter(self, depth, x=0.0)
    # def top_width(self, depth, x=0.0)

    # Generic hydraulics

    def hydraulic_radius(self, depth, x=0.0):
        # Rh = A / P
        # Used for Manning friction slope of channels and partially fileld pipes
        return self.area(depth, x) / self.wetted_perimeter()

    def hydraulic_depth(self, depth, x=0.0):
        # Dh = A / T
        # Used for determining the Froude number
        A = self.area(depth, x)
        T = self.top_width(depth, x)

        if T <= 0: raise ValueError(f"{self.id}: Top width must be greater than zero.")

        return A / T 

    def velocity(self, flow, depth, x=0.0):
        # V = Q / A
        A = self.area(depth, x)
        if A <= 0: raise ValueError(f"{self.id}: Area must be greater than zero.")

        return flow / A 

    def froude_number(self, flow, depth, x=0.0):
        # Fr = V / sqrt(G * Dh)
        # Used to assess flow regime in gradually varied flow (GVF)
        V = self.velocity(flow, depth, x)
        Dh = self.hydraulic_depth(depth, x)
        
        return V / math.sqrt(G * Dh)

    def manning_friction_slope(self, flow, depth, x=0.0):
        # Sf = (V * n / Rh ** (2/3)) ** 2
        # The rate of head loss per unit length; used for gradually varied flow (GVF)
        V = self.velocity(flow, depth, x)
        Rh = self.hydraulic_radius(depth, x)

        return (V * self.mannings_n / Rh ** (2/3)) ** 2

    def specific_energy(self, flow, depth, x=0.0):
        # E = H - z = y + velocity head
        # The hydraulic head minus the datum; used for estimated depth of a fluid at a boundary
        V = self.velocity(flow, depth, x)

        return depth + V**2 / (2 * G)

    def downstream_depth_from_energy(self, flow, available_energy, x=0.0):
        # Determines if the energy is above critical and calls a method to iterate
        yc = self.critical_depth(flow)
        Ec = self.specific_energy(flow, yc)

        if available_energy <= Ec:
            return yc
        
        return self.solve_depth_from_energy(flow = flow, target_energy = available_energy, lower_bound = yc, x = x)
    
    def solve_depth_from_energy(self, flow, target_energy, lower_bound, x=0.0, tolerance=1e-6, max_iterations=100):
        # E = y + velocity head(y), therefore implicit with y, 
        # iteration is needed to solve for depth for a given specific energy at a target flow
        # by setting a lower bound at yc, this is solving for sub-critical flow regime only

        def residual_energy(depth):
            return self.specific_energy(flow, depth, x) - target_energy
        
        depth_low = lower_bound    # minimum energy = critical depth 
        depth_high = target_energy # large depth energy ~= depth

        while residual_energy(depth_high) < 0:
            depth_high *= 2

        # Iterative bisection 
        for _ in range(max_iterations):
            depth_mid = 0.5 * (depth_low + depth_high)
            residual = residual_energy(depth_mid)

            if abs(residual) < tolerance:
                return depth_mid
            
            if residual < 0:
                # Depth is too shallow
                depth_low = depth_mid
            else:
                # Depth is too deep
                depth_high = depth_mid

        return 0.5 * (depth_low + depth_high)

    def critical_depth(self, flow, x=0.0, tolerance=1e-6, max_iterations=100):
        # Solve Fr = 1 using bisection
        # Froude decreases as depth increases (opposite direction to specific energy)

        def residual_froude(depth):
            return self.froude_number(flow, depth, x) - 1.0
        
        depth_low = 1e-8
        depth_high = self.max_depth

        # Iterative bisection 
        for _ in range(max_iterations):
            depth_mid = 0.5 * (depth_low + depth_high)
            residual = residual_froude(depth_mid)

            if abs(residual) < tolerance:
                return depth_mid
            
            if residual > 0:
                # Fr > 1: depth is too shallow
                depth_low  = depth_mid
            else:
                # Fr < 1: depth is too deep
                depth_high  = depth_mid

        return 0.5 * (depth_low + depth_high)
