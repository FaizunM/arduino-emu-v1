import curses


class RegisterWindow:
    def __init__(self, height, width, start_y, start_x, DMEM):
        self.window = curses.newwin(height, width, start_y, start_x)
        self.window.box()
        self.height, self.width = self.window.getmaxyx()

        self.DMEM = DMEM
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
                if y >= 31:
                    continue
                self.window.addstr(
                    y,
                    30,
                    f"R{(y - 1) + self.register_pointer}  -->  {hex(self.DMEM.get((y - 1) + self.register_pointer))}",
                )
        if self.selected_menu == 0x1:
            self.window.addstr(1, 30, f"[ 7 ] I  -->  {self.DMEM.get_SREG('I')}")
            self.window.addstr(2, 30, f"[ 6 ] T  -->  {self.DMEM.get_SREG('T')}")
            self.window.addstr(3, 30, f"[ 5 ] H  -->  {self.DMEM.get_SREG('H')}")
            self.window.addstr(4, 30, f"[ 4 ] S  -->  {self.DMEM.get_SREG('S')}")
            self.window.addstr(5, 30, f"[ 3 ] V  -->  {self.DMEM.get_SREG('V')}")
            self.window.addstr(6, 30, f"[ 2 ] N  -->  {self.DMEM.get_SREG('N')}")
            self.window.addstr(7, 30, f"[ 1 ] Z  -->  {self.DMEM.get_SREG('Z')}")
            self.window.addstr(8, 30, f"[ 0 ] C  -->  {self.DMEM.get_SREG('C')}")

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
                        > len(self.DMEM.get_INS_REG()) - 1
                    ):
                        self.register_pointer += 1
        else:
            return False
