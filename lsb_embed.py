import extractor
import numpy as np
from bitstring import ConstBitStream
from bitstring import ReadError
import struct


"""
This module embeds a secret into the least significant bits
of each color channel of a pixel throughout a whole image

It can be run both as a standalone program, or imported from another
python module and run from there.
"""


class Embedder:

    def __init__(self):
        # Don't use the zero entry
        self.em_masks = [0xff, 0xfe, 0xfc, 0xf8, 0xf0, 0xe0, 0xc0, 0x80, 0x00]

    def embed(self, filename, outfile, message, bits=1):
        length = struct.pack('!I', len(message))
        bitstream = ConstBitStream(bytes=length+message)
        ex = extractor.Extractor()
        rgb = ex.load(filename)
        em_mask = self.em_masks[bits]
        try:
            with np.nditer(rgb, op_flags=['readwrite']) as it:
                for x in it:
                    messagebit = bitstream.read(bits).uint
                    x[...] =  (x & em_mask) | messagebit
        except ReadError: # No more message bits to embed
            pass
        ex.save(outfile, rgb)

def main_files(inputfile, outputfile, messagefile, bits=1):
    em = Embedder()
    with open(messagefile, 'rb') as f:
        em.embed(inputfile, outputfile, f.read(), bits)

def main_bytes(inputfile, outputfile, message, bits=1):
    em = Embedder()
    em.embed(inputfile, outputfile, message, bits)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Embed a secret into a png/qoi')
    parser.add_argument('coverimage', type=str, help='Set the cover image file')
    parser.add_argument('outputfile', type=str, help='Set the output file name')
    parser.add_argument('messagefile', type=str, help='Set the file to read for the message')
    parser.add_argument('bits', type=int, nargs='?', default=1, help='Set the number of LSBs used for hiding')
    myargs = parser.parse_args()
    main_files(myargs.coverimage, myargs.outputfile, myargs.messagefile, myargs.bits)


