
import chunk
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, padding

shared_key = b'Q\xdf\xc7\x8c\xa6\x84\xf1d\r\n\x9a6\xbdq\xadA'

# For encrypting the input information to be hidden

class encryptor:
    def __init__(self, key, nonce):
        import pdb; pdb.set_trace()
        self.cipher = Cipher(algorithms.AES(key), modes.CTR(nonce)).encryptor()
    
    def __call__(self, data):
        """
        Uses the saved cipher to encrypt the next hack
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

class hasher:

    def __init__(self, initial):
        self.initial = initial
        self.hashobj = hashes.Hash(hashes.SHA256())
        self.last = initial

    def __call__(self):
        """
        This hashes the previous hash, creating a new block
        This is essentially continuing a random number generator
        """
        self.hashobj.update(self.last)
        self.last = self.hashobj.finalize()
        self.hashobj = hashes.Hash(hashes.SHA256())
        return self.last

