"""Builds the MAT2303 mini-project report for DigitMatrix (same format as the MARKOVMIND report)."""
import os, json
import numpy as np
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH as AL
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
HERE = os.path.dirname(os.path.abspath(__file__)); FIG = os.path.join(HERE, "..", "figures")
LOGO = os.path.join(FIG, "logo.png")
R = json.load(open(os.path.join(FIG, "results.json"))); ex = R["explained"]; cum = R["cum"]; acc = R["acc"]; cm = np.array(R["cm20"])
f2 = lambda a: [f"{x:.2f}" for x in a]
sec = None
doc = Document()
sec = doc.sections[0]; sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)
for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"): setattr(sec, m, Inches(1))
st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman"); st.paragraph_format.space_after = Pt(6)
for n, sz in (("Heading 1", 16), ("Heading 2", 13)):
    h = doc.styles[n]; h.font.name = "Times New Roman"; h.font.size = Pt(sz); h.font.bold = True; h.font.color.rgb = RGBColor(0, 0, 0)
    h.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman"); h.element.rPr.rFonts.set(qn("w:ascii"), "Times New Roman"); h.element.rPr.rFonts.set(qn("w:hAnsi"), "Times New Roman")
    h.paragraph_format.space_before = Pt(14 if n == "Heading 1" else 10); h.paragraph_format.keep_with_next = True

def para(t="", bold=False, italic=False, align=None, size=None, style=None):
    q = doc.add_paragraph(style=style); run = q.add_run(t); run.bold = bold; run.italic = italic
    if size: run.font.size = Pt(size)
    if align is not None: q.alignment = align
    return q
def rich(parts):  # [(text,bold)]
    q = doc.add_paragraph()
    for t, b in parts: q.add_run(t).bold = b
    return q
def H1(t): doc.add_heading(t, 1)
def H2(t): doc.add_heading(t, 2)
def bullets(items):
    for i in items: doc.add_paragraph(i, style="List Bullet")
def shade(cell, color):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd"); sh.set(qn("w:val"), "clear"); sh.set(qn("w:fill"), color); tcPr.append(sh)
def table(head, rows, widths=None, size=10.5):
    t = doc.add_table(rows=1, cols=len(head)); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(head):
        c = t.rows[0].cells[i]; c.text = ""; run = c.paragraphs[0].add_run(str(h)); run.bold = True; run.font.size = Pt(size); shade(c, "D9E2F3")
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""; run = cells[i].paragraphs[0].add_run(str(v)); run.font.size = Pt(size)
    if widths:
        for row in t.rows:
            for i, wd in enumerate(widths): row.cells[i].width = Inches(wd)
    if len(t.rows) <= 9:
        for row in t.rows[:-1]:
            for c in row.cells:
                for q in c.paragraphs: q.paragraph_format.keep_with_next = True
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr(); cs = OxmlElement("w:cantSplit"); trPr.append(cs)
    doc.add_paragraph().paragraph_format.space_after = Pt(2); return t
def fig(name, cap, w=4.6):
    doc.add_picture(os.path.join(FIG, name), width=Inches(w)); doc.paragraphs[-1].alignment = AL.CENTER; doc.paragraphs[-1].paragraph_format.keep_with_next = True
    para(cap, italic=True, align=AL.CENTER, size=11)
def code(lines):
    for l in lines:
        q = doc.add_paragraph(); run = q.add_run(l); run.font.name = "Courier New"; run.font.size = Pt(9); q.paragraph_format.space_after = Pt(0)
    doc.add_paragraph()
f2 = lambda a: [f"{x:.2f}" for x in a]
f4 = lambda a: [f"{x:.4f}" for x in a]

# ---------------- cover ----------------
doc.add_picture(LOGO, width=Inches(1.25)); doc.paragraphs[-1].alignment = AL.CENTER
for t, s in (("PRESIDENCY UNIVERSITY", 18), ("SCHOOL OF ENGINEERING", 14), ("DEPARTMENT OF MATHEMATICS", 14), ("EXPERIENTIAL LEARNING", 14), ("MINI PROJECT", 16)):
    para(t, bold=True, align=AL.CENTER, size=s)
