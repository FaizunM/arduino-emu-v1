from assembler.instruction import Instruction
import re

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
        self.symbol_table = {}
        self.address = 0x0

        self.data_section = False
        self.text_section = False
        self.label = None
        self.write = False

        self.compile_address = 0x0

    def just_value(self, value):
        if str(value).startswith("0x"):
            return int(value, 16)
        elif str(value).isdigit():
            return int(value)
        return value

    def encode_line(self, line, address):
        line = line.split(";")[0]
        opcode = line.split(" ")[0].upper()
        operands = line[len(opcode) :].replace(" ", "").split(",")

        filter_symbol = []
        for oprnd in operands:
            if str(oprnd).startswith("HIGH"):
                string = re.findall(r"\((.*?)\)", oprnd)[0]

                if string.startswith("0x"):
                    HIGH = format(int(string, 16), "X")
                    filter_symbol.append(HIGH[: (len(HIGH) // 2)])
                elif string in self.symbol_table:
                    founded = format(int(self.symbol_table[f"{string}"]["value"]), "X")
                    split_val = founded[: (len(founded) // 2)]
                    filter_symbol.append(hex(self.just_value(int(split_val, 16))))

            elif str(oprnd).startswith("LOW"):
                string = re.findall(r"\((.*?)\)", oprnd)[0]

                if string.startswith("0x"):
                    LOW = format(int(string, 16), "X")
                    filter_symbol.append(LOW[(len(LOW) // 2) :])
                elif string in self.symbol_table:
                    founded = format(int(self.symbol_table[f"{string}"]["value"]), "X")
                    split_val = founded[(len(founded) // 2) :]
                    filter_symbol.append(hex(self.just_value(int(split_val, 16))))

            if oprnd in self.symbol_table:
                if self.symbol_table[oprnd]["section"] == ".data":
                    filter_symbol.append(int(self.symbol_table[f"{oprnd}"]["value"]))
            if oprnd in self.symbol_table:
                if self.symbol_table[oprnd]["section"] == ".text":
                    if opcode in ['BRBC', 'BRBS', 'BRCC', 'BRCS', 'BREQ', 'BRGE', 'BRHC', 'BRHS', 'BRID', 'BRIE', 'BRLO', 'BRLT', 'BRMI', 'BRNE', 'BRPL', 'BRSH', 'BRTC', 'BRTS', 'BRTC', 'BRVS', 'RCALL', 'RJMP']:
                        offset = int(self.symbol_table[f"{oprnd}"]["address"]) - address
                        filter_symbol.append(hex(offset - 1))
                    else:
                        filter_symbol.append(int(self.symbol_table[f"{oprnd}"]["address"]))
            else:
                filter_symbol.append(oprnd)
        ins = Instruction(opcode, filter_symbol)
        result = ins.encode()
        if len(result) > 16:
            front = result[:16]
            back = result[16:]
            swap = int(back + front, 2)
            return format(swap, "b")
        else:
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

                    self.symbol_table[f"{label}"] = {
                        "section": ".data",
                        "address": self.address,
                        "type": "variable",
                        "value": int(value, 0),
                    }

                elif self.text_section:
                    if line[-1] == ":":
                        label = line.replace(":", "")
                        self.symbol_table[f"{label}"] = {
                            "section": ".text",
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
            self.symbol_table[f"{self.data_segment[idx].label}"]["address"] = address

        new_text_section = []
        self.write = False
        for idx, text in enumerate(self.text_segment):
            if text.label == "_start":
                self.write = True
            if self.write:
                if self.text_segment[idx].label != None:
                    self.symbol_table[f"{self.text_segment[idx].label}"][
                        "address"
                    ] = self.compile_address
                self.text_segment[idx].address = self.compile_address
                new_text_section.append(self.text_segment[idx])
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
                    self.symbol_table[f"{self.text_segment[idx].label}"][
                        "address"
                    ] = self.compile_address
                self.text_segment[idx].address = self.compile_address
                new_text_section.append(self.text_segment[idx])
                self.compile_address += 1

        Binary = [0] * self.address
        
        
        address = 0x0
        for text in new_text_section:
            encode = self.encode_line(text.instruction, address)
            Binary[text.address] = int(encode.replace(" ", ""), 2)
            address += 1
            
        for idx, data in enumerate(self.data_segment):
            Binary[data.address] = int(data.value, 0)

        return Binary
