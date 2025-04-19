from core.memory.flash import Flash
from core.program_counter import ProgramCounter


class Monitor:
    def __init__(self, flash: Flash, PC: ProgramCounter):
        self.PC: ProgramCounter = PC
        self.flash: Flash = flash

    def show(self):
        offsett = self.PC.address // 8
        print(f"On Process: {format(self.flash.get(self.PC.address), 'b').zfill(16)}")

        if self.PC.address > self.PC.address + 32:
            raise "Out of memory"
        print("\n      ADDRESS     -->  ", end="")
        for i in range(0, 16):
            print(format(i, "X").zfill(2), end=" ")
        print("")
        print("                       ", end="")
        for i in range(0, 8):
            print(
                f"{'__ __' if (self.PC.address % 8) == i else ''}",
                end="      ",
            )
        print("")

        for y in range(0 + (offsett * 8), 32 + (offsett * 8), 8):
            addrs = format(y, "X").zfill(8)

            print(
                f"{' --> ' if y in range((self.PC.address - 8), (self.PC.address - 8) + 8) or y == 0 + (offsett * 8) else '     '} 0x{addrs}  -->  ",
                end="",
            )
            for x in range(y, y + 8):
                try:
                    hexval = format(self.flash.get(x), "X").zfill(4)
                    print(hexval[2:], end=" ")
                    print(hexval[:2], end=" ")
                except:
                    print("      ", end="")
            print("")
