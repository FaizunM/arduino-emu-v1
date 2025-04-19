import struct

OPCODE = {
    "ADC": "0001 11rd dddd rrrr",
    "ADD": "0000 11rd dddd rrrr",
    "ADIW": "1001 0110 KKdd KKKK",
    "AND": "0010 00rd dddd rrrr",
    "ANDI": "0111 KKKK dddd KKKK",
    "ASR": "1001 010d dddd 0101",
    "BCLR": "1001 0100 1sss 1000",
    "BLD": "1111 100d dddd 0bbb",
    "BRBC": "1111 01kk kkkk ksss",
    "BRBS": "1111 00kk kkkk ksss",
    "BRCC": "1111 01kk kkkk k000",
    "BRCS": "1111 00kk kkkk k000",
    "BREAK": "1001 0101 1001 1000",
    "BREQ": "1111 00kk kkkk k001",
    "BRGE": "1111 01kk kkkk k100",
    "BRHC": "1111 01kk kkkk k101",
    "BRHS": "1111 00kk kkkk k101",
    "BRID": "1111 01kk kkkk k111",
    "BRIE": "1111 00kk kkkk k111",
    "BRLO": "1111 00kk kkkk k000",
    "BRLT": "1111 00kk kkkk k100",
    "BRMI": "1111 00kk kkkk k010",
    "BRNE": "1111 01kk kkkk k001",
    "BRPL": "1111 01kk kkkk k010",
    "BRSH": "1111 01kk kkkk k000",
    "BRTC": "1111 01kk kkkk k110",
    "BRTS": "1111 00kk kkkk k110",
    "BRVC": "1111 01kk kkkk k011",
    "BRVS": "1111 00kk kkkk k011",
    "BSET": "1001 0100 0sss 1000",
    "BST": "1111 101d dddd 0bbb",
    "CALL": "1001 010k kkkk 111k kkkk kkkk kkkk kkkk",
    "CBI": "1001 1000 AAAA Abbb",
    "CLC": "1001 0100 1000 1000",
    "CLH": "1001 0100 1101 1000",
    "CLI": "1001 0100 1111 1000",
    "CLN": "1001 0100 1010 1000",
    "CLR": "0010 01dd dddd dddd",
    "CLS": "1001 0100 1100 1000",
    "CLT": "1001 0100 1110 1000",
    "CLV": "1001 0100 1011 1000",
    "CLZ": "1001 0100 1001 1000",
    "COM": "1001 010d dddd 0000",
    "CP": "0001 01rd dddd rrrr",
    "CPC": "0000 01rd dddd rrrr",
    "CPI": "0011 KKKK dddd KKKK",
    "CPSE": "0001 00rd dddd rrrr",
    "DEC": "1001 010d dddd 1010",
    "EICALL": "1001 0101 0001 1001",
    "EIJMP": "1001 0100 0001 1001",
    "EOR": "0010 01rd dddd rrrr",
    "FMUL": "0000 0011 0ddd 1rrr",
    "FMULS": "0000 0011 1ddd 0rrr",
    "FMULSU": "0000 0011 1ddd 1rrr",
    "ICALL": "1001 0101 0000 1001",
    "IJMP": "1001 0100 0000 1001",
    "IN": "1011 0AAd dddd AAAA",
    "INC": "1001 010d dddd 0011",
    "JMP": "1001 010k kkkk 110k kkkk kkkk kkkk kkkk",
    "LDI": "1110 KKKK dddd KKKK",
    "LDS": "1001 000d dddd 0000 kkkk kkkk kkkk kkkk",
    "LSL": "0000 11dd dddd dddd",
    "LSR": "1001 010d dddd 0110",
    "MOV": "0010 11rd dddd rrrr",
    "MOVW": "0000 0001 dddd rrrr",
    "MUL": "1001 11rd dddd rrrr",
    "MULS": "0000 0010 dddd rrrr",
    "MULSU": "0000 0011 0ddd 0rrr",
    "NEG": "1001 010d dddd 0001",
    "NOP": "0000 0000 0000 0000",
    "OR": "0010 10rd dddd rrrr",
    "ORI": "0110 KKKK dddd KKKK",
    "OUT": "1011 1AAr rrrr AAAA",
    "POP": "1001 000d dddd 1111",
    "PUSH": "1001 001d dddd 1111",
    "RCALL": "1101 kkkk kkkk kkkk",
    "RET": "1001 0101 0000 1000",
    "RETI": "1001 0101 0001 1000",
    "RJMP": "1100 kkkk kkkk kkkk",
    "ROL": "0001 11dd dddd dddd",
    "ROR": "1001 010d dddd 0111",
    "SBC": "0000 10rd dddd rrrr",
    "SBCI": "0100 KKKK dddd KKKK",
    "SBI": "1001 1010 AAAA Abbb",
    "SBIC": "1001 1001 AAAA Abbb",
    "SBIS": "1001 1011 AAAA Abbb",
    "SBIW": "1001 0111 KKdd KKKK",
    "SBR": "0110 KKKK dddd KKKK",
    "SBRC": "1111 110r rrrr 0bbb",
    "SBRS": "1111 111r rrrr 0bbb",
    "SEC": "1001 0100 0000 1000",
    "SEH": "1001 0100 0101 1000",
    "SEI": "1001 0100 0111 1000",
    "SEN": "1001 0100 0010 1000",
    "SER": "1110 1111 dddd 1111",
    "SES": "1001 0100 0100 1000",
    "SET": "1001 0100 0110 1000",
    "SEV": "1001 0100 0011 1000",
    "SEZ": "1001 0100 0001 1000",
    "SLEEP": "1001 0101 1000 1000",
    "STS": "1001 001d dddd 0000 kkkk kkkk kkkk kkkk",
    "SUB": "0001 10rd dddd rrrr",
    "SUBI": "0101 KKKK dddd KKKK",
    "SWAP": "1001 010d dddd 0010",
    "TST": "0010 00dd dddd dddd",
    "WDR": "1001 0101 1010 1000",
}
# CBR, ELPM, LD (LDD), LPM, SPM, ST

