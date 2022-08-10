from cpu import CPU
from instruction import Instruction

cpu = CPU()

i = 0

r1 = cpu.registerDict['r1']
r2 = cpu.registerDict['r2']
r3 = cpu.registerDict['r3']

cpu.memory.setUint8(i, Instruction.MOV)
i+=1
cpu.memory.setUint8(i, r1)
i+=1
cpu.memory.setUint8(i, 0x12)
i+=1
cpu.memory.setUint8(i, 0x34)
i+=1

cpu.memory.setUint8(i, Instruction.MOV)
i+=1
cpu.memory.setUint8(i, r2)
i+=1
cpu.memory.setUint8(i, 0xab)
i+=1
cpu.memory.setUint8(i, 0xcd)
i+=1

cpu.memory.setUint8(i, Instruction.ADD)
i+=1
cpu.memory.setUint8(i, r3)
i+=1
cpu.memory.setUint8(i, r1)
i+=1
cpu.memory.setUint8(i, r2)
i+=1

cpu.memory.setUint8(i, Instruction.HLT)


cpu.memory.printChunk(0x0, 0x10)
cpu.printCPUState()

print("Running instructions...", end=" ")
cpu.run()
print("Finished!")

cpu.memory.printChunk(0x0, 0x10)
cpu.printCPUState()
