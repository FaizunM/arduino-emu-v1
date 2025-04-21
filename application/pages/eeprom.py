from application.pages.page import Page
from application.hexdump import HexDump
import curses


class EEPROMWindow(Page):
    def __init__(self, height, width, pos_y, pos_x, EEPROM):
        super().__init__(height, width, pos_y, pos_x)
        self.EEPROM = EEPROM

        self.address_pointer = 0x0

        self.hex_dump = HexDump(self.EEPROM.memory)

    def draw(self):

        self.window.erase()
        self.window.box()
        self.window.addstr(0, 2, f"EEPROM Tab ")

        self.hex_dump.dump(self.window, self.address_pointer, self.height)
        self.window.noutrefresh()

    def handle_input(self, key):
        if key == curses.KEY_UP:
            if not self.address_pointer - 1 < 0:
                self.address_pointer -= 1
        elif key == curses.KEY_DOWN:
            self.address_pointer += 1
        else:
            return False
