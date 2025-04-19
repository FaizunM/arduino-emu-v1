import os, struct


class Flash:
    def __init__(self):
        self.memory = [0] * 0x8000
        self.load_flash()

    def load_flash(self):
        with open(os.path.abspath("flash.bin"), "rb") as f:
            data = f.read()
            f.close()

        values = struct.unpack("<" + "H" * (len(data) // 2), data)
        fix_length = len(self.memory)
        self.memory[: len(values)] = values[:fix_length]

    def get(self, address: int):
        if address > len(self.memory) - 1:
            raise "Out of memory"

        return self.memory[address]

    def set(self, address: int, value: int):
        if address > len(self.memory) - 1:
            raise "Out of memory"

        self.memory[address] = value
