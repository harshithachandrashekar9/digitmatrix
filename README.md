# DigitMatrix – handwritten digits with SVD / PCA
```
backend/        data.py · digits_pipeline.py (math) · validate.py · make_figures.py · make_report.py
streamlit_app/  app.py (+ copies of data.py, digits_pipeline.py) · requirements.txt
figures/        fig1..fig9 PNG, results.json
DigitMatrix_MAT2303_Mini_Project_Report.docx
```
Run the web app: `cd streamlit_app && pip install -r requirements.txt && streamlit run app.py`
Regenerate numbers/figures/report: `cd backend && python validate.py && python make_figures.py && python make_report.py`
