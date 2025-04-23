class InstructionRegister:
    def __init__(self):
        self.registers = [0] * 32

    def get(self, address: int):
        if address > len(self.registers) - 1:
            raise ValueError("Out of memory")

        return self.registers[address]

    def set(self, address: int, value: int):
        if address > len(self.registers) - 1:
            raise ValueError("Out of memory")
        
        self.registers[address] = value
        
