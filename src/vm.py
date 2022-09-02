from cpu import CPU
from instruction import Instruction
from program import Program

cpu = CPU()

program = Program()

i = 0

r1 = cpu.registerDict['r1']
r2 = cpu.registerDict['r2']
r3 = cpu.registerDict['r3']
r8 = cpu.registerDict['r8']
ac = cpu.registerDict['ac']

program.instruction(Instruction.PSHI, 0x04, 0x00, func="sub")
program.instruction(Instruction.POP, r1, func="sub")

program.instruction(Instruction.PSHI, 0x02, 0x00, func="sub")
program.instruction(Instruction.POP, r2, func="sub")


program.instruction(Instruction.SUB, r1, r2, func="sub")

program.instruction(Instruction.RET, func="sub")

program.instruction(Instruction.PSHI, 0x12, 0x34, func="add")
program.instruction(Instruction.POP, r1, func="add")

program.instruction(Instruction.PSHI, 0x56, 0x78, func="add")
program.instruction(Instruction.POP, r2, func="add")

program.instruction(Instruction.ADD, r1, r2, func="add")

program.instruction(Instruction.RET, func="add")

program.instruction(Instruction.PSHI, 0x01, 0x12) # 0x0112 in r1 register
program.instruction(Instruction.POP, r1)

program.instruction(Instruction.PSHI, 0x21, 0x10) # 0x2110 in r2 register
program.instruction(Instruction.POP, r2)

program.instruction(Instruction.PSHI, 0xa2, 0xfe)

program.instruction(Instruction.PSHI, 0xe8, 0x9c)


program.instruction(Instruction.PSH, r1) # Place registers on stack
program.instruction(Instruction.PSH, r2)

program.instruction(Instruction.POP, r1) # Swap register values using stack
program.instruction(Instruction.POP, r2)

program.instruction(Instruction.JALI, label="sub") 

program.instruction(Instruction.PSH, ac)

program.instruction(Instruction.JALI, label="add")

program.instruction(Instruction.PSH, ac)

program.instruction(Instruction.POP, r2)
program.instruction(Instruction.POP, r1)

program.instruction(Instruction.DIV, r1, r2)

program.instruction(Instruction.HLT)

cpu.loadProgram(program.functions, program.byte_count)

cpu.stack.printChunk(0xcd0, 0x30)
cpu.printCPUState()

cpu.run()

cpu.stack.printChunk(0xcd0, 0x30)
cpu.printCPUState()
