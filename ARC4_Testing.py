from Crypto.Cipher import ARC4

class myARC4():
    def __init__(self, keytext):
        self.key = keytext
    #암호화
    def enc(self, plaintext):
        arc4 = ARC4.new(self.key)
        encmsg = arc4.encrypt(plaintext)
        return encmsg
    #복호화
    def dec(self, ciphertext):
        arc4 = ARC4.new(self.key)
        decmsg = arc4.decrypt(ciphertext)
        return decmsg
