import streamlit as st
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create watermark PDF in memory
def create_watermark(watermark_text):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 40)
    can.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.3)
    can.rotate(45)
    can.drawString(100, 300, watermark_text)
    can.save()
    packet.seek(0)
    return PyPDF2.PdfReader(packet)

# Apply watermark
def add_watermark(input_pdf, watermark_text):
    watermark = create_watermark(watermark_text)
    watermark_page = watermark.pages[0]

    output = PyPDF2.PdfWriter()
    reader = PyPDF2.PdfReader(input_pdf)

    for page in reader.pages:
        page.merge_page(watermark_page)
        output.add_page(page)

    result = BytesIO()
    output.write(result)
    result.seek(0)
    return result

# Streamlit UI
st.title("📄 PDF Watermarker App")

watermark_text = st.text_input("Enter watermark text")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file and watermark_text:
    watermarked_pdf = add_watermark(uploaded_file, watermark_text)
    st.success("✅ Watermark added successfully!")

    st.download_button(
        label="📥 Download Watermarked PDF",
        data=watermarked_pdf,
        file_name="watermarked.pdf",
        mime="application/pdf"
    )

