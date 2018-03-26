from ciphers.hill import Hill

if __name__ == "__main__":
    hill = Hill(key=[[7, 8], [19, 3]])
    text = ("Once upon a midnight dreary, while I pondered, weak and weary, "
            "Over many a quaint and curious volume of forgotten lore")
    cipher_text = hill.encrypt(text)
    plain_text = hill.decrypt(cipher_text)
    print("Plain text: %s" % plain_text)
    print("Cipher text: %s" % cipher_text)
    print("Used key: %s" % hill.key.tolist())
    key = hill.force_key(plain_text, cipher_text, hill.M).tolist()
    print("Retrieved key: %s" % key)
    # hill_key = Hill(key=key)
    # plain_text_key = hill_key.decrypt(cipher_text)
    # print("Plain text with generated key: %s" % plain_text_key)
