@dataclass
class HydraulicState:
    energy_level: float
    water_level: float | None = None
    depth: float | None = None
    velocity: float | None = None
    regime: str | None = None

@dataclass
class HydraulicResult:
    regime: str | None = None
    upstream_depth: float | None = None
    upstream_energy_level: float | None = None
    upstream_velocity: float | None = None
    head_loss: float | None = None

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