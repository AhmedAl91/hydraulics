@dataclass
class HydraulicState:
    energy_level: float
    water_level: float | None = None
    depth: float | None = None
    velocity: float | None = None
    regime: str | None = None

@dataclass
class DownstreamBoundary:
    kind: str
    elevation: float | None = None

    def hydraulic_state(self):
        if self.kind == "known_water_level":
            return HydraulicState(
                energy_level=self.elevation,
                water_level=self.elevation,
                velocity=0.0,
                regime="boundary"
            )
        
        raise NotImplementedError