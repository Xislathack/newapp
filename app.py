import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# Function to convert Excel to PDF
def convert_excel_to_pdf(excel_file):
    # Read Excel file
    df = pd.read_excel(excel_file, engine='openpyxl')

    # Create a temporary file for the PDF
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_path = temp_pdf.name

    # Create a PDF file
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, height - 50, "Excel to PDF Conversion")

    # Table header
    c.setFont("Helvetica-Bold", 10)
    y = height - 100
    for col in df.columns:
        c.drawString(50 + (df.columns.get_loc(col) * 100), y, col)

    # Table data
    c.setFont("Helvetica", 10)
    for index, row in df.iterrows():
        y -= 20
        for col in df.columns:
            c.drawString(50 + (df.columns.get_loc(col) * 100), y, str(row[col]))

    c.save()
    return pdf_path

# Streamlit UI
st.title("Excel to PDF Converter")

uploaded_file = st.file_uploader("Upload an Excel File", type=["xlsx", "csv"])

if uploaded_file:
    st.success("File uploaded successfully!")
    
    if st.button("Convert to PDF"):
        pdf_file_path = convert_excel_to_pdf(uploaded_file)
        
        # Provide a download link
        with open(pdf_file_path, "rb") as pdf_file:
            st.download_button("Download PDF", pdf_file, file_name="converted.pdf", mime="application/pdf")
