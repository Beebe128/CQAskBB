# SNES-to-HD2D Emulator Overlay: Feasibility + Development Plan

## 1) Short answer: is it feasible?

Yes, but with constraints.

A 3DSen-style approach for SNES is technically feasible if you treat each frame as layered 2D tiles/sprites and reconstruct pseudo-3D geometry in real time. The project is realistic as a long-term R&D-heavy emulator fork or graphics interception layer, not as a quick plugin. You can likely achieve convincing "HD-2D" looks for many scenes, but complete accuracy across all SNES games is unlikely without game-specific tuning profiles.

## 2) Core technical idea

Build a rendering pipeline that:

1. Emulates SNES normally (CPU/PPU/APU timing unchanged).
2. Captures PPU output at the tile/sprite/background layer level before final compositing.
3. Converts extracted primitives into 3D billboards/voxels/height layers in a modern GPU pipeline.
4. Renders with camera orbit/tilt, dynamic lights, shadows, depth-of-field, bloom, and color grading.
5. Keeps gameplay and input bound to original 2D coordinates while visuals are transformed.

## 3) Why SNES is harder than NES

SNES has richer PPU behavior and many edge cases:

- Multiple background modes (Mode 0–7) and per-game effects.
- Transparency, additive/subtractive blending, windows/masks.
- Per-scanline effects via HDMA (e.g., perspective/waves).
- Sprite priority interactions and mid-frame register changes.

These effects complicate extracting stable depth/geometry from raw pixels.

## 4) Recommended architecture

### A. Base emulator strategy

Pick one proven open-source SNES core and fork it:

- Primary candidates: bsnes/higan, Snes9x, or Mesen-S.
- Selection criteria: rendering pipeline clarity, debug tooling, license compatibility, build complexity, determinism, and performance.

### B. Data extraction layer (critical)

Insert hooks at the PPU pipeline stage to capture per-frame metadata:

- BG layer tilemaps and tile indices.
- Tile attributes (palette, flips, priority).
- Sprite/OAM entries and priority buckets.
- Scroll values and affine params (especially Mode 7).
- Per-scanline state changes where possible.

Output this into a frame graph structure the 3D renderer consumes.

### C. 3D reconstruction strategies (hybrid)

Use multiple representation modes and switch per layer/game:

1. **Billboard planes per layer**: fast, works broadly.
2. **Per-tile depth extrusion**: gives parallax and volume.
3. **Sprite voxelization (optional)**: expensive but dramatic style.
4. **Mode 7 specialized mesh path**: map the plane into actual 3D ground.

### D. Camera system

- Keep gameplay camera locked to emulated viewport logic.
- Add user-view camera offset (yaw/pitch/zoom) with safe limits.
- Use collision/occlusion helpers to avoid unreadable scenes.

### E. Lighting + shadows for HD-2D look

Modern post/lighting stack:

- Directional + local lights.
- Cascaded shadow maps for world layers.
- Contact shadows/SSAO for depth cues.
- Bloom, vignette, fog, DOF, tone mapping.
- Optional "pixel-stable" shading to preserve sprite identity.

### F. Compatibility profile system

Create per-game profiles:

- Layer depth mappings.
- Which layers are lit/unlit.
- Occlusion overrides.
- Mode 7 handling mode.
- Custom camera limits.

This is likely essential for high-quality output across titles.

## 5) Development roadmap (phased)

## Phase 0 — Research + proof constraints (2–4 weeks)

- Select emulator base and confirm legal path.
- Instrument PPU to dump frame/layer metadata.
- Build test corpus (10 games across varied SNES modes).
- Define success metrics: FPS, visual coherence, input latency.

**Deliverable:** Technical design doc + small frame-inspection tool.

## Phase 1 — Minimal 3D prototype (6–10 weeks)

- Integrate GPU renderer (OpenGL/Vulkan/Metal abstraction).
- Convert BG layers to stacked textured planes.
- Render sprites as camera-facing quads.
- Add camera tilt/yaw and basic depth ordering.

**Deliverable:** Real-time pseudo-3D in at least 3 games.

## Phase 2 — Depth semantics + style tooling (8–12 weeks)

- Per-layer/per-tile depth controls.
- Authoring UI for depth painting and profile tuning.
- Add physically inspired lighting and shadow pass.
- Add post-processing presets for HD-2D look.

**Deliverable:** "Looks good" vertical slice on 1–2 flagship games.

## Phase 3 — Hard cases + compatibility (12–20 weeks)

- Mode 7 dedicated reconstruction path.
- HDMA-aware corrections for scanline effects.
- Blend/window handling improvements.
- Profile library + auto-detection heuristics.

**Deliverable:** Broader compatibility list with quality grades.

## Phase 4 — Productization (ongoing)

- Performance optimization (GPU instancing, caching).
- Input/UI polish, save-state integrity checks.
- Mod/profile sharing format.
- Regression suite and CI.

**Deliverable:** Public alpha/beta builds.

## 6) Team + stack recommendation

### Core team (minimum)

- 1 emulator/low-level graphics engineer.
- 1 real-time rendering engineer.
- 1 tools/UI engineer.
- 1 technical artist (part-time) for profile/style tuning.
- 1 QA with emulator testing experience.

### Suggested stack

- C++20 or Rust for core integration.
- Renderer: bgfx, SDL + OpenGL/Vulkan, or wgpu.
- UI/tooling: Dear ImGui.
- Data: JSON/TOML profiles.

## 7) Risks and mitigations

1. **Accuracy regressions**
   - Mitigation: keep original 2D path always available as fallback.

2. **Performance drops**
   - Mitigation: scalable quality levels and dynamic effect toggles.

3. **Game-specific artifacts**
   - Mitigation: profile overrides + compatibility database.

4. **Legal/IP concerns**
   - Mitigation: distribute emulator code + tooling only, no ROM assets.

## 8) MVP definition (first playable milestone)

A realistic MVP:

- 60 FPS in 1080p on mid-tier GPU.
- Works well in one RPG and one platformer.
- Camera tilt ±20° and slight orbit.
- Directional light + shadows + bloom + DOF.
- Per-game profile editor with save/load.

## 9) Practical "start tomorrow" checklist

1. Fork emulator candidate and compile baseline.
2. Add PPU frame capture struct and debug dump.
3. Build external viewer to inspect layers/depth assumptions.
4. Implement plane-stacking renderer with fixed depth table.
5. Add keyboard-controlled camera tilt and screenshot compare tool.
6. Add one lighting pass + one post effect.
7. Evaluate 5 games and document breakpoints.

## 10) Bottom line

You can absolutely build a SNES "HD-2D camera" system, but treat it as a hybrid emulator + renderer product with strong per-game tuning. The fastest path is to ship a curated compatibility list rather than chasing perfect universal support at first.
