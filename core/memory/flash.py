import os, struct


class Flash:
    def __init__(self):
        self.memory = [0] * 0x8000
        self.load_flash()

    def load_flash(self):
        values = []
        with open(os.path.abspath("flash.bin"), "rb") as f:
            while True:
                chunks = f.read(4)
                if not chunks:
                    break
                value = struct.unpack("<" + "I", chunks)[0]
                values.append(value)
            f.close()

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
