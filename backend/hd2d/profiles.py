from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Dict, List


@dataclass
class LightingProfile:
    directional_intensity: float
    ambient_intensity: float
    shadow_softness: float
    bloom_strength: float


@dataclass
class RenderPreset:
    camera_pitch_limit_deg: int
    camera_yaw_limit_deg: int
    depth_of_field: bool
    fog: bool


@dataclass
class GameProfile:
    game_id: str
    title: str
    layer_depths: Dict[str, float]
    lit_layers: List[str]
    unlit_layers: List[str] = field(default_factory=list)
    mode7_strategy: str = "fallback_2d"
    notes: str = ""
    lighting: LightingProfile = field(
        default_factory=lambda: LightingProfile(1.0, 0.35, 0.45, 0.2)
    )
    preset: RenderPreset = field(
        default_factory=lambda: RenderPreset(20, 15, True, True)
    )

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def build_default_profiles() -> Dict[str, GameProfile]:
    """Kickoff profiles requested by the project owner."""
    alttp = GameProfile(
        game_id="alttp",
        title="The Legend of Zelda: A Link to the Past",
        layer_depths={
            "bg_far": -6.0,
            "bg_mid": -3.0,
            "bg_near": -1.0,
            "sprites": 0.0,
            "ui": 3.0,
        },
        lit_layers=["bg_mid", "bg_near", "sprites"],
        unlit_layers=["ui"],
        mode7_strategy="specialized_mesh",
        notes=(
            "Prioritize dungeon readability. Keep UI unlit for clean legibility, "
            "and clamp pitch to avoid hiding enemies behind tile extrusion."
        ),
    )

    chrono_trigger = GameProfile(
        game_id="chrono_trigger",
        title="Chrono Trigger",
        layer_depths={
            "bg_far": -7.0,
            "bg_mid": -4.0,
            "bg_near": -1.5,
            "sprites": 0.0,
            "effects": 1.0,
            "ui": 3.0,
        },
        lit_layers=["bg_mid", "bg_near", "sprites", "effects"],
        unlit_layers=["ui"],
        mode7_strategy="hybrid_profiled",
        notes=(
            "Town scenes should favor soft ambient fill while combat scenes can "
            "increase directional intensity for dramatic shadows."
        ),
        lighting=LightingProfile(1.1, 0.4, 0.35, 0.25),
        preset=RenderPreset(22, 18, True, True),
    )

    return {alttp.game_id: alttp, chrono_trigger.game_id: chrono_trigger}
