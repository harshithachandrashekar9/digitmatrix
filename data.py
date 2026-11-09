"""Small digit-image dataset: 8x8 grey images (0-16) from scikit-learn's bundled digits set.
30 training and 20 test images per digit (300 / 200 images)."""
import numpy as np
from sklearn.datasets import load_digits

def load_small(n_train=30, n_test=20, seed=0):
    d = load_digits(); rng = np.random.default_rng(seed)
    tr, te = [], []
    for c in range(10):
        idx = rng.permutation(np.where(d.target == c)[0])
        tr += list(idx[:n_train]); te += list(idx[n_train:n_train + n_test])
    tr, te = np.array(tr), np.array(te)
    return (d.images[tr] / 16.0, d.target[tr], d.images[te] / 16.0, d.target[te])
