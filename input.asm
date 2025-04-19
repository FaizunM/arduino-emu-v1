LDI R1, 0xFF
LDI R2, 0x01
ADD R1, R2

LDI R2, 0x10
ADC R1, R2

LDI R1, 0xFF
LDI R2, 0x01
SUB R1, R2

LDI R2, 0x10
SBC R1, R2

ADIW X, 63

ldi r16, 0x10 ; Load decimal 16 into r16
asr r16 ; r16=r16 / 2
ldi r17, 0xFC ; Load -4 in r17
asr r17 ; r17=r17/2

bclr 0 ; Clear Carry Flag
bclr 7 ; Disable interrupts

# bst r1, 2 ; Store bit 2 of r1 in T Flag
bld r0, 4 ; Load T Flag into bit 4 of r0

brbc 6, 0x000
brbs 1, 0x000
brcc 0x000
brcs 0x000
breq 0x000
brge 0x000
brhc 0x000
brhs 0x000

call 0x120
com r4

cbi 0x12, 7

CLC
CLR 0x20

cp r4, r19
cpc r3, r1
cpi r19, 3

dec r17

fmuls r23, r22

in r25, 0x16

lds r2, 0xFF00

lsl r0

# ON FIX
mul r5, r4
movw r4, r0

muls r21, r20 ; Multiply signed r21 and r20
movw r20, r0 ; Copy result back in r21:r20

mulsu r23, r20;

neg r11

out 0x18, r17

pop r13

rcall 0xff00

ROL r12
ror r18

subi r16, 0x23

sbi 0x1C, 0

sbic 0x1C, 1

sbiw r25, 1

sbrc r0, 7

sts 0xFF00, r2

swap r1

tst r0

wdr