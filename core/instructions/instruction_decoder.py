from core.alu import ALU


class InstructionDecoder:
    def __init__(self, ins_register = None, SRAM = None, PC = None, DefinitionMode = False):
        self.DefinitionMode = DefinitionMode
        if not DefinitionMode:
            self.alu = ALU(ins_register, SRAM, PC)
        

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
                    # self.alu.CALL(destination)
                    pass
    
                return f"JMP {hex(destination)}"

            # LDS
            elif word2 >> 9 & 0x7F == 0x48 and word2 & 0xF == 0b000:
                destination = word2 >> 4 & 0b11111
                source = word1 & 0xFFFF

                if not self.DefinitionMode:
                    # self.alu.CALL(destination)
                    pass
    
                return f"LDS R{destination}, { hex(source) }"

            # CALL
            elif word2 >> 9 & 0b1111111 == 0b1001010 and word2 >> 0x1 & 0b111 == 0b111:
                dest_H = word2 >> 4 & 0b11111
                dest_L = word2 & 0b1
                destination = (dest_H << 17) | (dest_L << 1) | word1

                if not self.DefinitionMode:
                    # self.alu.CALL(destination)
                    pass
    
                return f"CALL { hex(destination) }"
            # STS
            elif word2 >> 9 & 0b1111111 == 0b1001001 and word2 & 0b1111 == 0b0000:
                destination = word2 >> 4 & 0b11111
                source = word1 & 0xFFFF

                if not self.DefinitionMode:
                    # self.alu.CALL(destination)
                    pass
    
                return f"STS R{destination}, { hex(source) }"
        if operation == 0x0:
            return f"NOP"
        # ADC / ROL
        elif (operation >> 10) & 0b111111 == 0b000111:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"ADC/ROL R{destination}, {source}"

        # ADD / LSL
        elif (operation >> 10) & 0b111111 == 0b000011:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"ADD/LSL R{destination}, {source}"

        # ADIW
        elif (operation >> 8) & 0b11111111 == 0b10010110:
            destination = (operation >> 4) & 0b11
            high = (operation >> 6) & 0b11
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"ADIW R{destination}, {source}"

        # AND/TST
        elif (operation >> 10) & 0b111111 == 0b001000:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass
            if source == 0x0:
                return f"TST R{destination}"
            else:
                return f"AND R{destination}, {source}"

        # ANDI/CBR
        elif (operation >> 12) & 0b1111 == 0b0111:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"ANDI/CBR R{destination}, {source}"

        # ASR
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0101:
            destination = (operation >> 4) & 0b1111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"ASR R{destination}"

        # SEH
        elif (operation) & 0b1111111111111111 == 0b1001010001011000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SEH"

        # SEI
        elif (operation) & 0b1111111111111111 == 0b1001010001111000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SEI"

        # SEN
        elif (operation) & 0b1111111111111111 == 0b1001010000101000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SEN"

        # SEC
        elif (operation) & 0b1111111111111111 == 0b1001010000001000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SEC"

        # SER
        elif (
            operation >> 8
        ) & 0b11111111 == 0b11101111 and operation & 0b1111 == 0b1111:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SER"

        # SES
        elif (operation) & 0b1111111111111111 == 0b1001010001001000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SES"

        # SET
        elif (operation) & 0b1111111111111111 == 0b1001010001101000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SET"

        # SEV
        elif (operation) & 0b1111111111111111 == 0b1001010000111000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SEV"

        # SEZ
        elif (operation) & 0b1111111111111111 == 0b1001010000011000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SEZ"

        # SLEEP
        elif (operation) & 0b1111111111111111 == 0b1001010110001000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SLEEP"

        # SPM
        elif (operation) & 0b1111111111111111 == 0b1001010111101000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SPM"

        # CLC
        elif (operation) & 0b1111111111111111 == 0b1001010010001000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLC"
        # CLH
        elif (operation) & 0b1111111111111111 == 0b1001010011011000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLH"
        # CLI
        elif (operation) & 0b1111111111111111 == 0b1001010011111000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLI"
        # CLN
        elif (operation) & 0b1111111111111111 == 0b1001010010101000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLN"
        # CLS
        elif (operation) & 0b1111111111111111 == 0b1001010011001000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLS"
        # CLT
        elif (operation) & 0b1111111111111111 == 0b1001010011101000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLT"
        # CLV
        elif (operation) & 0b1111111111111111 == 0b1001010010111000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLV"
        # CLZ
        elif (operation) & 0b1111111111111111 == 0b1001010010011000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CLZ"
        # BCLR
        elif (
            operation >> 7
        ) & 0b111111111 == 0b100101001 and operation & 0b1111 == 0b1000:
            destination = (operation >> 4) & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BCLR {destination}"

        # BLD
        elif (operation >> 9) & 0b1111111 == 0b1111100 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BLD R{destination}, {source}"

        # BRCC dan BRSH
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b000:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRCC/BRSH {hex(destination)}"

        # BRCS dan BRLO
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b000:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRCS/BRLO {hex(destination)}"

        # BREQ
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b001:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BREQ {hex(destination)}"

        # BRGE
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b100:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRGE {hex(destination)}"

        # BRHC
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b101:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRHC {hex(destination)}"

        # BRHS
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b101:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRHS {hex(destination)}"

        # BRID
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b111:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRID {hex(destination)}"

        # BRIE
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b111:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRIE {hex(destination)}"

        # BRLT
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b100:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRLT {hex(destination)}"

        # BRMI
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b010:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRMI {hex(destination)}"

        # BRNE
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b001:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRNE {hex(destination)}"

        # BRPL
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b010:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRPL {hex(destination)}"

        # BRTC
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b110:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRTC {hex(destination)}"

        # BRTS
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b110:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRTS {hex(destination)}"

        # BRVC
        elif (operation >> 10) & 0b111111 == 0b111101 and operation & 0b111 == 0b011:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRVC {hex(destination)}"

        # BRVS
        elif (operation >> 10) & 0b111111 == 0b111100 and operation & 0b111 == 0b011:
            destination = (operation >> 3) & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRVS {hex(destination)}"

        # BRBC
        elif (operation >> 10) & 0b111111 == 0b111101:
            destination = (operation) & 0b111
            source = operation >> 3 & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRBC {destination}, {hex(source)}"

        # BRBS
        elif (operation >> 10) & 0b111111 == 0b111100:
            destination = (operation) & 0b111
            source = operation >> 3 & 0b1111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BRBS {destination}, {hex(source)}"

        # BREAK
        elif (operation) & 0b1111111111111111 == 0b1001010110011000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BREAK"
        # BSET
        elif (
            operation >> 7
        ) & 0b111111111 == 0b100101000 and operation & 0b1111 == 0b1000:
            destination = (operation >> 4) & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BSET {destination}"
        # BST
        elif (operation >> 9) & 0b1111111 == 0b1111101 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"BST R{destination}, {source}"

        # CBI
        elif operation >> 8 & 0b11111111 == 0b10011000:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                # self.alu.CALL(destination)
                pass

            return f"CBI { destination }, {source}"
        # EOR
        elif (operation >> 10) & 0b111111 == 0b001001:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"EOR R{destination}, R{source}"
        # CLR
        elif operation >> 10 & 0b111111 == 0b001001:
            destination = (operation) & 0b1111111111

            if not self.DefinitionMode:
                # self.alu.CALL(destination)
                pass

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
                # self.alu.ADD(destination, source)
                pass

            return f"CP R{destination}, R{source}"
        # CPC
        elif (operation >> 10) & 0b111111 == 0b000001:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CPC R{destination}, R{source}"
        # CPI
        elif (operation >> 12) & 0b1111 == 0b0011:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CPI R{destination}, {source}"
        # CPSE
        elif (operation >> 10) & 0b111111 == 0b000100:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"CPSE R{destination}, R{source}"
        # DEC
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b1010:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"DEC R{destination}"
        # EICALL
        elif (operation) & 0b1111111111111111 == 0b1001010100011001:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"EICALL"
        # EIJMP
        elif (operation) & 0b1111111111111111 == 0b1001010000011001:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"EIJMP"

        # FMUL
        elif (
            operation >> 7
        ) & 0b111111111 == 0b000000110 and operation >> 3 & 0b1 == 1:
            destination = (operation >> 4) & 0b111
            source = operation & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"FMUL R{destination}, R{source}"

        # FMULS
        elif (
            operation >> 7
        ) & 0b111111111 == 0b000000111 and operation >> 3 & 0b1 == 0:
            destination = (operation >> 4) & 0b111
            source = operation & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"FMULS R{destination}, R{source}"

        # FMULSU
        elif (
            operation >> 7
        ) & 0b111111111 == 0b000000111 and operation >> 3 & 0b1 == 1:
            destination = (operation >> 4) & 0b111
            source = operation & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"FMULSU R{destination}, R{source}"

        # ICALL
        elif (operation) & 0b1111111111111111 == 0b1001010100001001:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"ICALL"

        # IJUMP
        elif (operation) & 0b1111111111111111 == 0b1001010000001001:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"IJUMP"

        # IN
        elif (operation >> 11) & 0b11111 == 0b10110:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b11
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.SUB(destination, source)
                pass

            return f"IN R{destination}, {source}"
        # INC
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0011:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"INC R{destination}"

        # LDI
        elif (operation >> 12) & 0b1111 == 0b1110:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                self.alu.LDI(destination, source)

            return f"LDI R{destination}, {source}"

        # LSR
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0110:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"LSR R{destination}"

        # MOV
        elif (operation >> 10) & 0b111111 == 0b001011:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"MOV R{destination}, {source}"

        # MOVW
        elif (operation >> 8) & 0b11111111 == 0b00000001:
            destination = (operation >> 4) & 0b1111
            source = operation & 0b1111
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"MOVW R{destination}, {source}"

        # MUL
        elif (operation >> 10) & 0b111111 == 0b100111:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"MUL R{destination}, {source}"

        # MULS
        elif (operation >> 8) & 0b11111111 == 0b00000010:
            destination = (operation >> 4) & 0b1111
            source = operation & 0b1111
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"MULS R{destination}, {source}"

        # NEG
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0001:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"NEG R{destination}"

        # OR
        elif (operation >> 10) & 0b111111 == 0b001010:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                self.alu.ADC(destination, source)

            return f"OR R{destination}, {source}"

        # ORI/SBR
        elif (operation >> 12) & 0b1111 == 0b0110:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"ORI/SBR R{destination}, {source}"

        # OUT
        elif (operation >> 11) & 0b11111 == 0b10111:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b11
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.SUB(destination, source)
                pass

            return f"OUT R{destination}, {source}"

        # POP
        elif (operation >> 9) & 0b1111111 == 0b1001000 and operation & 0b1111 == 0b1111:
            destination = (operation >> 4) & 0b1111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"POP R{destination}"

        # PUSH
        elif (operation >> 9) & 0b1111111 == 0b1001001 and operation & 0b1111 == 0b1111:
            destination = (operation >> 4) & 0b1111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"PUSH R{destination}"

        # RCALL
        elif (operation >> 12) & 0b1111 == 0b1101:
            destination = (operation) & 0b111111111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"RCALL {hex(destination)}"

        # RET
        elif (operation) & 0b1111111111111111 == 0b1001010100001000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"RET"

        # RETI
        elif (operation) & 0b1111111111111111 == 0b1001010100011000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"RETI"

        # RJMP
        elif (operation >> 12) & 0b1111 == 0b1101:
            destination = (operation) & 0b111111111111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"RJMP {hex(destination)}"

        # ROR
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0111:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

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
                # self.alu.ADD(destination, source)
                pass

            return f"SBCI R{destination}, {source}"

        # SBI
        elif operation >> 8 & 0b11111111 == 0b10011010:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                # self.alu.CALL(destination)
                pass

            return f"SBI { destination }, {source}"

        # SBIC
        elif operation >> 8 & 0b11111111 == 0b10011001:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                # self.alu.CALL(destination)
                pass

            return f"SBIC { destination }, {source}"

        # SBIS
        elif operation >> 8 & 0b11111111 == 0b10011011:
            destination = (operation >> 3) & 0b11111
            source = operation & 0b111

            if not self.DefinitionMode:
                # self.alu.CALL(destination)
                pass

            return f"SBIS { destination }, {source}"

        # SBIW
        elif (operation >> 8) & 0b11111111 == 0b10010111:
            destination = (operation >> 4) & 0b11
            high = (operation >> 6) & 0b11
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SBIW R{destination}, {source}"

        # SBRC
        elif (operation >> 9) & 0b1111111 == 0b1111110 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SBRC R{destination}"

        # SBRS
        elif (operation >> 9) & 0b1111111 == 0b1111111 and operation >> 3 & 0b1 == 0b0:
            destination = (operation >> 4) & 0b11111
            source = operation & 0b111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SBRS R{destination}"

        # SUB
        elif (operation >> 10) & 0b111111 == 0b000110:
            destination = (operation >> 4) & 0b11111
            high = (operation >> 9) & 0b1
            low = (operation) & 0b1111
            source = (high << 5) | low
            if not self.DefinitionMode:
                # self.alu.SUB(destination, source)
                pass

            return f"SUB R{destination}, {source}"

        # SUBI
        elif (operation >> 12) & 0b1111 == 0b0101:
            destination = (operation >> 4) & 0b1111
            high = (operation >> 8) & 0b1111
            low = (operation) & 0b1111
            source = (high << 4) | low
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SUBI R{destination}, {source}"

        # SWAP
        elif (operation >> 9) & 0b1111111 == 0b1001010 and operation & 0b1111 == 0b0010:
            destination = (operation >> 4) & 0b11111
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"SWAP R{destination}"

        # WDR
        elif (operation) & 0b1111111111111111 == 0b1001010110101000:
            if not self.DefinitionMode:
                # self.alu.ADD(destination, source)
                pass

            return f"WDR"

        else:
            if not self.DefinitionMode:

                raise ValueError("Unknown OPCODE")
            else:
                return "Unknown OPCODE"
