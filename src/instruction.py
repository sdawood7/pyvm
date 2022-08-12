from enum import IntEnum

class Instruction(IntEnum):
    LW      = 0x10 # lw     rd, 0x0000      # Loads word from memory address specified by immediate value into register destination
    LWR     = 0x11 # lwr    rd, rs          # Loads word from memory address specified by register source into register destination
    SW      = 0x12 # sw     rs, 0x0000      # Stores word from register source into memory address specified by immediate value
    SWR     = 0x13 # swr    rs, rd          # Stores word from register source into memory address specified by register destination
    MOV     = 0x14 # mov    rd, 0x0000      # Move literal into register
    SWP     = 0x15 # swp    r1, r2          # Swap two registers values

    ADD     = 0x50 # add    rd, r1, r2      # Add two registers and store result in register destination
    ADDI    = 0x51 # addi   rd, r1, 0x0000  # Add register and immediate value and store result in register destination
    SUB     = 0x52 # sub    rd, r1, r2      # Subtract first register by second register and store result in register destination
    SUBI    = 0x53 # subi   rd, r1, 0x0000  # Subtract register by immediate value and store result in register destination
    MULT    = 0x54 # mult   rd, r1, r2      # Multiply two registers and store result in register destination
    MULTI   = 0x55 # multi  rd, r1, 0x0000  # Multiply register and immediate value and store result in register destination
    DIV     = 0x56 # div    rd, r1, r2      # Divide first register by second register and store result in register destination
    DIVI    = 0x57 # divi   rd, r1, 0x0000  # Divide register by immediate value and store result in register destination
    MOD     = 0x58 # mod    rd, r1, r2      # Modulo divide first register by second register and store result in register destination
    MODI    = 0x59 # modi   rd, r1, 0x0000  # Modulo divide register by immediate value and store result in register destination

    AND     = 0x60 # and    rd, r1, r2      # Logical and two registers and store result in register destination
    ANDI    = 0x61 # andi   rd, r1, 0x0000  # Logical and register and immediate value and store result in register destination
    OR      = 0x62 # or     rd, r1, r2      # Logical or two registers and store result in register destination
    ORI     = 0x63 # ori    rd, r1, 0x0000  # Logical or register and immediate value and store result in register destination
    XOR     = 0x64 # xor    rd, r1, r2      # Logical xor two registers and store result in register destination
    XORI    = 0x65 # xori   rd, r1, 0x0000  # Logical xor register and immediate value and store result in register destination
    LSHFT   = 0x66 # lshft  rd, r1, r2      # Left shift first register by value specified in second register
    LSHFTI  = 0x67 # lshfti rd, r1, 0x0000  # Left shift first register by immediate value
    RSHFT   = 0x68 # rshft  rd, r1, r2      # Right shift first register by value specified in second register
    RSHFTI  = 0x69 # rshfti rd, r1, 0x0000  # Right shift first register by immediate value

    JR      = 0x80 # jr     rs              # Jump instruction pointer to value specified by register source
    JI      = 0x81 # ji     0x0000          # Jump instruction pointer to immediate value
    JAL     = 0x82 # jal
    BEQ     = 0x83 # beq    
    BNE     = 0x84 # bne    
    BLT     = 0x85 # blt    
    BLE     = 0x86 # ble    
    BGT     = 0x87 # bgt    
    BGE     = 0x88 # bge    

    HLT     = 0xFF # hlt                    # Halt execution of program