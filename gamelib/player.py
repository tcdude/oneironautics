from panda3d.core import CollideMask
from panda3d.core import CollisionNode
from panda3d.core import CollisionSegment
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerQueue
from panda3d.core import BitMask32
from panda3d.core import KeyboardButton
from panda3d.core import Vec3


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
        self.traverser = CollisionTraverser()
        self.ray = setup_ray(
            self.root, self.traverser, self.world.mask,
            # ray ends well below feet to register downward slopes
            (0,0,1), (0,0,-1)
        )
        self.xyh_inertia = Vec3(0,0,0)
        self.xyh_acceleration = Vec3(0.5,0.5,4.5)
        self.friction = 0.2
        self.torque = 0.5

        base.input.set_mouse_relativity(True)

    def handle_input(self):
        dt = globalClock.get_dt()
        directional_keys = (
            ["strafe_right", "strafe_left"],
            ["forward", "backward"]
        )
        for k, keys in enumerate(directional_keys):
            if base.input.buttons[keys[0]]:
                self.xyh_inertia[k] += self.xyh_acceleration[k]*dt
            elif base.input.buttons[keys[1]]:
                self.xyh_inertia[k] -= self.xyh_acceleration[k]*dt
            self.xyh_inertia[k] /= 1+self.friction

        h = base.input.mouse_movement.x*self.xyh_acceleration[2]*dt
        self.pivot.set_h(self.pivot, h)
        p = base.input.mouse_movement.y*self.xyh_acceleration[2]*dt
        base.cam.set_p(base.cam, p)
        base.cam.set_p(max(-70, min(base.cam.get_p(), 70)))

    def ray_to_destination(self):
        self.ray["node"].set_x(self.pivot, self.xyh_inertia[0])
        self.ray["node"].set_y(self.pivot, self.xyh_inertia[1])

    def move_to_ray(self):
        self.ray["handler"].sort_entries()
        closest_entry = list(self.ray["handler"].entries)[0]
        collision_point = closest_entry.get_surface_point(render)
        collision_normal = closest_entry.get_surface_normal(render)
        # take heed of the ray ending well below feet
        collision_point.set_z(max(0,collision_point.z))
        self.root.set_pos(render, collision_point)
        self.root.look_at(render, collision_point, collision_normal)

    def update(self):
        dt = globalClock.get_dt()
        self.handle_input()
        self.ray_to_destination()
        self.traverser.traverse(render)
        if self.ray["handler"].get_num_entries() > 0:
            self.move_to_ray()
        self.ray["node"].set_y(self.pivot, 0)