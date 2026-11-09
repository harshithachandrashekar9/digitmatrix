"""Digit image -> matrix -> vector -> normalisation -> SVD/PCA -> projection
-> inner-product similarity -> prediction."""
import numpy as np


def vectorize(img):
    """8x8 matrix -> vector in R^64 (row-major)."""
    return np.asarray(img, float).reshape(-1)


def fit(train_imgs, train_labels):
    X = np.array([vectorize(i) for i in train_imgs])          # N x 64 data matrix
    mu = X.mean(axis=0)                                         # mean image (normalisation)
    Xc = X - mu
    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)           # Xc = U S V^T
    var = s**2 / (X.shape[0] - 1)                               # eigenvalues of covariance
    return {"mu": mu, "U": U, "s": s, "Vt": Vt, "var": var,
            "explained": var / var.sum(), "labels": np.asarray(train_labels), "Xc": Xc}


def project_many(model, X, k):
    return (X - model["mu"]) @ model["Vt"][:k].T


def reconstruct(model, z, k):
    """Back-projection x_hat = mu + V_k z (closest point in the subspace)."""
    return model["mu"] + model["Vt"][:k].T @ z


def class_templates(model, k):
    """Stored patterns: mean projected vector of every digit class."""
    Z = model["U"][:, :k] * model["s"][:k]                      # training coordinates = U_k S_k
    labels = model["labels"]
    return np.array([Z[labels == c].mean(axis=0) for c in range(10)])


def cosine(a, B):
    """Normalised inner product between vector a and each row of B."""
    return (B @ a) / (np.linalg.norm(B, axis=1) * np.linalg.norm(a) + 1e-12)


def predict(model, img, k):
    z = project_many(model, vectorize(img)[None, :], k)[0]
    T = class_templates(model, k)
    sims = cosine(z, T)
    x = vectorize(img); xhat = reconstruct(model, z, k)
    return {"digit": int(np.argmax(sims)), "scores": sims, "z": z,
            "residual": float(np.linalg.norm(x - xhat)),
            "xhat": xhat}


def evaluate(model, imgs, labels, k):
    T = class_templates(model, k)
    Z = project_many(model, np.array([vectorize(i) for i in imgs]), k)
    Zn = Z / (np.linalg.norm(Z, axis=1, keepdims=True) + 1e-12); Tn = T / np.linalg.norm(T, axis=1, keepdims=True)
    pred = np.argmax(Zn @ Tn.T, axis=1)
    cm = np.zeros((10, 10), int)
    for t, p in zip(labels, pred): cm[t, p] += 1
    return float((pred == labels).mean()), cm, pred
