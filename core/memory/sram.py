class SRAM:
    def __init__(self):
        self.memory = [0] * 0x800
           
    def get(self, address: int):
        if address > len(self.memory) - 1:
            raise "Out of memory"

        return self.memory[address]

    def set(self, address: int, value: int):
        if address > len(self.memory) - 1:
            raise "Out of memory"
        
        if value > 0xFFFF:
            raise "Value over the limit (0xFFFF)"
            
        
        self.memory[address] = value
        
