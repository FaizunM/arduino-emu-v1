from core.instructions.instruction_decoder import InstructionDecoder
from application.pages.page import Page
import curses


class MonitorWindow(Page):
    def __init__(self, height, width, pos_y, pos_x, PC, flash, DMEM):
        super().__init__(height, width, pos_y, pos_x)
        self.PC = PC
        self.flash = flash
        self.DMEM = DMEM
        self.address_pointer = 0x0
        self.height = height - 1
        self.decoder: InstructionDecoder = InstructionDecoder(DefinitionMode=True)

    def draw(self):
        self.window.erase()
        self.window.box()
        self.window.addstr(0, 2, f"Monitor Tab ")
        self.window.addstr(1, 7, f"ADDRESS")
        self.window.addstr(1, 17, f"OPCODE")
        
        for num_line in range(0 + 3, self.height):
            if (self.address_pointer + (num_line - 3)) > 0x7FFF:
                self.address_pointer = 0
            self.window.addstr(
                num_line,
                2,
                (
                    f"-->"
                    if self.address_pointer + (num_line - 3) == self.PC.address
                    else "    "
                ),
            )
            self.window.addstr(
                num_line,
                7,
                f"{format(self.address_pointer + (num_line - 3), 'X').zfill(8)}",
            )
            self.window.addstr(num_line, 58, f"->")
            hexval = format(
                self.flash.get(self.address_pointer + (num_line - 3)), "b"
            ).zfill(32)
            self.window.addstr(
                num_line,
                17,
                f"{' '.join(hexval[i : i + 4] for i in range(0, len(hexval), 4))}",
            )
            self.window.addstr(
                num_line,
                62,
                f"{self.decoder.decode(self.flash.get(self.address_pointer + (num_line - 3)))}",
            )

        self.PC.draw_debug(self.window)
        
        self.window.addstr(3, 84, f'Stack Pointer --> {self.DMEM.get_SP()}')
        
        self.window.addstr(4, 84, str(self.DMEM.get_SREG('I')))
        self.window.addstr(5, 84, f'I')
        self.window.addstr(4, 86, str(self.DMEM.get_SREG('T')))
        self.window.addstr(5, 86, f'T')
        self.window.addstr(4, 88, str(self.DMEM.get_SREG('H')))
        self.window.addstr(5, 88, f'H')
        self.window.addstr(4, 90, str(self.DMEM.get_SREG('S')))
        self.window.addstr(5, 90, f'S')
        self.window.addstr(4, 92, str(self.DMEM.get_SREG('V')))
        self.window.addstr(5, 92, f'V')
        self.window.addstr(4, 94, str(self.DMEM.get_SREG('N')))
        self.window.addstr(5, 94, f'N')
        self.window.addstr(4, 96, str(self.DMEM.get_SREG('Z')))
        self.window.addstr(5, 96, f'Z')
        self.window.addstr(4, 98, str(self.DMEM.get_SREG('C')))
        self.window.addstr(5, 98, f'C')
        
        for i in range(0, 16):
            self.window.addstr(7, 84 + i * 3, f"{format(self.DMEM.get(i), 'X')}")
            
        for i in range(0, 16):
            self.window.addstr(8, 84 + i * 3, f"{format(self.DMEM.get(16 + i), 'X')}")
            
        self.window.noutrefresh()

    def handle_input(self, key):
        if key == curses.KEY_UP:
            if not self.address_pointer - 1 < 0:
                self.address_pointer -= 1
            else:
                self.address_pointer = len(self.flash.memory) - (self.height - 3)
                
        elif key == curses.KEY_DOWN:
            if (
                not (self.address_pointer + self.height - 4) + 1
                > len(self.flash.memory) - 1
            ):
                self.address_pointer += 1
            else:
                self.address_pointer = 0
        elif key == ord("c"):
            self.address_pointer = self.PC.address

            self.PC.cycle()
        else:
            return False
