# Repository Agent Notes

## Code Organization Preferences
- Keep source files in the 300-500 line range when practical.
- Avoid mega-files; split large systems into focused modules.
- Group code by responsibility so related behavior lives together.
- Prefer clear boundaries between orchestration, data/model types, and mechanics.

## Physics Direction
- Prioritize simple, readable platformer physics over rigid-body complexity.
- Keep collision behavior deterministic and debuggable.
- Prefer explicit rules (tiles first, then entity interactions) over implicit side effects.
