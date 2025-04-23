.data
SPL: .bytes 0x5D (0x3D on I/O Register)
SPH: .bytes 0x5E (0x3E on I/O Register)
RAMSTART: .hword 0x100
RAMEND: .hword 0x8FF

.text
skip:
    LDI R16, 0x01
    NOP
.text
noskip:
    LDI R17, 0x01
    NOP

.text
_start:
    ; INITILIZE STACK POINTER
    LDI R16, HIGH(RAMEND)
    OUT SPH, R16
    LDI R16, LOW(RAMEND)
    OUT SPL, R16
    ; BASIC CODE
    LDI R31, 0x5
    LDI R30, 0xe
    LPM
    NOP
    JMP 0x7FFF