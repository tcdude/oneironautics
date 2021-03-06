from panda3d.core import ConfigVariableDouble
from panda3d.core import CollideMask
from panda3d.core import CollisionNode
from panda3d.core import CollisionSegment
from panda3d.core import CollisionSphere
from panda3d.core import CollisionTraverser
from panda3d.core import CollisionHandlerEvent
from panda3d.core import CollisionHandlerQueue
from panda3d.core import Vec3


ROTATION_SPEED = 2


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
        self.root_target = self.world.root.attach_new_node("player_target")
        self.pivot = self.root.attach_new_node("player_pivot")
        base.camera.reparent_to(self.pivot)
        base.camera.set_z(1.7)
        base.cam.node().get_lens().set_fov(90)
        self.traverser = CollisionTraverser()
        self.ray = setup_ray(
            self.pivot, self.traverser, self.world.mask,
            # ray ends well below feet to register downward slopes
            (0,0,1), (0,0,-1)
        )
        self.xyh_inertia = Vec3(0,0,0)
        h_acc = ConfigVariableDouble('mouse-accelleration', 0.1).get_value()
        self.xyh_acceleration = Vec3(0.8,0.8,h_acc)
        self.friction = 0.15
        self.torque = 0.5
        self.last_up = Vec3(0, 0, 1)

        # Collider for portals
        csphere = CollisionSphere(0, 0, 1.25, 1.5)
        cnode = CollisionNode('player')
        cnode.add_solid(csphere)
        cnode.set_from_collide_mask(0x2)
        cnode.set_into_collide_mask(CollideMask.all_off())
        self.collider = self.root.attach_new_node(cnode)
        self.event_handler = CollisionHandlerEvent()
        self.event_handler.add_in_pattern('into-%in')
        self.traverser.add_collider(self.collider, self.event_handler)
        self.collider.show()
        self.teleported = False

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

        if base.mouseWatcherNode.hasMouse():
            h = base.input.mouse_movement.x*self.xyh_acceleration[2]*dt
            self.pivot.set_h(self.pivot, h)
            p = base.input.mouse_movement.y*self.xyh_acceleration[2]*dt
            base.cam.set_p(base.cam, p)
            base.cam.set_p(max(-70, min(base.cam.get_p(), 70)))
            #base.cam.set_r(0)

    def ray_to_destination(self, xonly=0):
        if xonly:
            self.ray["node"].set_x(self.pivot, self.xyh_inertia[1] * xonly)
            self.ray["node"].set_y(self.pivot, 0)
        else:
            self.ray["node"].set_x(self.pivot, self.xyh_inertia[0])
            self.ray["node"].set_y(self.pivot, self.xyh_inertia[1])

    def move_to_ray(self):
        self.ray["handler"].sort_entries()
        #closest_entry = list(self.ray["handler"].entries)[0]
        closest_entry = None
        delta = float('inf')
        dot = -1.0
        for c in list(self.ray["handler"].entries):
            if closest_entry is None:
                closest_entry = c
                delta = c.get_surface_point(self.root).length()
                dot = self.last_up.dot(c.get_surface_normal(render))
                continue
            if c.get_surface_point(self.root).length() < delta:
                if self.last_up.dot(c.get_surface_normal(render)) > dot:
                    closest_entry = c
                    dot = self.last_up.dot(c.get_surface_normal(render))
                    delta = c.get_surface_point(self.root).length()

        collision_point = closest_entry.get_surface_point(render)
        collision_normal = closest_entry.get_surface_normal(render)
        self.last_up = collision_normal
        # take heed of the ray ending well below feet
        #collision_point.set_z(max(0,collision_point.z))
        self.root.set_pos(render, collision_point)
        self.root_target.set_pos(render, collision_point)
        self.root_target.heads_up(render, collision_point, collision_normal)

    def update(self):
        if self.teleported:
            self.xyh_inertia = Vec3(0, self.xyh_acceleration[1], 0)
            self.teleported = False
        dt = globalClock.get_dt()
        self.handle_input()
        if self.xyh_inertia.length() > 0:
            self.ray_to_destination()
            self.traverser.traverse(render)
            if self.ray["handler"].get_num_entries() > 0:
                self.move_to_ray()
            else:
                self.ray_to_destination(-1)
                self.traverser.traverse(render)
                if self.ray["handler"].get_num_entries() > 0:
                    self.move_to_ray()
                else:
                    self.ray_to_destination(1)
                    self.traverser.traverse(render)
                    if self.ray["handler"].get_num_entries() > 0:
                        self.move_to_ray()
            self.ray["node"].set_y(self.pivot, 0)
        current_quat = self.root.get_quat()
        target_quat = self.root_target.get_quat()
        current_quat.normalize()
        target_quat.normalize()
        if current_quat.is_same_direction(target_quat):
            self.root.set_quat(target_quat)
            return
        self.root.set_quat(current_quat + (target_quat - current_quat) * (ROTATION_SPEED * dt))
