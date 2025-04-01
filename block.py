import hashlib
import json

class Block:

    def __init__(self, indice, timestamp, date, hash_previous, nonce=0):
        self.indice = indice
        self.timestamp = timestamp
        self.date = date
        self.hash_previous = hash_previous
        self.nonce = nonce
        self.hash_current = self.make_hash()

    def make_hash(self):
        block_str = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()
    
    def __str__(self):
        return f"Bloco #{self.indice} | Hash: {self.hash_current}"
    
bloco1 = Block(1, "12:12:00", "31/03/2025", "DFD5FD2F84D3F8D4F2D8G")
print(bloco1)