from core.alu import ALU


class InstructionDecoder:
    def __init__(self, PC, alu):
        self.alu: ALU = alu
        self.PC = PC

    def decode(self, operation: int):
        if operation == 0:
            self.PC.address += 1
            return
        # ADC
        if (operation >> 10) & 0b111111 == 0b000111:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            self.alu.ADC(destination, source)
            self.PC.address += 1
        # ADD
        elif (operation >> 10) & 0b111111 == 0b000011:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            self.alu.ADD(destination, source)
            self.PC.address += 1
        # SUB
        elif (operation >> 10) & 0b111111 == 0b000010:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            self.alu.SUB(destination, source)
            self.PC.address += 1
        # SBC
        elif (operation >> 10) & 0b111111 == 0b000110:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            self.alu.SUB(destination, source)
            self.PC.address += 1
        # LDI
        elif (operation >> 12) & 0b1111 == 0b1110:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            self.alu.LDI(destination, source)
            self.PC.address += 1
        else:
            self.PC.address += 1
            raise ValueError("Unknown OPCODE")
