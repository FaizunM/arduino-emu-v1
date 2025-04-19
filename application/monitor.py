from core.memory.flash import Flash
from core.program_counter import ProgramCounter
from core.instructions.instruction_decoder import InstructionDecoder


class Monitor:
    def __init__(self, flash: Flash, PC: ProgramCounter):
        self.PC: ProgramCounter = PC
        self.flash: Flash = flash
        self.Decoder: InstructionDecoder = InstructionDecoder()

    def show(self):
        print(f"On Process: {format(self.flash.get(self.PC.address), 'b').zfill(16)}")

        if self.PC.address > self.PC.address + 32:
            raise "Out of memory"
        print("\n      ADDRESS     -->  OPCODE            -->  Definition\n")

        for y in range(0 + self.PC.address, 5 + self.PC.address):
            addrs = format(y, "X").zfill(8)

            print(
                f"{' --> 'if self.PC.address == y else '     '} 0x{addrs}  -->  ",
                end="",
            )
            hexval = format(self.flash.get(y), "b").zfill(16)
            print(hexval, end="")
            try:
                definition = self.Decoder.decode(self.flash.get(y), True)
                print(f"  -->  {definition}")
            except Exception as e:
                print(f"  -->  {e}")
