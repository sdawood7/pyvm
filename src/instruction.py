from enum import IntEnum

class Instruction(IntEnum):
    LW      = 0x11 # lwr    rd, rs      # Loads word from memory address specified by register source into register destination
    SW      = 0x13 # swr    rs, rd      # Stores word from register source into memory address specified by register destination
    SWP     = 0x15 # swp    r1, r2      # Swap two registers values

    PSH     = 0x30 # psh    rs
    PSHI    = 0x31 # psh    0x0000
    POP     = 0x32 # pop    rd
    JAL     = 0x33 # jal
    RET     = 0x34 # ret

    ADD     = 0x50 # add    r1, r2      # Add two registers
    SUB     = 0x52 # sub    r1, r2      # Subtract first register by second register
    MULT    = 0x54 # mult   r1, r2      # Multiply two registers
    DIV     = 0x56 # div    r1, r2      # Divide first register by second register
    MOD     = 0x58 # mod    r1, r2      # Modulo divide first register by second register

    AND     = 0x60 # and    r1, r2      # Bitwise and two registers
    OR      = 0x62 # or     r1, r2      # Bitwise or two registers
    XOR     = 0x64 # xor    r1, r2      # Bitwise xor two registers
    LSHFT   = 0x66 # lshft  r1, r2      # Bitwise left shift first register by value specified in second register
    RSHFT   = 0x68 # rshft  r1, r2      # Bitwise right shift first register by value specified in second register

    JR      = 0x80 # jr     rs              # Jump instruction pointer to value specified by register source
    JI      = 0x81 # ji     0x0000          # Jump instruction pointer to immediate value
    BEQ     = 0x82 # beq
    BNE     = 0x83 # bne    
    BLT     = 0x84 # blt    
    BLE     = 0x85 # ble    
    BGT     = 0x86 # bgt    
    BGE     = 0x87 # bge    

    HLT     = 0xFF # hlt                    # Halt execution of program