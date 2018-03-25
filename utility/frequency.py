from collections import Counter
from moby_dick import CHAPTER_ONE

import matplotlib.pyplot as plt
import numpy as np
import string


def letters_frequency(text=None):
    """Return the histogram of letter frequencies in a given
    text and draw the plot using matplotlib.

    Args:
        text: the text to be parsed [DEFAULT; Firts chapter of Moby Dick]
    """
    if not text:
        text = CHAPTER_ONE
    text_len = float(len(text))

    # calculate frequencies
    frequencies = {
        k: (v, v / text_len) for k, v in Counter(text.lower()).items()
        if k in string.ascii_lowercase
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
