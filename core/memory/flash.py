import os, struct


class Flash:
    def __init__(self):
        self.memory = [0] * 0x8000
        self.load_flash()

    def load_flash(self):
        values = []
        with open(os.path.abspath("firmware.bin"), "rb") as f:
            while True:
                chunks = f.read(4)
                if not chunks:
                    break
                value = struct.unpack("<" + "I", chunks)[0]
                values.append(value)
            f.close()

        fix_length = len(self.memory)
        self.memory[: len(values)] = values[:fix_length]

    def get_used(self):
        for num in range(len(self.memory) - 1, 0, -1):
            if self.memory[num] != 0x0:
                percent = num / (len(self.memory) - 1) * 100
                return {
                    "start": 0x0,
                    "end": num,
                    "percent": percent,
                    "total": len(self.memory) - 1,
                }

    def get(self, address: int):
        if address > len(self.memory) - 1:
            raise ValueError(f"Out of memory {hex(address)}, max {hex(len(self.memory) - 1)}")

        return self.memory[address]

    def set(self, address: int, value: int):
        if address > len(self.memory) - 1:
            raise ValueError(f"Out of memory {hex(address)}, max {hex(len(self.memory) - 1)}")

        self.memory[address] = value
