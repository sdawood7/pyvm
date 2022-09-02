from enum import IntEnum

class Instruction(IntEnum):
    LW      = 0x10 # lw     rd, rs      # Loads word from memory address specified by register source into register destination
    SW      = 0x11 # sw     rs, rd      # Stores word from register source into memory address specified by register destination
    SWP     = 0x12 # swp    r1, r2      # Swap two registers values

    PSH     = 0x30 # psh    rs          # Push contents of register source onto stack
    PSHI    = 0x31 # pshi   0x0000      # Push immediate value onto stack
    POP     = 0x32 # pop    rd          # Pop value at stack pointer and place into register destination
    
    JALI    = 0x40 # jali   0x0000      # Jump and link to immediate value, save state of CPU on stack
    JAL     = 0x41 # jal    rs          # Jump and link to value in register source, save state of CPU on stack
    RET     = 0x42 # ret                # Return from linked function

    ADD     = 0x50 # add    r1, r2      # Add two registers
    SUB     = 0x51 # sub    r1, r2      # Subtract first register by second register
    MULT    = 0x52 # mult   r1, r2      # Multiply two registers
    DIV     = 0x53 # div    r1, r2      # Divide first register by second register
    MOD     = 0x54 # mod    r1, r2      # Modulo divide first register by second register

    AND     = 0x60 # and    r1, r2      # Bitwise and two registers
    OR      = 0x61 # or     r1, r2      # Bitwise or two registers
    XOR     = 0x62 # xor    r1, r2      # Bitwise xor two registers
    LSHFT   = 0x63 # lshft  r1, r2      # Bitwise left shift first register by value specified in second register
    RSHFT   = 0x64 # rshft  r1, r2      # Bitwise right shift first register by value specified in second register
    NOT     = 0x65 # not    r1          # Bitwise not one register

    JR      = 0x80 # jr     rs          # Jump instruction pointer to value specified by register source
    JI      = 0x81 # ji     0x0000      # Jump instruction pointer to immediate value
    BEQ     = 0x82 # beq    0x0000      # Branch if ALU zero flag is True (don't care about the ALU negative flag)
    BNE     = 0x83 # bne    0x0000      # Branch if ALU zero flag is False (don't care about the ALU negative flag)
    BLT     = 0x84 # blt    0x0000      # Branch if ALU negative flag is True (don't care about the ALU negative flag)
    BLE     = 0x85 # ble    0x0000      # Branch if ALU negative flag is True or ALU zero flag is True
    BGT     = 0x86 # bgt    0x0000      # Branch if ALU negative flag is False (don't care about the ALU negative flag)
    BGE     = 0x87 # bge    0x0000      # Branch if ALU negative flag is False or ALU Zero flag is True

    HLT     = 0xFF # hlt                # Halt execution of program