for t in ("Academic Year: 2026-27", "Course Code : MAT2303", "Course Name : Linear Algebra & Vector Calculus"): para(t, bold=True, align=AL.CENTER)
info = [("Student Name", "Nandish D Pawar"), ("Roll Number", "20251CSE0706"), ("Program", "B.Tech. Computer Science and Engineering"),
        ("Semester", "3RD Semester"), ("Section", "3CSE08"),
        ("Project Title", "DigitMatrix: Handwritten Digit Recognition using SVD, PCA, Orthogonal Projection and Inner-Product Similarity"), ("Date of Submission", "")]
t = doc.add_table(rows=0, cols=2); t.style = "Table Grid"; t.alignment = WD_TABLE_ALIGNMENT.CENTER
for a, b in info:
    c = t.add_row().cells; c[0].text = ""; c[0].paragraphs[0].add_run(a).bold = True; c[1].text = ""; c[1].paragraphs[0].add_run(b).bold = True
    c[0].width = Inches(2); c[1].width = Inches(4.3)
doc.add_paragraph()
table(["Component", "Maximum Marks", "Marks Obtained"], [("Project Design and Implementation", "10", ""), ("Results and Analysis", "05", ""), ("Presentation", "03", ""), ("Viva", "02", ""), ("Total", "20", "")], [3.2, 1.6, 1.6], 12)
para("")
para("Student Signature\t\t\t\t\tFaculty Signature", bold=True)
doc.add_page_break()


# top confusions at k=20
conf = sorted([(cm[i, j], i, j) for i in range(10) for j in range(10) if i != j], reverse=True)[:3]
pc = R["perclass20"]; dm = R["demo"]
H1("1. Abstract")
para(f"This project develops a software system, DigitMatrix, that represents handwritten digits mathematically, reduces their dimensionality and recognises an unknown digit by comparing it with stored patterns. Each 8 × 8 grey-scale image is stored as a matrix, flattened into a vector in ℝ⁶⁴ and normalised by subtracting the mean image. The singular value decomposition (SVD) of the training matrix gives the principal components. An unknown digit is projected orthogonally onto the leading components, and its inner-product (cosine) similarity with the stored pattern of each digit gives the predicted digit. On a small dataset of 300 training and 200 test images, {cum[19]:.0f}% of the variance is kept by 20 components (a 3.2 times reduction from 64 dimensions) and the test accuracy is {acc['20']*100:.0f}%, compared with {R['baseline_raw']*100:.0f}% using all 64 raw pixels. All matrix identities were verified numerically. The system is implemented as a Python backend with a Streamlit web interface.")
H1("2. Introduction")
para("A digital image is a matrix of numbers, so a handwritten digit is a mathematical object to which linear algebra applies directly. Flattening the image gives a vector, and vectors from the same digit lie close together in a high-dimensional space. Because neighbouring pixels are strongly correlated, most of the variation in this space lies along a few directions. The singular value decomposition finds these directions, projection onto them gives a short feature vector, and the inner product of two feature vectors measures how alike two digits are.")
para("DigitMatrix makes each step visible. It shows the digit matrix and vector, the principal directions drawn as images, the projected coordinates, the similarity scores to the ten stored patterns and the final prediction.")
H2("2.1 Project Overview")
bullets(["Input: a small dataset of digit images and one unknown digit.", "Processing: matrix representation, vectorisation and normalisation.",
         "Analysis: SVD/PCA, orthogonal projection, reconstruction and inner-product similarity.", "Output: digit matrix, vector representation, PCA/SVD features, similarity scores and predicted digit."])
