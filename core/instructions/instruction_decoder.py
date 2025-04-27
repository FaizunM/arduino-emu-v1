from core.alu import ALU


class InstructionDecoder:
    def __init__(
        self, ins_register=None, SRAM=None, PC=None, SREG=None, DefinitionMode=False
    ):
        self.DefinitionMode = DefinitionMode
        if not DefinitionMode:
            self.alu = ALU(ins_register, SRAM, PC, SREG)

    def decode(self, operation: int):
        if operation > 0xFFFF:
            words = format(operation, "b").zfill(32)
            word1 = int(words[:16], 2)
            word2 = int(words[16:], 2)
            # JMP
            if word2 >> 9 & 0b1111111 == 0b1001010 and word2 >> 1 & 0b111 == 0b110:
                dest_H = word2 >> 4 & 0b11111
                dest_L = word2 & 0b1
                destination = (dest_H << 17) | (dest_L << 1) | word1

                if not self.DefinitionMode:
                    self.alu.JMP(destination)

                return f"JMP {hex(destination)}"

            # LDS
            elif word2 >> 9 & 0x7F == 0x48 and word2 & 0xF == 0b000:
                destination = word2 >> 4 & 0b11111
                source = word1 & 0xFFFF

                if not self.DefinitionMode:
                    self.alu.LDS(destination, source)

                return f"LDS R{destination}, { hex(source) }"

            # CALL
            elif word2 >> 9 & 0b1111111 == 0b1001010 and word2 >> 0x1 & 0b111 == 0b111:
                dest_H = word2 >> 4 & 0b11111
                dest_L = word2 & 0b1
                destination = (dest_H << 17) | (dest_L << 1) | word1

                if not self.DefinitionMode:
                    self.alu.CALL(destination)

                return f"CALL { hex(destination) }"
            # STS
            elif word2 >> 9 & 0b1111111 == 0b1001001 and word2 & 0b1111 == 0b0000:
                source = word2 >> 4 & 0b11111
                destination = word1 & 0xFFFF

                if not self.DefinitionMode:
                    self.alu.STS(destination, source)
                    pass

                return f"STS {hex(destination)}, R{ source }"

        if operation == 0x0:
            if not self.DefinitionMode:
                self.alu.NOP()
            return f"NOP"
        # ADC / ROL
        elif (operation >> 10) & 0b111111 == 0b000111:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = ((high << 5) | low) - 16
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"ADC/ROL R{destination}, R{source}"

        # ADD / LSL
        elif (operation >> 10) & 0b111111 == 0b000011:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.ADD(destination, source)

            return f"ADD/LSL R{destination}, R{source}"

        # ADIW
        elif (operation >> 8) & 0b11111111 == 0b10010110:
            destination = ((operation >> 4) & 0b11) + 24
            high = (operation >> 6) & 0b11
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.ADIW(destination, source)
                pass

            return f"ADIW R{destination}, {hex(source)}"

        # AND/TST
        elif (operation >> 10) & 0b111111 == 0b001000:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.AND(destination, source)

            return f"AND R{destination}, R{source}"
            # if source == 0x0:
            # return f"TST R{destination}"
            # else:

        # ANDI/CBR
        elif (operation >> 12) & 0b1111 == 0b0111:
            destination = ((operation >> 4) & 0b1111) + 16
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.ANDI(destination, source)

            return f"ANDI/CBR R{destination}, {hex(source)}"

        # ASR
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0101:
            destination = ((operation >> 4) & 0b1111) + 16
            if not self.DefinitionMode:
                self.alu.ASR(destination)

            return f"ASR R{destination}"

        # SEH
        elif (operation) & 0b1111111111111111 == 0b1001010001011000:
            if not self.DefinitionMode:
                self.alu.SEH()
                pass

            return f"SEH"

        # SEI
        elif (operation) & 0b1111111111111111 == 0b1001010001111000:
            if not self.DefinitionMode:
                self.alu.SEI()
                pass

            return f"SEI"

        # SEN
        elif (operation) & 0b1111111111111111 == 0b1001010000101000:
            if not self.DefinitionMode:
                self.alu.SEN()

                pass

            return f"SEN"

        # SEC
        elif (operation) & 0b1111111111111111 == 0b1001010000001000:
            if not self.DefinitionMode:
                self.alu.SEC()
                pass

            return f"SEC"

        # LDI
        elif (operation >> 12) & 0b1111 == 0b1110:
            destination = ((operation >> 4) & 0b1111) + 16
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.LDI(destination, source)

            return f"LDI R{destination}, {hex(source)}"

        # SER
        elif (
            operation >> 8
        ) & 0b11111111 == 0b11101111 and operation & 0b1111 == 0b1111:
            if not self.DefinitionMode:
                self.alu.SER()

                pass

            return f"SER"

        # SES
        elif (operation) & 0b1111111111111111 == 0b1001010001001000:
            if not self.DefinitionMode:
                self.alu.SES()

                pass

            return f"SES"

        # SET
        elif (operation) & 0b1111111111111111 == 0b1001010001101000:
            if not self.DefinitionMode:
                self.alu.SET()

                pass

            return f"SET"

        # SEV
        elif (operation) & 0b1111111111111111 == 0b1001010000111000:
            if not self.DefinitionMode:
                self.alu.SEV()

                pass

            return f"SEV"

        # SEZ
        elif (operation) & 0b1111111111111111 == 0b1001010000011000:
            if not self.DefinitionMode:
                self.alu.SEZ()

                pass

            return f"SEZ"

        # SLEEP
        elif (operation) & 0b1111111111111111 == 0b1001010110001000:
            if not self.DefinitionMode:
                self.alu.SLEEP()

                pass

            return f"SLEEP"

        # SPM
        elif (operation) & 0b1111111111111111 == 0b1001010111101000:
            if not self.DefinitionMode:

                pass

            return f"SPM"

        # BCLR
        elif (
            operation >> 7
        ) & 0b111111111 == 0b100101001 and operation & 0b1111 == 0b1000:
            destination = (operation >> 4) & 0b111
            if not self.DefinitionMode:
                self.alu.BCLR(destination)

            return f"BCLR {destination}"

        # CLC
        elif (operation) & 0b1111111111111111 == 0b1001010010001000:
            if not self.DefinitionMode:
                self.alu.CLC()

            return f"CLC"
        # CLH
        elif (operation) & 0b1111111111111111 == 0b1001010011011000:
            if not self.DefinitionMode:
                self.alu.CLH()

            return f"CLH"
        # CLI
        elif (operation) & 0b1111111111111111 == 0b1001010011111000:
            if not self.DefinitionMode:
                self.alu.CLI()
                pass

            return f"CLI"
        # CLN
        elif (operation) & 0b1111111111111111 == 0b1001010010101000:
            if not self.DefinitionMode:
                self.alu.CLN()

            return f"CLN"
        # CLS
        elif (operation) & 0b1111111111111111 == 0b1001010011001000:
            if not self.DefinitionMode:
                self.alu.CLS()

            return f"CLS"
        # CLT
        elif (operation) & 0b1111111111111111 == 0b1001010011101000:
            if not self.DefinitionMode:
                self.alu.CLT()

            return f"CLT"
        # CLV
        elif (operation) & 0b1111111111111111 == 0b1001010010111000:
            if not self.DefinitionMode:
                self.alu.CLV()

            return f"CLV"
        # CLZ
        elif (operation) & 0b1111111111111111 == 0b1001010010011000:
            if not self.DefinitionMode:
                self.alu.CLZ()

            return f"CLZ"

        # BLD
        elif (operation >> 9) & 0b1111111 == 0b1111100 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                self.alu.BLD(destination, source)
                pass

            return f"BLD R{destination}, {source}"

        # BRCC dan BRSH
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b000:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRCC(destination)

            return f"BRCC/BRSH {hex(destination)}"

        # BRCS dan BRLO
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b000:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRLO(destination)

            return f"BRCS/BRLO {hex(destination)}"

        # BREQ
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b001:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BREQ(destination)

            return f"BREQ {hex(destination)}"
        # BRHS
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b101:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRHS(destination)

            return f"BRHS {hex(destination)}"

        # BRBS
        elif (operation >> 10) & 0b111111 == 0b111100:
            destination = (operation) & 0b111
            source = operation >> 3 & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRBS(destination, source)
                pass

            return f"BRBS {destination}, {source}"

        # BRGE
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b100:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRGE(destination)

            return f"BRGE {hex(destination)}"

        # BRHC
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b101:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRHC(destination)

            return f"BRHC {hex(destination)}"

        # BRID
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b111:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRID(destination)

            return f"BRID {hex(destination)}"

        # BRIE
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b111:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRIE(destination)

            return f"BRIE {hex(destination)}"

        # BRLT
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b100:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRLT(destination)

            return f"BRLT {hex(destination)}"

        # BRMI
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b010:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRMI(destination)

            return f"BRMI {hex(destination)}"

        # BRBC
        elif (operation >> 10) & 0b111111 == 0b111101:
            destination = (operation) & 0b111
            source = operation >> 3 & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRBC(destination, source)

            return f"BRBC {destination}, {hex(source)}"

        # BRNE
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b001:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRNE(destination)

            return f"BRNE {hex(destination)}"

        # BRPL
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b010:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRPL(destination)

            return f"BRPL {hex(destination)}"

        # BRTC
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b110:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRTC(destination)

            return f"BRTC {hex(destination)}"

        # BRTS
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b110:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRTS(destination)

            return f"BRTS {hex(destination)}"

        # BRVC
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b011:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRVC(destination)

            return f"BRVC {hex(destination)}"

        # BRVS
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b011:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                self.alu.BRVS(destination)

            return f"BRVS {hex(destination)}"

        # BREAK
        elif (operation) & 0b1111111111111111 == 0b1001010110011000:
            if not self.DefinitionMode:
                self.alu.BREAK()

            return f"BREAK"
        # BSET
        elif (
            operation >> 7
        ) & 0b111111111 == 0b100101000 and operation & 0b1111 == 0b1000:
            destination = (operation >> 4) & 0b111
            if not self.DefinitionMode:
                self.alu.BSET(destination)

            return f"BSET {destination}"
        # BST
        elif (operation >> 9) & 0b1111111 == 0b1111101 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                self.alu.BST(destination, source)

            return f"BST R{destination}, {source}"

        # CBI
        elif operation >> 8 & 0b11111111 == 0b10011000:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                self.alu.CBI(destination, source)

            return f"CBI { hex(destination) }, {source}"
        # EOR
        elif (operation >> 10) & 0b111111 == 0b001001:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:

                pass

            return f"EOR R{destination}, R{source}"
        # CLR
        elif operation >> 10 & 0b111111 == 0b001001:
            destination = (operation) & 0b1111111111

            if not self.DefinitionMode:
                self.alu.CLR(destination)

            return f"CLR R{ destination }"
        # COM
        elif operation >> 9 & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0000:
            destination = (operation >> 4) & 0b11111

            if not self.DefinitionMode:
                # self.alu.CALL(destination)
                pass

            return f"COM R{ destination }"

        # CP
        elif (operation >> 10) & 0b111111 == 0b000101:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.CP(destination, source)

            return f"CP R{destination}, R{source}"
        # CPC
        elif (operation >> 10) & 0b111111 == 0b000001:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.CPC(destination, source)

            return f"CPC R{destination}, R{source}"
        # CPI
        elif (operation >> 12) & 0b1111 == 0b0011:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.CPC(destination, source)

            return f"CPI R{destination}, {source}"
        # CPSE
        elif (operation >> 10) & 0b111111 == 0b000100:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.CPC(destination, source)

                pass

            return f"CPSE R{destination}, R{source}"
        # DEC
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b1010:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.DEC(destination)

            return f"DEC R{destination}"

        # FMUL
        elif (
            operation >> 7
        ) & 0b111111111 == 0b000000110 and operation >> 3 & 0b1 == 1:
            destination = ((operation >> 4) & 0b111) + 16
            source = (operation & 0b111) + 16
            if not self.DefinitionMode:
                self.alu.FMUL(destination, source)

            return f"FMUL R{destination}, R{source}"

        # FMULS
        elif (
            operation >> 7
        ) & 0b111111111 == 0b000000111 and operation >> 3 & 0b1 == 0:
            destination = (operation >> 4) & 0b111
            source = operation & 0b111
            if not self.DefinitionMode:

                pass

            return f"FMULS R{destination}, R{source}"

        # FMULSU
        elif (
            operation >> 7
        ) & 0b111111111 == 0b000000111 and operation >> 3 & 0b1 == 1:
            destination = (operation >> 4) & 0b111
            source = operation & 0b111
            if not self.DefinitionMode:

                pass

            return f"FMULSU R{destination}, R{source}"

        # ICALL
        elif (operation) & 0b1111111111111111 == 0b1001010100001001:
            if not self.DefinitionMode:
                self.alu.ICALL()

            return f"ICALL"

        # IJUMP
        elif (operation) & 0b1111111111111111 == 0b1001010000001001:
            if not self.DefinitionMode:
                self.alu.IJMP()

            return f"IJUMP"

        # IN
        elif (operation >> 11) & 0b11111 == 0b10110:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b11
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.IN(destination, source)

            return f"IN R{destination}, {hex(source)}"
        # INC
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0011:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.INC(destination, source)

            return f"INC R{destination}"

        # LSR
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0110:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.LSR(destination)

            return f"LSR R{destination}"

        # MOV
        elif (operation >> 10) & 0b111111 == 0b001011:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low

            if not self.DefinitionMode:
                self.alu.MOV(destination, source)

            return f"MOV R{destination}, R{source}"

        # MOVW
        elif (operation >> 8) & 0b11111111 == 0b00000001:
            destination = (operation >> 4) & 0b1111
            source = operation & 0b1111
            if not self.DefinitionMode:
                self.alu.MOVW(destination, source)

            return f"MOVW R{destination+1}:R{destination}, R{source+1}:R{source}"

        # MUL
        elif (operation >> 10) & 0b111111 == 0b100111:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                self.alu.MUL(destination, source)

            return f"MUL R{destination}, R{source}"

        # MULS
        elif (operation >> 8) & 0b11111111 == 0b00000010:
            destination = (operation >> 4) & 0b1111
            source = operation & 0b1111
            # if not self.DefinitionMode:
            #     self.alu.ADC(destination, source)

            return f"MULS R{destination}, {source}"

        # NEG
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0001:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.NEG(destination, source)

            return f"NEG R{destination}"

        # OR
        elif (operation >> 10) & 0b111111 == 0b001010:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                self.alu.OR(destination, source)

            return f"OR R{destination}, {source}"

        # ORI/SBR
        elif (operation >> 12) & 0b1111 == 0b0110:
            destination = ((operation >> 4) & 0b1111) + 16
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.ORI(destination, source)
                pass

            return f"ORI/SBR R{destination}, {source}"

        # OUT
        elif (operation >> 11) & 0b11111 == 0b10111:
            high = (operation >> 9) & 0b11
            low = (operation) & 0b1111
            destination = (high << 4) | low
            source = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.OUT(destination, source)

            return f"OUT {hex(destination)}, R{source}"

        elif (operation >> 9) & 0b1111111 == 0b1001000 and (
            (operation & 0b1111 == 0b1100)
            or operation & 0b1111 == 0b1101
            or operation & 0b1111 == 0b1110
        ):
            destination = operation >> 4 & 0b11111
            source = operation & 0x1111
            type = None

            if not self.DefinitionMode:
                self.alu.LDX(destination, source)

            if operation & 0b1111 == 0b1100:
                type = "X"
            elif operation & 0b1111 == 0b1101:
                type = "X+"
            elif operation & 0b1111 == 0b1110:
                type = "-X"

            return f"LD R{destination}, {type}"

        elif (
            (operation >> 9) & 0b1111111 == 0b1000000
            or (operation >> 9) & 0b1111111 == 0b1001000
        ) and (
            (operation & 0b1111 == 0b1000)
            or operation & 0b1111 == 0b1001
            or operation & 0b1111 == 0b1010
        ):
            destination = operation >> 4 & 0b11111
            source = operation & 0x1111
            type = None

            if not self.DefinitionMode:
                self.alu.LDY(destination, source)

            if operation & 0b1111 == 0b1000:
                type = "Y"
            elif operation & 0b1111 == 0b1001:
                type = "Y+"
            elif operation & 0b1111 == 0b1010:
                type = "-Y"

            return f"LD R{destination}, {type}"

        elif (
            (operation >> 9) & 0b1111111 == 0b1000000
            or (operation >> 9) & 0b1111111 == 0b1001000
        ) and (
            (operation & 0b1111 == 0b0000)
            or operation & 0b1111 == 0b0001
            or operation & 0b1111 == 0b0010
        ):
            destination = operation >> 4 & 0b11111
            source = operation & 0x1111
            type = None

            if not self.DefinitionMode:
                self.alu.LDZ(destination, source)

            if operation & 0b1111 == 0b0000:
                type = "Z"
            elif operation & 0b1111 == 0b0001:
                type = "Z+"
            elif operation & 0b1111 == 0b0010:
                type = "-Z"
        elif (operation >> 9) & 0b1111111 == 0b1001001 and (
            (operation & 0b1111 == 0b1100)
            or operation & 0b1111 == 0b1101
            or operation & 0b1111 == 0b1110
        ):
            destination = operation >> 4 & 0b11111
            source = operation & 0x1111
            type = None

            if not self.DefinitionMode:
                self.alu.STX(destination, source)

            if operation & 0b1111 == 0b1100:
                type = "X"
            elif operation & 0b1111 == 0b1101:
                type = "X+"
            elif operation & 0b1111 == 0b1110:
                type = "-X"

            return f"ST R{destination}, {type}"

        elif (
            (operation >> 9) & 0b1111111 == 0b1000000
            or (operation >> 9) & 0b1111111 == 0b1001001
        ) and (
            (operation & 0b1111 == 0b1000)
            or operation & 0b1111 == 0b1001
            or operation & 0b1111 == 0b1010
        ):
            destination = operation >> 4 & 0b11111
            source = operation & 0x1111
            type = None

            if not self.DefinitionMode:
                self.alu.STY(destination, source)

            if operation & 0b1111 == 0b1000:
                type = "Y"
            elif operation & 0b1111 == 0b1001:
                type = "Y+"
            elif operation & 0b1111 == 0b1010:
                type = "-Y"

            return f"ST R{destination}, {type}"

        elif (
            (operation >> 9) & 0b1111111 == 0b1000000
            or (operation >> 9) & 0b1111111 == 0b1001001
        ) and (
            (operation & 0b1111 == 0b0000)
            or operation & 0b1111 == 0b0001
            or operation & 0b1111 == 0b0010
        ):
            destination = operation >> 4 & 0b11111
            source = operation & 0x1111
            type = None

            if not self.DefinitionMode:
                self.alu.STZ(destination, source)

            if operation & 0b1111 == 0b0000:
                type = "Z"
            elif operation & 0b1111 == 0b0001:
                type = "Z+"
            elif operation & 0b1111 == 0b0010:
                type = "-Z"

            return f"ST R{destination}, {type}"
        elif operation & 0b1111111111111111 == 0b1001010111001000:
            if not self.DefinitionMode:
                self.alu.LPM()

            return f"LPM"
        elif (
            operation >> 9 & 0b1111111 == 0b1001000
            and (operation & 0b1111 == 0b0100)
            or (operation & 0b1111 == 0b0101)
        ):
            destination = operation >> 4 & 0b11111
            source = operation & 0x1111
            type = None

            if not self.DefinitionMode:
                self.alu.LPMZ(destination, source)

            if operation & 0b1111 == 0b0100:
                type = "Z"
            elif operation & 0b1111 == 0b0101:
                type = "Z+"
            return f"LPM R{destination}, {type}"
        # POP
        elif (operation >> 9) & 0b1111111 == 0b1001000 and operation & 0b1111 == 0b1111:
            destination = ((operation >> 4) & 0b1111) + 16
            if not self.DefinitionMode:
                self.alu.POP(destination)

            return f"POP R{destination}"

        # PUSH
        elif (operation >> 9) & 0b1111111 == 0b1001001 and operation & 0b1111 == 0b1111:
            destination = (operation >> 4) & 0b1111 + 16
            if not self.DefinitionMode:
                self.alu.PUSH(destination)
                pass

            return f"PUSH R{destination}"

        # RCALL
        elif (operation >> 12) & 0b1111 == 0b1101:
            destination = (operation) & 0b111111111111
            if not self.DefinitionMode:
                self.alu.RCALL(destination)

            return f"RCALL {hex(destination)}"

        # RET
        elif (operation) & 0b1111111111111111 == 0b1001010100001000:
            if not self.DefinitionMode:
                self.alu.RET()

            return f"RET"

        # RETI
        elif (operation) & 0b1111111111111111 == 0b1001010100011000:
            if not self.DefinitionMode:
                self.alu.RETI()

                pass

            return f"RETI"

        # RJMP
        elif (operation >> 12) & 0b1111 == 0b1100:
            KKK = (operation) & 0b111111111111
            if KKK >> 11 & 0b1 == 0b1:
                destination = int(
                    f"-{self.flip_binary(format(int(KKK), 'b').zfill(12))}", 2
                )
            else:
                destination = KKK
            if not self.DefinitionMode:
                self.alu.RJMP(destination)

            return f"RJMP {destination}"

        # ROR
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0111:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.ROR(destination)

            return f"ROR R{destination}"

        # SBC
        elif (operation >> 10) & 0b111111 == 0b000010:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                self.alu.SBC(destination, source)

            return f"SBC R{destination}, {source}"

        # SBCI
        elif (operation >> 12) & 0b1111 == 0b0100:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.SBCI(destination, source)


            return f"SBCI R{destination}, {hex(source)}"

        # SBI
        elif operation >> 8 & 0b11111111 == 0b10011010:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                self.alu.SBI(destination, source)

            return f"SBI { hex(destination) }, {source}"

        # SBIC
        elif operation >> 8 & 0b11111111 == 0b10011001:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                self.alu.SBIC(destination, source)

            return f"SBIC { destination }, {source}"

        # SBIS
        elif operation >> 8 & 0b11111111 == 0b10011011:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                self.alu.SBIS(destination, source)

            return f"SBIS { destination }, {source}"

        # SBIW
        elif (operation >> 8) & 0b11111111 == 0b10010111:
            destination = (operation >> 4) & 0b11
            high = (operation >> 6) & 0b11
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.SBIW(destination, source)

            return f"SBIW R{destination}, {source}"

        # SBRC
        elif (operation >> 9) & 0b1111111 == 0b1111110 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                self.alu.SBRC(destination, source)
                

            return f"SBRC R{destination}"

        # SBRS
        elif (operation >> 9) & 0b1111111 == 0b1111111 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                self.alu.SBRS(destination, source)

            return f"SBRS R{destination}"

        # SUB
        elif (operation >> 10) & 0b111111 == 0b000110:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = ((high << 5) | low) - 16
            if not self.DefinitionMode:
                self.alu.SUB(destination, source)
                pass

            return f"SUB R{destination}, {source}"

        # SUBI
        elif (operation >> 12) & 0b1111 == 0b0101:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.SUBI(destination, source)

            return f"SUBI R{destination}, {source}"

        # SWAP
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0010:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.SUBI(destination)
                pass

            return f"SWAP R{destination}"

        # WDR
        elif (operation) & 0b1111111111111111 == 0b1001010110101000:
            if not self.DefinitionMode:
                self.alu.WDR()

                pass

            return f"WDR"

        else:
            if not self.DefinitionMode:
                self.alu.PC.address += 1
            else:
                return "Unknown OPCODE"

    def flip_binary(self, value):
        return "".join("1" if bit == "0" else "0" for bit in value)
