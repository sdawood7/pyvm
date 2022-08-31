from alu import ALU
from memory import Memory
from instruction import Instruction

class CPU:
    def __init__(self, memory_size=8192):
        self.memory_size = memory_size

        self.general = Memory(int(self.memory_size / 4))            # 2048 +
        self.program = Memory(int(self.memory_size / 4))            # 2048 +
        self.io      = Memory(int(self.memory_size / 16))           # 512  +
        self.screen  = Memory(int(self.memory_size / 32))           # 256  +
        self.stack   = Memory(int(((self.memory_size / 32) * 13)))  # 3328 = 8192 bytes

        self.labels = {}

        self.alu = ALU()

        self.registerNames = [
            'ip', 'lr', 'ac',
            'r1', 'r2', 'r3', 'r4',
            'r5', 'r6', 'r7', 'r8',
            'sp', 'fp',
        ]

        self.registers = Memory(len(self.registerNames) * 2) # Create memory for 16-bit registers

        self.registerDict = {self.registerNames[i]: i * 2 for i in range(len(self.registerNames))}

        self.SP_MAX = ((self.stack.size - 1) - 1)

        self.setRegisterValue(self.getRegisterIndex('sp'), self.SP_MAX) # Stack pointer starts at last address, set address to 1 less than max, and subtract 1 for 0 indexing

    def loadProgram(self, functions, byte_count):
        if (byte_count + len(functions)) >= self.program.size:
            raise Exception("Program size too large")

        program_index = 0
        for func in functions:
            self.labels[func] = program_index
            for byte in functions[func]:
                print("{} : {}".format(type(byte), byte))
                self.program.setUint8(program_index, int(byte))
                program_index += 1
            program_index += 1

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

    def push(self, value) -> None:
        stack_pointer = self.getRegisterIndex('sp')
        address = self.getRegisterValue(stack_pointer)

        self.stack.setUint16(address, value)

        if address > 0: # Prevent the stack pointer from going out of bounds
            address -= 2
            self.setRegisterValue(stack_pointer, address) # Stack grows upwards

    def pop(self) -> int:
        stack_pointer = self.getRegisterIndex('sp')
        address = self.getRegisterValue(stack_pointer)

        if address < self.SP_MAX: # Prevent the stack pointer from going out of bounds
            address += 2
            self.setRegisterValue(stack_pointer, address)

        return self.stack.getUint16(address)

    def jump(self, address) -> None:
        ip_index = self.getRegisterIndex('ip')

        self.setRegisterValue(ip_index, address)

    def fetch(self) -> int:
        ip_reg = self.getRegisterIndex('ip')
        ip_value = self.getRegisterValue(ip_reg)
        instruction = self.program.getUint8(ip_value)
        ip_value += 1
        self.setRegisterValue(ip_reg, ip_value)
        return instruction

    def fetchWord(self) -> int:
        ip_reg = self.getRegisterIndex('ip')
        ip_value = self.getRegisterValue(ip_reg)
        instruction = self.program.getUint16(ip_value)
        ip_value += 2
        self.setRegisterValue(ip_reg, ip_value)
        return instruction

    def execute(self, instruction) -> int:
        # Register/Memory manipulation
        if instruction == Instruction.LW:
            rd = self.fetch()
            rs = self.fetch()

            address = self.getRegisterValue(rs)
            word_from_memory = self.general.getUint16(address)

            self.setRegisterValue(rd, word_from_memory)
            return 1
        elif instruction == Instruction.SW:
            rs = self.fetch()
            rd = self.fetch()

            address = self.getRegisterValue(rd)
            word_to_memory = self.getRegisterValue(rs)

            self.general.setUint16(address, word_to_memory)
            return 1
        elif instruction == Instruction.SWP:
            r1 = self.fetch()
            r2 = self.fetch()

            self.push(self.getRegisterValue(r1))
            self.push(self.getRegisterValue(r2))

            self.setRegisterValue(r1, self.pop())
            self.setRegisterValue(r2, self.pop())

            return 1

        # Stack Operations
        elif instruction == Instruction.PSH:
            rs = self.fetch()
            value = self.getRegisterValue(rs)

            self.push(value)

            return 1
        elif instruction == Instruction.PSHI:
            value = self.fetchWord()

            self.push(value)

            return 1
        elif instruction == Instruction.POP:
            rd = self.fetch()

            value = self.pop()

            self.setRegisterValue(rd, value)
            
            return 1
        elif instruction == Instruction.JAL:
            return 1
        elif instruction == Instruction.RET:
            return 1

        # Arithmetic
        elif instruction == Instruction.ADD:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('+', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.SUB:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('-', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.MULT:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('*', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.DIV:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('/', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.MOD:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('%', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        
        # Logical Operands
        elif instruction == Instruction.AND:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('&', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.OR:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('|', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.XOR:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('^', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.LSHFT:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('<<', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.RSHFT:
            r1 = self.fetch()
            r2 = self.fetch()

            r1Val = self.getRegisterValue(r1)
            r2Val = self.getRegisterValue(r2)

            self.alu.compute('>>', r1Val, r2Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1
        elif instruction == Instruction.NOT:
            r1 = self.fetch()

            r1Val = self.getRegisterValue(r1)

            self.alu.compute('~', r1Val)

            ac_reg = self.getRegisterIndex('ac')
            val = self.alu.result

            self.setRegisterValue(ac_reg, val)
            return 1

        # Instruction Pointer Manipulation
        elif instruction == Instruction.JR:
            rs = self.fetch()
            address = self.getRegisterValue(rs)

            self.jump(address)

            return 1
        elif instruction == Instruction.JI:
            address = self.fetchWord()

            self.jump(address)

            return 1
        elif instruction == Instruction.BEQ:
            address = self.fetchWord()
            if self.alu.zero:
                self.jump(address)

            return 1
        elif instruction == Instruction.BNE:
            address = self.fetchWord()
            if not self.alu.zero:
                self.jump(address)

            return 1
        elif instruction == Instruction.BLT:
            address = self.fetchWord()
            if self.alu.negative:
                self.jump(address)

            return 1
        elif instruction == Instruction.BLE:
            address = self.fetchWord()
            if self.alu.negative or self.alu.zero:
                self.jump(address)

            return 1
        elif instruction == Instruction.BGT:
            address = self.fetchWord()
            if not self.alu.negative:
                self.jump(address)

            return 1
        elif instruction == Instruction.BGE:
            address = self.fetchWord()
            if not self.alu.negative or self.alu.zero:
                self.jump(address)

            return 1
        elif instruction == Instruction.HLT:
            return 0

        # Default
        else:
            raise Exception("Unknown instruction given: {}".format(instruction))

    def step(self) -> int:
        instruction = self.fetch()
        print("Executing instruction: {}".format(instruction))
        return self.execute(instruction)

    def run(self) -> None:
        halt = 1
        while halt != 0:
            halt = self.step()
