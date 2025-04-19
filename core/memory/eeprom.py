class EEPROM:
    def __init__(self):
        self.memory = [0] * 0x400

    def get(self, address: int):
        if address > len(self.registers) - 1:
            raise "Out of memory"

        return self.registers[address]

    def set(self, address: int, value: int):
        if address > len(self.registers) - 1:
            raise "Out of memory"

        self.registers[address] = value
