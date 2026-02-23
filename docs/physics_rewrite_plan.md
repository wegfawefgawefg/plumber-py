# Physics Rewrite Plan

## Goals
- Replace current collision/position resolution with a simpler, more reliable AABB-based system.
- Keep high-refresh rendering (144Hz+) while using stable fixed-step simulation.
- Remove pinch/teleport artifacts (notably wall-pinch upward snaps).
- Support entity-to-entity pushing using weight.

## Constraints
- Simulation should be deterministic and frame-rate independent.
- Keep existing gameplay code as intact as possible.
- Maintain small, focused modules instead of one large physics file.

## Proposed Runtime Model
- Use fixed simulation ticks with an accumulator:
  - target simulation rate: `60Hz` (`SIM_DT = 1/60`)
  - render loop remains uncapped.
- On each render frame:
  1. Add elapsed real time to accumulator.
  2. Run `while accumulator >= SIM_DT`: execute one simulation step and subtract `SIM_DT`.
  3. Compute interpolation alpha `alpha = accumulator / SIM_DT`.
  4. Render interpolated transform between previous and current physics positions.
- Physics step (per fixed tick):
  1. Integrate velocity from acceleration.
  2. Resolve X movement against tiles.
  3. Resolve X entity overlaps/push.
  4. Resolve Y movement against tiles.
  5. Resolve Y entity overlaps/push.

## Collision Rules
- Tiles are the hard boundary source of truth.
- Axis-separated movement uses sweep-style clamp along the leading edge only.
- Entity push/depenetration uses weight split:
  - Higher weight => less displacement.
  - Lower weight => more displacement.
- If one body cannot move due to tile blocking, remaining correction is shifted to the other body when possible.

## Data & Module Layout
- `src/physics/config.py`: tunables and constants.
- `src/physics/time_step.py`: fixed-step accumulator helpers.
- `src/physics/tile_solver.py`: tile sweep clamps and world-bound handling.
- `src/physics/entity_solver.py`: pair overlap detection, weight-based depenetration, push resolution.
- `src/physics/solver.py`: substep orchestration and integration pipeline.

## Integration Changes
- `main.py`: uncapped clock tick + fixed-step accumulator loop.
- `state.py`: track previous/current transform for interpolation render.
- `systems/physics.py`: delegate to new solver modules.
- Keep gameplay timers in simulation ticks (no variable dt conversion needed):
  - coyote timer
  - AI timers
  - alert/message lifetimes
  - sprite animation countdowns
- `render.py`: interpolate entity positions using `alpha` to avoid visual chunking at 144Hz.

## Validation Plan
- Reproduce prior goombor wall-pinch setup and confirm no vertical teleport.
- Ensure player/goombor still collide and push meaningfully by weight.
- Quick checks:
  - movement feel at low and high FPS
  - no obvious tunneling at normal speeds
  - no frequent jitter in resting contact

## Risks
- 60Hz simulation can still show slight motion quantization without interpolation.
- Interpolation needs careful handling for camera + one-frame events to avoid visual mismatch.
- Pair depenetration may need small tuning (iteration count, epsilon, push split).
