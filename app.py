"""DigitMatrix – handwritten-digit recognition with SVD/PCA.  Run: streamlit run app.py"""
import numpy as np, pandas as pd, streamlit as st
import matplotlib.pyplot as plt
from data import load_small
from digits_pipeline import fit, vectorize, project_many, reconstruct, predict, evaluate, class_templates

st.set_page_config(page_title="DigitMatrix", page_icon="🔢", layout="wide"); plt.style.use("dark_background")

@st.cache_data
def prepare():
    Xi, y, Ti, ty = load_small(); return Xi, y, Ti, ty, fit(Xi, y)
Xi, y, Ti, ty, m = prepare(); Vt = m["Vt"]

st.sidebar.title("🔢 DigitMatrix")
k = st.sidebar.slider("Components k", 1, 56, 20)
src = st.sidebar.radio("Unknown digit", ["Pick a test image", "Edit pixels (8×8)"])
if src == "Pick a test image":
    idx = st.sidebar.number_input("Test image index", 0, len(ty) - 1, 7); unk = Ti[int(idx)]; truth = int(ty[int(idx)])
else:
    base = pd.DataFrame(np.zeros((8, 8)), columns=[f"c{i}" for i in range(8)])
    ed = st.sidebar.data_editor(base, num_rows="fixed"); unk = np.clip(ed.to_numpy(float) / 16, 0, 1); truth = None
    st.sidebar.caption("Enter intensities 0–16 in the grid.")

st.title("🔢 DigitMatrix")
st.caption("Digit image → matrix → vector → normalisation → SVD/PCA → projection → inner-product similarity → prediction")
c1, c2, c3 = st.columns(3)
acc, cm, _ = evaluate(m, Ti, ty, k)
c1.metric("Training images", len(y)); c2.metric(f"Variance kept (k={k})", f"{m['explained'][:k].sum()*100:.1f}%"); c3.metric("Test accuracy", f"{acc*100:.1f}%")
tabs = st.tabs(["🖼 Matrix & vector", "📉 SVD / PCA", "🎯 Projection", "🔍 Prediction", "📊 Evaluation"])

with tabs[0]:
    a, b = st.columns(2)
    fig, ax = plt.subplots(figsize=(4, 4)); ax.imshow(unk, cmap="gray_r"); ax.axis("off"); a.pyplot(fig)
    b.write("Digit matrix (0–16):"); b.dataframe(pd.DataFrame(np.round(unk * 16)).astype(int))
    st.write("Vector in R⁶⁴ (row-major):"); st.code(str(np.round(vectorize(unk) * 16).astype(int).tolist()))
    st.latex(r"x = \mathrm{vec}(D)\in\mathbb R^{64},\qquad \tilde x = x-\mu")

with tabs[1]:
    a, b = st.columns(2)
    fig, ax = plt.subplots(figsize=(5, 3.4)); e = m["explained"][:30] * 100; ax.bar(range(1, 31), e, color="#f59e0b"); ax.plot(range(1, 31), np.cumsum(e), "o-", color="#38bdf8", ms=3)
    ax.set_xlabel("component"); ax.set_ylabel("% variance"); a.pyplot(fig)
    fig, ax = plt.subplots(2, 5, figsize=(6, 3)); ax = ax.ravel(); ax[0].imshow(m["mu"].reshape(8, 8), cmap="gray_r"); ax[0].set_title("mean", fontsize=8)
    for i in range(9): ax[i + 1].imshow(Vt[i].reshape(8, 8), cmap="RdBu_r", vmin=-.6, vmax=.6); ax[i + 1].set_title(f"PC{i+1}", fontsize=8)
    for q in ax: q.axis("off")
    b.pyplot(fig); st.latex(r"X_c = U\Sigma V^\top,\qquad \lambda_i=\sigma_i^2/(N-1)")

with tabs[2]:
    z = project_many(m, vectorize(unk)[None], k)[0]; xh = reconstruct(m, z, k)
    a, b = st.columns(2)
    fig, ax = plt.subplots(figsize=(4, 4)); ax.imshow(xh.reshape(8, 8), cmap="gray_r", vmin=0, vmax=1); ax.axis("off"); a.pyplot(fig)
    b.metric("‖x − x̂‖ (residual)", f"{np.linalg.norm(vectorize(unk) - xh):.3f}")
    b.write("Coordinates z (first 10):"); b.write(np.round(z[:10], 3))
    Z = project_many(m, np.array([vectorize(i) for i in Xi]), 2)
    fig, ax = plt.subplots(figsize=(5.5, 4)); sc = ax.scatter(Z[:, 0], Z[:, 1], c=y, cmap="tab10", s=12)
    z2 = project_many(m, vectorize(unk)[None], 2)[0]; ax.scatter(*z2, marker="*", s=300, c="white", edgecolor="red"); st.pyplot(fig)
    st.latex(r"z=V_k^\top(x-\mu),\qquad \hat x=\mu+V_k z")

with tabs[3]:
    res = predict(m, unk, k)
    st.success(f"Predicted digit: **{res['digit']}**" + (f"  (true digit: {truth})" if truth is not None else ""))
    fig, ax = plt.subplots(figsize=(6, 3)); ax.bar(range(10), res["scores"], color=["#15803d" if c == res["digit"] else "#777" for c in range(10)]); ax.set_xticks(range(10))
    ax.set_xlabel("stored digit pattern"); ax.set_ylabel("cosine similarity"); st.pyplot(fig)
    st.latex(r"\mathrm{sim}(z,t_c)=\frac{\langle z,t_c\rangle}{\|z\|\,\|t_c\|},\qquad \text{prediction}=\arg\max_c \mathrm{sim}")
    st.dataframe(pd.DataFrame({"digit": range(10), "similarity": np.round(res["scores"], 3)}), hide_index=True)

with tabs[4]:
    ks = [1, 2, 3, 5, 10, 15, 20, 30, 40, 56]; accs = [evaluate(m, Ti, ty, q)[0] * 100 for q in ks]
    a, b = st.columns(2)
    fig, ax = plt.subplots(figsize=(5, 3.4)); ax.plot(ks, accs, "o-", color="#f59e0b"); ax.set_xlabel("k"); ax.set_ylabel("test accuracy %"); a.pyplot(fig)
    fig, ax = plt.subplots(figsize=(4.6, 4)); ax.imshow(cm, cmap="Blues")
    for i in range(10):
        for j in range(10): ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=7, color="white" if cm[i, j] > 10 else "black")
    ax.set_xlabel("predicted"); ax.set_ylabel("true"); b.pyplot(fig)
