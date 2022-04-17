
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding
import bitarray
import bitarray.util

shared_key = b'Q\xdf\xc7\x8c\xa6\x84\xf1d\r\n\x9a6\xbdq\xadA'

# For encrypting the input information to be hidden

class encryptor:
    def __init__(self, key, nonce):
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    
    def __call__(self, data):
        """
        Uses the saved cipher to encrypt  
        """
        remaining_chunk = len(data) % 128
        if remaining_chunk != 0:
            pad = padding.ANSIX923(128).padder()
            last_boundary = len(data) - remaining_chunk
            chunked_data = data[:last_boundary]
            last_chunk = data[last_boundary:last_boundary+remaining_chunk]
            padded_last = pad.update(last_chunk)
            padded_last += pad.finalize()
            return self.cipher.update(chunked_data+padded_last)
        else:
            return self.cipher.update(data)

class decryptor:
    def __init__(self, key, nonce):
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(nonce)).decryptor()
    
    def __call__(self, data):
        return self.cipher.update(data)

def hasher(initial, yieldamt):
    last = initial
    while True:
        hashobj = hashes.Hash(hashes.SHA256())
        hashobj.update(last)
        curhash = hashobj.finalize()
        last = curhash
        ba = bitarray.bitarray(buffer=curhash)
        pos = 0
        ba2int = bitarray.util.ba2int
        while True:
            yi = ba[pos:pos+yieldamt]
            if len(yi) != yieldamt: break
            pos += yieldamt
            yield ba2int(yi, signed=False)

if __name__ == '__main__':
    import os
    import pdb; pdb.set_trace()
    ha = hasher(shared_key, 2)
    for x in range(10000):
        ba = next(ha)

# class hasher:

#     def __init__(self, initial):
#         self.initial = initial
#         self.hashobj = hashes.Hash(hashes.SHA256())
#         self.last = initial
#         self.hashobj.update(self.last)

#     def __call__(self):
#         """
#         This hashes the previous hash, creating a new block
#         This is essentially continuing a random number generator
#         """
#         self.hashobj.update(self.last)
#         self.last = self.hashobj.finalize()
#         self.hashobj = hashes.Hash(hashes.SHA256())
#         return self.last
    
#     def __next__(self):
        


