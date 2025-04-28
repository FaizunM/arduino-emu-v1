from core.data_memory_map import DataMemoryMap


class ALU:

    def __init__(self, prog_counter, DMEM):
        self.DMEM: DataMemoryMap = DMEM
        self.PC = prog_counter

    def to_signed(self, value):
        value = value & 0xFF
        return value if value < 0x80 else value - 0x100

    def ADC(self, destination: int, source: int):
        dest = self.DMEM.get(destination)
        src = self.DMEM.get(source)
        real_result = dest + src + self.DMEM.get_SREG("C")
        result = real_result & 0xFF
        signed_result = self.to_signed(result)

        if (
            self.to_signed(dest) > 0 and self.to_signed(src) > 0 and signed_result < 0
        ) or (
            self.to_signed(dest) < 0 and self.to_signed(src) < 0 and signed_result > 0
        ):
            self.DMEM.set_SREG("V", 1)
        else:
            self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG(
            "H",
            1 if ((dest & 0xF) + (src & 0xF) + self.DMEM.get_SREG("C")) > 0xF else 0,
        )
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S", 1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1 if real_result > 0xFF else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def ADD(self, destination: int, source: int):
        dest = self.DMEM.get(destination)
        src = self.DMEM.get(source)
        real_result = dest + src
        result = real_result & 0xFF
        signed_result = self.to_signed(result)

        if (
            self.to_signed(dest) > 0 and self.to_signed(src) > 0 and signed_result < 0
        ) or (
            self.to_signed(dest) < 0 and self.to_signed(src) < 0 and signed_result > 0
        ):
            self.DMEM.set_SREG("V", 1)
        else:
            self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("H", 1 if ((dest & 0xF) + (src & 0xF)) > 0xF else 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S", 1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1 if real_result > 0xFF else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def SUB(self, destination: int, source: int):
        dest = self.DMEM.get(destination)
        src = self.DMEM.get(source)
        real_result = dest - src
        result = real_result & 0xFF
        signed_result = self.to_signed(result)

        if (
            self.to_signed(dest) > 0 and self.to_signed(src) > 0 and signed_result < 0
        ) or (
            self.to_signed(dest) < 0 and self.to_signed(src) < 0 and signed_result > 0
        ):
            self.DMEM.set_SREG("V", 1)
        else:
            self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("H", 1 if ((dest & 0xF) - (src & 0xF)) > 0xF else 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S", 1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1 if real_result > 0xFF else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def SBC(self, destination: int, source: int):
        dest = self.DMEM.get(destination)
        src = self.DMEM.get(source)
        real_result = (dest - src) + self.DMEM.get_SREG("C")
        result = real_result & 0xFF
        signed_result = self.to_signed(result)

        if (
            self.to_signed(dest) > 0 and self.to_signed(src) > 0 and signed_result < 0
        ) or (
            self.to_signed(dest) < 0 and self.to_signed(src) < 0 and signed_result > 0
        ):
            self.DMEM.set_SREG("V", 1)
        else:
            self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("H", 
            1 if ((dest & 0xF) - (src & 0xF)) - self.DMEM.get_SREG("C") > 0xF else 0
        )
        self.DMEM.set_SREG("N",  1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C",  1 if dest >= (src + self.DMEM.get_SREG("C")) else 0)
        self.PC.address += 1

    def SBCI(self, destination: int, source: int):
        dest = self.DMEM.get(destination)
        real_result = (dest - source) + self.DMEM.get_SREG("C")
        result = real_result & 0xFF
        signed_result = self.to_signed(result)

        if (
            self.to_signed(dest) > 0
            and self.to_signed(source) > 0
            and signed_result < 0
        ) or (
            self.to_signed(dest) < 0
            and self.to_signed(source) < 0
            and signed_result > 0
        ):
            self.DMEM.set_SREG("V", 1)
        else:
            self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("H", 1 if ((dest & 0xF) - (source & 0xF)) -  self.SREG.status['C'] < 0x0 else 0)

        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C",  1 if dest >= (source + self.DMEM.get_SREG("C")) else 0)

        self.PC.address += 1

    def LDI(self, destination: int, value: int):
        self.DMEM.set(destination, value)
        self.PC.address += 1

    def JMP(self, destination: int):
        self.PC.address = destination

    def MOV(self, destination, source):
        value = self.DMEM.get(source)
        self.DMEM.set(destination, value)
        self.PC.address += 1

    def OR(self, destination, source):
        dest_val = self.DMEM.get(destination)
        src_val = self.DMEM.get(source)
        result = dest_val | src_val

        self.DMEM.set_SREG("N", result >> 7 & 0b1)
        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def AND(self, destination, source):
        dest_val = self.DMEM.get(destination)
        src_val = self.DMEM.get(source)
        value = dest_val & src_val
        result = value & 0xFF

        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def OUT(self, destination, source):
        value = self.DMEM.get(source)
        self.DMEM.set(destination, value)
        self.PC.address += 1

    def CALL(self, destination):
        SP = self.DMEM.get_SP()

        SP = SP - 1
        self.DMEM.set(SP, self.PC.address + 1)
        self.PC.address = destination
        self.DMEM.set_SP(SP)

    def RET(self):
        SP = self.DMEM.get_SP()
        address = self.DMEM.get(SP)
        SP = SP + 1

        self.DMEM.set_SP(SP)
        self.PC.address = address

    def RJMP(self, destination):
        self.PC.address = (self.PC.address + 1) + destination

    def IN(self, destination, source):
        value = self.DMEM.get(source)

        self.DMEM.set(destination, value)
        self.PC.address += 1

    def PUSH(self, source):
        SP = self.DMEM.get_SP()

        SP = SP - 1
        value = self.DMEM.get(source)
        self.DMEM.set(SP, value)

        self.DMEM.set_SP(SP)

        self.PC.address += 1

    def POP(self, destination):
        SP = self.DMEM.get_SP()

        SP = SP + 1
        value = self.DMEM.get(SP)

        self.DMEM.set(destination, value)

        self.DMEM.set_SP(SP)
        self.PC.address += 1

    def STS(self, destination, source):
        value = self.DMEM.get(source)

        self.DMEM.set(destination, value)
        self.PC.address += 1

    def LDS(self, destination, source):
        value = self.DMEM.get(source)
        self.DMEM.set(destination, value)
        self.PC.address += 1

    def ADIW(self, destination, source):
        LOW = self.DMEM.get(destination)
        HIGH = self.DMEM.get(destination + 1)

        value = (HIGH << 8) | LOW
        
        result = (value + source) & 0xFFFF

        self.DMEM.set_SREG("V", int((value >> 15) == 0) and ((result >> 15) == 1))
        self.DMEM.set_SREG("N", 1 if result >> 15 & 0b1 else 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1) if result > 0xFFFF else 0

        self.DMEM.set(destination, result & 0xFF)
        self.DMEM.set(destination + 1, (result >> 8) & 0xFF)

        self.PC.address += 1

    def ANDI(self, destination: int, source: int):
        dest_val = self.DMEM.get(destination)
        value = dest_val & source
        result = value & 0xFF

        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def SEI(self):
        self.DMEM.get_SREG('I', 1)
        self.PC.address += 1

    def ORI(self, destination, source):
        dest_val = self.DMEM.get(destination)
        result = dest_val | source

        self.DMEM.set_SREG("N", result >> 7 & 0b1)
        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def ASR(self, destination):
        value = self.DMEM.get(destination)
        ML = value & 0b1
        self.DMEM.set_SREG("C", ML)

        shift = value >> 1
        result = shift & 0xFF

        self.DMEM.set(destination, result)

        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("V",
            1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("C") else 0
        )
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.PC.address += 1

    def BCLR(self, flag):
        if flag == 0:
            self.DMEM.set_SREG("C", 0)
        if flag == 1:
            self.DMEM.set_SREG("Z", 0)
        if flag == 2:
            self.DMEM.set_SREG("N", 0)
        if flag == 3:
            self.DMEM.set_SREG("V", 0)
        if flag == 4:
            self.DMEM.set_SREG("S", 0)
        if flag == 5:
            self.DMEM.set_SREG("H", 0)
        if flag == 6:
            self.DMEM.set_SREG("T", 0)
        if flag == 7:
            self.DMEM.set_SREG("I", 0)

        self.PC.address += 1

    def BST(self, destination, pos):
        value = self.DMEM.get(destination)

        T = (value >> pos) & 1
        self.DMEM.set_SREG("T", T)
        self.PC.address += 1

    def BLD(self, destination, pos):
        T = self.DMEM.get_SREG("T")

        value = self.DMEM.get(destination)

        if T:
            value = value | (1 << pos)
            self.DMEM.set(destination, value)
        else:
            value = value & ~(1 << pos)
            self.DMEM.set(destination, value)
        self.PC.address += 1

    def BRBC(self, destination, offset):
        state = self.DMEM.get_SREG() >> destination

        if state == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRBS(self, destination, offset):
        state = self.DMEM.get_SREG() >> destination

        if state == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRCC(self, offset):
        C = self.DMEM.get_SREG("C")

        if C == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRCS(self, offset):
        C = self.DMEM.get_SREG("C")

        if C == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BREAK(self):
        self.PC.address += 1

    def NOP(self):
        raise ValueError("System Finished")

    def BREQ(self, offset):
        Z = self.DMEM.get_SREG("Z")

        if Z == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRGE(self, offset):
        N = self.DMEM.get_SREG("N")
        V = self.DMEM.get_SREG("V")
        S = N ^ V

        if S == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRHC(self, offset):
        H = self.DMEM.get_SREG("H")

        if H == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRHS(self, offset):
        H = self.DMEM.get_SREG("H")

        if H == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRID(self, offset):
        I = self.DMEM.get_SREG("I")

        if I == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRIE(self, offset):
        I = self.DMEM.get_SREG("I")

        if I == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRLO(self, offset):
        C = self.DMEM.get_SREG("C")

        if C == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRLT(self, offset):
        N = self.DMEM.get_SREG("N")
        V = self.DMEM.get_SREG("V")
        S = N ^ V

        if S == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRMI(self, offset):
        N = self.DMEM.get_SREG("N")

        if N == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRNE(self, offset):
        Z = self.DMEM.get_SREG("Z")

        if Z == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRPL(self, offset):
        N = self.DMEM.get_SREG("N")

        if N == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRSH(self, offset):
        C = self.DMEM.get_SREG("C")

        if C == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRTC(self, offset):
        T = self.DMEM.get_SREG("T")

        if T == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRTS(self, offset):
        T = self.DMEM.get_SREG("T")

        if T == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRVC(self, offset):
        V = self.DMEM.get_SREG("V")

        if V == 0:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BRVS(self, offset):
        V = self.DMEM.get_SREG("V")

        if V == 1:
            self.PC.address = (self.PC.address + 1) + offset
        else:
            self.PC.address += 1

    def BSET(self, flag):
        if flag == 0:
            self.DMEM.set_SREG("C", 1)
        if flag == 1:
            self.DMEM.set_SREG("Z", 1)
        if flag == 2:
            self.DMEM.set_SREG("N", 1)
        if flag == 3:
            self.DMEM.set_SREG("V", 1)
        if flag == 4:
            self.DMEM.set_SREG("S", 1)
        if flag == 5:
            self.DMEM.set_SREG("H", 1)
        if flag == 6:
            self.DMEM.set_SREG("T", 1)
        if flag == 7:
            self.DMEM.set_SREG("I", 1)

        self.PC.address += 1

    def BST(self, destination, pos):
        value = self.DMEM.get(destination)
        shift = value >> pos & 0b1

        self.DMEM.set_SREG("T", shift)

        self.PC.address += 1

    def CBI(self, destination, pos):
        value = self.DMEM.get(destination)
        shift = value & ~(1 << pos)

        self.DMEM.set(destination, shift)

        self.PC.address += 1

    def CLC(self):
        self.DMEM.set_SREG("C", 0
)
        self.PC.address += 1

    def CLH(self):
        self.DMEM.set_SREG("H", 0)

        self.PC.address += 1

    def CLI(self):
        self.DMEM.set_SREG("I", 0)

        self.PC.address += 1

    def CLN(self):
        self.DMEM.set_SREG("N", 0)

        self.PC.address += 1

    def CLR(self, reg1):
        value1 = self.DMEM.get(reg1)

        result = value1 ^ value1
        self.DMEM.set(reg1, result)

        self.DMEM.set_SREG("S", 0)
        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("N", 0)
        self.DMEM.set_SREG("Z", 1)
        self.PC.address += 1

    def CLS(self):
        self.DMEM.set_SREG("S", 0)

        self.PC.address += 1

    def CLT(self):
        self.DMEM.set_SREG("T", 0)

        self.PC.address += 1

    def CLV(self):
        self.DMEM.set_SREG("V", 0)

        self.PC.address += 1

    def CLZ(self):
        self.DMEM.get_SREG('Z', 0)
        self.PC.address += 1

    def COM(self, destination):
        value = self.DMEM.get(destination)
        result = ~value & 0xFF
        self.DMEM.set(destination, result)

        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S", self.DMEM.get_SREG("N"))
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1)

        self.PC.address += 1

    def CP(self, destination, source):
        value1 = self.DMEM.get(destination)
        value2 = self.DMEM.get(source)

        result = value1 - value2
        self.DMEM.set_SREG("H", 1 if ((value1 & 0xF)) < ((value2 & 0xF)) else 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("V",
            1
            if (
                ((value1 & 0x80) == (value2 & 0x80))
                and ((result & 0x80) != (value1 & 0x80))
            )
            else 0
        )
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1) if value1 >= value2 else 0
        self.PC.address += 1

    def CPC(self, destination, source):
        value1 = self.DMEM.get(destination)
        value2 = self.DMEM.get(source)

        result = (value1 - value2) + self.DMEM.get_SREG("C")
        self.DMEM.set_SREG("H", 1 if ((value1 & 0xF)) < ((value2 & 0xF)) else 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("V",
            1
            if (
                ((value1 & 0x80) == (value2 & 0x80))
                and ((result & 0x80) != (value1 & 0x80))
            )
            else 0
        )
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1) if value1 >= (value2 + self.DMEM.get_SREG("C")) else 0
        self.PC.address += 1

    def CPI(self, destination, source):
        value1 = self.DMEM.get(destination)

        result = value1 - source
        self.DMEM.set_SREG("H", 1 if ((value1 & 0xF)) < ((source & 0xF)) else 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("V",
            1
            if (
                ((value1 & 0x80) == (source & 0x80))
                and ((result & 0x80) != (value1 & 0x80))
            )
            else 0
        )
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1) if value1 >= (source) else 0
        self.PC.address += 1

    def CPSE(self, destination, source):
        value1 = self.DMEM.get(destination)
        value2 = self.DMEM.get(source)

        if value1 == value2:
            self.PC.address = self.PC.address + 2

    def DEC(self, destination):
        value1 = self.DMEM.get(destination)
        result = value1 - 1

        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("V", 1) if ((value1 == 0x80)) else 0
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def EOR(self, register1, register2):
        value1 = self.DMEM.get(register1)
        value2 = self.DMEM.get(register2)

        result = value1 ^ value2

        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(register1, result)

        self.PC.address += 1

    def FMUL(self, destination, source):
        value1 = self.DMEM.get(destination)
        value2 = self.DMEM.get(source)

        Q1 = value1 * value2
        shift = Q1 >> 1

        result = format(shift, "X").zfill(16)
        self.DMEM.set(0x1, int(result[:8], 16))
        self.DMEM.set(0x0 + 1, int(result[8:], 16))
        self.PC.address += 1

    def ICALL(self):
        SP = self.DMEM.get_SP()

        SP = SP - 1

        self.DMEM.set(SP, self.PC.address + 1)

        self.DMEM.set_SP(SP)

        value1 = self.DMEM.get(30)
        value2 = self.DMEM.get(31)

        address = (value1 << 8) | value2

        self.PC.address = address

    def IJMP(self):
        value1 = self.DMEM.get(30)
        value2 = self.DMEM.get(31)

        address = (value1 << 8) | value2

        self.PC.address = address

    def INC(self, destination):
        value1 = self.DMEM.get(destination)
        result = value1 + 1

        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("V", 1) if ((value1 == 0x7F)) else 0
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def LDX(self, destination, source):
        value1 = self.DMEM.get(27)
        value2 = self.DMEM.get(26)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1101:
            target = target + 1
        elif source == 0b1110:
            target = target - 1
        elif source == 0b1100:
            target = target

        value = self.DMEM.get(target)

        self.DMEM.set(destination, value)
        self.PC.address += 1

    def LDY(self, destination, source):
        value1 = self.DMEM.get(29)
        value2 = self.DMEM.get(28)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1001:
            target = target + 1
        elif source == 0b1010:
            target = target - 1
        elif source == 0b1000:
            target = target

        value = self.DMEM.get(target)

        self.DMEM.set(destination, value)
        self.PC.address += 1

    def LDZ(self, destination, source):
        value1 = self.DMEM.get(31)
        value2 = self.DMEM.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b0001:
            target = target + 1
        elif source == 0b0010:
            target = target - 1
        elif source == 0b0000:
            target = target

        value = self.DMEM.get(target)

        self.DMEM.set(destination, value)
        self.PC.address += 1

    def STX(self, destination, source):
        value1 = self.DMEM.get(27)
        value2 = self.DMEM.get(26)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1101:
            target = target + 1
        elif source == 0b1110:
            target = target - 1
        elif source == 0b1100:
            target = target

        value = self.DMEM.get(destination)
        self.DMEM.set(target, value)

        self.PC.address += 1

    def STY(self, destination, source):
        value1 = self.DMEM.get(29)
        value2 = self.DMEM.get(28)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b1001:
            target = target + 1
        elif source == 0b1010:
            target = target - 1
        elif source == 0b1000:
            target = target

        value = self.DMEM.get(destination)
        self.DMEM.set(target, value)

        self.PC.address += 1

    def STZ(self, destination, source):
        value1 = self.DMEM.get(31)
        value2 = self.DMEM.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b0001:
            target = target + 1
        elif source == 0b0010:
            target = target - 1
        elif source == 0b0000:
            target = target

        value = self.DMEM.get(destination)
        self.DMEM.set(target, value)

        self.PC.address += 1

    def LPMZ(self, destination, source):
        value1 = self.DMEM.get(31)
        value2 = self.DMEM.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)

        if source == 0b0101:
            target = target + 1
        elif source == 0b0100:
            target = target

        value = self.DMEM.get(target)

        self.DMEM.set(destination, value)
        self.PC.address += 1

    def LPM(self):
        value1 = self.DMEM.get(31)
        value2 = self.DMEM.get(30)

        target = int("".join([format(value1, "X"), format(value2, "X")]), 16)
        value = self.DMEM.get(target)

        self.DMEM.set(0x0, value)
        self.PC.address += 1

    def LSR(self, destination):
        value = self.DMEM.get(destination)
        result = value >> 1
        C = result & 1
        self.DMEM.set_SREG("C", C
)
        self.DMEM.set_SREG("N", 0)
        self.DMEM.set_SREG("V",
            1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("C") else 0
        )
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)

        self.PC.address += 1

    def MOVW(self, destination, source):
        value1 = self.DMEM.get(source + 1)
        value2 = self.DMEM.get(source)

        self.DMEM.set(destination + 1, value1)
        self.DMEM.set(destination, value2)

        self.PC.address += 1

    def MUL(self, destination, source):
        value1 = self.DMEM.get(destination)
        value2 = self.DMEM.get(source)

        cal = format(int(value1 * value2), "X").zfill(16)

        self.DMEM.set(0x1, cal[:8])
        self.DMEM.set(0x0, cal[8:])
        self.PC.address += 1

    def NEG(self, destination):
        value = self.DMEM.get(destination)

        result = 0x00 - value

        self.DMEM.set_SREG("H", 1 if value & 0xF < result & 0xF else 0)
        self.DMEM.set_SREG("N", result >> 7 & 0b1)
        self.DMEM.set_SREG("V", 1) if result == 0x80 else 0
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1) if result != 0x0 else 0

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def RCALL(self, destination):
        SP = self.DMEM.get_SP()

        SP = SP - 1

        self.DMEM.set(SP, self.PC.address + 1)

        self.DMEM.set_SP(SP)

        self.PC.address = (self.PC.address + 1) + destination

    def RETI(self):
        SP = self.DMEM.get_SP()

        address = self.DMEM.get(SP)
        SP = SP + 1

        self.DMEM.set_SP(SP)

        self.DMEM.set_SREG("I", 1)
        self.PC.address = address

    def ROR(self, destination):
        value = self.DMEM.get(destination)

        CI = self.DMEM.get_SREG("C")
        CO = value & 0b1
        result = (value >> 1) | (CI << 7)
        result &= (1 << 8) - 1
        self.DMEM.get(destination, result)

        self.DMEM.set_SREG("C", CO)

        self.DMEM.set_SREG("N", result >> 7 & 0b1)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("V",
            1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("C") else 0
        )
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.PC.address += 1

    def SBIC(self, destination, pos):
        value = self.DMEM.get(destination)
        mask = 1 << pos

        if value & mask == 0b0:
            self.PC.address += 2
        else:
            self.PC.address += 1

    def SBIS(self, destination, pos):
        value = self.DMEM.get(destination)
        mask = 1 << pos

        if value & mask == 0b1:
            self.PC.address += 2
        else:
            self.PC.address += 1

    def SBIW(self, destination: int, source: int):
        LOW = self.DMEM.get(destination)
        HIGH = self.DMEM.get(destination + 1)

        value = (HIGH << 8) | LOW
        result = (value - source) & 0xFFFF

        self.DMEM.set_SREG("V", int((value >> 15) == 0) and ((result >> 15) == 1))
        self.DMEM.set_SREG("N", 1 if result >> 15 & 0b1 else 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1) if result == 0x0000 else 0
        self.DMEM.set_SREG("C", 1) if result <= 0xFFFF else 0

        self.DMEM.set(destination, result & 0xFF)
        self.DMEM.set(destination + 1, (result >> 8) & 0xFF)
        self.PC.address += 1

    def SBR(self, destination, source):
        value = self.DMEM.get(destination)

        result = value | source
        self.DMEM.set_SREG("N", result >> 7 & 0b1)
        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def SBRC(self, destination, pos):
        value = self.DMEM.get(destination)

        if value >> pos & 0b1 == 0:
            self.PC.address += 2
        else:
            self.PC.address += 1

    def SBRS(self, destination, pos):
        value = self.DMEM.get(destination)

        if value >> pos & 0b1 == 1:
            self.PC.address += 2
        else:
            self.PC.address += 1

    def SEC(self):
        self.DMEM.set_SREG("C", 1)
        self.PC.address += 1

    def SEH(self):
        self.DMEM.set_SREG("H", 1)
        self.PC.address += 1

    def SEI(self):
        self.DMEM.set_SREG('I', 1)
        self.PC.address += 1

    def SEN(self):
        self.DMEM.set_SREG("N", 1)
        self.PC.address += 1

    def SER(self, destination):
        self.DMEM.set(destination, 0xFF)

    def SES(self):
        self.DMEM.set_SREG("S", 1)
        self.PC.address += 1

    def SET(self):
        self.DMEM.set_SREG("T", 1)
        self.PC.address += 1

    def SEV(self):
        self.DMEM.set_SREG("V", 1)
        self.PC.address += 1

    def SEZ(self):
        self.DMEM.set_SREG("Z", 1)
        self.PC.address += 1

    def SLEEP(self):
        self.PC.address += 1

    def SUBI(self, destination: int, source: int):
        dest = self.DMEM.get(destination)
        real_result = dest - source
        result = real_result & 0xFF
        signed_result = self.to_signed(result)

        if (
            self.to_signed(dest) > 0
            and self.to_signed(source) > 0
            and signed_result < 0
        ) or (
            self.to_signed(dest) < 0
            and self.to_signed(source) < 0
            and signed_result > 0
        ):
            self.DMEM.set_SREG("V", 1)
        else:
            self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("H", 1 if ((dest & 0xF) - (source & 0xF)) > 0xF else 0)
        self.DMEM.set_SREG("N", 1 if result >> 7 & 0b1 else 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)
        self.DMEM.set_SREG("C", 1) if dest >= source else 0

        self.DMEM.set(destination, result)
        self.PC.address += 1

    def SWAP(self, destination):
        value = self.DMEM.get(destination)

        hex_str = format(value, "X").zfill(8)

        result = f"{hex_str[4:]}hex_str[:4]"

        self.DMEM.set_SREG("N", result >> 7 & 0b1)
        self.DMEM.set_SREG("V", 0)
        self.DMEM.set_SREG("S",  1 if self.DMEM.get_SREG("N") ^ self.DMEM.get_SREG("V") else 0)
        self.DMEM.set_SREG("Z", 1 if result == 0x0 else 0)

        self.DMEM.set(destination, int(result))
        self.PC.address += 1

    def WDR(self):
        self.PC.address += 1
