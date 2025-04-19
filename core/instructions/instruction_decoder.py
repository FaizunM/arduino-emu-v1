from core.alu import ALU


class InstructionDecoder:
    def __init__(self, PC=None, alu=None):
        self.alu: ALU = alu
        self.PC = PC

    def decode(self, operation: int, definition=False):
        if operation == 0:
            if not definition:
                self.PC.address += 1
                return
            else:
                return "NOP"
        # ADC
        elif (operation >> 10) & 0b111111 == 0b000111:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not definition:
                self.alu.ADC(destination, source)
                self.PC.address += 1
            return f"ADC R{source}, {source}"
        # ADD
        elif (operation >> 10) & 0b111111 == 0b000011:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not definition:
                self.alu.ADD(destination, source)
                self.PC.address += 1
            return f"ADD R{source}, {source}"
        # SUB
        elif (operation >> 10) & 0b111111 == 0b000010:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not definition:
                self.alu.SUB(destination, source)
                self.PC.address += 1
            return f"SUB R{source}, {source}"
        # SBC
        elif (operation >> 10) & 0b111111 == 0b000110:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not definition:
                self.alu.SBC(destination, source)
                self.PC.address += 1
            return f"SBC R{source}, {source}"
        # LDI
        elif (operation >> 12) & 0b1111 == 0b1110:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not definition:
                self.alu.LDI(destination, source)
                self.PC.address += 1
            return f"LDI R{source}, {source}"
        else:
            if not definition:
                self.PC.address += 1
                raise ValueError("Unknown OPCODE")
            else:
                return "Unknown OPCODE"
