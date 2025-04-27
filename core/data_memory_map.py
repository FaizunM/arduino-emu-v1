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
        
            
        