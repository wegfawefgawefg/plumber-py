from entity import EntityType

# Keep 60Hz simulation so existing movement tuning remains stable.
SIMULATION_HZ = 60.0
MAX_FRAME_TIME_SECONDS = 0.25
MAX_SIM_STEPS_PER_FRAME = 8

# Motion subdivision within a fixed simulation tick.
MAX_MOTION_PER_SUBSTEP = 4.0
MAX_SUBSTEPS_PER_TICK = 8
MIN_SUBSTEPS_PER_TICK = 1

MAX_SPEED = 9.0
GRAVITY = 0.3

ENTITY_DEPENETRATION_ITERATIONS = 4
POSITION_EPSILON = 0.001

DEFAULT_ENTITY_WEIGHT = 4.0
ENTITY_WEIGHTS = {
    EntityType.PLAYER: 5.0,
    EntityType.GOOMBA: 3.0,
    EntityType.GOOMBINI: 2.0,
    EntityType.GOOMBOR: 7.0,
}
