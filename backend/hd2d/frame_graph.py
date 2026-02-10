from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Iterable, List, Tuple


class LayerType(str, Enum):
    BG = "bg"
    SPRITE = "sprite"
    MODE7 = "mode7"
    UI = "ui"


@dataclass(frozen=True)
class Tile:
    tile_id: int
    x: int
    y: int
    palette: int = 0
    priority: int = 0


@dataclass(frozen=True)
class Sprite:
    sprite_id: int
    x: int
    y: int
    width: int
    height: int
    priority: int = 0


@dataclass
class Layer:
    name: str
    layer_type: LayerType
    priority: int
    tiles: List[Tile] = field(default_factory=list)
    sprites: List[Sprite] = field(default_factory=list)


@dataclass
class FrameGraph:
    """Normalized frame payload exported from an emulator PPU hook.

    Keeps raw 2D placement while exposing derived depth helpers for our renderer.
    """

    width: int
    height: int
    scanline_events: List[Dict[str, int]] = field(default_factory=list)
    layers: List[Layer] = field(default_factory=list)

    def add_layer(self, layer: Layer) -> None:
        self.layers.append(layer)
        self.layers.sort(key=lambda item: item.priority)

    def depth_table(self, profile_depths: Dict[str, float]) -> Dict[str, float]:
        """Resolve layer depth with profile overrides and stable fallback ordering."""
        table: Dict[str, float] = {}
        fallback_stride = 1.0

        for index, layer in enumerate(self.layers):
            table[layer.name] = profile_depths.get(layer.name, index * fallback_stride)

        return table

    def sprite_bounds(self) -> Iterable[Tuple[int, int, int, int]]:
        for layer in self.layers:
            for sprite in layer.sprites:
                yield (sprite.x, sprite.y, sprite.x + sprite.width, sprite.y + sprite.height)
