from assembler.opcode_list import OPCODE, SPECIAL_REGISTER, REGISTER_COUNT


class Instruction:
    def __init__(self, opcode, operands, symbol_map):
        self.opcode = opcode
        self.operands = operands
        self.symbol_map = symbol_map

    def encode(self):
        if self.opcode in ["SUBI", "SBCI", "SBIW", "ANDI", "ORI", "LDI", "CPI", "SBR"]:
            value = None
            if self.operands[1] in self.symbol_map[".data"]:
                value = self.symbol_map[".data"][f"{self.operands[1]}"]["value"]
            else:
                value = self.operands[1]

            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(4)
            )
            mask2 = self.value_pusher(
                mask1, "K", self.immediate2bin(str(value)).zfill(8)
            )
            return mask2.replace(' ', '')

        elif self.opcode in [
            "ADD",
            "ADC",
            "SUB",
            "SBC",
            "AND",
            "OR",
            "EOR",
            "MOV",
            "CP",
            "CPC",
            "CPSE",
            "MUL",
            "SUB",
        ]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1, "r", self.reg2bin(self.operands[1]).zfill(5)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["SBRC", "SBRS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "r", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1, "b", self.immediate2bin(self.operands[1]).zfill(5)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["ADIW"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", SPECIAL_REGISTER[self.operands[0]]
            )
            mask2 = self.value_pusher(
                mask1, "K", self.immediate2bin(self.operands[1]).zfill(6)
            )
            return mask2.replace(' ', '')
        elif self.opcode in [
            "ASR",
            "COM",
            "DEC",
            "INC",
            "NEG",
            "POP",
            "PUSH",
            "SBCI",
            "SWAP",
        ]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["BCLR"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode],
                "s",
                self.immediate2bin(
                    self.operands[0],
                ).zfill(3),
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["BLD", "BST"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1,
                "b",
                self.immediate2bin(
                    self.operands[1],
                ).zfill(3),
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["BRBC", "BRBS", "BSET"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "s", self.immediate2bin(self.operands[0]).zfill(3)
            )
            mask2 = self.value_pusher(
                mask1,
                "k",
                self.immediate2bin(
                    self.operands[1],
                ).zfill(7),
            )
            return mask2.replace(' ', '')
        elif self.opcode in [
            "BRCC",
            "BRCS",
            "BREQ",
            "BRGE",
            "BRHC",
            "BRHS",
            "BRID",
            "BRIE",
            "BRLO",
            "BRLT",
            "BRMI",
            "BRNE",
            "BRPL",
            "BRSH",
            "BRTC",
            "BRTS",
            "BRVC",
            "BRVS",
        ]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "k", self.immediate2bin(self.operands[0]).zfill(7)
            )

            return mask1.replace(' ', '')

        elif self.opcode in ["CALL", "JMP"]:
            value = None
            if self.operands[0] in self.symbol_map[".text"]:
                value = self.symbol_map[".text"][f"{self.operands[0]}"]["address"]
            else:
                value = self.operands[0]
            mask2 = self.value_pusher(
                OPCODE[self.opcode],
                "k",
                self.immediate2bin(str(value)).zfill(22),
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["LDS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1, "k", self.immediate2bin(self.operands[1]).zfill(16)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["STS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode],
                "k",
                self.immediate2bin(self.operands[0]).zfill(16),
            )
            mask2 = self.value_pusher(
                mask1, "d", self.reg2bin(self.operands[1]).zfill(5)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["SBIW"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(2)
            )
            mask2 = self.value_pusher(
                mask1, "k", self.immediate2bin(self.operands[1]).zfill(6)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["CBI", "SBI", "SBIC", "SBIS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode],
                "A",
                self.immediate2bin(self.operands[0]).zfill(5),
            )
            mask2 = self.value_pusher(
                mask1,
                "b",
                self.immediate2bin(
                    self.operands[1],
                ).zfill(3),
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["CLR"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.immediate2bin(self.operands[0]).zfill(10)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["FMUL", "FMULS", "FMULSU", "MULSU"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(3)
            )
            mask2 = self.value_pusher(
                mask1, "r", self.reg2bin(self.operands[1]).zfill(3)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["IN"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1,
                "A",
                self.immediate2bin(
                    self.operands[1],
                ).zfill(6),
            )
            return mask2.replace(' ', '')

        elif self.opcode in ["LSL", "LSR", "ROL"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(10)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["ROR"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(4)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["MOVW", "MULS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(4)
            )
            mask2 = self.value_pusher(
                mask1, "r", self.reg2bin(self.operands[1]).zfill(4)
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["OUT"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "A", self.immediate2bin(self.operands[0]).zfill(6)
            )
            mask2 = self.value_pusher(
                mask1,
                "r",
                self.reg2bin(
                    self.operands[1],
                ).zfill(4),
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["RCALL", "RJMP"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode],
                "k",
                self.immediate2bin(self.operands[0]).zfill(12),
            )
            return mask2.replace(' ', '')
        elif self.opcode in ["TST"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(12)
            )
            return mask2.replace(' ', '')
        elif self.opcode in [
            "BREAK",
            "CLC",
            "CLH",
            "CLI",
            "CLN",
            "CLS",
            "CLT",
            "CLV",
            "CLZ",
            "EICALL",
            "EIJMP",
            "ECALL",
            "IJMP",
            "NOP",
            "RET",
            "RETI",
            "SEC",
            "SEH",
            "SEI",
            "SEN",
            "SER",
            "SES",
            "SET",
            "SEV",
            "SEZ",
            "SLEEP",
            "SPM",
            "WDR",
        ]:
            return OPCODE[self.opcode]
        else:
            raise ValueError(f"Unknows OPCODE: {self.opcode}")

    def reg2bin(self, value: str):
        num = int(value.replace("R", "").replace("r", ""))

        if num > REGISTER_COUNT:
            raise ValueError("Register out of range")

        return format(num, "b")

    def immediate2bin(self, value: str):
        return format(int(value, 0), "b")

    def value_pusher(self, text, character, value):
        array = []

        offset = 0
        for idx in range(0, len(text)):
            if text[idx] == character:
                array.append(value[offset])
                offset += 1
            else:
                array.append(text[idx])

        return "".join(array)
