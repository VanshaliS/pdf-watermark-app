import streamlit as st
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

# Create watermark PDF in memory
def create_watermark(watermark_text):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 40)
    can.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.3)

    # Get width and height to center text
    width, height = letter
    text_width = can.stringWidth(watermark_text, "Helvetica", 40)
    x = (width - text_width) / 2
    y = height / 2

    can.drawString(x, y, watermark_text)
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

    # Generate filename: "WatermarkText_YYYYMMDD.pdf"
    today_str = datetime.now().strftime("%Y%m%d")
    safe_name = watermark_text.replace(" ", "_")  # remove spaces
    filename = f"{safe_name}_{today_str}.pdf"

    st.download_button(
        label="📥 Download Watermarked PDF",
        data=watermarked_pdf,
        file_name=filename,
        mime="application/pdf"
    )
