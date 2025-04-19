from core.instructions.instruction_register import InstructionRegister
from core.memory.sram import SRAM
from core.instructions.status_register import StatusRegister


class ALU:
    def __init__(self, ins_register, sram):
        self.sram: SRAM = sram
        self.ins_register: InstructionRegister = ins_register
        self.SREG: StatusRegister = StatusRegister()

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

    def LDI(self, destination: int, value: int):
        self.ins_register.set(destination, value)
