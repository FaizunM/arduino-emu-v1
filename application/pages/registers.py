import curses


class RegisterWindow:
    def __init__(self, height, width, start_y, start_x, ins_register):
        self.window = curses.newwin(height, width, start_y, start_x)
        self.window.box()
        self.height, self.width = self.window.getmaxyx()

        self.ins_register = ins_register
        self.register_pointer = 0x0

        self.show_register = False

        self.menus = ["General Purpose", "I/O Register"]
        self.menu_highlight = 0x0

        self.selected_menu = None

    def draw(self):
        self.window.erase()
        self.window.box()
        self.window.addstr(0, 2, f"Register Tab ")

        for idx, menu in enumerate(self.menus):
            self.window.addstr(
                idx + 1,
                2,
                f"[{'•' if idx == self.selected_menu else ' '}] {menu} ",
                curses.A_REVERSE if idx == self.menu_highlight else curses.A_BOLD,
            )
            
        self.window.addstr(1, 24, f"-->")

        if self.selected_menu == 0x0:
            for y in range(0 + 1, self.height):
                self.window.addstr(
                    y,
                    30,
                    f"R{(y - 1) + self.register_pointer}  -->  {hex(self.ins_register.get((y - 1) + self.register_pointer))}",
                )

        self.window.noutrefresh()

    def handle_input(self, key):
        if key == ord("\n"):
            self.selected_menu = self.menu_highlight
        elif key == curses.KEY_BACKSPACE:
            if self.selected_menu != None:
                self.selected_menu = None
        elif key == curses.KEY_UP:
            if self.selected_menu == None:
                self.menu_highlight = (self.menu_highlight - 1) % len(self.menus)

            if self.selected_menu != None:
                if self.selected_menu == 0x0:

                    if not self.register_pointer - 1 < 0:
                        self.register_pointer -= 1
        elif key == curses.KEY_DOWN:
            if self.selected_menu == None:
                self.menu_highlight = (self.menu_highlight + 1) % len(self.menus)

            if self.selected_menu != None:
                if self.selected_menu == 0x0:

                    if (
                        not (self.register_pointer + (self.height - 2)) + 1
                        > len(self.ins_register.registers) - 1
                    ):
                        self.register_pointer += 1
        else:
            return False
