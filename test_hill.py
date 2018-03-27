from ciphers.hill import Hill

if __name__ == "__main__":
    hill = Hill()
    text = "Friday monday thusday"
    cipher_text = hill.encrypt(text)
    plain_text = hill.decrypt(cipher_text)
    print("Plain text: %s" % plain_text)
    print("Cipher text: %s" % cipher_text)
    print("Used key: %s" % hill.key.tolist())
    key = hill.force_key(plain_text, cipher_text, hill.M)
    print("Retrieved key: %s" % key)
    print("Same keys: %s" % (key == hill.key.tolist()))