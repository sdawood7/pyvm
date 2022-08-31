from cpu import CPU
from instruction import Instruction
from program import Program

cpu = CPU()

program = Program()

i = 0

r1 = cpu.registerDict['r1']
r2 = cpu.registerDict['r2']
r3 = cpu.registerDict['r3']

program.instruction(Instruction.PSHI, 0x01, 0x12)

program.instruction(Instruction.POP, r1)

program.instruction(Instruction.PSHI, 0x21, 0x10)

program.instruction(Instruction.POP, r2)

program.instruction(Instruction.PSH, r1)

program.instruction(Instruction.PSH, r2)

program.instruction(Instruction.POP, r1)

program.instruction(Instruction.POP, r2)

program.instruction(Instruction.HLT)

cpu.loadProgram(program.functions, program.byte_count)

cpu.stack.printChunk(0xcf0, 0x10)
cpu.printCPUState()

print("Running instructions...", end=" ")
cpu.run()
print("Finished!")

cpu.stack.printChunk(0xcf0, 0x10)
cpu.printCPUState()
