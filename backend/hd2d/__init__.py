"""Starter utilities for SNES HD-2D prototyping.

This package does not emulate SNES hardware. It provides foundational data models
and profile tooling so we can begin implementing the roadmap in small, testable
pieces.
"""

from .frame_graph import FrameGraph, Layer, LayerType, Sprite, Tile
from .profiles import GameProfile, LightingProfile, RenderPreset, build_default_profiles
from .prototype import Camera, DirectionalLight, PrototypeRenderer
from .scenes import make_alttp_sample_frame, make_chrono_trigger_sample_frame

__all__ = [
    "FrameGraph",
    "Layer",
    "LayerType",
    "Sprite",
    "Tile",
    "GameProfile",
    "LightingProfile",
    "RenderPreset",
    "build_default_profiles",
    "Camera",
    "DirectionalLight",
    "PrototypeRenderer",
    "make_alttp_sample_frame",
    "make_chrono_trigger_sample_frame",
]
