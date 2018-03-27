from math import gcd
import numpy as np
import string
import random
import re


class Hill:
    """Hill cipher."""

    def __init__(self, key=None, key_dimension=2, alphabet=None):
        """Init the Hill cypher class.

        Args:
            key: a specific matrix key, must be invertible. es: [[1,2], [3,4]]
                [DEFAULT: None]
            key_dimension: the dimension of the key matrix.
                [DEFAULT: 2]
            alphabet: the alphabet to be used to encrypt and decrypt.
                [DEFAULT: ascii_lowercase letters]
        """
        self.random = random.SystemRandom()
        self.M = key_dimension if key is None else len(key)
        self.alphabet = (alphabet if alphabet is not None
                         else string.ascii_lowercase)
        self.N = len(self.alphabet)
        self.key, self.key_i = self._generate_key(key)
        self.extra_letters = 0

    def _generate_key(self, key):
        """Generate a random matrix M x M."""
        not_invertible = True
        f = np.vectorize(lambda x: int(round(x)) if x.is_integer() else None)
        f2 = np.vectorize(lambda x: int(round(x)))
        if key:
            # check if invertible
            try:
                key = np.array(key)
                key_i = np.linalg.inv(key)
                return key, key_i
            except:
                raise Exception("Key is not invertible.")
        # try making a random generate key until it get an invertible one
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
            self.extra_letters = self.M - (len(text) % self.M)
            if self.extra_letters != 0:
                text += ''.join(['z' for i in range(self.extra_letters)])
        matrix = list(map(
            lambda q: [self.alphabet.index(c) for c in q],
            [text[n:n + self.M] for n in range(0, len(text), self.M)]
        ))
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
        cipher_grams = []
        for q_gram in q_grams:
            cipher_grams.append(mod_func(self.key.dot(q_gram.T)).tolist())
        cipher_grams = np.array(cipher_grams)
        return self._matrix_to_string(cipher_grams)

    def decrypt(self, cipher_text):
        """Decrypt a precedently encrypted plain text with the class key."""
        q_grams = self._string_to_matrix(cipher_text, plain_text=False)
        mod_func = np.vectorize(lambda x: x % self.N)
        plain_text = []
        for q_gram in q_grams:
            plain_text.append(mod_func(self.key_i.dot(q_gram.T)).tolist())
        plain_text = np.array(plain_text)
        # if there where extra letters, remove them
        if self.extra_letters != 0:
            return self._matrix_to_string(plain_text)[:-(self.extra_letters)]
        return self._matrix_to_string(plain_text)

    def _is_invertible(self, matrix):
        """Check if a matrix is invertible mod N.
        Is invertible if the GDC of the matrix determinant and
        the alphabet lenght is 1.
        """
        return gcd(int(round(np.linalg.det(matrix))) % self.N, self.N) == 1

    @staticmethod
    def _egcd(a, b):
        """Extends the euclidian gdc with negative numbers."""
        if a == 0:
            return (b, 0, 1)
        g, y, x = Hill._egcd(b % a, a)
        return (g, x - (b // a) * y, y)

    def _modinv(self, det):
        """Returns the inverse of a matrix's determinant with the alphabet
        lenght.
        """
        g, x, y = Hill._egcd(det, self.N)
        return x % self.N

    def _invert_matrix(self, matrix):
        """ Invert a matrix using Cramer method adapted in mod N.
        Aji is the A matrix without the j-th row and i-th column.
        Every element in A^-1 i,j = -1^(i+j) * det A^1- * 1/det A
        where 1/det A = (det A)^-1 mod N.
        """
        det_A = int(round(np.linalg.det(matrix))) % self.N
        det_A_inv = self._modinv(det_A)
        P_inv = np.empty([len(matrix), len(matrix)])
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                tmp_matrix = np.delete(matrix, j, 0)  # remove row j
                tmp_matrix = np.delete(tmp_matrix, i, 1)  # remove column i
                P_inv[i][j] = (
                    (pow(-1, i + j) *
                     int(round(np.linalg.det(tmp_matrix))) * det_A_inv)
                    % self.N
                )
        return P_inv

    def force_key(self, plain_text, cipher_text, block_length):
        """Force the retrivement of the cipher's key using a matrix made
        from block of known plain text and cipher text.
        It calculate the inverse of a matrix of plain texts P and use it
        with a matrix of cipher texts C to calculate the key K.
            K = C * P^-1

        Args:
            plain_text: a plain text.
            cipher_text: its cipher text encrypted with the same Hill cipher/
            block_length: the lenght of the block
        """
        plain_text = self._clear_text(plain_text)
        mod_func = np.vectorize(lambda x: int(x % self.N))
        last_block = 0
        is_invertible = False
        # keep trying forcing block of plain text until it gets an invertible P
        while not is_invertible:
            P, C = [], []
            if last_block + pow(block_length, 2) > len(plain_text):
                print("> Invertible P not found, trying anyway...")
                break
            for block in range(
                    last_block,
                    last_block + pow(block_length, 2),
                    block_length):
                if last_block + pow(block_length, 2) > len(plain_text):
                    break
                P.append(self._string_to_matrix(
                    plain_text[block:block + block_length]).tolist()[0])
                C.append(self._string_to_matrix(
                    cipher_text[block:block + block_length]).tolist()[0])
            P = np.matrix(P).T
            C = np.matrix(C).T
            last_block += block_length
            is_invertible = self._is_invertible(P)

        # invert and calculate key
        P_inv = self._invert_matrix(P)
        key = mod_func(C * P_inv)
        return key.tolist()
