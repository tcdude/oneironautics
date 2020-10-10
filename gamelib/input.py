from panda3d.core import WindowProperties
from panda3d.core import KeyboardButton
from panda3d.core import Vec2


class Input():
    def __init__(self):
        self.relative = False
        self.mouse_movement = Vec2(0, 0)
        self.sensitivity = Vec2(100,75)
        self.window_properties = WindowProperties()

        ascii = KeyboardButton.ascii_key
        self.binds = {
            "forward": ascii("w"),
            "backward": ascii("s"),
            "strafe_left": ascii("a"),
            "strafe_right": ascii("d"),
        }
        self.buttons = {}
        for key in self.binds:
            self.buttons[key] = 0

        base.taskMgr.add(self.update)

    def set_mouse_relativity(self, relative=True):
        self.relative = relative
        self.window_properties.setCursorHidden(relative)
        base.win.requestProperties(self.window_properties)

    def update(self, task):
        is_down = base.mouseWatcherNode.is_button_down
        for button in self.buttons:
            if is_down(self.binds[button]):
                self.buttons[button] = 1 # key held down
            elif self.buttons[button] == 1:
                self.buttons[button] = 2 # key release
            else:
                self.buttons[button] = 0 # key inactive

        if base.mouseWatcherNode.has_mouse():
            if self.relative:
                self.mouse_movement.x = -base.mouseWatcherNode.get_mouse_x()*self.sensitivity.x*50
                self.mouse_movement.y = base.mouseWatcherNode.get_mouse_y()*self.sensitivity.y*50
                base.win.move_pointer(0, base.win.get_x_size() // 2, base.win.get_y_size() // 2)
            else:
                self.mouse_movement.x = base.mouseWatcherNode.get_mouse_x()
                self.mouse_movement.y = base.mouseWatcherNode.get_mouse_y()
        return task.cont