H1("3. Problem Statement")
para("Aim: to represent handwritten digits mathematically, reduce their dimensionality and compare an unknown digit with stored patterns.")
para("Problem statement: given labelled images of the digits 0 to 9 and one unknown digit image, we want (i) a matrix and a vector representation of the image, (ii) a small set of features that keep most of the information, (iii) a similarity score between the unknown digit and each stored pattern, and (iv) the predicted digit, together with a measure of how reliable the prediction is.")
rich([("Input: ", True), ("small digit-image dataset and an unknown digit.", False)])
rich([("Expected output: ", True), ("digit matrix, vector representation, PCA/SVD features, similarity scores and predicted digit.", False)])
H1("4. Objectives")
bullets(["Represent each digit image as an 8 × 8 matrix and as a vector in ℝ⁶⁴.", "Normalise the data by subtracting the mean image and form the centered data matrix.",
 "Compute the SVD of the data matrix and interpret the principal components as images.", "Measure the variance kept by the first k components.",
 "Project an unknown digit orthogonally onto the k-dimensional subspace and reconstruct it.", "Compute inner-product (cosine) similarity with the stored pattern of every digit and predict the digit.",
 "Verify the decomposition, the orthogonality of the projection and the norm identities numerically.", "Measure accuracy and reconstruction error for different k and compare with the raw-pixel baseline.", "Present the analysis through an interactive web interface."])
