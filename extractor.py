
from PIL import Image
import qoi
import numpy as np
import os


class PNGExtractor:
    def __init__(self):
        pass
    
    def load(self, filename):
        self.im = Image.open(filename)
        self.wid, self.height = self.im.size
        mybytes = self.im.tobytes()
        # These convert from bytes to a PNG image
        myarray = np.frombuffer(mybytes, dtype=np.uint8)
        myarray = np.resize(myarray, [self.height, self.wid, 3])

        self.data = myarray
        return self.data
    
    def save(self, filename, rgb):
        height, wid, _ = rgb.shape
        img = Image.frombytes('RGB', (wid, height), rgb.tobytes())
        img.save(filename, 'PNG')
        

class QOIExtractor:
    def __init__(self):
        pass
    
    def load(self, filename):
        self.data = qoi.read(filename)
        return self.data
    
    def save(self, filename, rgb):
        qoi.write(filename, rgb)


class Extractor:
    def __init__(self):
        self.png = PNGExtractor()
        self.qoi = QOIExtractor()

    def load(self, filename):
        ext = os.path.splitext(filename)
        if ext[-1] == 'qoi':
            return self.qoi.load(filename)
        else:
            return self.png.load(filename)

    def save(self, filename, rgb):
        ext = os.path.splitext(filename)
        if ext[-1] == 'qoi':
            self.qoi.save(filename, rgb)
        else:
            self.png.save(filename, rgb)
    

if __name__ == '__main__':
    ex = Extractor()
    rgb = ex.load('qoi_test_images\wikipedia_009.qoi')
    ex.save('qoi_test_images\wikipedia_009.png', rgb)
        