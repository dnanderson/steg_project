import extractor
import numpy as np
from bitstring import ConstBitStream
from bitstring import ReadError
from bitstring import BitArray
from bitstring import Bits


class Revealer:

    def __init__(self):
        pass

    def reveal(self, filename):
        bitarray = BitArray()
        ex = extractor.Extractor()
        rgb = ex.load(filename)
        try:
            with np.nditer(rgb) as it:
                for x in it:
                    #x[...] = messagebit & 0b00000001
                    xb = x & 0b1
                    bitarray.append(Bits(uint=xb, length=1))
        except ReadError:
            pass
        
        asdf = bitarray.tobytes()
            


if __name__ == '__main__':
    em = Revealer()
    em.reveal('outfile.png')