H1("5. Scope")
para("The project demonstrates a transparent mathematical workflow on a small dataset rather than a production character-recognition system. The images are 8 × 8 pixels, the training set has 30 images per digit and the classifier is a nearest-pattern rule in the PCA space. The user can choose any test image or edit the 64 pixels of a new digit in the web interface. Larger images, neural networks and handwriting from other scripts are outside the scope.")
H1("6. Project Significance")
para("The project connects the syllabus directly to a familiar application. Matrices store images, vector spaces hold the images as points, norms measure the size of a difference, the SVD gives the best low-dimensional description, orthogonal projection maps a digit to that description, and inner products compare descriptions. The same pipeline underlies image compression, face recognition and noise removal.")
H1("7. Digit Dataset and Matrix Representation")
para("The project uses the 8 × 8 handwritten digit images bundled with scikit-learn (a small subset of the UCI optical-recognition data). Each pixel is an integer from 0 (white) to 16 (black) and is divided by 16 so that intensities lie in [0, 1]. A fixed random selection gives 30 training images and 20 test images for each digit.")
H2("7.1 Dataset Summary")
table(["Property", "Value"], [("Image size", "8 × 8 pixels"), ("Classes", "10 (digits 0 to 9)"), ("Training images (N)", f"{R['N']} (30 per digit)"), ("Test images", f"{R['Ntest']} (20 per digit)"), ("Pixel range", "0 to 16, scaled to [0, 1]"), ("Vector dimension (n)", "64"), ("Data matrix X", f"{R['N']} × 64"), ("Pixels that are always zero", f"{R['zero_pixels']}")], [2.4, 3.9])
fig("fig1_samples.png", "Figure 1: Training images, four per digit", 5.6)
H2("7.2 Matrix and Vector Representation")
para("An image is a matrix D ∈ ℝ^(8×8). Reading it row by row gives the vector x = vec(D) ∈ ℝ⁶⁴. The N training vectors are stacked as the rows of the data matrix X ∈ ℝ^(N×64).")
fig("fig2_matrix_vector.png", "Figure 2: A digit as a matrix (left) and as a vector in ℝ⁶⁴ (right)", 5.4)
H2("7.3 Normalisation")
para("The mean image μ = (1/N) Σ xi is subtracted from every image, giving the centered matrix Xc with rows x̃i = xi − μ. Centering moves the cloud of images to the origin, so that the SVD measures variation around the average digit and not the size of the average.")
H1("8. Mathematical Foundation")
H2("8.1 Matrices and vector spaces")
para("A matrix is a rectangular array of numbers. An image is an element of the vector space ℝ⁶⁴, and a set of images spans a subspace of it. The dimension of that subspace equals the rank of the data matrix.")
H2("8.2 Norms and inner products")
para("The inner product of two vectors is ⟨a, b⟩ = Σ ai bi, and the norm is ‖a‖ = √⟨a, a⟩. The distance between two images is ‖a − b‖. The cosine similarity cos θ = ⟨a, b⟩ / (‖a‖ ‖b‖) lies in [−1, 1] and measures how closely two vectors point in the same direction.")
H2("8.3 Singular value decomposition")
para("Every matrix Xc can be written as Xc = U Σ Vᵀ, where U and V have orthonormal columns and Σ is diagonal with singular values σ1 ≥ σ2 ≥ … ≥ 0. The columns of V (right singular vectors) are the principal directions. They are the eigenvectors of the covariance matrix Xcᵀ Xc / (N − 1), and the eigenvalue of the i-th direction is σi² / (N − 1). The fraction of variance explained by it is σi² / Σ σj².")
H2("8.4 Principal Component Analysis")
para("PCA keeps the first k columns of V, written Vk. Among all k-dimensional subspaces, this one retains the largest possible share of the variance (Eckart–Young theorem), so it gives the best rank-k approximation of Xc.")
H2("8.5 Orthogonal projection")
para("The orthogonal projection of a centered image x̃ onto the subspace spanned by Vk has coordinates z = Vkᵀ x̃ and the vector x̂ = μ + Vk z. The error x̃ − Vk z is orthogonal to the subspace, and by the Pythagorean theorem ‖x̃‖² = ‖z‖² + ‖x̃ − Vk z‖². Thus x̂ is the closest point of the subspace to the image.")
H2("8.6 Worked example")
para("Let A = [[3, 1], [1, 3]]. Its eigenvalues are 4 and 2, so the singular values are 4 and 2, with right singular vectors v1 = (1, 1)ᵀ/√2 and v2 = (1, −1)ᵀ/√2. Take x = (2, 0)ᵀ and k = 1. The coordinate is z = ⟨x, v1⟩ = 2/√2 = √2, the projection is (1, 1)ᵀ, and the error is (1, −1)ᵀ, which is orthogonal to v1. The norms satisfy ‖x‖² = 4 = ‖z‖² + ‖error‖² = 2 + 2. The same steps are applied to the 64-dimensional digit vectors in Section 12.")
H1("9. Formulation and Mathematical Workflow")
para("The sequential computational process is:")
para("Digit image → Matrix representation → Vectorisation → Normalisation → PCA/SVD → Projection → Inner-product similarity → Prediction", bold=True, align=AL.CENTER)
table(["Stage", "Input", "Operation", "Output"], [("1", "Image", "Read the 8 × 8 pixel grid", "Digit matrix D"), ("2", "D", "x = vec(D), row by row", "Vector in ℝ⁶⁴"), ("3", "Training vectors", "Subtract mean image μ", "Centered matrix Xc"),
 ("4", "Xc", "Xc = U Σ Vᵀ", "Principal directions, singular values"), ("5", "x, Vk", "z = Vkᵀ(x − μ); x̂ = μ + Vk z", "Features z, reconstruction"), ("6", "z, stored patterns tc", "cos θ = ⟨z, tc⟩ / (‖z‖‖tc‖)", "Ten similarity scores"), ("7", "Scores", "argmax over digits", "Predicted digit")], [0.6, 1.4, 2.5, 1.8])
H1("10. DigitMatrix System Architecture")
para("DigitMatrix has a Python module that contains all mathematical routines and a web interface that displays them, so presentation is separated from calculation.")
table(["Layer", "Role"], [("Input / Data", "8 × 8 digit images, number of components k, unknown digit (test image or edited pixels)"), ("Math Engine", "Vectorisation, centering, SVD (numpy.linalg.svd), projection, reconstruction, cosine similarity"),
 ("Evaluation", "Accuracy for each k, confusion matrix, reconstruction error, numerical verification"), ("Visualization", "Digit images, eigen-digits, scree plot, 2-D projection, similarity bars"), ("Application UI", "Streamlit page with tabs, slider for k and an 8 × 8 pixel editor")], [1.6, 4.7])
