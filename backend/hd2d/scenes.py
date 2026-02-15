from __future__ import annotations

from .frame_graph import FrameGraph, Layer, LayerType, Sprite, Tile


def make_alttp_sample_frame() -> FrameGraph:
    graph = FrameGraph(width=256, height=224)
    graph.add_layer(
        Layer(
            name="bg_far",
            layer_type=LayerType.BG,
            priority=0,
            tiles=[Tile(tile_id=1, x=0, y=0), Tile(tile_id=2, x=8, y=0), Tile(tile_id=3, x=16, y=0)],
        )
    )
    graph.add_layer(
        Layer(
            name="bg_mid",
            layer_type=LayerType.BG,
            priority=1,
            tiles=[Tile(tile_id=10, x=40, y=80), Tile(tile_id=11, x=48, y=80), Tile(tile_id=12, x=56, y=80)],
        )
    )
    graph.add_layer(
        Layer(
            name="sprites",
            layer_type=LayerType.SPRITE,
            priority=2,
            sprites=[Sprite(sprite_id=100, x=120, y=112, width=16, height=24)],
        )
    )
    graph.add_layer(
        Layer(
            name="ui",
            layer_type=LayerType.UI,
            priority=3,
            sprites=[Sprite(sprite_id=200, x=4, y=4, width=80, height=16)],
        )
    )
    return graph


def make_chrono_trigger_sample_frame() -> FrameGraph:
    graph = FrameGraph(width=256, height=224)
    graph.add_layer(
        Layer(
            name="bg_far",
            layer_type=LayerType.BG,
            priority=0,
            tiles=[Tile(tile_id=21, x=0, y=16), Tile(tile_id=22, x=8, y=16), Tile(tile_id=23, x=16, y=16)],
        )
    )
    graph.add_layer(
        Layer(
            name="bg_mid",
            layer_type=LayerType.BG,
            priority=1,
            tiles=[Tile(tile_id=31, x=72, y=100), Tile(tile_id=32, x=80, y=100), Tile(tile_id=33, x=88, y=100)],
        )
    )
    graph.add_layer(
        Layer(
            name="effects",
            layer_type=LayerType.BG,
            priority=2,
            tiles=[Tile(tile_id=45, x=84, y=92), Tile(tile_id=46, x=92, y=92)],
        )
    )
    graph.add_layer(
        Layer(
            name="sprites",
            layer_type=LayerType.SPRITE,
            priority=3,
            sprites=[
                Sprite(sprite_id=300, x=108, y=112, width=16, height=24),
                Sprite(sprite_id=301, x=126, y=112, width=16, height=24),
            ],
        )
    )
    graph.add_layer(
        Layer(
            name="ui",
            layer_type=LayerType.UI,
            priority=4,
            sprites=[Sprite(sprite_id=399, x=4, y=4, width=96, height=16)],
        )
    )
    return graph
