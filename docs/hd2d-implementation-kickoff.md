# HD-2D SNES Prototype Kickoff (ALTTP + Chrono Trigger)

This repository now includes a **working software prototype** under `backend/hd2d` to begin executing the SNES HD-2D roadmap.

## What is implemented now

- `FrameGraph` data model to represent extracted PPU layers/sprites.
- Depth mapping helper to convert layer ordering into 3D depth values.
- Profile system with two initial game targets:
  - The Legend of Zelda: A Link to the Past (`alttp`)
  - Chrono Trigger (`chrono_trigger`)
- Bootstrap CLI to export profile JSON files for tuning/editing.
- Prototype renderer pipeline that:
  - applies profile depth maps,
  - projects quads with camera yaw/pitch,
  - applies simple directional + ambient brightness,
  - exports pseudo-3D render payloads to JSON.

## How to run the bootstrap

From repository root:

```bash
python -m backend.hd2d.bootstrap
```

Generated files:

- `docs/profiles/alttp.json`
- `docs/profiles/chrono_trigger.json`

## How to run the prototype renderer

```bash
python -m backend.hd2d.run_prototype --game alttp
python -m backend.hd2d.run_prototype --game chrono_trigger
```

Generated files:

- `docs/prototype-renders/alttp.json`
- `docs/prototype-renders/chrono_trigger.json`

These files contain projected screen-space quads and brightness values that can be consumed by a future GPU renderer/UI viewer.


## Backend API endpoint

Start backend from repository root:

```bash
python -m backend.api
```

The Flask API now exposes the prototype renderer directly:

```bash
GET /hd2d/prototype?game=alttp
GET /hd2d/prototype?game=chrono_trigger&yaw=6&pitch=12&zoom=1.1
```

This allows quick iteration from UI tools without writing files first.

## Immediate next milestones

1. Hook a chosen SNES emulator's PPU layer output into `FrameGraph` (replace sample scenes).
2. Build a minimal OpenGL renderer that draws layered quads using exported profile depths.
3. Add camera controls from each profile (`pitch/yaw` bounds).
4. Replace simple brightness with normal-aware lighting and shadow maps.
5. Validate scenes from ALTTP + Chrono Trigger and iterate profile values.