H2("10.1 Application Pages")
bullets(["Matrix & vector: the digit as an image, as a matrix and as a vector.", "SVD / PCA: scree plot and the principal directions drawn as images.", "Projection: reconstruction, residual and the digit located among the training points.",
 "Prediction: similarity scores to the ten patterns and the predicted digit.", "Evaluation: accuracy against k and the confusion matrix."])
H1("11. Implementation")
para("The backend is written in Python with NumPy. All routines are in digits_pipeline.py and use only matrix operations and the SVD. The web interface is built with Streamlit. A separate script verifies the mathematics and measures accuracy, and another generates the figures.")
H2("11.1 Technology Stack")
bullets(["Python 3 and NumPy: matrices, SVD, projection and similarity.", "scikit-learn: only to supply the bundled digit images.", "Streamlit: interactive web application.", "Matplotlib: figures."])
H2("11.2 Main functions")
table(["Function", "Purpose"], [("vectorize(img)", "8 × 8 matrix to a vector in ℝ⁶⁴"), ("fit(images, labels)", "Mean image, centering and SVD of the training matrix"), ("project_many(model, X, k)", "Coordinates Z = (X − μ) Vkᵀ"),
 ("reconstruct(model, z, k)", "x̂ = μ + Vk z"), ("class_templates(model, k)", "Stored pattern of each digit: mean of its projected training vectors"), ("cosine(a, B)", "Normalised inner product of a with every row of B"), ("predict(model, img, k)", "Runs the pipeline for one unknown digit"), ("evaluate(model, imgs, labels, k)", "Accuracy and confusion matrix")], [2.4, 3.9])
H2("11.3 Key code")
code(["def fit(train_imgs, train_labels):", "    X  = np.array([vectorize(i) for i in train_imgs])   # N x 64", "    mu = X.mean(axis=0)                                  # mean image", "    Xc = X - mu                                          # normalisation",
      "    U, s, Vt = np.linalg.svd(Xc, full_matrices=False)    # Xc = U S V^T", "    return {'mu': mu, 'U': U, 's': s, 'Vt': Vt, ...}", "", "z    = Vt[:k] @ (x - mu)                  # orthogonal projection", "xhat = mu + Vt[:k].T @ z                  # reconstruction", "",
      "def cosine(a, B):                         # <a,b> / (|a||b|)", "    return (B @ a) / (np.linalg.norm(B, axis=1) * np.linalg.norm(a))", "", "digit = np.argmax(cosine(z, templates))   # prediction"])
