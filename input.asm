.data
x1: .hword 20
x2: .hword 30
x3: .hword 15

.text
basic_sub:
    LDI R1, x1
    LDI R2, 0x01
    SUB R1, R2
    RET

.text
basic_add:
    LDI R3, 0xFF
    LDI R4, x2
    add R3, R4
    RET

.text
_start:
    LDI R10, x3
    LDI R11, x2
    add R10, R11
    CALL basic_add
    CALL basic_sub
