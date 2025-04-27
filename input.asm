.data
SPL: .bytes 0x5D (0x3D on I/O Register)
SPH: .bytes 0x5E (0x3E on I/O Register)
RAMSTART: .hword 0x100
RAMEND: .hword 0x8FF

.text
_start:
    ldi r16, 0xFF
    ldi r17, 0xA0
    eor r16, r17
    JMP 0x0
    NOP