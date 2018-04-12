from collections import Counter
from moby_dick import CHAPTER_ONE

# import matplotlib.pyplot as plt
import numpy as np
import string
import re


def clear_text(text):
    """Remove every space and punctuations."""
    return re.sub('[' + string.punctuation + '|\s]', '', text).lower()


def letters_frequency(text):
    """Return the histogram of letter frequencies in a given
    text and draw the plot using matplotlib.

    Args:
        text: the text to be parsed [DEFAULT; Firts chapter of Moby Dick]
    """
    text = clear_text(text)
    text_len = float(len(text))

    # calculate frequencies
    frequencies = {
        k: (v, v / text_len) for k, v in Counter(text.lower()).items()
    }
    for k, v in frequencies.items():
        print('Letter: {} - Count: {} - Frequency: {} ~ {} %'
              .format(k, v[0], v[1], v[1]*100))

    # draw histogram plot
    bar = np.arange(len(frequencies))
    plt.bar(bar, [f[1] for f in frequencies.values()], align='center')
    plt.xticks(bar, frequencies.keys())
    plt.grid()
    plt.show()


FP = {
    'A': 0.08167,
    'B': 0.01492,
    'C': 0.02782,
    'D': 0.04253,
    'E': 0.12702,
    'F': 0.02228,
    'G': 0.02015,
    'H': 0.06094,
    'I': 0.06966,
    'J': 0.00153,
    'K': 0.00772,
    'L': 0.04025,
    'M': 0.02406,
    'N': 0.06749,
    'O': 0.07507,
    'P': 0.01929,
    'Q': 0.00095,
    'R': 0.05987,
    'S': 0.06327,
    'T': 0.09056,
    'U': 0.02758,
    'V': 0.00978,
    'W': 0.0236,
    'X': 0.0015,
    'Y': 0.01974,
    'Z': 0.00074
}


def shift_frequency(row):
    """Returns the max Mg value of a single row by comparing every
    possible letter.
    """
    fp = list(FP.values())
    row_count, row_len = Counter(row), len(row)
    max_value, max_g = 0, 0
    row = list(set(row))
    row_d = {l: row_count[l] for l in row}
    alpha = string.ascii_uppercase
    for l in string.ascii_uppercase:
        if l not in row_d:
            row_d[l] = 0
    for g in range(26):
        mg = []
        for j in range(26):
            letter = alpha[(g+j) % 26]
            fg = row_count[letter]/row_len
            pj = fp[j]
            mg.append(fg*pj)
        value_mg = sum(mg)
        if value_mg > max_value:
            max_value = value_mg
            max_g = alpha[g]
    return max_g, max_value
