import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Cipher import AES

class AESCipher(object):

    def __init__(self, key='matilda'):
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return base64.b64encode(iv + cipher.encrypt(b'%r'%raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.decrypt(enc[AES.block_size:]).decode('utf-8')

