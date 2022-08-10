from tkinter import E


class Memory:
    def __init__(self, num_bytes):
        if num_bytes <=0:
            num_bytes = 256
        self.memory = bytearray(num_bytes)

    def addressExists(self, address):
        if address > len(self.memory) or address < 0:
            return False
        return True

    def getUint8(self, address):
        if not self.addressExists(address):
            raise Exception("Address out of bounds")
        return int(self.memory[address])

    def getUint16(self, address):
        if not self.addressExists(address):
            raise Exception("Address out of bounds")
        if not self.addressExists(address+1):
            raise Exception("")
        return int(self.memory[address:(address + 1) + 1].hex(), 16) # Add an additional 1 because python slicing is exclusive >:(

    def setUint8(self, address, value):
        if not self.addressExists(address):
            raise Exception("Address out of bounds")
        self.memory[address] = value & 0xff

    def setUint16(self, address, value):
        if not self.addressExists(address):
            raise Exception("Address out of bounds")
        
        self.memory[address] = (value & 0xff00) >> 8 # Bit mask first byte of the value, then bit shift down to be 0-255
        self.memory[address + 1] = (value & 0x00ff)

    def printChunk(self, address, chunkSize=16):
        if not self.addressExists(address):
            raise Exception("Address out of bounds")

        print("Memory at {}".format(hex(address)))

        for i in range(0, chunkSize):
            print("{}".format(hex(self.getUint8(address + i))[2:].zfill(2)), end=" " if i%2 == 1 else "") # This is super ugly lol
        print("\n")
