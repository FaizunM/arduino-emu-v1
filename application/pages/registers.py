import curses

class GPRWindow:
    def __init__(self, height, width, start_y, start_x):
        self.window = curses.newwin(height, width, start_y, start_x)
        self.window.box()
        self.heigth, self.width = height, width

    def draw(self):
        self.window.clear()
        self.window.box()
        self.window.addstr(0, 2, f"General Purpose Register Tab ")
        self.window.refresh()