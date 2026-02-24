# Spelunky Physics Notes (Design Reference)

These notes capture examples from Spelunky 2 that are useful for our physics design decisions.

## Armored Olmites and Stacking

- In Spelunky 2, Armored Olmites are separate entities with explicit stacking behavior.
- The bottom Olmite acts as the movement leader.
- Olmites above are driven to stay directly on top of the one below.
- Because they are separate entities, they can be knocked off individually.
  - Hitting the middle can drop the upper section while lower section remains.
- Unlike most enemies that phase through each other, Olmites use collision behavior that lets one stand on another as if it were solid ground.
- If separated, their AI can seek nearby Olmites and restack into a totem.
- Camera flash/stun behavior makes this clear: each entity drops current action and the stack disassembles.

## Shield Pushing Behavior

- The shield acts like a moving wall that displaces entities.
- Most enemies/NPCs are pushed backward when contacting the shield front.
- Pushing an entity into solid tiles can crush/kill it.
- Some large/boss entities are immune to shield pushing.

### Natural Pushing (Non-shield Cases)

- Most enemies do not generally push each other in the same way.
- Some attacks/animations can displace entities (context specific).
- Stunned enemies/corpses can be moved by explosions, traps, and moving bodies.

### Shield vs Shield (Multiplayer)

- Two opposing shields can create unstable overlap resolution.
- Mutual displacement can create very high-speed movement/glitchy outcomes.
- Shield pinning can crush a player against solid geometry.

## Implications For Plumber-Py

- Keep enemy-vs-enemy overlap permissive by default for scale and stability.
- Use explicit behavior flags for special cases instead of global mass math:
  - `can_push`
  - `can_be_pushed`
  - `is_kinematic_pusher` (moving-platform style, never slowed by push)
  - `supports_stacking` (Olmite-style opt-in)
- Keep stacking as AI/state logic on top of simple collision, not as a generic rule for all entities.
- Treat shield-like mechanics as explicit gameplay systems with deterministic push/crush rules.
