class DataMemoryMap:
    def __init__(self):
        self.map_address = [0] * 0x8FF
        
        self.INSREG_START = 0x0
        self.INSREG_END = 0x1F
        self.IOREG_START = 0x20
        self.IOREG_END = 0x5F
        self.EXTIOREG_START = 0x60
        self.EXTIOREG_END = 0xFF
        self.SRAM_START = 0x100
        self.SRAM_END = 0x8FF
        
    def get(self, address: int):
        if address > len(self.map_address) - 1:
            raise ValueError("Out of memory")

        return self.map_address[address]

    def set(self, address: int, value: int):
        if address > len(self.map_address) - 1:
            raise ValueError("Out of memory")
        
        self.map_address[address] = value
        
    def get_SRAM(self):
        return self.map_address[0x100:]
        
    def get_INS_REG(self):
        return self.map_address[:0x1F]
    
    def get_SP(self):
        SPH = self.map_address[0x5E]
        SPL = self.map_address[0x5D]
        return (SPH << 8) | SPL
    
    def set_SP(self, new_sp):
        self.map_address[0x5E] = new_sp >> 8 & 0b11111111
        self.map_address[0x5D] = new_sp & 0b11111111
        
    def set_bit(self, bits, pos):
        return bits | (1 << pos)
    
    def clear_bit(self, bits, pos):
        
        return bits & ~(1 << pos)
    
    def get_SREG(self, status):
        sreg = self.map_address[0x5F]
        
        if status == 'I':
            return sreg >> 7 & 0b1
        if status == 'T':
            return sreg >> 6 & 0b1
        if status == 'H':
            return sreg >> 5 & 0b1
        if status == 'S':
            return sreg >> 4 & 0b1
        if status == 'V':
            return sreg >> 3 & 0b1
        if status == 'N':
            return sreg >> 2 & 0b1
        if status == 'Z':
            return sreg >> 1 & 0b1
        if status == 'C':
            return sreg >> 0 & 0b1
        
        else:
            return sreg
    
    def set_SREG(self, status, value):
        sreg = self.map_address[0x5F]
        
        
        if status == 'I':
            if value == 1:
                new_sreg = self.set_bit(sreg, 7)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                new_sreg = self.clear_bit(sreg, 7)
                self.map_address[0x5F] = new_sreg
        if status == 'T':
            if value == 1:
                new_sreg = self.set_bit(sreg, 6)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                new_sreg = self.clear_bit(sreg, 6)
                self.map_address[0x5F] = new_sreg
        if status == 'H':
            if value == 1:
                new_sreg = self.set_bit(sreg, 5)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                new_sreg = self.clear_bit(sreg, 5)
                self.map_address[0x5F] = new_sreg
        if status == 'S':
            if value == 1:
                new_sreg = self.set_bit(sreg, 4)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                new_sreg = self.clear_bit(sreg, 4)
                self.map_address[0x5F] = new_sreg
        if status == 'V':
            if value == 1:
                new_sreg = self.set_bit(sreg, 3)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                
                new_sreg = self.clear_bit(sreg, 3)
                self.map_address[0x5F] = new_sreg
        if status == 'N':
            if value == 1:
                new_sreg = self.set_bit(sreg, 2)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                new_sreg = self.clear_bit(sreg, 2)
                self.map_address[0x5F] = new_sreg
        if status == 'Z':
            if value == 1:
                
                new_sreg = self.set_bit(sreg, 1)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                new_sreg = self.clear_bit(sreg, 1)
                self.map_address[0x5F] = new_sreg
        if status == 'C':
            if value == 1:
                new_sreg = self.set_bit(sreg, 0)
                self.map_address[0x5F] = new_sreg
            if value == 0:
                new_sreg = self.clear_bit(sreg, 0)
                self.map_address[0x5F] = new_sreg
                
        
            
        
        
        