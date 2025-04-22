from core.instructions.instruction_decoder import InstructionDecoder
from application.pages.page import Page
import curses


class MonitorWindow(Page):
    def __init__(self, height, width, pos_y, pos_x, PC, flash):
        super().__init__(height, width, pos_y, pos_x)
        self.PC = PC
        self.flash = flash
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
