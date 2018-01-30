def twos_comp(val, bits):
    """compute the twos complement of int value val"""
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g, 8 bit: 128-255 ( we know that you can't have a value this high, so first bit must be 1)
        val = val - (1 << bits)         # compute negative value (value - 2 * max value) 
        # e.g 10000001 is -127 in 2's comp, read as 129 in binary. 129 - ( 1 << 8 ) is 129 - 256 = -127
    return val
