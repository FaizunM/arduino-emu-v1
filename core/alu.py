from core.instructions.instruction_register import InstructionRegister
from core.memory.sram import SRAM
from core.instructions.status_register import StatusRegister
from core.instructions.stack_pointer import StackPointer


class ALU:
    def __init__(self, ins_register, sram, prog_counter):
        self.sram: SRAM = sram
        self.ins_register: InstructionRegister = ins_register
        self.SREG: StatusRegister = StatusRegister()
        self.PC = prog_counter

    def ADC(self, destination: int, source: int):
        dest = self.ins_register.get(destination)
        src = self.ins_register.get(source)
        real_result = dest + src + self.SREG.status["C"]
        result = real_result & 0xFF

        H = 1 if ((dest & 0x0F) + (src & 0x0F) + self.SREG.status["C"]) > 0x0F else 0
        S = self.SREG.status["N"] ^ self.SREG.status["V"]

        Rd7 = (dest >> 7) & 0b1
        Rr7 = (source >> 7) & 0b1
        R7 = (result >> 7) & 0b1
        V = (Rd7 & Rr7 & ~R7) | (~Rd7 & ~Rr7 & R7)

        N = R7
        Z = 0 if result != 0 else 1

        C = 1 if real_result > 0xFF else 0

        self.SREG.status["H"] = H
        self.SREG.status["V"] = V
        self.SREG.status["N"] = N
        self.SREG.status["S"] = S
        self.SREG.status["Z"] = Z
        self.SREG.status["C"] = C

        self.ins_register.set(destination, result)
        self.PC.address += 1

    def ADD(self, destination: int, source: int):
        dest = self.ins_register.get(destination)
        src = self.ins_register.get(source)
        real_result = dest + src
        result = real_result & 0xFF

        Rd3 = (dest >> 3) & 1
        Rr3 = (src >> 3) & 1
        R3 = (result >> 3) & 1
        H = (Rd3 & Rr3) | (Rr3 & ~R3) | (R3 & ~Rd3)

        Rd7 = (dest >> 7) & 1
        Rr7 = (src >> 7) & 1
        R7 = (result >> 7) & 1
        V = (Rd7 & Rr7 & ~R7) | (~Rd7 & ~Rr7 & R7)
        N = R7
        S = N ^ V
        Z = 1 if result == 0 else 0
        C = 1 if real_result > 0xFF else 0

        self.SREG.status["H"] = H
        self.SREG.status["V"] = V
        self.SREG.status["N"] = N
        self.SREG.status["S"] = S
        self.SREG.status["Z"] = Z
        self.SREG.status["C"] = C

        self.ins_register.set(destination, result)
        self.PC.address += 1

    def SUB(self, destination: int, source: int):
        dest = self.ins_register.get(destination)
        src = self.ins_register.get(source)
        real_result = dest - src
        result = real_result & 0xFF

        Rd3 = (dest >> 3) & 1
        Rr3 = (src >> 3) & 1
        R3 = (result >> 3) & 1
        H = (Rd3 & Rr3) | (Rr3 & ~R3) | (R3 & ~Rd3)

        Rd7 = (dest >> 7) & 1
        Rr7 = (src >> 7) & 1
        R7 = (result >> 7) & 1
        V = (Rd7 & Rr7 & ~R7) | (~Rd7 & ~Rr7 & R7)
        N = R7
        S = N ^ V
        Z = 1 if result == 0 else 0
        C = 1 if real_result > 0xFF else 0

        self.SREG.status["H"] = H
        self.SREG.status["V"] = V
        self.SREG.status["N"] = N
        self.SREG.status["S"] = S
        self.SREG.status["Z"] = Z
        self.SREG.status["C"] = C
        self.ins_register.set(destination, result)
        self.PC.address += 1

    def SBC(self, destination: int, source: int):
        dest = self.ins_register.get(destination)
        src = self.ins_register.get(source)
        real_result = dest + src - self.SREG.status["C"]
        result = real_result & 0xFF

        H = 1 if ((dest & 0x0F) + (src & 0x0F) + self.SREG.status["C"]) > 0x0F else 0
        S = self.SREG.status["N"] ^ self.SREG.status["V"]

        Rd7 = (dest >> 7) & 0b1
        Rr7 = (source >> 7) & 0b1
        R7 = (result >> 7) & 0b1
        V = (Rd7 & Rr7 & ~R7) | (~Rd7 & ~Rr7 & R7)

        N = R7
        Z = 0 if result != 0 else 1

        C = 1 if real_result > 0xFF else 0

        self.SREG.status["H"] = H
        self.SREG.status["V"] = V
        self.SREG.status["N"] = N
        self.SREG.status["S"] = S
        self.SREG.status["Z"] = Z
        self.SREG.status["C"] = C
        self.PC.address += 1

    def LDI(self, destination: int, value: int):
        self.ins_register.set(destination, value)
        self.PC.address += 1

    def JMP(self, destination: int):
        self.PC.address = destination

    def MOV(self, destination, source):
        value = self.ins_register.get(source)
        self.sram.set(destination, value)
        self.PC.address += 1

    def OR(self, destination, source):
        dest_val = self.ins_register.get(destination)
        src_val = self.ins_register.get(source)
        result = dest_val | src_val
        self.ins_register.set(destination, result)
        self.PC.address += 1

    def AND(self, destination, source):
        dest_val = self.ins_register.get(destination)
        src_val = self.ins_register.get(source)
        result = dest_val & src_val
        self.ins_register.set(destination, result)
        self.PC.address += 1

    def OUT(self, destination, source):
        value = self.ins_register.get(source)
        self.sram.set(destination, value)
        self.PC.address += 1

    def CALL(self, destination):
        SPL = self.sram.get(0x3D)
        SPH = self.sram.get(0x3E)
        SP = int("".join([format(SPH, "X"), format(SPL, "X")]), 16)

        SP = SP - 1
        self.sram.set(SP, self.PC.address + 1)
        self.PC.address = destination
        hex_string = format(SP, "X").zfill(4)

        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))

    def RET(self):
        SPL = self.sram.get(0x3D)
        SPH = self.sram.get(0x3E)
        SP = int("".join([format(SPH, "X"), format(SPL, "X")]), 16)

        address = self.sram.get(SP)
        SP = SP + 1

        self.PC.address = address

        hex_string = format(SP, "X").zfill(4)
        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))

    def RJMP(self, destination):
        self.PC.address = self.PC.address + destination + 1

    def IN(self, destination, source):
        value = self.sram.get(source)

        self.ins_register.set(destination, value)
        self.PC.address += 1

    def PUSH(self, source):
        SPL = self.sram.get(0x3D)
        SPH = self.sram.get(0x3E)
        SP = int("".join([format(SPH, "X"), format(SPL, "X")]), 16)

        SP = SP - 1
        value = self.ins_register.get(source)
        self.sram.set(SP, value)

        hex_string = format(SP, "X").zfill(4)

        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))

        self.PC.address += 1

    def POP(self, destination):
        SPL = self.sram.get(0x3D)
        SPH = self.sram.get(0x3E)
        SP = int("".join([format(SPH, "X"), format(SPL, "X")]), 16)

        SP = SP + 1
        value = self.sram.get(SP)

        self.ins_register.set(destination, value)

        hex_string = format(SP, "X").zfill(4)
        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))
        self.PC.address += 1

    def STS(self, destination, source):
        value = self.ins_register.get(source)
        
        self.sram.set(destination, value)
        self.PC.address += 1

    def LDS(self, destination, source):
        value = self.sram.get(source)
        self.ins_register.set(destination, value)
        self.PC.address += 1
        