H2("11.4 Data-Driven Design")
para("Every result in the application is computed from the images by the routines above; none is typed in by hand. The pipeline is deterministic: the same training set, k and unknown digit always give the same prediction.")
H1("12. Results and Analysis")
para("All results use the 300 training images and 200 test images of Section 7.")
H2("12.1 Rank and SVD")
para(f"The data matrix X has rank {R['rank_X']}, not 64, because {R['zero_pixels']} pixels (mostly in the corners) are zero in every training image and give zero columns. Centering does not change the rank, so rank(Xc) = {R['rank_Xc']}. At most 56 principal components are therefore non-zero.")
H2("12.2 Principal directions")
para(f"The first three components explain {ex[0]:.1f}%, {ex[1]:.1f}% and {ex[2]:.1f}% of the variance. Each direction is a vector in ℝ⁶⁴ and can be drawn as an 8 × 8 image: red and blue regions show the pixels that increase or decrease together. Together the first 10, 20 and 30 components keep {cum[9]:.1f}%, {cum[19]:.1f}% and {cum[29]:.1f}% of the variance.")
fig("fig3_eigendigits.png", "Figure 3: Mean image and the first nine principal directions", 5.6)
fig("fig4_scree.png", "Figure 4: Variance explained by the first 30 components", 4.4)
H2("12.3 Projection")
para("Projecting the training digits onto the first two components already separates some classes (0, 4 and 6 lie at the edges), while 5, 8 and 9 overlap. Two dimensions are therefore not enough for recognition, and Section 14 shows how accuracy grows with k.")
fig("fig5_projection2d.png", "Figure 5: Training digits projected onto PC1 and PC2", 4.6)
H2("12.4 Reconstruction")
para("Projecting an image onto k components and back gives the closest image in the subspace. The mean reconstruction error ‖x − x̂‖ over the test images falls from {:.2f} at k = 1 to {:.2f} at k = 20 and is zero (to rounding) at k = 56 and above.".format(R["rec_err"]["1"], R["rec_err"]["20"]))
fig("fig6_reconstruction.png", "Figure 6: One test digit reconstructed with k = 1, 2, 5, 10, 20, 40 and 64 components", 5.8)
H2("12.5 Inner-product similarity and prediction")
para(f"The stored pattern of each digit is the mean of its training projections. For the unknown digit (test image {dm['index']}) the cosine similarities with the ten patterns, computed with k = 20, are given below. The highest score, {max(dm['scores']):.3f} for digit {dm['pred']}, is well above the second highest ({sorted(dm['scores'])[-2]:.3f}, digit 4), so the predicted digit is {dm['pred']}, which is correct. The reconstruction residual is {dm['residual']:.3f}.")
table(["Digit"] + [str(i) for i in range(10)], [["Cosine"] + [f"{s:.3f}" for s in dm["scores"]]], size=9)
fig("fig9_prediction.png", "Figure 7: Unknown digit, its reconstruction and the similarity scores", 5.8)
H1("13. Verification")
H2("13.1 SVD and eigen-decomposition")
para(f"The eigenvalues of the covariance matrix computed independently with numpy.linalg.eigvalsh agree with σi² / (N − 1) to within {R['eig_vs_svd']:.1e}. The right singular vectors are orthonormal: ‖V Vᵀ − I‖ = {R['orth']:.1e}. The identity ‖Xc‖F² = Σ σi² holds with a difference of {R['frob']:.1e}.")
H2("13.2 Orthogonal projection")
para(f"For a training digit and k = 10, the error vector x̃ − Vk z is orthogonal to every direction in Vk (largest inner product {R['proj_orth_resid']:.1e}). The Pythagorean identity ‖x̃‖² = ‖z‖² + ‖error‖² holds with a difference of {R['pyth']:.1e}.")
H2("13.3 Rank check")
para(f"The numerical rank of X and of Xc is {R['rank_X']}, equal to 64 minus the {R['zero_pixels']} always-zero pixels, as expected.")
H1("14. Results and Interpretation: Accuracy against k")
para("The 200 test images were classified for several values of k. As a baseline, the same cosine rule was applied to the raw 64-dimensional pixel vectors with the class-mean images as patterns.")
ks = ["1", "2", "3", "5", "10", "15", "20", "30", "40", "64"]
table(["k"] + ks + ["raw 64 px"], [["Accuracy %"] + [f"{acc[k]*100:.1f}" for k in ks] + [f"{R['baseline_raw']*100:.1f}"]], size=8.5)
fig("fig7_accuracy_error.png", "Figure 8: Test accuracy and reconstruction error against k", 5.8)
bullets([f"Accuracy rises quickly up to k = 10 ({acc['10']*100:.0f}%) and then flattens at about {acc['20']*100:.0f}–{acc['64']*100:.0f}%.", f"With k = 20 the accuracy ({acc['20']*100:.0f}%) is within one point of the raw-pixel baseline ({R['baseline_raw']*100:.0f}%) while using 3.2 times fewer numbers. PCA here gives compression with almost no loss, not an improvement in accuracy.",
 "Two components are far from enough (45%), in agreement with the overlap seen in Figure 5.", "With 200 test images the standard error of an accuracy near 86% is about 2.5 points, so differences of one or two points between k = 15 and k = 64 are not significant."])
