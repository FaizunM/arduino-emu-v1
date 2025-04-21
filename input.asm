.data
xglobal: .hword 0xA0

.text
noteq:
    NOP

.text
nocarry:
    NOP

.text
carry:
    NOP

.text
check:
    NOP

.text
farplc:
    NOP

.text
routine:
    NOP

.text
_start:
    jmp 0x34
    lds r2, 0xFF00
    CALL 0xFFA0
    sts 0xFF00, r2
    tst r0
    swap r1
    subi r22, 0x11
    sub r13, r12
    SEH
    SEC
    sbrs r0,7
    sbrc r0,7
    sbr r16,3
    sbiw X, 0x2A
    sbis 0x1C, 1
    sbic 0x1C, 1
    sbi 0x1C, 0
    sbci r17, xglobal
    sbc r3,r1
    ror r18
    rol r19
    RET
    rcall routine
    push r13
    pop r13
    out 0x18, r16
    ORI R5, xglobal
    OR r21,r20
    NOP
    NEG r0
    muls r21,r20
    mul r5,r4
    movw r16,r0
    mov r16,r0
    lsr r0
    LSL R10
    INC R5
    in r25,16 ; Read Port B
    ICALL
    FMULSU r4,r0
    FMULS r4,r0
    FMUL r4,r0
    EOR r4,r0
    EICALL
    DEC R5
    cpse r4,r0
    cpi r19,3
    cpc r3,r1
    cp r4, r19
    COM R12
    CLS
    CLR R12
    CBI 12, 7
    CLH
    CLC
    CBR R5, xglobal
    CBI 12, 7
    CALL check
    BST r2, 5
    BSET 6
    BRVS carry
    BRVC carry
    BRTS carry
    BRTC carry
    BRSH carry
    BRPL carry
    BRNE carry
    BRMI carry
    BRLT carry
    BRLO carry
    BRIE carry
    BRID carry
    BRHS carry
    BRHC carry
    BRGE carry
    BREQ carry
    BRCS carry
    BRCC nocarry
    BREAK
    BRBS 1, noteq
    BRBC 1, noteq
    BLD r1, 4
    ADIW X, 0x2A
    AND R2, R4
    ANDI R5, xglobal
    ASR R10
    BCLR 7