import curses

class Page:
    def __init__(self, height, width, pos_y, pos_x):
        self.height = height
        self.width = width
        self.window = curses.newwin(height, width, pos_y, pos_x)
        self.window.keypad(True)
        self.window.box()
        self.heigth, self.width = height, width

    def draw(self):
        raise NotImplementedError()

    def handle_input(self, key):
        return False
