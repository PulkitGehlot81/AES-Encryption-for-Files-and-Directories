import os
from Cryptodome.Cipher import AES
from Cryptodome import Random


def encrypt_path(path, key):
    """
    Encrypts a file or directory at the specified path using AES encryption with the given key.

    If `path` is a directory, encrypts all files in the directory recursively.

    :param path: the path to the file or directory to encrypt
    :param key: the encryption key (must be 16, 24, or 32 bytes long)
    """
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                print(f"{file_path} is encrypting.")
                encrypt_file(file_path, key)
    elif os.path.isfile(path):
        encrypt_file(path, key)
    else:
        print("it's a special file(socket,FIFO,device file)")


def encrypt_file(path, key):
    """
    Encrypts a file at the specified path using AES encryption with the given key.

    :param path: the path to the file to encrypt
    :param key: the encryption key (must be 16, 24, or 32 bytes long)
    """
    # get the plaintext
    with open(path, "rb") as f:
        plain_text = f.read()

    iv = Random.new().read(AES.block_size)
    mycipher = AES.new(key, AES.MODE_CFB, iv)
    ciphertext = iv + mycipher.encrypt(plain_text)

    # output
    with open(path + ".bin", "wb") as file_out:
        file_out.write(ciphertext[16:])


if __name__ == "__main__":
    path = input("Enter the path to the file or directory to encrypt: ")
    key = input("Enter the encryption key (must be 16, 24, or 32 bytes long): ")

    try:
        key_bytes = bytes(key, encoding="utf-8")
        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError("Encryption key must be 16, 24, or 32 bytes long")
    except Exception as e:
        print(f"Invalid encryption key: {e}")
        exit(1)

    if os.path.exists(path):
        encrypt_path(path, key_bytes)
    else:
        print(f"Invalid path: {path}")
        exit(1)
