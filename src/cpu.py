from memory import Memory
from instruction import Instruction

class CPU:
    def __init__(self, memory_size=256):
        self.memory = Memory(memory_size)

        self.registerNames = [
            'ip',
            'r1', 'r2', 'r3', 'r4',
            'r5', 'r6', 'r7', 'r8',
            'sp', 'fp',
        ]

        self.registers = Memory(len(self.registerNames) * 2) # Create memory for 16-bit registers

        self.registerDict = {self.registerNames[i]: i * 2 for i in range(len(self.registerNames))}

    def getRegisterIndex(self, name):
        if name not in self.registerNames:
            raise Exception("Register name: {} not found".format(name))
        return self.registerDict[name]

    def getRegisterValue(self, name):
        if name not in self.registerNames:
            raise Exception("Register name: {} not found".format(name))
        return self.registers.getUint16(self.registerDict[name])

    def setRegisterValue(self, index, value):
        if not self.registers.addressExists(index):
            raise Exception("Register index: {} not found".format(index))
        return self.registers.setUint16(index, value)

    def printCPUState(self):
        for name in self.registerDict:
            print("{} : {}".format(name, hex(self.getRegisterValue(name))))

    def writeToMemory(self, address, value):
        self.memory.setUint16(address, value)

    def readFromMemory(self, address):
        return self.memory.getUint16(address)

    def fetch(self):
        ip_value = self.getRegisterValue('ip')
        instruction = self.memory.getUint8(ip_value)
        ip_value += 1
        self.setRegisterValue(self.getRegisterIndex('ip'), (ip_value))
        print("Instruction Pointer is now at {}".format(ip_value))
        return instruction

    def fetchWord(self):
        ip_value = self.getRegisterValue('ip')
        instruction = self.memory.getUint16(ip_value)
        ip_value += 2
        self.setRegisterValue(self.getRegisterIndex('ip'), (ip_value))
        print("Instruction Pointer is now at {}".format(ip_value))
        return instruction

    def execute(self, instruction):
        match instruction:
            case Instruction.LW:
                return 1
            case Instruction.LWR:
                return 1
            case Instruction.SW:
                return 1
            case Instruction.SWR:
                return 1
            case Instruction.MOV:
                rd = self.fetch()
                immediate = self.fetchWord()

                self.setRegisterValue(rd, immediate)

                return 1
            case Instruction.SWP:
                return 1

            case Instruction.ADD:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val + r2Val)
                return 1
            case Instruction.ADDI:
                return 1
            case Instruction.SUB:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val - r2Val)
                return 1
            case Instruction.SUBI:
                return 1
            case Instruction.MULT:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val * r2Val)
                return 1
            case Instruction.MULTI:
                return 1
            case Instruction.DIV:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val / r2Val)
                return 1
            case Instruction.DIVI:
                return 1
            case Instruction.MOD:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val % r2Val)
                return 1
            case Instruction.MODI:
                return 1
            
            case Instruction.AND:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val & r2Val)
                return 1
            case Instruction.ANDI:
                return 1
            case Instruction.OR:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val | r2Val)
                return 1
            case Instruction.ORI:
                return 1
            case Instruction.XOR:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val ^ r2Val)
                return 1
            case Instruction.XORI:
                return 1
            case Instruction.LSHFT:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val << r2Val)
                return 1
            case Instruction.LSHFTI:
                return 1
            case Instruction.RSHFT:
                rd = self.fetch()
                r1 = self.fetch()
                r2 = self.fetch()

                r1Val = self.getRegisterValue(self.registerNames[int(r1 / 2)])
                r2Val = self.getRegisterValue(self.registerNames[int(r2 / 2)])


                self.setRegisterValue(rd, r1Val >> r2Val)
                return 1
            case Instruction.RSHFTI:
                return 1

            case Instruction.JR:
                return 1
            case Instruction.JI:
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


    def step(self):
        instruction = self.fetch()
        print("Executing instruction: {}".format(instruction))
        return self.execute(instruction)

    def run(self):
        halt = 1
        while halt != 0:
            halt = self.step()


class CPU2:
    def __init__(self, memory_size=256):
        self.registerNames = [
            'ip',
            'r1', 'r2', 'r3', 'r4',
            'sp', 'fp',
        ]

        self.registerValues = Memory(len(self.registerNames) * 2)

        self.registerMap = {self.registerNames[i]: i*2 for i in range(len(self.registerNames))}