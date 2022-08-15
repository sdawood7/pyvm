from memory import Memory
from instruction import Instruction

class CPU:
    def __init__(self, memory_size=256):
        self.memory = Memory(memory_size)

        self.registerNames = [
            'ip', 'lr', 'ac',
            'r1', 'r2', 'r3', 'r4',
            'r5', 'r6', 'r7', 'r8',
            'sp', 'fp',
        ]

        self.registers = Memory(len(self.registerNames) * 2) # Create memory for 16-bit registers

        self.registerDict = {self.registerNames[i]: i * 2 for i in range(len(self.registerNames))}

        self.MAX_STACK_POINTER = (memory_size - 1) - 1 # Stack pointer starts at last address, set address to 1 less than max, and subtract 1 for 0 indexing

        self.MIN_STACK_POINTER = int(self.MAX_STACK_POINTER / 2)

        self.setRegisterValue(self.getRegisterIndex('sp'), self.MAX_STACK_POINTER) 

    def getRegisterIndex(self, name) -> int:
        if name not in self.registerNames:
            raise Exception("Register name: {} not found".format(name))
        return self.registerDict[name]

    def getRegisterValue(self, index) -> int:
        if not self.registers.addressExists(index):
            raise Exception("Register index: {} not found".format(index))
        return self.registers.getUint16(index)

    def setRegisterValue(self, index, value) -> None:
        if not self.registers.addressExists(index):
            raise Exception("Register index: {} not found".format(index))
        self.registers.setUint16(index, value)

    def printCPUState(self) -> None:
        for name in self.registerDict:
            print("{} : {}".format(name, hex(self.getRegisterValue(self.getRegisterIndex(name)))[2:].zfill(4)))

    def writeToMemory(self, address, value) -> None:
        self.memory.setUint16(address, value)

    def readFromMemory(self, address) -> int:
        return self.memory.getUint16(address)

    def push(self, value) -> None:
        stack_pointer = self.getRegisterIndex('sp')
        address = self.getRegisterValue(stack_pointer)

        self.writeToMemory(address, value)

        if address > self.MIN_STACK_POINTER: # Prevent the stack pointer from going out of bounds
            address -= 2
            self.setRegisterValue(stack_pointer, address) # Stack grows upwards

    def pop(self) -> int:
        stack_pointer = self.getRegisterIndex('sp')
        address = self.getRegisterValue(stack_pointer)

        if address < self.MAX_STACK_POINTER: # Prevent the stack pointer from going out of bounds
            address += 2
            self.setRegisterValue(stack_pointer, address)

        return self.readFromMemory(address)

    def jump(self, address) -> None:
        ip_index = self.getRegisterIndex('ip')

        self.setRegisterValue(ip_index, address)

    def fetch(self) -> int:
        ip_reg = self.getRegisterIndex('ip')
        ip_value = self.getRegisterValue(ip_reg)
        instruction = self.memory.getUint8(ip_value)
        ip_value += 1
        self.setRegisterValue(ip_reg, ip_value)
        return instruction

    def fetchWord(self) -> int:
        ip_reg = self.getRegisterIndex('ip')
        ip_value = self.getRegisterValue(ip_reg)
        instruction = self.memory.getUint16(ip_value)
        ip_value += 2
        self.setRegisterValue(ip_reg, ip_value)
        return instruction

    def execute(self, instruction) -> int:
        match instruction:
            # Register/Memory manipulation
            case Instruction.LW:
                rd = self.fetch()
                address = self.fetchWord()

                word_from_memory = self.readFromMemory(address)

                self.setRegisterValue(rd, word_from_memory)
                return 1
            case Instruction.LWR:
                rd = self.fetch()
                rs = self.fetch()

                address = self.getRegisterValue(rs)
                word_from_memory = self.readFromMemory(address)

                self.setRegisterValue(rd, word_from_memory)
                return 1
            case Instruction.SW:
                rs = self.fetch()
                address = self.fetchWord()

                word_to_memory = self.getRegisterValue(rs)

                self.writeToMemory(address, word_to_memory)
                return 1
            case Instruction.SWR:
                rs = self.fetch()
                rd = self.fetch()

                address = self.getRegisterValue(rd)
                word_to_memory = self.getRegisterValue(rs)

                self.writeToMemory(address, word_to_memory)
                return 1
            case Instruction.MOV:
                rd = self.fetch()
                immediate = self.fetchWord()

                self.setRegisterValue(rd, immediate)
                return 1
            case Instruction.SWP:
                r1 = self.fetch()
                r2 = self.fetch()

                tmpVal = self.getRegisterValue(r1)
                self.setRegisterValue(r1, self.getRegisterValue(r2))
                self.setRegisterValue(r2, tmpVal)

                return 1

            # Stack Operations
            case Instruction.PSH:
                rs = self.fetch()
                value = self.getRegisterValue(rs)

                self.push(value)

                return 1
            case Instruction.PSHI:
                value = self.fetchWord()

                self.push(value)

                return 1
            case Instruction.POP:
                rd = self.fetch()

                value = self.pop()

                self.setRegisterValue(rd, value)
                
                return 1
            case Instruction.JAL:
                return 1
            case Instruction.RET:
                return 1

            # Arithmetic
            case Instruction.ADD:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val + r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.ADDI:
                return 1
            case Instruction.SUB:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val - r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.SUBI:
                return 1
            case Instruction.MULT:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val * r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.MULTI:
                return 1
            case Instruction.DIV:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val / r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.DIVI:
                return 1
            case Instruction.MOD:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val % r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.MODI:
                return 1
            
            # Logical Operands
            case Instruction.AND:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val & r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.ANDI:
                return 1
            case Instruction.OR:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val | r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.ORI:
                return 1
            case Instruction.XOR:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val ^ r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.XORI:
                return 1
            case Instruction.LSHFT:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val << r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.LSHFTI:
                return 1
            case Instruction.RSHFT:
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(r1)
                r2Val = self.getRegisterValue(r2)

                ac_reg = self.getRegisterIndex('ac')
                val = r1Val >> r2Val

                self.setRegisterValue(ac_reg, val)
                return 1
            case Instruction.RSHFTI:
                return 1

            # Instruction Pointer Manipulation
            case Instruction.JR:
                rs = self.fetch()
                address = self.getRegisterValue(rs)

                self.jump(address)

                return 1
            case Instruction.JI:
                address = self.fetchWord()

                self.jump(address)

                return 1
            case Instruction.BEQ:
                return 1
            case Instruction.BNE:
                return 1
            case Instruction.BLT:
                return 1
            case Instruction.BLE:
                return 1
            case Instruction.BGT:
                return 1
            case Instruction.BGE:
                return 1
            case Instruction.HLT:
                return 0


    def step(self) -> int:
        instruction = self.fetch()
        print("Executing instruction: {}".format(instruction))
        return self.execute(instruction)

    def run(self) -> None:
        halt = 1
        while halt != 0:
            halt = self.step()