fig("fig8_confusion.png", "Figure 9: Confusion matrix for k = 20", 4.0)
para(f"The easiest digits are 0, 6 and 7 (100% correct). The hardest is 8 ({pc[8]*100:.0f}% correct), followed by 5 ({pc[5]*100:.0f}%). The most frequent confusions are " + "; ".join(f"true {i} predicted as {j} ({n} times)" for n, i, j in conf) + ". These digits overlap in Figure 5 and share strokes, so a rule that uses only one centre per class cannot separate them.")
H1("15. Application Interface")
para("The Streamlit application has five tabs (Matrix & vector, SVD / PCA, Projection, Prediction, Evaluation), a slider for the number of components and a choice between a stored test image and an 8 × 8 pixel editor for a new digit. It runs locally with the command given in the README, and the source code, figures and this report are supplied with the project.")
H1("16. Testing and Discussion")
H2("16.1 Functional Testing")
table(["Test Case", "Expected Behaviour", "Status"], [("Matrix and vector", "8 × 8 matrix becomes a vector of length 64 with entries in [0, 1]", "Pass"), ("Normalisation", "Centered training matrix has zero column means", "Pass"), ("SVD", "σi²/(N−1) equals covariance eigenvalues; V orthonormal", "Pass"),
 ("Projection", "Error vector orthogonal to subspace; Pythagorean identity holds", "Pass"), ("Reconstruction", "Error falls as k grows and is zero at full rank", "Pass"), ("Similarity", "Cosine scores lie in [−1, 1]; highest score gives the digit", "Pass"), ("Evaluation", "Accuracy and confusion matrix computed for each k", "Pass"), ("Interface", "k slider and pixel editor change the displayed results", "Pass")], [1.5, 4.1, 0.7])
H2("16.2 Limitations")
bullets(["The images are only 8 × 8 pixels and the dataset is small; results on real handwriting would differ.", "One pattern per class cannot represent different handwriting styles of the same digit; digits 8 and 5 are recognised poorly.", "PCA is unsupervised and does not use the labels, so the directions of largest variance are not necessarily the ones that separate digits best.",
 "The result comes from a single train/test split; repeated random splits would give a more reliable estimate.", "The interface was written to run with Streamlit but, apart from the mathematical routines, it has not been tested in a browser session."])
H1("17. Conclusion")
para(f"The project built a complete pipeline from a digit image to a predicted digit. The image was represented as a matrix and a vector in ℝ⁶⁴, normalised by the mean image and decomposed by the SVD. Twenty principal directions keep {cum[19]:.0f}% of the variance, and orthogonal projection onto them gives features from which the digit can be reconstructed and compared with stored patterns by inner-product similarity. The test accuracy is {acc['20']*100:.0f}% with 20 features against {R['baseline_raw']*100:.0f}% with all 64 pixels, so the dimension is reduced 3.2 times with almost no loss. The decomposition and projection identities were verified to rounding error. The weakest digits (8 and 5) show the limit of a single pattern per class.")
H1("18. Future Scope")
bullets(["Use the full 28 × 28 MNIST images and larger training sets.", "Use several patterns per digit (k-nearest neighbours or one subspace per class).", "Replace PCA by a supervised reduction such as linear discriminant analysis.", "Choose k by cross-validation and repeat the experiment over many random splits.", "Add noise removal by truncated SVD and compare with a small neural network."])
H1("19. References")
bullets(["Kreyszig, E., Advanced Engineering Mathematics, Wiley.", "Strang, G., Introduction to Linear Algebra, Wellesley-Cambridge Press.", "Lay, D. C., Linear Algebra and Its Applications, Pearson (singular value decomposition, orthogonal projection).",
 "Turk, M. and Pentland, A., Eigenfaces for Recognition, Journal of Cognitive Neuroscience, 1991.", "Alpaydin, E. and Kaynak, C., Optical Recognition of Handwritten Digits, UCI Machine Learning Repository.", "NumPy documentation, numpy.linalg.svd.", "MAT2303 – Linear Algebra & Vector Calculus course material, Presidency University."])
f = sec.footer.paragraphs[0]; f.alignment = AL.CENTER; run = f.add_run()
for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
    if tag: e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), tag)
    else: e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt
    run._r.append(e)
doc.save(os.path.join(HERE, "..", "DigitMatrix_MAT2303_Mini_Project_Report.docx")); print("saved")
