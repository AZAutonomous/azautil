import json
import codecs
import numpy as np


def save(data, filename):
    assert type(lol) is dict
    # Copy data to preserve original form in memory
    data = data.copy()
    # Preprocess data
    for (key, val) in data.iteritems():
        # Convert np arrays to lists
        if (type(val) is np.ndarray):
            key = "[np] " + key
            val = val.tolist()

    json.dump(self.data, codecs.open(filename, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

def load(filename):
    raw = codecs.open(filename, 'r', encoding='utf-8').read()
    indata = json.loads(raw)
    # Convert things to ndarray
    for (key, val) in indata.iteritems():
        # Check for [np] tags
        if (key.split(' ', 1)[0] == '[np]'):
            val = np.ndarray(val)
    return data
