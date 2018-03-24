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
        self.key = self._generate_key()
        self.extra_letters = 0

    def _generate_key(self):
        """Generate a random matrix self.M x self.M."""
        return [
            [self.random.randint(0, self.N - 1) for j in range(0, self.M)]
            for i in range(0, self.M)
        ]

    def _clear_text(self, text):
        """Remove every space and punctuations."""
        return re.sub('[' + string.punctuation + '|\s]', '', text).lower()

    def _string_to_matrix(self, text):
        """Convertr a text into a matrix of q-grams long M."""
        matrix = map(
            lambda q: [self.alphabet.index(c) for c in q],
            [text[n:n+2] for n in range(0, len(text), self.M)]
        )
        if len(matrix[-1]) < self.M:
            for extra in range(self.M - len(matrix[-1])):
                matrix[-1].append(self.random.randint(0, self.N - 1))
                self.extra_letters += 1
        return matrix

    def _matrix_to_string(self, matrix):
        """Convert a matrix of q-grams to a text."""
        plain_text = ''
        for q_gram in matrix:
            plain_text += ''.join([self.alphabet[i] for i in q_gram])
        return plain_text[:-(self.extra_letters)]

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
        cypher_grams = []
        for q_gram in q_grams:
            c_gram = []
            for row in self.key:
                c_gram.append(
                    sum([row[i] * q_gram[i] for i in range(0, len(row))]) %
                    self.N)
            cypher_grams.append(c_gram)

        return self._matrix_to_string(cypher_grams)
