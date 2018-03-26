from collections import Counter
from moby_dick import CHAPTER_ONE

import matplotlib.pyplot as plt
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


def empiric_distrobution(q, text):
    """ TODO """
    assert q >= 2, ("Choose a q >= 2")
    q_grams = [text[n:n+2] for n in range(0, len(text), q)]
    counter = Counter(q_grams)


def coincidence_and_entropy(q, text):
    """ TODO """
    assert q >= 2, ("Choose a q >= 2")
    q_grams = [text[n:n+2] for n in range(0, len(text), q)]
    counter = Counter(q_grams)
