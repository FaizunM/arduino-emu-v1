class SRAM:
    def __init__(self):
        self.memory = [0] * 0x8FF
           
    def get(self, address: int):
        if address > len(self.memory) - 1:
            raise ValueError(f"Out of memory {hex(address) } ")

        return self.memory[address]

    def set(self, address: int, value: int):
        if address > len(self.memory) - 1:
            raise ValueError(f"Out of memory {hex(address) }")
        
        if value > 0xFF:
            raise ValueError("Value over the limit (0xFFFF)")
            
        
        self.memory[address] = value
        
