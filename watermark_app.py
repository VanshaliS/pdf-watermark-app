import streamlit as st
import os
import tempfile
import subprocess
import pypandoc
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Convert to PDF if needed
def convert_to_pdf(file):
    suffix = os.path.splitext(file.name)[-1].lower()
    input_temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    input_temp.write(file.read())
    input_temp.close()

    if suffix == ".pdf":
        return input_temp.name
    else:
        # Convert using pandoc
        output_path = input_temp.name.replace(suffix, ".pdf")
        try:
            pypandoc.convert_file(input_temp.name, 'pdf', outputfile=output_path)
            return output_path
        except Exception as e:
            st.error(f"Failed to convert {file.name} to PDF: {e}")
            return None

# Create watermark
def create_watermark(text):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=A4)
    c.setFont("Helvetica", 40)
    c.setFillAlpha(0.3)
    c.drawCentredString(300, 500, text)
    c.save()
    return temp_file.name

# Apply watermark
def apply_watermark(pdf_path, watermark_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    watermark = PdfReader(watermark_path).pages[0]

    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)

    output_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    with open(output_pdf.name, "wb") as f_out:
        writer.write(f_out)

    return output_pdf.name

# Streamlit UI
st.set_page_config(page_title="📄 Any File to Watermarked PDF", layout="centered")
st.title("💧 Watermark Any File")

watermark_text = st.text_input("Enter the watermark text")
uploaded_files = st.file_uploader("Upload files (PDF, Word, Excel, etc.)", accept_multiple_files=True)

if watermark_text and uploaded_files:
    if st.button("Convert & Add Watermark"):
        watermark_pdf = create_watermark(watermark_text)
        for file in uploaded_files:
            pdf_path = convert_to_pdf(file)
            if pdf_path:
                output = apply_watermark(pdf_path, watermark_pdf)
                with open(output, "rb") as f:
                    st.download_button(
                        label=f"Download Watermarked: {file.name}.pdf",
                        data=f,
                        file_name=f"WM_{file.name}.pdf",
                        mime="application/pdf"
                    )
        os.remove(watermark_pdf)
