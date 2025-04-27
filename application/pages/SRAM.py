from application.pages.page import Page
from application.hexdump import HexDump
import curses


class SRAMWindow(Page):
    def __init__(self, height, width, pos_y, pos_x, DMEM):
        super().__init__(height, width, pos_y, pos_x)
        self.DMEM = DMEM

        self.address_pointer = 0x0
        self.height, self.width = self.window.getmaxyx()
        
        self.hex_dump = HexDump(self.DMEM.map_address)
        self.section = ''

    def draw(self):

        self.window.erase()
        self.window.box()
        self.window.addstr(0, 2, f"SRAM Tab ")
        
        if (self.address_pointer * 4) >= 0x0000 and (self.address_pointer * 4) <= 0x001F:
            self.section = 'GPR'
        if (self.address_pointer * 4) >= 0x0020 and (self.address_pointer * 4) <= 0x005F:
            self.section = 'I/O Register'
        if (self.address_pointer * 4) >= 0x0060 and (self.address_pointer * 4) <= 0x00FF:
            self.section = 'Ext I/O Register'
        if (self.address_pointer * 4) >= 0x0100 and (self.address_pointer * 4) <= 0x08FF:
            self.section = 'Internal SRAM'
    
        self.window.addstr(1, (self.width // 2) + 30, f"Section --> {str(self.section)}")

        self.hex_dump.dump(self.window, self.address_pointer, self.height)
        self.window.noutrefresh()

    def handle_input(self, key):
        if key == ord('1'):
            self.address_pointer = 0x0000
        elif key == ord('2'):
            self.address_pointer = 0x0020
        elif key == ord('3'):
            self.address_pointer = 0x0060
        elif key == curses.KEY_UP:
            if not self.address_pointer - 1 < 0:
                self.address_pointer -= 1
            else:
                self.address_pointer = ((0x8FF) // 4) - (self.height)
        elif key == curses.KEY_DOWN:
            if not (self.address_pointer + 1) * 4 > ((0x8FF) // 4) + self.height:
                self.address_pointer += 1
            else:
                self.address_pointer = 0
        else:
            return False
