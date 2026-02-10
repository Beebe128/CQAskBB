from __future__ import annotations

from dataclasses import dataclass
from math import cos, radians, sin
from typing import Dict, List, Tuple

from .frame_graph import FrameGraph, Layer
from .profiles import GameProfile


@dataclass(frozen=True)
class Camera:
    yaw_deg: float = 10.0
    pitch_deg: float = 15.0
    zoom: float = 1.0


@dataclass(frozen=True)
class DirectionalLight:
    direction: Tuple[float, float, float] = (-0.4, -1.0, -0.25)
    intensity: float = 1.0


@dataclass(frozen=True)
class Quad:
    layer: str
    kind: str
    world: Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]
    screen: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float], Tuple[float, float]]
    brightness: float


class PrototypeRenderer:
    """Minimal pseudo-3D renderer for frame-graph debugging.

    This is intentionally lightweight and deterministic so we can validate profile
    depth/camera/lighting behavior before integrating a GPU backend.
    """

    def __init__(self, profile: GameProfile, camera: Camera | None = None, light: DirectionalLight | None = None):
        self.profile = profile
        self.camera = camera or Camera(
            yaw_deg=min(10.0, profile.preset.camera_yaw_limit_deg),
            pitch_deg=min(15.0, profile.preset.camera_pitch_limit_deg),
            zoom=1.0,
        )
        self.light = light or DirectionalLight(
            intensity=profile.lighting.directional_intensity,
        )

    def render(self, graph: FrameGraph) -> Dict[str, object]:
        depth_table = graph.depth_table(self.profile.layer_depths)
        quads: List[Quad] = []

        for layer in graph.layers:
            layer_depth = depth_table.get(layer.name, 0.0)
            quads.extend(self._render_tiles(layer, layer_depth, graph))
            quads.extend(self._render_sprites(layer, layer_depth, graph))

        serialized = [
            {
                "layer": q.layer,
                "kind": q.kind,
                "world": q.world,
                "screen": q.screen,
                "brightness": round(q.brightness, 4),
            }
            for q in quads
        ]

        return {
            "game_id": self.profile.game_id,
            "camera": {
                "yaw_deg": self.camera.yaw_deg,
                "pitch_deg": self.camera.pitch_deg,
                "zoom": self.camera.zoom,
            },
            "quad_count": len(serialized),
            "quads": serialized,
        }

    def _render_tiles(self, layer: Layer, layer_depth: float, graph: FrameGraph) -> List[Quad]:
        result: List[Quad] = []
        for tile in layer.tiles:
            size = 8.0
            x = float(tile.x)
            y = float(tile.y)
            quad_world = (
                (x, y, layer_depth),
                (x + size, y, layer_depth),
                (x + size, y + size, layer_depth),
                (x, y + size, layer_depth),
            )
            result.append(
                Quad(
                    layer=layer.name,
                    kind="tile",
                    world=quad_world,
                    screen=tuple(self._project(p, graph.width, graph.height) for p in quad_world),
                    brightness=self._brightness(layer.name),
                )
            )
        return result

    def _render_sprites(self, layer: Layer, layer_depth: float, graph: FrameGraph) -> List[Quad]:
        result: List[Quad] = []
        for sprite in layer.sprites:
            x = float(sprite.x)
            y = float(sprite.y)
            w = float(sprite.width)
            h = float(sprite.height)
            quad_world = (
                (x, y, layer_depth),
                (x + w, y, layer_depth),
                (x + w, y + h, layer_depth),
                (x, y + h, layer_depth),
            )
            result.append(
                Quad(
                    layer=layer.name,
                    kind="sprite",
                    world=quad_world,
                    screen=tuple(self._project(p, graph.width, graph.height) for p in quad_world),
                    brightness=self._brightness(layer.name),
                )
            )
        return result

    def _project(self, point: Tuple[float, float, float], width: int, height: int) -> Tuple[float, float]:
        x, y, z = point
        yaw = radians(self.camera.yaw_deg)
        pitch = radians(self.camera.pitch_deg)

        cx = x - (width / 2.0)
        cy = y - (height / 2.0)

        x1 = cx * cos(yaw) - z * sin(yaw)
        z1 = cx * sin(yaw) + z * cos(yaw)

        y1 = cy * cos(pitch) - z1 * sin(pitch)

        sx = (x1 * self.camera.zoom) + (width / 2.0)
        sy = (y1 * self.camera.zoom) + (height / 2.0)
        return (round(sx, 3), round(sy, 3))

    def _brightness(self, layer_name: str) -> float:
        if layer_name in self.profile.unlit_layers:
            return 1.0

        base = self.profile.lighting.ambient_intensity
        directional = max(0.0, -self.light.direction[1]) * self.light.intensity
        return min(1.0, max(0.1, base + directional))
