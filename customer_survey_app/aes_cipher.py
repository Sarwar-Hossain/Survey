import base64
import hashlib
import json
from random import Random
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher(object):

    KEY = '0147896325'

    def __init__(self):
        self.bs = AES.block_size
        self.key = hashlib.sha256(self.KEY.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    @staticmethod
    def encrypt_aes_cbc():
        message = bytearray('password', 'utf-8')
        # key = bytearray('9513578524568426', 'utf-8')
        key = get_random_bytes(16)

        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(message, AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        result = json.dumps({'iv': iv, 'ciphertext': ct})
        # print(result)
        return iv, base64.b64encode(key).decode('utf-8')

    @staticmethod
    def decrypt_aes_cbc(encrypted_message, secret_key, initialization_vector):
        print(initialization_vector + ' ' + secret_key)

        key = base64.b64decode(secret_key)
        iv = base64.b64decode(initialization_vector)
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # print(encrypted_message)
        # plaintext = unpad(cipher.decrypt(encrypted_message), AES.block_size)
        # print(plaintext)