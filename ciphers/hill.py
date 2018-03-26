from fractions import gdc
import numpy as np
import string
import random
import re


class Hill:
    """Hill cypher."""

    def __init__(self, key_dimension=2, alphabet=None):
        """Init the Hill cypher class.

        Args:
            key_dimension: the dimension of the key matrix.
                [DEFAULT: 2]
            alphabet: the alphabet to be used to encrypt and decrypt.
                [DEFAULT: ascii_lowercase letters]
        """
        self.random = random.SystemRandom()
        self.M = key_dimension
        self.alphabet = (alphabet if alphabet is not None
                         else string.ascii_lowercase)
        self.N = len(self.alphabet)
        self.key, self.key_i = self._generate_key()
        self.extra_letters = 0

    def _generate_key(self):
        """Generate a random matrix M x M."""
        not_invertible = True
        f = np.vectorize(lambda x: int(x) if x.is_integer() else None)
        while not_invertible:
            key = np.array(np.random.randint(self.N, size=(self.M, self.M)))
            try:
                key_i = f(np.linalg.inv(key))
                not_invertible = None in key_i
            except:
                not_invertible = True
        return key, key_i

    def _clear_text(self, text):
        """Remove every space and punctuations."""
        return re.sub('[' + string.punctuation + '|\s]', '', text).lower()

    def _string_to_matrix(self, text, plain_text=True):
        """Convertr a text into a matrix of q-grams long M. If the lenght
        of the text is not a multiplier of M, then add extra letters to
        the text that will be removed later.
        """
        if plain_text:
            self.extra_letters = len(text) % self.M
            if self.extra_letters != 0:
                text += ''.join(['z' for i in range(self.extra_letters)])
        matrix = map(
            lambda q: [self.alphabet.index(c) for c in q],
            [text[n:n+2] for n in range(0, len(text), self.M)]
        )
        return np.array(matrix)

    def _matrix_to_string(self, matrix):
        """Convert a matrix of q-grams to a text. If extra letters where added
         to the initial string they are removed.
        """
        text = ''
        for q_gram in matrix:
            text += ''.join([self.alphabet[i] for i in q_gram])
        return text

    def encrypt(self, plain_text):
        """Encrypt a plain text using the entered or generated key. Before
        encrypting it strips the text of its spaces and punctuations calling
        the clear_text function and create the q-grams matrix for
        the plain text.

        Args:
            plain_text: a basic text to be encrypted.
        Returns:
            The relative encrypted cypher text.
        """
        q_grams = self._string_to_matrix(self._clear_text(plain_text))
        mod_func = np.vectorize(lambda x: x % self.N)
        cypher_grams = []
        for q_gram in q_grams:
            cypher_grams.append(mod_func(self.key.dot(q_gram)).tolist())
        cypher_grams = np.array(cypher_grams)
        return self._matrix_to_string(cypher_grams)

    def decrypt(self, cipher_text):
        """Decrypt a precedently encrypted plain text with the class key."""
        q_grams = self._string_to_matrix(cipher_text, plain_text=False)
        mod_func = np.vectorize(lambda x: x % self.N)
        plain_text = []
        for q_gram in q_grams:
            plain_text.append(mod_func(self.key_i.dot(q_gram)).tolist())
        plain_text = np.array(plain_text)
        if self.extra_letters != 0:
            return self._matrix_to_string(plain_text)[:-(self.extra_letters)]
        return self._matrix_to_string(plain_text)

    def _is_invertible(self, matrix):
        """Check if a matrix is invertible mod N."""
        pass

    def force_key(self, plain_text, cipher_text, block_length):
        plain_text = self._clear_text(plain_text)
        last_block = 0
        is_invertible = False
        while not is_invertible:
            P, C = [], []
            for block in range(last_block, block_length**2, block_length):
                P.append(self._string_to_matrix(
                    plain_text[block:block+block_length]).tolist()[0])
                C.append(self._string_to_matrix(
                    cipher_text[block:block+block_length]).tolist()[0])
            P = np.matrix(P)
            C = np.matrix(C)
            is_invertible = self._is_invertible(P)
            print(is_invertible)
