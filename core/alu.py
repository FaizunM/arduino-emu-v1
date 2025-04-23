from core.instructions.instruction_register import InstructionRegister
from core.memory.sram import SRAM
from core.instructions.status_register import StatusRegister


class ALU:
    def __init__(self, ins_register, sram, prog_counter, SREG):
        self.sram: SRAM = sram
        self.ins_register: InstructionRegister = ins_register
        self.SREG: StatusRegister = SREG
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

    def SBCI(self, destination: int, source: int):
        dest = self.ins_register.get(destination)
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

        hex_string = format(SP, "X").zfill(4)
        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))
        self.PC.address = address

    def RJMP(self, destination):
        self.PC.address = (self.PC.address + 1) + destination

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

    def ADIW(self, destination, source):
        HIGH = format(self.ins_register.get(destination), "X")
        LOW = format(self.ins_register.get(destination + 1), "X")

        value = int(f"{HIGH}{LOW}", 16)

        result = format(value + source, "X").zfill(16)
        self.ins_register.set(destination, int(result[:8], 16))
        self.ins_register.set(destination + 1, int(result[8:], 16))
        self.PC.address += 1

    def ANDI(self, destination: int, source: int):
        dest_val = self.ins_register.get(destination)
        result = dest_val & source

        self.ins_register.set(destination, result)
        self.PC.address += 1

    def SEI(self):
        self.SREG.status["I"] = 1
        self.PC.address += 1

    def ORI(self, destination, source):
        dest_val = self.ins_register.get(destination)
        result = dest_val | source
        self.ins_register.set(destination, result)
        self.PC.address += 1

    def ASR(self, destination):
        value = self.ins_register.get(destination)
        ML = value & 0b1

        shift = value >> 1
        self.ins_register.set(destination, shift)
        self.SREG.status["C"] = ML
        self.PC.address += 1

    def BCLR(self, flag):
        if flag == 0:
            self.SREG.status["C"] = 0
        if flag == 1:
            self.SREG.status["Z"] = 0
        if flag == 2:
            self.SREG.status["N"] = 0
        if flag == 3:
            self.SREG.status["V"] = 0
        if flag == 4:
            self.SREG.status["S"] = 0
        if flag == 5:
            self.SREG.status["H"] = 0
        if flag == 6:
            self.SREG.status["T"] = 0
        if flag == 7:
            self.SREG.status["I"] = 0

        self.PC.address += 1

    def BST(self, destination, pos):
        value = self.ins_register.get(destination)

        T = (value >> pos) & 1
        self.SREG.status["T"] = T
        self.PC.address += 1

    def BLD(self, destination, pos):
        T = self.SREG.status["T"]

        value = self.ins_register.get(destination)

        if T:
            value != (1 << pos)
            self.ins_register.set(destination, value)
        else:
            value &= ~(1 << pos)
            self.ins_register.set(destination, value)
        self.PC.address += 1

    def BRBC(self, destination, offset):
        state = list(self.SREG.status.values())[destination]

        if state == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRBS(self, destination, offset):
        state = list(self.SREG.status.values())[destination]

        if state == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRCC(self, offset):
        C = self.SREG.status["C"]

        if C == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRCS(self, offset):
        C = self.SREG.status["C"]

        if C == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BREAK(self):
        self.PC.address += 1

    def NOP(self):
        raise ValueError("System Finished")

    def BREQ(self, offset):
        Z = self.SREG.status["Z"]

        if Z == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRGE(self, offset):
        N = self.SREG.status["N"]
        V = self.SREG.status["V"]
        S = N ^ V

        if S == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRHC(self, offset):
        H = self.SREG.status["H"]

        if H == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRHS(self, offset):
        H = self.SREG.status["H"]

        if H == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRID(self, offset):
        I = self.SREG.status["I"]

        if I == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRIE(self, offset):
        I = self.SREG.status["I"]

        if I == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRLO(self, offset):
        C = self.SREG.status["C"]

        if C == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRLT(self, offset):
        N = self.SREG.status["N"]
        V = self.SREG.status["V"]
        S = N ^ V

        if S == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRMI(self, offset):
        N = self.SREG.status["N"]

        if N == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRNE(self, offset):
        Z = self.SREG.status["Z"]

        if Z == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRPL(self, offset):
        N = self.SREG.status["N"]

        if N == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRSH(self, offset):
        C = self.SREG.status["C"]

        if C == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRTC(self, offset):
        T = self.SREG.status["T"]

        if T == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRTS(self, offset):
        T = self.SREG.status["T"]

        if T == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRVC(self, offset):
        V = self.SREG.status["V"]

        if V == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRVS(self, offset):
        V = self.SREG.status["V"]

        if V == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BSET(self, flag):
        if flag == 0:
            self.SREG.status["C"] = 1
        if flag == 1:
            self.SREG.status["Z"] = 1
        if flag == 2:
            self.SREG.status["N"] = 1
        if flag == 3:
            self.SREG.status["V"] = 1
        if flag == 4:
            self.SREG.status["S"] = 1
        if flag == 5:
            self.SREG.status["H"] = 1
        if flag == 6:
            self.SREG.status["T"] = 1
        if flag == 7:
            self.SREG.status["I"] = 1

        self.PC.address += 1

    def BST(self, destination, pos):
        value = self.ins_register.get(destination)
        shift = value >> pos & 0b1

        self.SREG.status["T"] = shift

        self.PC.address += 1

    def CBI(self, destination, pos):
        value = self.sram.get(destination)
        shift = value & ~(1 << pos)

        self.sram.set(destination, shift)

        self.PC.address += 1

    def CLC(self):
        self.SREG.status["C"] = 0

        self.PC.address += 1

    def CLH(self):
        self.SREG.status["H"] = 0

        self.PC.address += 1

    def CLI(self):
        self.SREG.status["I"] = 0

        self.PC.address += 1

    def CLN(self):
        self.SREG.status["N"] = 0

        self.PC.address += 1

    def CLR(self, reg1):
        value1 = self.ins_register.get(reg1)

        result = value1 ^ value1
        self.ins_register.set(reg1, result)

        self.SREG.status["S"] = 0
        self.SREG.status["V"] = 0
        self.SREG.status["N"] = 0
        self.SREG.status["Z"] = 1
        self.PC.address += 1

    def CLS(self):
        self.SREG.status["S"] = 0

        self.PC.address += 1

    def CLT(self):
        self.SREG.status["T"] = 0

        self.PC.address += 1

    def CLV(self):
        self.SREG.status["V"] = 0

        self.PC.address += 1

    def CLZ(self):
        self.SREG.status["Z"] = 0

        self.PC.address += 1

    def COM(self, destination):
        value = self.ins_register.get(destination)
        result = 0xFF - value
        self.ins_register.set(destination, result)

        self.PC.address += 1

    def CP(self, destination, source):
        value1 = self.ins_register.get(destination)
        value2 = self.ins_register.get(source)

        if value1 == value2:
            pass

    def CPC(self, destination, source):
        value1 = self.ins_register.get(destination)
        value2 = self.ins_register.get(source)

        if value1 == value2:
            pass

    def CPI(self, destination, source):
        value1 = self.ins_register.get(destination)
        value2 = self.ins_register.get(source)

        if value1 == value2:
            pass

    def CPSE(self, destination, source):
        value1 = self.ins_register.get(destination)
        value2 = self.ins_register.get(source)

        if value1 == value2:
            self.PC.address = self.PC.address + 2

    def DEC(self, destination):
        value1 = self.ins_register.get(destination)
        result = value1 - 1
        self.ins_register.set(destination, result)

    def DEC(self, destination):
        value1 = self.ins_register.get(destination)
        result = value1 - 1
        self.ins_register.set(destination, result)

    def EOR(self, register1, register2):
        value1 = self.ins_register.get(register1)
        value2 = self.ins_register.get(register2)

        result = value1 ^ value2

        self.ins_register.set(register1, result)

        self.PC.address += 1

    def FMUL(self, destination, source):
        value1 = self.ins_register.get(destination)
        value2 = self.ins_register.get(source)

        Q1 = value1 * value2
        shift = Q1 >> 1

        result = format(shift, "X").zfill(16)
        self.ins_register.set(0x1, int(result[:8], 16))
        self.ins_register.set(0x0 + 1, int(result[8:], 16))
        self.PC.address += 1

    def ICALL(self):
        SPL = self.sram.get(0x3D)
        SPH = self.sram.get(0x3E)
        SP = int("".join([format(SPH, "X"), format(SPL, "X")]), 16)

        SP = SP - 1

        self.sram.set(SP, self.PC.address + 1)

        hex_string = format(SP, "X").zfill(4)

        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))

        value1 = self.ins_register.get(30)
        value2 = self.ins_register.get(31)

        address = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        self.PC.address = address

    def IJMP(self):
        value1 = self.ins_register.get(30)
        value2 = self.ins_register.get(31)

        address = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        self.PC.address = address

    def INC(self, destination):
        value1 = self.ins_register.get(destination)
        result = value1 - 1
        self.ins_register.set(destination, result)
        self.PC.address += 1

    def LDX(self, destination, source):
        value1 = self.ins_register.get(27)
        value2 = self.ins_register.get(26)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1101:
            target = target + 1
        elif source == 0b1110:
            target = target - 1
        elif source == 0b1100:
            target = target

        value = self.sram.get(target)

        self.ins_register.set(destination, value)
        self.PC.address += 1

    def LDY(self, destination, source):
        value1 = self.ins_register.get(29)
        value2 = self.ins_register.get(28)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1001:
            target = target + 1
        elif source == 0b1010:
            target = target - 1
        elif source == 0b1000:
            target = target

        value = self.sram.get(target)

        self.ins_register.set(destination, value)
        self.PC.address += 1

    def LDZ(self, destination, source):
        value1 = self.ins_register.get(31)
        value2 = self.ins_register.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b0001:
            target = target + 1
        elif source == 0b0010:
            target = target - 1
        elif source == 0b0000:
            target = target

        value = self.sram.get(target)

        self.ins_register.set(destination, value)
        self.PC.address += 1
    def STX(self, destination, source):
        value1 = self.ins_register.get(27)
        value2 = self.ins_register.get(26)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1101:
            target = target + 1
        elif source == 0b1110:
            target = target - 1
        elif source == 0b1100:
            target = target

        value = self.ins_register.get(destination)
        self.sram.set(target, value)

        self.PC.address += 1

    def STY(self, destination, source):
        value1 = self.ins_register.get(29)
        value2 = self.ins_register.get(28)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1001:
            target = target + 1
        elif source == 0b1010:
            target = target - 1
        elif source == 0b1000:
            target = target

        value = self.ins_register.get(destination)
        self.sram.set(target, value)

        self.PC.address += 1

    def STZ(self, destination, source):
        value1 = self.ins_register.get(31)
        value2 = self.ins_register.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b0001:
            target = target + 1
        elif source == 0b0010:
            target = target - 1
        elif source == 0b0000:
            target = target

        value = self.ins_register.get(destination)
        self.sram.set(target, value)

        self.PC.address += 1

    def LPMZ(self, destination, source):
        value1 = self.ins_register.get(31)
        value2 = self.ins_register.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b0101:
            target = target + 1
        elif source == 0b0100:
            target = target

        value = self.sram.get(target)

        self.ins_register.set(destination, value)
        self.PC.address += 1

    def LPM(self):
        value1 = self.ins_register.get(31)
        value2 = self.ins_register.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)
        value = self.sram.get(target)

        self.ins_register.set(0x0, value)
        self.PC.address += 1

    def LSR(self, destination):
        value = self.ins_register.get(destination)

        C = (value >> 1) & 1
        self.SREG.status["C"] = C
        self.PC.address += 1

    def MOVW(self, destination, source):
        value1 = self.ins_register.get(source + 1)
        value2 = self.ins_register.get(source)

        self.ins_register.set(destination + 1, value1)
        self.ins_register.set(destination, value2)

        self.PC.address += 1

    def MUL(self, destination, source):
        value1 = self.ins_register.get(destination)
        value2 = self.ins_register.get(source)

        cal = format(int(value1 * value2), "X").zfill(16)

        self.ins_register.set(0x1, cal[:8])
        self.ins_register.set(0x0, cal[8:])
        self.PC.address += 1

    def NEG(self, destination):
        value = self.ins_register.get(destination)

        result = 0x00 - value
        self.ins_register.set(destination, result)
        self.PC.address += 1

    def RCALL(self, destination):
        SPL = self.sram.get(0x3D)
        SPH = self.sram.get(0x3E)
        SP = int("".join([format(SPH, "X"), format(SPL, "X")]), 16)

        SP = SP - 1

        self.sram.set(SP, self.PC.address + 1)

        hex_string = format(SP, "X").zfill(4)

        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))

        self.PC.address = (self.PC.address + 1) + destination

    def RETI(self):
        SPL = self.sram.get(0x3D)
        SPH = self.sram.get(0x3E)
        SP = int("".join([format(SPH, "X"), format(SPL, "X")]), 16)

        address = self.sram.get(SP)
        SP = SP + 1

        hex_string = format(SP, "X").zfill(4)
        self.sram.set(0x3D, int(hex_string[2:], 16))
        self.sram.set(0x3E, int(hex_string[:2], 16))

        self.SREG.status["I"] = 1
        self.PC.address = address

    def ROR(self, destination):
        value = self.ins_register.get(destination)

        CI = self.SREG.status["C"]
        CO = value & 0b1
        result = (value >> 1) | (CI << 7)
        result &= (1 << 8) - 1
        self.ins_register.get(destination, result)

        self.SREG.status["C"] = CO

        self.PC.address += 1

    def SBIC(self, destination, pos):
        value = self.sram.get(destination)
        mask = 1 << pos
        
        if value & mask == 0b0:
            self.PC.address += 2
        else:
            self.PC.address += 1

    def SBIS(self, destination, pos):
        value = self.sram.get(destination)
        mask = 1 << pos
        
        if value & mask == 0b1:
            self.PC.address += 2
        else:
            self.PC.address += 1


    def SBIW(self, destination: int, source: int):
        value1 = self.ins_register.get(destination + 1)
        value2 = self.ins_register.get(destination)
        
        combine = int("".join([format(value1, "X"), format(value2, "X")]), 16)
        
        result = combine - source
        hex_string = format(result, "X").zfill(4)

        self.ins_register.set(destination + 1, hex_string[:8])
        self.ins_register.set(destination, hex_string[8:])
        self.PC.address += 1
        

    def SBR(self, destination, source):
        value = self.ins_register.get(destination)
        
        self.ins_register.set(destination, value | source)
        self.PC.address += 1
    
    def SBRC(self, destination, pos):
        value = self.ins_register.get(destination)
        
        if value >> pos & 0b1 == 0:
            self.PC.address += 2
        else:
            self.PC.address += 1
    
    def SBRS(self, destination, pos):
        value = self.ins_register.get(destination)
        
        if value >> pos & 0b1 == 1:
            self.PC.address += 2
        else:
            self.PC.address += 1
            
    def SEC(self):
        self.SREG.status['C'] = 1
        self.PC.address += 1
            
    def SEH(self):
        self.SREG.status['H'] = 1
        self.PC.address += 1
    def SEI(self):
        self.SREG.status['I'] = 1
        self.PC.address += 1
        
    def SEN(self):
        self.SREG.status['N'] = 1
        self.PC.address += 1
        
    def SER(self, destination):
        self.ins_register.set(destination, 0xFF)
        
    
    def SES(self):
        self.SREG.status['S'] = 1
        self.PC.address += 1
    
    def SET(self):
        self.SREG.status['T'] = 1
        self.PC.address += 1
    
    def SEV(self):
        self.SREG.status['V'] = 1
        self.PC.address += 1
    
    def SEZ(self):
        self.SREG.status['Z'] = 1
        self.PC.address += 1
    
    def SLEEP(self):
        self.PC.address += 1
        
    def SUBI(self, destination: int, source: int):
        dest = self.ins_register.get(destination)
        result = dest - source
        
        self.ins_register.get(destination, result)
        self.PC.address += 1

        
    def SWAP(self, destination):
        value = self.ins_register.get(destination)
        
        hex_str = format(value, 'X').zfill(8)
        
        result = f"{hex_str[4:]}hex_str[:4]"
        self.ins_register.set(destination, int(result))
        self.PC.address += 1

    
    def WDR(self):
        self.PC.address += 1
    