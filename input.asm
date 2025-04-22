.data
SPL: .bytes 0x3D
SPH: .bytes 0x3E
RAMSTART: .hword 0x100
RAMEND: .hword 0x8FF

.text
setup_SP:
    

.text
basic:
    LDI R18, 0x5
    LDI R19, 0x6
    ADD R18, R19
    PUSH R18
    POP R18
    RET

.text
_start:
    ; INITILIZE STACK POINTER
    LDI R16, HIGH(RAMEND)
    OUT SPH, R16
    LDI R16, LOW(RAMEND)
    OUT SPL, R16
    ; BASIC CODE
    CALL basic
    LDI R23, 0x30
    STS 0x100, R23
    LDS R17, 0x100
    NOP
    JMP 0x7FFF