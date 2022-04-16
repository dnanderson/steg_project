import extractor
import numpy as np
from bitstring import ConstBitStream
from bitstring import ReadError


class Embedder:

    def __init__(self):
        pass

    def embed(self, filename, message):
        byt = bytes(message, 'ascii')
        bitstream = ConstBitStream(bytes=byt)
        ex = extractor.Extractor()
        rgb = ex.load(filename)
        try:
            with np.nditer(rgb, op_flags=['readwrite']) as it:
                for x in it:
                    messagebit = bitstream.read(1).uint
                    x[...] =  (x & 0xfe) | messagebit
        except ReadError:
            pass
            
        ex.save('outfile.png', rgb)


if __name__ == '__main__':
    em = Embedder()
    em.embed('qoi_test_images\kodim23.png', 'Hello!')


