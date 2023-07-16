import os
from cryptography.fernet import Fernet

# # string the key in a file
# if os.path.isfile('filekey.key'):
#     with open('filekey.key', 'rb') as filekey:
#         key = filekey.read()
#         fernet = Fernet(key)

# else:    
#     with open('filekey.key', 'wb') as filekey:
#         key = Fernet.generate_key()
#         filekey.write(key)
#         fernet = Fernet(key)



def encrypt(path, key):
    fernet = Fernet(key)
    with open(path, 'rb') as file:
        original = file.read()

    encrypted = fernet.encrypt(original)

    with open(path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

    #확장자 바꾸기
    new_filename = path + '.enc'
    os.rename(path, new_filename)


def decrypt(path, key):
    fernet = Fernet(key)
    with open(path, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    decrypted = fernet.decrypt(encrypted)

    with open(path, 'wb') as dec_file:
        dec_file.write(decrypted)
            
    #확장자 복구하기
    new_filename = path[:-4]
    os.rename(path, new_filename)
