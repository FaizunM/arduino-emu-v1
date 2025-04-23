from core.memory.flash import Flash
from core.instructions.instruction_decoder import InstructionDecoder


class ProgramCounter:
    def __init__(self, flash: Flash, ins_register, SRAM, SREG):
        self.address = 0x0
        self.flash: Flash = flash
        self.ins_decoder = InstructionDecoder(ins_register, SRAM, self, SREG, DefinitionMode=False)
        self.Debug = ''


    def cycle(self):

        try:
            self.ins_decoder.decode(self.flash.get(self.address))
        except Exception as e:
            self.Debug = str(e)
                
    def draw_debug(self, stdscr):
        height, width = stdscr.getmaxyx()
        stdscr.addstr(1, width // 2, f"DEBUG -> {self.Debug}")