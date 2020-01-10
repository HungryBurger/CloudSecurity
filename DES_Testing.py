from Crypto.Cipher import DES3
from Crypto.Hash import SHA256 as SHA

class myDES():
    def __init__(self, keytext, ivtext):
        hash = SHA.new()
        hash.update(keytext.encode('utf-8'))
        key = hash.digest()
        self.key = key[:24]
        hash.update(ivtext.encode('utf-8'))
        iv = hash.digest()
        self.iv = iv[:8]

    def make8String(self, msg):
        msglen = len(msg)
        filler = ''

        if msglen % 8 != 0:
            filler = '0' * (8 - msglen % 8)

        msg = msg + filler
        return msg
    #암호화
    def enc(self, plaintext):
        plaintext = self.make8String(plaintext)
        des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        encmsg = des3.encrypt(bytes(plaintext, 'utf-8'))
        # encmsg= des3.encrypt(plaintext)
        return encmsg
    #복호화
    # def dec(self, ciphertext):
    #     des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)
    #     decmsg = des3.decrypt(ciphertext)
    #     return decmsg