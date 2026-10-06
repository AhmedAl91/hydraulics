
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
        self.max_depth = diameter
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
        
        depth = self.diameter

        V = self.velocity(flow, depth, x)

        Re = V * self.diameter / NU

		# Darcy friction factor using Swamee-Jain approximation

		# Laminar flow
        if Re < 2_300:
            return 64 / Re

        # Turbulent
        return 0.25 / (math.log10(self.roughness / (3.7 * self.diameter) + 5.74 / Re**0.9 ) ** 2)

    def k_value(self, fitting):
        if fitting["k_value"] is None:
            return K_VALUES[fitting["type"]]
        
        return fitting["k_value"]

    def total_k_values(self):
        return sum(self.k_value(fitting) for fitting in self.fittings)

    def headloss_filled(self, flow):
        depth = self.diameter

        V = self.velocity(flow, depth)
        f = self.friction_factor_filled(flow, depth)
        K = self.total_k_values()

        friction_loss = f * self.length / self.diameter * V**2 / (2 * G)

        fittings_loss = K * V**2 / (2 * G)


        print(f"Solving pipe head loss for {self.id}:")
        print(f"Flow: {flow:.3f} m³/s")
        print(f"Friction losses: {friction_loss:.3f} m")
        print(f"Minor losses:   {fittings_loss:.3f} m")
        print(f"Total losses:   {friction_loss + fittings_loss:.4f} m")
        print("-----------------------------")

        return friction_loss + fittings_loss

    def standard_step(self, flow, known_state, x_from, x_to, tolerance=1e-6, regime="subcritical"):
        # Standard step method - best as the default solver method as it is direction agnostic

        # For any steady state flow:

        #       H = z + E = z + y + velocity head

        #       H up = H down + head loss

        # where 
        #       head loss ~= Sf_mean.Δx

        # therefore 
        #       H up - H down = Sf_mean.Δx

        # Positive dx is defined as downstream flow i.e. head loss is proportionate to Sf_mean * dx
           
        if not 0 <= x_from <= self.length:
            print(f"Warning: position of x_from {x_from} cannot be negative nor greater than the conduit length.")
            return

        if not 0 <= x_to <= self.length:
            print(f"Warning: position of x_to {x_to} cannot be negative nor greater than the conduit length.")
            return

        # For subcritical flow
        # UPSTREAM                          DOWNSTREAM

        # unknown  ← ← ← ← ← ←  known boundary
        

        # For supercritical flow
        # UPSTREAM                          DOWNSTREAM

        # known control  → → → → → → →   unknown

        energy_tolerance = 1e-3
        critical_tolerance = 5e-2

        if regime == "subcritical":
            pass

        elif regime == "supercritical":
            pass

        else:
            print("Warning: direction based on flow regime not defined.")
            return

        x = x_from
        y = known_state.depth
        H = known_state.energy_grade

        z = self.z_value(x)
        E = H - z
        Fr = self.froude_number(flow, y, x)
        head_loss = 0.0

        direction = 1 if x_to > x_from else -1

        delta_x = direction * min(abs(x_to - x_from) * 1e-4, 1e-3)

        while direction * (x_to - x) > 0:

            # ---------------------------------
            # Define next spatial section
            # ---------------------------------

            x_next = x + delta_x

            if direction * (x_next - x_to) > 0:
                x_next = x_to

            dx = x_next - x

            z_next = self.z_value(x_next)

            # ---------------------------------
            # Known friction slope
            # ---------------------------------

            Sf = self.manning_friction_slope(flow, y, x)

            Sf_mean = Sf

            # ---------------------------------
            # Standard-step iteration
            # ---------------------------------
            
            for _ in range(20):
                yc = self.critical_depth(flow)
                Ec = self.specific_energy(flow, yc, x_next)

                if E_next <= Ec * (1 + energy_tolerance):
                    print("Critical-control event.") 
                    return # GVF status
                
                H_next = H - Sf_mean * dx

                E_next = H_next - z_next 

                y_next = self.depth_from_energy(flow, E_next, x_next, regime)

                Sf_next = self.manning_friction_slope(flow, y_next, x_next)

                Sf_new = (Sf + Sf_next) / 2

                if abs(Sf_new - Sf_mean) < tolerance:
                    Sf_mean = Sf_new
                    break

                Sf_mean = Sf_new

            # ---------------------------------
            # Evaluate hydraulic state
            # ---------------------------------
                
            Fr_next = self.froude_number(flow, y_next, x_next)

            if y_next >= self.max_depth:
                print("Surcharge event.") 
                return # GVF status

            # ---------------------------------
            # Accept step
            # ---------------------------------

            step_head_loss = Sf_mean * abs(dx)
            head_loss += step_head_loss
            x = x_next
            y = y_next
            z = z_next
            H = H_next
            E = E_next
            Fr = Fr_next

        freeboard = self.max_depth - y
        
        if freeboard <= 0:
            print(f"Warning: Freeboard of {freeboard:.3f} for component {self.id}")

        print(f"Solving GVF by Standard Step Method for {self.id}:")
        print(f"Flow: {1000 * flow:.3f} l/s with a {regime} regime")
        print(f"Finishing depth:   {y:.3f} m")
        print(f"Freeboard:        {freeboard:.3f} m")
        print(f"Finishing Fr:      {Fr:.3f}")
        print("-----------------------------")

        if Fr_next < 1: 
            regime = "subcritical"

        elif Fr_next == 1: 
            regime = "critical"

        elif Fr_next > 1: 
            regime = "supercritical"

        result = {
            "regime" : regime,
            "energy_grade" : E + z,
            "hydraulic_grade" : y + z,
            "velocity" : self.velocity(flow, y, x_to),
            "head_loss" : head_loss
        }

        return result

    
    def dy_dx_integration(self, flow, available_specific_energy, tolerance=1e-6):
        # Depth from distance method
        # For steady gradually varied flow:
        #
        #     dy/dx = (Sf - S0) / (1 - Fr**2)
        #
        # when integrating from downstream to upstream i.e subcritical regime.
        #
        # Sf represents distributed frictional energy loss per unit length,
        # while S0 represents the change in channel invert elevation.
        # Their difference determines the change in specific energy.
        # The Froude term (function of velocity) determines how that specific-energy change
        # translates into a change in flow depth.

        # This method plugs in a small change in length (Δx) to estimate the new upstream depth (y).
        # Fixed-point iteration is used to estimate a mean gradient across the downstream and upstream 
        # hydraulic states to determine the upstream state.

        # Determine downstream depth from specific energy at boundary
        initial_depth = self.depth_from_energy(flow, available_specific_energy)
        # Iterative calculation to find water depth for given flow
        total_x = 0.0
        delta_x = self.length * 1e-4
        depth = initial_depth

        fittings = self.fittings.copy()
        
        # This is iterating from the downstream end of the pipe to the upstream end, 
        # calculating the water depth at each step based on the friction slope and Froude number. 

        # The discrete losses in a pipe are factored in by estimating the fittings loss and summing
        # this to the energy downstream. It uses the downstream velocity to estimate this, which is not 
        # always correct but the error is assumed to be tolerable.

        # The loop continues until the total distance covered equals the channel length. 
        # If the water depth becomes negative, a warning is printed, and the loop breaks.

        # Finally, it prints the calculated water depth, the freeboard avaialable, and the Froude number.

        while total_x < self.length:
            x_down = total_x
            # Prevent overshooting
            x_up = min(total_x + delta_x, self.length)
            dx = x_up - x_down  

            if fittings:
                fitting_down = fittings[-1]

                # Apply discrete head losses for fittings
                if x_down <= fitting_down["position_by_x"] <= x_up:
                    velocity_down = self.velocity(flow, depth, x_down)

                    K = self.k_value(fitting_down)

                    fitting_loss = K * velocity_down**2 / (2 * G)

                    energy_down = self.specific_energy(flow, depth, x_down)

                    energy_up = energy_down + fitting_loss

                    depth = self.depth_from_energy(flow, energy_up, x_up, "subcritical")

                    fittings.pop()

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
                froude_up = self.froude_number(flow, trial_depth, x_up)
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

        if froude_up < 1: 
            regime = "subcritical"
        elif froude_up == 1: 
            regime = "critical"
        elif froude_up > 1: 
            regime = "supercritical"

        energy_grade = self.specific_energy(flow, depth, self.length) + self.upstream_invert
        hydraulic_grade = depth + self.upstream_invert
        velocity = self.velocity(flow, depth, self.length)
        head_loss = self.specific_energy(flow, depth, self.length) + self.upstream_invert - self.specific_energy(flow, initial_depth, 0.0) - self.downstream_invert 

        return regime, depth, energy_grade, velocity, hydraulic_grade, head_loss

    
    def solve_upstream(self, downstream_state):
        # Fetch the downstream state
        flow = downstream_state.flow
        crown = self.downstream_invert + self.diameter
        hydraulic_grade = downstream_state.hydraulic_grade
        velocity = self.velocity(flow, self.diameter)
        velocity_head = velocity ** 2 / (2*G)

        # -------------------------------------------------
        # 1. Pressurised outlet
        # -------------------------------------------------
        if hydraulic_grade >= crown: 
            print("CASE 1")
            # NOTE This is a simplified assumption as the flow may transition to partial flow upstream, will need to do another check upstream
            # Pipe is surcharged/pressurised
            head_loss = self.headloss_filled(flow)
            # EGL up = EGL down + head_loss
            # HGL = EGL - velocity head
            hydraulic_result = HydraulicResult(
                upstream_state=HydraulicState(
                    regime="pressurised",
                    flow=flow,
                    depth=self.diameter,
                    energy_grade=downstream_state.energy_grade + head_loss,
                    hydraulic_grade=downstream_state.energy_grade - velocity_head,
                    velocity=velocity,
                ),
                head_loss=head_loss,
            )

        # -------------------------------------------------
        # 2. Free-surface outlet
        # -------------------------------------------------
        # NOTE this needs the most rework:
        # a) if the freeboard is estimated as -ve during a GVF profile, then the pipe is actually surcharged and the method should
        #  return a boolean to state re-running the calc as surcharged/pressurised

        # b) if the GVF profile determines a Fr approaching 1 then it should return a boolean for a regime boundary
        # and instead call solve_downstream()
        #                   critical
        #                     │
        #                     ▼
        # upstream  ───────────●────────── downstream

        #     supercritical →       OR       ← subcritical

        # class GVFStatus(Enum):
        #   COMPLETE = "complete"
        #   SURCHARGED = "surcharged"
        #   CRITICAL_CONTROL = "critical_control"

        # profile = self.gvf_profile_by_x(
        #     flow,
        #     downstream_specific_energy,
        # )

        # if profile.status == GVFStatus.SURCHARGED:
        #     # Part-full assumption failed.
        #     # Re-evaluate using full-pipe hydraulics.
        #     ...

        # elif profile.status == GVFStatus.CRITICAL_CONTROL:
        #     # Downstream-controlled subcritical solution
        #     # cannot propagate farther upstream.
        #     ...
        else:
            if hydraulic_grade <= self.downstream_invert:
                print("CASE 2", hydraulic_grade, self.downstream_invert)
                # Free outlet - downstream receiving level does not control the conduit.
                # NOTE this is a simplified model.
                # Approximate the downstream specific energy as Ec + (S0 - Sf).Δx
                # Where Δx is assumed as 0.01 of the pipe length.
                yc = self.critical_depth(flow)
                Ec = self.specific_energy(flow, yc)
                downstream_specific_energy = Ec + (self.slope - self.manning_friction_slope(flow, yc)) * (0.01 * self.length)
            else:
                print("CASE 3")
                # Connected outlet - downstream hydraulic state controls the conduit.
                tailwater_depth = hydraulic_grade - self.downstream_invert
                downstream_specific_energy = self.specific_energy(flow, tailwater_depth)

            # Partially filled pipe: Solve GVF by Δx
            regime, depth, energy_grade, hydraulic_grade, velocity, head_loss = self.dy_dx_integration(flow, downstream_specific_energy)
            # EGL and HGL propagate upstream
            hydraulic_result = HydraulicResult(
                upstream_state=HydraulicState(
                    regime=regime,
                    flow=flow,
                    depth=depth,
                    energy_grade=energy_grade,
                    hydraulic_grade=hydraulic_grade,
                    velocity=velocity,
                ),
                head_loss=head_loss,
            )

        return hydraulic_result