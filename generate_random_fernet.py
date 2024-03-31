from cryptography.fernet import Fernet

def Fernet_generate_key():
    with open('fernet.txt', 'wb') as fernet_write:
        fernet_write.write(Fernet.generate_key())
    
if __name__ == '__main__':
    Fernet_generate_key()