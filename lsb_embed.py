import extractor
import numpy as np
from bitstring import ConstBitStream
from bitstring import ReadError
import struct


class Embedder:

    def __init__(self):
        pass

    def embed(self, filename, outfile, message):
        length = struct.pack('!I', len(message))
        bitstream = ConstBitStream(bytes=length+message)
        ex = extractor.Extractor()
        rgb = ex.load(filename)
        try:
            with np.nditer(rgb, op_flags=['readwrite']) as it:
                for x in it:
                    messagebit = bitstream.read(1).uint
                    x[...] =  (x & 0xfe) | messagebit
        except ReadError:
            pass
        ex.save(outfile, rgb)


if __name__ == '__main__':
    em = Embedder()
    with open('qoi_test_images\\testcard.png', 'rb') as f:
        em.embed('qoi_test_images\\kodim23.png', 'outfile.png', f.read())


