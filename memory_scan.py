from ReadWriteMemory import ReadWriteMemory


def GetGridsFromMemory(processID):
    '''
    player = [0x00181c88+0x000187f4+playerID*0x04]
    playerGrids = [player+0x04]+0x08
    '''
    memory = ReadWriteMemory()
    process = memory.get_process_by_id(processID)
    process.open()
    for index in range(19*11):
        pointer = process.get_pointer(
            0x00181c88+0x000187f4, offsets=(0x04, 0x08+index))
        grid = process.read(pointer)
        yield grid & 0xff
    process.close()
