from core.memory.flash import Flash
from core.instructions.instruction_decoder import InstructionDecoder


class ProgramCounter:
    def __init__(self, flash: Flash, ins_register, SRAM):
        self.address = 0x0
        self.flash: Flash = flash
        self.ins_decoder = InstructionDecoder(ins_register, SRAM, self)

    def cycle(self):

        try:
            self.ins_decoder.decode(self.flash.get(self.address))
        except Exception as e:
            print(f"DECODER FAIL -> {str(e)}")
        finally:
            self.address += 1
