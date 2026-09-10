
from fittings import K_VALUES                # resistance coefficient library
import math                                  # for basic mathematic operations
import matplotlib.pyplot as plt              # for plotting system curve

from constants import G, KINEMATIC_VISCOSITY

class Pipe:
    def __init__(self, id, length, diameter, roughness, flow, fittings=None):
        self.id = id
        self.length = length
        self.diameter = diameter
        self.roughness = roughness 
        self.flow = flow 

        self.fittings = fittings or []

    def velocity(self, flow):
        area = math.pi * self.diameter**2 / 4
        return flow / area

    def friction_factor(self, flow):
        if flow == 0:
            return 0.0

        v = self.velocity(flow)

        reynolds = (v * self.diameter / KINEMATIC_VISCOSITY)
		# Darcy friction factor using Swamee-Jain approximation
		# Laminar flow
        if reynolds < 2_300:
            return 64 / reynolds

        return 0.25 / (math.log10(self.roughness / (3.7 * self.diameter) + 5.74 / reynolds**0.9 ) ** 2)

    def total_k_values(self):
            return sum(K_VALUES[fitting] for fitting in self.fittings)

    def headloss_full(self, flow):
        v = self.velocity(flow)
        f = self.friction_factor(flow)
        k = self.total_k_values()

        friction_loss = (f * self.length / self.diameter * v**2 / (2 * G))

        fittings_loss = (k * v**2 / (2 * G))

        return friction_loss + fittings_loss

    def headloss_partial(self, flow):
        pass

    def plot_system_curves(self, nodes, flow):
        upstream_node = nodes[self.from_node]
        downstream_node = nodes[self.to_node]
        available_head = upstream_node.aod - downstream_node.aod

        flows = [q / 1000 for q in range(1, flow, 1)]                       # m3/s
        
        losses = [self.headloss_full(q) for q in flows]
        
        plt.plot(flows, losses, label="System resistance")
    
        plt.xlabel("Flow (m³/s)")
        plt.ylabel("Headloss (m)")
        # Intersect system curve with available head
        plt.axhline(
            y=available_head,
            label="Available head (m)"
        )
        plt.title("System Resistance Curve")
        plt.grid()
        plt.legend()
    
        plt.savefig(
        f"outputs/system_curve_{self.id}.png",
        dpi=150,
        bbox_inches="tight"
        )
    
        plt.show()
