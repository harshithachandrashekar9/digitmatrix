import json, os, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from data import load_small
from digits_pipeline import *
FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures"); R = json.load(open(f"{FIG}/results.json"))
Xi, y, Ti, ty = load_small(); m = fit(Xi, y); Vt = m["Vt"]; cm_ = "gray_r"
def save(f, n): f.tight_layout(); f.savefig(f"{FIG}/{n}", dpi=130); plt.close(f)
# 1 samples
f, ax = plt.subplots(4, 10, figsize=(9, 3.9))
for c in range(10):
    ids = np.where(y == c)[0][:4]
    for r_, i in enumerate(ids): ax[r_, c].imshow(Xi[i], cmap=cm_); ax[r_, c].axis("off")
    ax[0, c].set_title(str(c))
f.suptitle("Training images (8 × 8 pixel matrices)"); save(f, "fig1_samples.png")
# 2 matrix & vector
d = Xi[np.where(y == 3)[0][0]]; f, ax = plt.subplots(1, 2, figsize=(8, 4))
ax[0].imshow(d, cmap=cm_)
for i in range(8):
    for j in range(8): ax[0].text(j, i, f"{d[i,j]*16:.0f}", ha="center", va="center", color="red" if d[i, j] > .5 else "black", fontsize=8)
ax[0].set_title("Digit '3' as an 8×8 matrix (0–16)"); ax[0].set_xticks([]); ax[0].set_yticks([])
ax[1].plot(vectorize(d), color="#1d4ed8"); ax[1].set_title("Same digit as a vector in R⁶⁴"); ax[1].set_xlabel("pixel index"); ax[1].set_ylabel("intensity (0–1)"); save(f, "fig2_matrix_vector.png")
# 3 mean + eigen digits
f, ax = plt.subplots(2, 5, figsize=(9, 4.2)); ax = ax.ravel()
ax[0].imshow(m["mu"].reshape(8, 8), cmap=cm_); ax[0].set_title("mean image μ")
for i in range(9): ax[i + 1].imshow(Vt[i].reshape(8, 8), cmap="RdBu_r", vmin=-.6, vmax=.6); ax[i + 1].set_title(f"PC{i+1} ({R['explained'][i]:.1f}%)", fontsize=9)
for a in ax: a.axis("off")
f.suptitle("Mean image and the first nine principal directions (right singular vectors)"); save(f, "fig3_eigendigits.png")
# 4 scree
f, a = plt.subplots(figsize=(6.5, 4)); n = 30; a.bar(range(1, n + 1), R["explained"][:n], color="#1d4ed8", label="each"); a.plot(range(1, n + 1), R["cum"][:n], "o-", color="#c2410c", ms=3, label="cumulative")
a.axhline(90, ls="--", color="gray"); a.text(22, 91.5, "90%"); a.set_xlabel("component"); a.set_ylabel("% variance"); a.set_title("Variance explained"); a.legend(); save(f, "fig4_scree.png")
# 5 2D scatter
Z = project_many(m, np.array([vectorize(i) for i in Xi]), 2); f, a = plt.subplots(figsize=(6.4, 5))
sc = a.scatter(Z[:, 0], Z[:, 1], c=y, cmap="tab10", s=18)
for c in range(10): a.text(*Z[y == c].mean(0), str(c), fontsize=14, weight="bold")
a.set_xlabel("PC1"); a.set_ylabel("PC2"); a.set_title("Training digits projected to 2 dimensions"); f.colorbar(sc, ax=a, ticks=range(10)); save(f, "fig5_projection2d.png")
# 6 reconstructions
ks = [1, 2, 5, 10, 20, 40, 64]; i0 = 7; x = vectorize(Ti[i0]); f, ax = plt.subplots(1, len(ks) + 1, figsize=(10, 1.9))
ax[0].imshow(Ti[i0], cmap=cm_); ax[0].set_title("original", fontsize=9)
for j, k in enumerate(ks):
    z = project_many(m, x[None], k)[0]; ax[j + 1].imshow(reconstruct(m, z, k).reshape(8, 8), cmap=cm_, vmin=0, vmax=1); ax[j + 1].set_title(f"k={k}", fontsize=9)
for a in ax: a.axis("off")
save(f, "fig6_reconstruction.png")
# 7 accuracy and reconstruction error
f, ax = plt.subplots(1, 2, figsize=(9, 3.6)); kk = [int(k) for k in R["acc"]]
ax[0].plot(kk, [R["acc"][str(k)] * 100 for k in kk], "o-", color="#1d4ed8"); ax[0].axhline(R["baseline_raw"] * 100, ls="--", color="#c2410c", label="raw 64 pixels")
ax[0].set_xlabel("components k"); ax[0].set_ylabel("test accuracy %"); ax[0].set_title("Accuracy vs k"); ax[0].legend()
ax[1].plot(kk, [R["rec_err"][str(k)] for k in kk], "o-", color="#15803d"); ax[1].set_xlabel("components k"); ax[1].set_ylabel("mean ‖x − x̂‖"); ax[1].set_title("Reconstruction error vs k"); save(f, "fig7_accuracy_error.png")
# 8 confusion
cm = np.array(R["cm20"]); f, a = plt.subplots(figsize=(5.6, 5)); a.imshow(cm, cmap="Blues")
for i in range(10):
    for j in range(10): a.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > 10 else "black", fontsize=8)
a.set_xticks(range(10)); a.set_yticks(range(10)); a.set_xlabel("predicted"); a.set_ylabel("true"); a.set_title("Confusion matrix (k = 20, 200 test images)"); save(f, "fig8_confusion.png")
# 9 unknown digit
res = predict(m, Ti[i0], 20); f, ax = plt.subplots(1, 3, figsize=(10, 3.2), gridspec_kw={"width_ratios": [1, 1, 2.2]})
ax[0].imshow(Ti[i0], cmap=cm_); ax[0].set_title("unknown digit"); ax[0].axis("off")
ax[1].imshow(res["xhat"].reshape(8, 8), cmap=cm_, vmin=0, vmax=1); ax[1].set_title("reconstruction (k=20)"); ax[1].axis("off")
ax[2].bar(range(10), res["scores"], color=["#15803d" if c == res["digit"] else "#999" for c in range(10)]); ax[2].set_xticks(range(10)); ax[2].set_xlabel("stored digit pattern"); ax[2].set_ylabel("cosine similarity"); ax[2].set_title(f"similarity scores → predicted {res['digit']}"); save(f, "fig9_prediction.png")
print("ok")
