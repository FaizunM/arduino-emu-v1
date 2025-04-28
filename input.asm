.data
SPL: .bytes 0x5D (0x3D on I/O Register)
SPH: .bytes 0x5E (0x3E on I/O Register)
RAMSTART: .hword 0x100
RAMEND: .hword 0x8FF

.text
all_func:
    ldi r25, 0x1f
    ldi r23, 0x1f
    adc r16, r17
    NOP

.text
basic_math:
    ldi r25, 0x1f
    ldi r23, 0x1f
    adc r16, r17
    NOP

.text
basic:
    ldi r25, 0x1f
    ldi r23, 0x1f
    adc r16, r17
    NOP

.text
_start:
    ldi r16, 0xFF
    ldi r17, 0xA0
    adc r16, r17
    bset 6
    brbc 6, all_func
    brbs 6, basic