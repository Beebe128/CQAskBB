"""CLI helpers to bootstrap HD-2D work artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from .profiles import build_default_profiles


def write_profiles(output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    profiles = build_default_profiles()

    for game_id, profile in profiles.items():
        (output_dir / f"{game_id}.json").write_text(
            json.dumps(profile.to_dict(), indent=2), encoding="utf-8"
        )

    return len(profiles)


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[2] / "docs" / "profiles"
    count = write_profiles(target)
    print(f"Wrote {count} HD-2D game profiles to {target}")
