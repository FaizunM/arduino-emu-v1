from assembler.instruction import Instruction

# .byte	1 byte	Simpan 8-bit data
# .half	2 byte	Simpan 16-bit data (kadang disebut .hword)
# .word	4 byte	Simpan 32-bit data
# .dword	8 byte	Simpan 64-bit data
# .ascii	-	Simpan string ASCII tanpa null
# .asciiz	-	Simpan string ASCII dengan null (\0) di akhir


class Data:
    def __init__(self, label, value, address):
        self.label = label
        self.value = value
        self.address = address


class Text:
    def __init__(self, address, label, instruction):
        self.address = address
        self.label = label
        self.instruction = instruction


class Assembler:
    def __init__(self, instructions: list):
        self.instructions: list = instructions
        self.text_segment: Text = []
        self.data_segment: Data = []
        self.symbol_table = {".data": {}, ".text": {}}
        self.address = 0x0

        self.data_section = False
        self.text_section = False
        self.label = None
        self.write = False

        self.compile_address = 0x0

    def encode_line(self, line):
        line = line.split(";")[0]
        opcode = line.split(" ")[0].upper()
        operands = line[len(opcode) :].replace(" ", "").split(",")

        ins = Instruction(opcode, operands, self.symbol_table)
        result = ins.encode()
        return result

    def parse_line(self):
        for num, line in enumerate(self.instructions):
            try:
                if line.startswith(";"):
                    continue

                if line == "":
                    self.data_section = False
                    self.text_section = False
                    self.label = None
                    continue

                if line == ".data":
                    self.data_section = True
                    continue

                if line == ".text":
                    self.text_section = True
                    continue

                if self.data_section:
                    split = line.split(":")
                    label = split[0]
                    values = split[1].split(" ")
                    value = values[2]
                    data = Data(label, value, self.address)
                    self.data_segment.append(data)

                    self.symbol_table[".data"][f"{label}"] = {
                        "address": self.address,
                        "type": "variable",
                        "value": int(value, 0),
                    }

                elif self.text_section:
                    if line[-1] == ":":
                        label = line.replace(":", "")
                        self.symbol_table[".text"][f"{label}"] = {
                            "address": self.address,
                            "type": "label",
                            "value": None,
                        }
                        self.label = label
                        continue

                    if len(line.replace(" ", "")) > 16:
                        self.address += 1

                    text = Text(self.address, self.label, line)
                    self.text_segment.append(text)
                    self.label = None
                else:
                    continue

            except Exception as e:
                print(f"{str(num+1).rjust(5)}  -> ERRORS on line -> {line} : {e}")
            self.address += 1

    def compile(self):
        self.parse_line()


        for idx, address in enumerate(
            range((self.address) - len(self.data_segment), (self.address))
        ):
            self.data_segment[idx].address = address
            self.symbol_table[".data"][f"{self.data_segment[idx].label}"][
                "address"
            ] = address

        self.write = False
        for idx, text in enumerate(self.text_segment):
            if text.label == "_start":
                self.write = True
            if self.write:
                if self.text_segment[idx].label != None:
                    self.symbol_table[".text"][f"{self.text_segment[idx].label}"][
                        "address"
                    ] = self.compile_address
                self.text_segment[idx].address = self.compile_address
                self.compile_address += 1

            if text.label != None and text.label != "_start":
                self.write = False

        self.write = False
        for idx, text in enumerate(self.text_segment):
            if text.label != "_start" and text.label != None:
                self.write = True

            if text.label != None and text.label == "_start":
                self.write = False

            if self.write:
                if self.text_segment[idx].label != None:
                    self.symbol_table[".text"][f"{self.text_segment[idx].label}"][
                        "address"
                    ] = self.compile_address
                self.text_segment[idx].address = self.compile_address
                self.compile_address += 1

        
        Binary = [0] * self.address        

        for idx, text in enumerate(self.text_segment):
            encode = self.encode_line(text.instruction)
            Binary[text.address] = int(encode.replace(' ', ''), 2)
            
        for idx, data in enumerate(self.data_segment):
            Binary[data.address] = int(data.value, 0)
        
        return Binary
