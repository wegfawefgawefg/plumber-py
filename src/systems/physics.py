import glm

from tiles import TILE_SIZE, collidable_tile_in_list


def zero_accelerations(state):
    for e in state.entities:
        e.acc = glm.vec2(0, 0)


MAX_SPEED = 9.0


def physics_post_step(state):
    for e in state.entities:
        e.vel += e.acc

        # clamp
        if e.vel.x > MAX_SPEED:
            e.vel.x = MAX_SPEED
        elif e.vel.x < -MAX_SPEED:
            e.vel.x = -MAX_SPEED
        if e.vel.y > MAX_SPEED:
            e.vel.y = MAX_SPEED
        elif e.vel.y < -MAX_SPEED:
            e.vel.y = -MAX_SPEED

        # tile collisions

        e.pos += e.vel


GRAVITY = 0.01


def gravity(state):
    for e in state.entities:
        e.acc.y += GRAVITY


# pub fn set_grounded(ecs: &mut World, state: &State) {
#     // remove grounded from all entities with it
#     let currently_grounded: Vec<Entity> = ecs
#         .query::<&Grounded>()
#         .iter()
#         .map(|(entity, _)| entity)
#         .collect();
#     for entity in currently_grounded {
#         let _ = ecs.remove_one::<Grounded>(entity);
#     }
#     ecs.flush();

#     // find who is grounded
#     let mut newly_grounded: Vec<Entity> = vec![];
#     for (entity, (ctransform, shape)) in ecs.query::<(&CTransform, &Shape)>().iter() {
#         let (feet_tl, feet_br) = get_entity_feet(ctransform.pos, shape.size);

#         // check stage floor
#         if feet_br.y >= state.stage.get_height() as i32 {
#             newly_grounded.push(entity);
#             continue;
#         }

#         // get tiles in player bounds
#         let feet_tl_tile_pos = feet_tl / Tile::SIZE as i32;
#         let feet_br_tile_pos = feet_br / Tile::SIZE as i32;
#         let tiles_at_feet = state
#             .stage
#             .get_tiles_in_rect(&feet_tl_tile_pos, &feet_br_tile_pos);
#         let collided = collidable_tile_in_list(&tiles_at_feet);
#         if collided {
#             newly_grounded.push(entity);
#         }
#     }

#     // set grounded for grounded entities
#     for entity in newly_grounded {
#         let _ = ecs.insert(entity, (Grounded,));
#     }

#     for (_, physics) in ecs.query::<&mut Physics>().with::<&Grounded>().iter() {
#         physics.vel.y = 0.0;
#     }
# }


def set_grounded(state):
    # clear grounded
    for e in state.entities:
        e.grounded = False

    # find who is grounded
    for e in state.entities:
        feet_tl = e.pos
        feet_br = e.pos + e.size

        # check stage floor
        if feet_br.y >= state.stage.dims.y:
            e.grounded = True
            continue

        # get tiles in player bounds
        feet_tl_tile_pos = feet_tl / TILE_SIZE
        feet_br_tile_pos = feet_br / TILE_SIZE
        tiles_at_feet = state.stage.get_tiles_in_rect(
            feet_tl_tile_pos, feet_br_tile_pos
        )
        collided = collidable_tile_in_list(tiles_at_feet)
        if collided:
            e.grounded = True
            e.vel.y = 0.0
            print("grounded")
