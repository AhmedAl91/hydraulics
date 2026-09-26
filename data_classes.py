from dataclasses import dataclass
from constants import G

@dataclass
class HydraulicState:
    energy_grade: float
    hydraulic_grade: float
    velocity: float = 0.0
    depth: float | None = None
    regime: str | None = None       # "subcritical", "critical", "supercritical"

@dataclass
class HydraulicResult:
    upstream_state: HydraulicState
    head_loss: float | None = None
    is_hydraulic_control: bool | False = False

@dataclass
class DownstreamBoundary:
    kind: str
    elevation: float | None = None
    velocity: float = 0.0

    def hydraulic_state(self):
        if self.kind == "known_water_level":

            # At a free-surface boundary:
            # HGL = water surface elevation
            # EGL = HGL + velocity head

            velocity_head = self.velocity ** 2 / (2 * G)

            # Velocity can be negligible e.g. discharge into a reservoir / outfall
            # and therefore energy grade level (EGL) ~= hydraulic grade level (HGL)
            # Depth is not used for the boundary state
            
            return HydraulicState(
                energy_grade=self.elevation + velocity_head,      # EGL
                hydraulic_grade=self.elevation,                   # HGL / free surface
                velocity=self.velocity,                   
                regime="boundary"
            )

            # Open channel / partially filled pipe:
            #     hydraulic_grade = water surface elevation
            #     depth = HGL - invert

            # Pressurised pipe:
            #     hydraulic_grade = piezometric head
            #     depth = diameter

            # Boundary:
            #     hydraulic_grade = known water level
        
        raise NotImplementedError