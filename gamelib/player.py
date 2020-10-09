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
        base.cam.reparent_to(self.root)
        base.cam.set_z(1.7)
        base.cam.node().get_lens().set_fov(90)

        self.move_speed = 10
        self.turn_speed = 100
        self.heading = 0

        self.traverser = CollisionTraverser()
        self.ray = setup_ray(
            self.root, self.traverser, self.world.mask,
            (0,0,1), (0,0,-1) # ray ends well below feet to register downward slopes
        )

    def update(self, context):
        self.root.set_h(self.root, -context["movement"].x*self.turn_speed*base.dt)
        self.ray["node"].set_y(self.root, context["movement"].y*self.move_speed*base.dt)
        self.traverser.traverse(render)
        if self.ray["handler"].get_num_entries() > 0:
            self.ray["handler"].sort_entries()
            closest_entry = list(self.ray["handler"].entries)[0]
            collision_point = closest_entry.get_surface_point(self.root)
            collision_normal = closest_entry.get_surface_normal(self.root)
            self.root.set_hpr(self.root.get_hpr()-collision_normal)
            #self.root.look_at(render, (0,-1,0))

        else:
            return
            print("something went really wrong, player is off the navmesh")