REGISTER_COUNT = 31


def reg_to_addr(value: str):
    num = int(value.replace("R", ""))
    if num > 31:
        raise ValueError("Register out of range")

    return format(num, "b")


def immediate_to_bin(value: str, limit):

    if value.startswith(("0x", "0X")):
        num = int(value, 16)
        if num < limit | num > limit:
            raise ValueError(f"Immediate over the limit ({limit})")

        return format(num, "b")
    elif value.startswith(("0b", "0B")):
        num = int(value, 2)
        if num < limit | num > limit:
            raise ValueError(f"Immediate over the limit ({limit})")
        return format(num, "b")
    elif int(value) == 0:
        num = int(value)
        if num < limit | num > limit:
            raise ValueError(f"Immediate over the limit ({limit})")

        return format(num, "b")
    elif int(value):
        num = int(value)
        if num < limit | num > limit:
            raise ValueError(f"Immediate over the limit ({limit})")
        return format(num, "b")
    else:
        raise ValueError(f"Value not supported")


def value_pusher(text, character, value):
    array = []

    offset = 0
    for idx in range(0, len(text)):
        if text[idx] == character:
            array.append(value[offset])
            offset += 1
        else:
            array.append(text[idx])

    return "".join(array)


def compiler(line: str):
    if line == "" or line.startswith("#") or line == "\n" or line == "\t":
        return
    parts = line.replace(",", "").split(" ")

    opcode = OPCODE[parts[0]]

    if parts[0] in ["ADIW", "SUBI", "SBCI", "SBIW", "ANDI", "ORI", "LDI", "LDS"]:
        mask1 = value_pusher(opcode, "d", reg_to_addr(parts[1]).zfill(4))
        mask2 = value_pusher(mask1, "K", immediate_to_bin(parts[2], 0xFF).zfill(8))
        return mask2

    elif parts[0] in ["ADD", "ADC", "SUB", "SBC", "AND", "OR", "EOR", "MOV", "MOVW"]:
        mask1 = value_pusher(opcode, "d", reg_to_addr(parts[1]).zfill(5))
        mask2 = value_pusher(mask1, "r", reg_to_addr(parts[2]).zfill(5))
        return mask2
    else:
        raise ValueError(f"Unknows OPCODE: {parts[0]}:{OPCODE[parts[0]]}")


if __name__ == "__main__":
    print("--- COMPILING ---")
    binary_lines = []
    with open("input.asm", "r") as f:
        l = 1
        for line in f:
            try:
                print(f"[{l}] ", end="")
                binary = compiler(line)
                if binary != None:
                    print(f"{binary}", end="")
                    binary_lines.append(int(binary.replace(" ", ""), 2))
                print()
            except Exception as e:
                print(f"  --->  {str(e)}")
            l += 1

        f.close()

    data = struct.pack("<" + "H" * len(binary_lines), *binary_lines)
    with open("flash.bin", "wb") as f:
        f.write(data)
        f.flush()
        f.close()
    print(f"--- COMPILE COMPLETE : {len(binary_lines)} WRITED ---")
