from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict

from .profiles import GameProfile, build_default_profiles
from .prototype import Camera, PrototypeRenderer
from .scenes import make_alttp_sample_frame, make_chrono_trigger_sample_frame


SCENES = {
    "alttp": make_alttp_sample_frame,
    "chrono_trigger": make_chrono_trigger_sample_frame,
}


def build_render_payload(
    game: str,
    yaw_deg: float | None = None,
    pitch_deg: float | None = None,
    zoom: float = 1.0,
) -> Dict[str, object]:
    profiles = build_default_profiles()
    if game not in profiles:
        raise ValueError(f"Unsupported game '{game}'. Expected one of: {', '.join(sorted(profiles))}")

    profile: GameProfile = profiles[game]
    if game not in SCENES:
        raise ValueError(f"Scene generator missing for game '{game}'")

    default_yaw = min(10.0, float(profile.preset.camera_yaw_limit_deg))
    default_pitch = min(15.0, float(profile.preset.camera_pitch_limit_deg))
    camera = Camera(
        yaw_deg=default_yaw if yaw_deg is None else yaw_deg,
        pitch_deg=default_pitch if pitch_deg is None else pitch_deg,
        zoom=zoom,
    )

    scene = SCENES[game]()
    renderer = PrototypeRenderer(profile=profile, camera=camera)
    return renderer.render(scene)


def write_render_payload(payload: Dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run HD-2D software prototype renderer")
    parser.add_argument("--game", choices=["alttp", "chrono_trigger"], required=True)
    parser.add_argument("--yaw", type=float, default=None, help="Camera yaw in degrees")
    parser.add_argument("--pitch", type=float, default=None, help="Camera pitch in degrees")
    parser.add_argument("--zoom", type=float, default=1.0, help="Camera zoom factor")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path. Defaults to docs/prototype-renders/{game}.json",
    )
    args = parser.parse_args()

    payload = build_render_payload(
        game=args.game,
        yaw_deg=args.yaw,
        pitch_deg=args.pitch,
        zoom=args.zoom,
    )

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = (
            Path(__file__).resolve().parents[2] / "docs" / "prototype-renders" / f"{args.game}.json"
        )

    write_render_payload(payload, output_path)
    print(f"Wrote prototype render for {args.game} to {output_path}")


if __name__ == "__main__":
    main()
