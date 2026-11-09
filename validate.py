"""Verification and experiments. Prints numbers used in the report; writes figures/results.json."""
import json, numpy as np
from data import load_small
from digits_pipeline import *
Xi, y, Ti, ty = load_small(); m = fit(Xi, y)
X = np.array([vectorize(i) for i in Xi]); Xc = m["Xc"]; Vt = m["Vt"]
out = {"N": len(y), "Ntest": len(ty)}
cov = Xc.T @ Xc / (len(y) - 1); w = np.sort(np.linalg.eigvalsh(cov))[::-1]
out["eig_vs_svd"] = float(np.max(np.abs(w[:64] - m["var"][:64])))
out["orth"] = float(np.linalg.norm(Vt @ Vt.T - np.eye(Vt.shape[0])))
out["rank_Xc"] = int(np.linalg.matrix_rank(Xc)); out["rank_X"] = int(np.linalg.matrix_rank(X))
out["zero_pixels"] = int((X.std(axis=0) < 1e-12).sum())
k = 10; z = project_many(m, X[:1], k)[0]; xh = reconstruct(m, z, k)
r = (X[0] - m["mu"]) - (xh - m["mu"]); out["proj_orth_resid"] = float(np.abs(Vt[:k] @ r).max())  # residual orthogonal to subspace
out["pyth"] = float(abs(np.linalg.norm(X[0] - m["mu"])**2 - np.linalg.norm(z)**2 - np.linalg.norm(r)**2))
out["frob"] = float(abs(np.sum(Xc**2) - np.sum(m["s"]**2)))
out["explained"] = (m["explained"] * 100).round(2).tolist(); out["cum"] = (np.cumsum(m["explained"]) * 100).round(2).tolist()
ks = [1, 2, 3, 5, 10, 15, 20, 30, 40, 64]; acc = {}; rec = {}
for k in ks:
    acc[k] = evaluate(m, Ti, ty, k)[0]
    Z = project_many(m, np.array([vectorize(i) for i in Ti]), k)
    Xh = m["mu"] + Z @ Vt[:k]; rec[k] = float(np.mean(np.linalg.norm(np.array([vectorize(i) for i in Ti]) - Xh, axis=1)))
out["acc"] = acc; out["rec_err"] = rec
# baseline: nearest class mean in raw pixel space (cosine)
Tm = np.array([X[y == c].mean(0) for c in range(10)]); Xt = np.array([vectorize(i) for i in Ti])
b = np.argmax((Xt / np.linalg.norm(Xt, axis=1, keepdims=True)) @ (Tm / np.linalg.norm(Tm, axis=1, keepdims=True)).T, axis=1)
out["baseline_raw"] = float((b == ty).mean())
k = 20; a, cm, pred = evaluate(m, Ti, ty, k); out["cm20"] = cm.tolist()
out["perclass20"] = (cm.diagonal() / cm.sum(1)).round(2).tolist()
# unknown digit demo
idx = 7; res = predict(m, Ti[idx], 20); out["demo"] = {"index": idx, "true": int(ty[idx]), "pred": res["digit"], "scores": res["scores"].round(3).tolist(), "residual": res["residual"]}
json.dump(out, open("../figures/results.json", "w"), indent=1); print(json.dumps({k: v for k, v in out.items() if k not in ("cm20",)}, indent=1))
