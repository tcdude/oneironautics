from panda3d.core import CollideMask
from panda3d.core import CollisionNode
from panda3d.core import CollisionSegment
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerQueue
from panda3d.core import BitMask32


def setup_ray(node, traverser, bitmask, point_a=(0,0,1), point_b=(0,0,0)):
    ray = CollisionSegment(point_a, point_b)
    col = CollisionNode(node.getName()+"-ray")
    col.add_solid(ray)
    col.set_from_collide_mask(bitmask)
    col.set_into_collide_mask(CollideMask.all_off())
    col_node = node.attach_new_node(col)
    handler = CollisionHandlerQueue()
    traverser.add_collider(col_node, handler)
    return {"collider":col,"ray":ray,"handler":handler,"node":col_node}


class Player():
    def __init__(self, world):
        self.world = world
        self.root = self.world.root.attach_new_node("player")
        self.pivot = self.root.attach_new_node("player_pivot")
        base.camera.reparent_to(self.pivot)
        base.camera.set_z(1.7)
        base.cam.node().get_lens().set_fov(90)

        self.move_speed = 10
        self.turn_speed = 100

        self.traverser = CollisionTraverser()
        self.ray = setup_ray(
            self.root, self.traverser, self.world.mask,
            (0,0,1), (0,0,-1) # ray ends well below feet to register downward slopes
        )

    def update(self):
        dt = globalClock.get_dt()
        context = base.device_listener.read_context('game')
        head_speed  = -context["movement"].x*self.turn_speed*dt
        walk_speed  = context["movement"].y*self.move_speed*dt
        self.root.set_h(self.root, head_speed)
        self.ray["node"].set_y(self.root, walk_speed)
        self.traverser.traverse(render)
        if self.ray["handler"].get_num_entries() > 0:
            self.ray["handler"].sort_entries()
            closest_entry = list(self.ray["handler"].entries)[0]
            collision_point = closest_entry.get_surface_point(render)
            collision_normal = closest_entry.get_surface_normal(render)
            # take heed of the ray ending well below feet
            collision_point.set_z(max(0,collision_point.z))
            self.root.set_pos(render, collision_point)
            original_heading = self.root.get_h()
            self.root.look_at(render, collision_point, collision_normal)
            self.root.set_h(original_heading)
        else:
            print("can't go that way")