import extractor
import numpy as np
from bitstring import ConstBitStream
from bitstring import ReadError
from bitstring import BitArray
from bitstring import Bits
import struct


"""
This module reverses the embedding process to reveal the secret that 
was placed into an image by examining the least significant bits

The module can be run directly as a python program or it can be imported
elsewhere and used from there.
"""


class Revealer:

    def __init__(self):
        # Don't use the zero entry here
        self.ex_masks = [0b0, 0b1, 0b11, 0b111, 0b1111, 0b11111, 0b111111, 0b1111111, 0xff]

    def reveal(self, filename, bits=1):
        bitarray = BitArray()
        ex = extractor.Extractor()
        rgb = ex.load(filename)
        ex_mask = self.ex_masks[bits]
        try:
            with np.nditer(rgb) as it:
                for x in it:
                    xb = x & ex_mask
                    bitarray.append(Bits(uint=xb, length=bits))
        except ReadError:
            pass
        
        extracted_bytes = bitarray.tobytes()
        length = struct.unpack('!I', extracted_bytes[0:4])[0]
        hidden_bytes = extracted_bytes[4:4+length]
        return hidden_bytes
            

def main_file(stegoimage, outputname, bits=1):
    re = Revealer()
    hidden_bytes = re.reveal(stegoimage, bits)
    with open(outputname, 'wb') as f:
        f.write(hidden_bytes)

def main_bytes(stegoimage, bits=1):
    re = Revealer()
    hidden_bytes = re.reveal(stegoimage, bits)
    return hidden_bytes



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Embed a secret into a png/qoi')
    parser.add_argument('stegoimage', type=str, help='Set the input image with the secret message')
    parser.add_argument('outputfile', type=str, help='Set the name of the output file which will contain the hidden bytes')
    parser.add_argument('bits', type=int, nargs='?', default=1, help='Set the number of LSBs used for hiding')
    myargs = parser.parse_args()
    main_file(myargs.stegoimage, myargs.outputfile)


