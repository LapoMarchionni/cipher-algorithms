from itertools import cycle
from random import SystemRandom
import string
import binascii
import os
import re


class Vigenere:
    """Vigenere cypher."""

    def __init__(self, key=None, alphabet=None, key_length=32):
        """Init the Vigenere Cypher class.

        Args:
            key: a string used as the cypher key.
                [DEFAULT: random generated string of letters]
            alphabet: the alphabet to be used to encrypt and decrypt.
                [DEFAULT: ascii_lowercase letters]
            key_length: the length of the randomly generated key.
                [DEFAULT: 32]
        """
        self.key_length = key_length
        self.key = key if key is not None else self._generate_key()
        self.alphabet = (alphabet if alphabet is not None
                         else string.ascii_lowercase)
        self.language_length = len(self.alphabet)

    def _generate_key(self):
        """Generate a random key with lenght key_length."""
        random = SystemRandom()
        return ''.join(random.choice(
            string.ascii_lowercase) for x in range(self.key_length))

    def _clear_text(self, text):
        """Remove every space and punctuations."""
        return re.sub('[' + string.punctuation + '|\s]', '', text).lower()

    def encrypt(self, plain_text):
        """Encrypt a plain text using the entered or generated key. Before
        encrypting it strips the text of its spaces and punctuations calling
        the _clear_text function.

        Args:
            plain_text: a basic text to be encrypted.
        Returns:
            The relative encrypted cypher text.
        """
        key_char_pairs = zip(self._clear_text(plain_text), cycle(self.key))
        cypher_text = ""
        for pair in key_char_pairs:
            e_char = ((self.alphabet.index(pair[0]) +
                       self.alphabet.index(pair[1])) % self.language_length)
            cypher_text += self.alphabet[e_char]
        return cypher_text

    def decrypt(self, cypher_text):
        """Decrypt a cypher text using key used to encrypt it. The result is
        still without spaces and punctuations.

        Args:
            cypher_text: an encrypted text to be decrypted.
        Returns:
            The relative decrypted plain text.
        """
        key_char_pairs = zip(cypher_text, cycle(self.key))
        plain_text = ""
        for pair in key_char_pairs:
            e_char = ((self.alphabet.index(pair[0]) -
                       self.alphabet.index(pair[1])) % self.language_length)
            plain_text += self.alphabet[e_char]
        return plain_text
