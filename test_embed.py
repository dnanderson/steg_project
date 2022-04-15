
from PIL import Image
import qoi
import numpy as np


def bit_getter(message):
    for byte in bytes(message):
        for x in range(8):
            yield (byte & 1) 
            byte = byte >> 1



class Embedder:

    def __init__(self):
        pass

    def embed(self, rgbvals, message, wid, height):
        import pdb; pdb.set_trace()
        msggetter = bit_getter(message)
        try:
            for pixel in rgbvals:
                print(pixel)
        except StopIteration:
            pass
                
            print(pixel[0])


class PNGExtractor:
    def __init__(self, filename):
        import pdb; pdb.set_trace()
        self.im = Image.open(filename)
        self.wid, self.height = self.im.size
        mybytes = self.im.tobytes()
        # These convert from bytes to a PNG image
        #img = Image.frombytes('RGB', self.im.size, mybytes)
        #img.save('outpath.png', 'PNG')
        myarray = np.frombuffer(mybytes, dtype=np.uint8)
        myarray = np.resize(myarray, [self.height, self.wid, 3])

        self.data = myarray

class QOIExtractor:
    def __init__(self, filename):
        self.data = qoi.read(filename)
        




if __name__ == '__main__':
    ex = PNGExtractor('qoi_test_images\kodim23.png')
    wid, height = ex.im.size
    em = Embedder().embed(ex.getdata(), 'Hello!', wid, height)
        