from Crypto.Cipher import AES
import base64
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloudnote.settings")
django.setup()

from backend.models import Note


class AESUtil:
    def __init__(self,key,model,iv,encode_):
        self.encode_ = encode_
        self.model =  {'ECB':AES.MODE_ECB,'CBC':AES.MODE_CBC}[model]
        self.key = self.add_to_16(key)
        if model == 'ECB':
            self.aes = AES.new(self.key,self.model) #创建一个aes对象
        elif model == 'CBC':
            self.aes = AES.new(self.key,self.model,iv) #创建一个aes对象

    def add_to_16(self,par):
        par = par.encode(self.encode_)
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self,text):
        text = self.add_to_16(text)
        self.encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(self.encrypt_text).decode().strip()

    def aesdecrypt(self,text):
        text = base64.decodebytes(text.encode(self.encode_))
        self.decrypt_text = self.aes.decrypt(text)
        return self.decrypt_text.decode(self.encode_).strip('\0')

if __name__ == '__main__':
    pr = AESUtil('testtest','CBC',b'HjRP7LlXuSsFMisz','utf-8')
    tempNote = Note.objects.filter(id = 25)
    note_text = tempNote.first().note_text
    en_text = pr.aesencrypt(note_text)
    print('密文:',en_text)
    pr = AESUtil('testtest', 'CBC', b'HjRP7LlXuSsFMisz', 'utf-8')
    t = pr.aesdecrypt(en_text)
    print('明文:',t)
    tempNote.update(note_text = en_text)