import extractor
import numpy as np

import bitarray
import bitarray.util
import struct
from crypto_util import encryptor
import crypto_util
import os


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

    def embed(self, filename, outfile, message, rate=3):
        nonce = os.urandom(16)
        encr = encryptor(crypto_util.shared_key, nonce)
        hasher = crypto_util.hasher(crypto_util.shared_key, rate)
        ba2int = bitarray.util.ba2int
        length = struct.pack('!I', len(message))
        enc_data = nonce+encr(length+message)
        barray = bitarray.bitarray(buffer=enc_data)
        ex = extractor.Extractor()
        rgb = ex.load(filename)
        em_mask = self.em_masks[1]
        try:
            pos = 0
            for i,row in enumerate(rgb):
                for j,col in enumerate(row):
                    r,g,b = col[0],col[1],col[2]
                    doembed = next(hasher) # Infinite generator
                    if doembed == 1:
                        msgb = barray[pos]
                        pos += 1
                        rgb[i][j][0] = (r & em_mask) | msgb
                    elif doembed == 2:
                        msgb = barray[pos]
                        pos += 1
                        rgb[i][j][1] = (g & em_mask) | msgb
                    elif doembed == 3:
                        msgb = barray[pos]
                        pos += 1
                        rgb[i][j][2] = (b & em_mask) | msgb
            else:
                ex.save(outfile, rgb)
                return pos
        except IndexError:
            pass
        ex.save(outfile, rgb)
        return None

def main_files(inputfile, outputfile, messagefile, rate):
    em = Embedder()
    with open(messagefile, 'rb') as f:
        em.embed(inputfile, outputfile, f.read(), rate)

def main_bytes(inputfile, outputfile, message, rate):
    em = Embedder()
    return em.embed(inputfile, outputfile, message, rate)

def test_func(data, rate=3):
    em = Embedder()
    inputfile = os.path.join('img', 'clean_lenna.png')
    outputfile = os.path.join('img', 'steg_test_lenna.png') 
    return em.embed(inputfile, outputfile, data, rate)




if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Embed a secret into a png/qoi')
    parser.add_argument('coverimage', type=str, help='Set the cover image file')
    parser.add_argument('outputfile', type=str, help='Set the output file name')
    parser.add_argument('messagefile', type=str, help='Set the file to read for the message')
    parser.add_argument('bits', type=int, nargs='?', default=1, help='Set the number of LSBs used for hiding')
    myargs = parser.parse_args()
    main_files(myargs.coverimage, myargs.outputfile, myargs.messagefile, myargs.bits)
    #main_bytes(myargs.coverimage, myargs.outputfile, b'Hello world!', myargs.bits)


