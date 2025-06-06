from assembler.opcode_list import OPCODE, REGISTER_COUNT, SPECIAL_REGISTER


class Instruction:
    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.operands = operands

    def encode(self):
        if self.opcode in [
            "SUBI",
            "SBCI",
            "ANDI",
            "ORI",
            "LDI",
            "CPI",
            "SBR",
            "CBR",
        ]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.halfreg2bin(self.operands[0]).zfill(4)
            )
            mask2 = self.value_pusher(
                mask1, "K", self.formater_value(self.operands[1]).zfill(8)
            )
            return mask2.replace(" ", "")

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
            return mask2.replace(" ", "")
        elif self.opcode in ["SBRC", "SBRS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "r", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1, "b", self.formater_value(self.operands[1]).zfill(5)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["ADIW", "SBIW"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode],
                "d",
                self.reg2bin_special(self.operands[0], 24).zfill(2),
            )
            mask2 = self.value_pusher(
                mask1, "K", self.formater_value(self.operands[1]).zfill(6)
            )
            return mask2.replace(" ", "")
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
            return mask2.replace(" ", "")
        elif self.opcode in ["BCLR"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode],
                "s",
                self.formater_value(self.operands[0]).zfill(3),
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["BLD", "BST"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1,
                "b",
                self.formater_value(self.operands[1]).zfill(3),
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["BRBC", "BRBS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "s", self.formater_value(self.operands[0]).zfill(3)
            )
            mask2 = self.value_pusher(
                mask1,
                "k",
                self.formater_value(self.operands[1]).zfill(7),
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["BSET"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "s", self.formater_value(self.operands[0]).zfill(3)
            )
            return mask1.replace(" ", "")
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
                OPCODE[self.opcode], "k", self.formater_value(self.operands[0]).zfill(7)
            )

            return mask1.replace(" ", "")

        elif self.opcode in ["CALL", "JMP"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode],
                "k",
                self.formater_value(self.operands[0]).zfill(22),
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["LDS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1, "k", format(int(self.operands[1], 0), "b").zfill(16)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["STS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode],
                "k",
                self.formater_value(self.operands[0]).zfill(16),
            )
            mask2 = self.value_pusher(
                mask1, "d", self.reg2bin(self.operands[1]).zfill(5)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["SBIW"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(2)
            )
            mask2 = self.value_pusher(
                mask1, "k", self.formater_value(self.operands[1]).zfill(6)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["CBI", "SBI", "SBIC", "SBIS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode],
                "A",
                self.formater_value(self.operands[0]).zfill(5),
            )
            mask2 = self.value_pusher(
                mask1,
                "b",
                self.formater_value(self.operands[1]).zfill(3),
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["CLR"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(10)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["FMUL", "FMULS", "FMULSU", "MULSU"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode],
                "d",
                self.reg2bin_special(self.operands[0], 16).zfill(3),
            )
            mask2 = self.value_pusher(
                mask1, "r", self.reg2bin_special(self.operands[1], 16).zfill(3)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["IN"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            mask2 = self.value_pusher(
                mask1,
                "A",
                self.formater_value(self.operands[1]).zfill(6),
            )
            return mask2.replace(" ", "")

        elif self.opcode in ["LSL", "LSR", "ROL"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(10)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["ROR"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(4)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["MOVW"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(4)
            )
            mask2 = self.value_pusher(
                mask1, "r", self.reg2bin(self.operands[1]).zfill(4)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["MULS"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin_special(self.operands[0], 16).zfill(4)
            )
            mask2 = self.value_pusher(
                mask1, "r", self.reg2bin_special(self.operands[1], 16).zfill(4)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["OUT"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "A", self.formater_value(self.operands[0], base_start=0x20).zfill(6)
            )
            mask2 = self.value_pusher(
                mask1,
                "r",
                self.reg2bin(
                    self.operands[1],
                ).zfill(5),
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["RCALL", "RJMP"]:
            print(self.relative_value(self.operands[0], 12))

            mask2 = self.value_pusher(
                OPCODE[self.opcode],
                "k",
                self.relative_value(self.operands[0], 12),
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["TST"]:
            mask2 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(12)
            )
            return mask2.replace(" ", "")
        elif self.opcode in ["LD"]:
            mask1 = self.value_pusher(
                OPCODE[self.opcode], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            operand = SPECIAL_REGISTER[self.operands[1]]
            mask2 = self.value_pusher(mask1, "i", operand)
            return mask2.replace(" ", "")
        elif self.opcode in ["ST"]:
            mask1 = self.value_pusher(OPCODE[self.opcode], "i", operand)
            mask2 = self.value_pusher(mask2, 
                 "d", self.reg2bin(self.operands[1]).zfill(5)
            )
            operand = SPECIAL_REGISTER[self.operands[1]]
            return mask2.replace(" ", "")
        elif self.opcode in ["LPM"]:
            if self.operands[0] == "":
                return OPCODE["LPM"]
            mask1 = self.value_pusher(
                OPCODE["LPM1"], "d", self.reg2bin(self.operands[0]).zfill(5)
            )
            if self.operands[1] == "Z":
                mask2 = self.value_pusher(mask1, "i", "0100")
            if self.operands[1] == "Z+":
                mask2 = self.value_pusher(mask1, "i", "0101")
            return mask2.replace(" ", "")

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
            "ICALL",
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

    def formater_value(self, value, base_start = 0):
        if str(value).startswith("0x"):
            return format(int(value, 16) - base_start, "b")
        elif str(value).isdigit():
            return format(int(value) - base_start, "b")

    def reg2bin(self, value: str):
        num = int(value.replace("R", "").replace("r", ""))

        if num > REGISTER_COUNT:
            raise ValueError("Register out of range")
        return format(num, "b")

    def reg2bin_special(self, value: str, base_start):
        num = int(value.replace("R", "").replace("r", "")) - base_start
        if num < 0 or num > REGISTER_COUNT:
            raise ValueError(f"Register out of range, use only from register {base_start}")
        return format(num, "b")

    def halfreg2bin(self, value: str):
        num = int(value.replace("R", "").replace("r", "")) - 16

        if num < 0 or num > REGISTER_COUNT:
            raise ValueError("Register out of range")
        return format(num, "b")

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

    def relative_value(self, value, padding):
        clear = value.replace("-", "")
        if str(value).startswith("-"):
            return self.flip_binary(format(int(clear), "b").zfill(padding))
        else:
            if str(clear).startswith('0x'):
                return format(int(clear, 16), "b").zfill(padding)
            else:
                return format(int(clear), "b").zfill(padding)

    def flip_binary(self, value):
        return "".join("1" if bit == "0" else "0" for bit in value)
