import streamlit as st
import PyPDF2
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

# Create a diagonal repeating watermark
def create_watermark(watermark_text, page_width, page_height):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    can.setFont("Helvetica-Bold", 35)

     # Softer red with moderate transparency
    can.setFillColorRGB(1, 0.3, 0.3, alpha=0.35)

    # Draw watermark diagonally across page
    step_x = 300
    step_y = 200
    for x in range(-100, int(page_width) + 300, step_x):
        for y in range(-100, int(page_height) + 200, step_y):
            can.saveState()
            can.translate(x, y)
            can.rotate(45)
            can.drawString(0, 0, watermark_text)
            can.restoreState()

    can.save()
    packet.seek(0)
    return PyPDF2.PdfReader(packet)


# Apply watermark
def add_watermark(input_pdf, watermark_text, original_filename):
    output = PyPDF2.PdfWriter()
    reader = PyPDF2.PdfReader(input_pdf)

    # Use first page dimensions
    first_page = reader.pages[0]
    width = float(first_page.mediabox.width)
    height = float(first_page.mediabox.height)

    watermark_pdf = create_watermark(watermark_text, width, height)
    watermark_page = watermark_pdf.pages[0]

    for page in reader.pages:
        page.merge_page(watermark_page)
        output.add_page(page)

    result = BytesIO()
    output.write(result)
    result.seek(0)

    # Create new filename
    base_name = os.path.splitext(original_filename)[0]
    safe_watermark = watermark_text.replace(" ", "_")
    new_filename = f"{base_name}__{safe_watermark}.pdf"

    return result, new_filename

# --- Streamlit App ---
st.title("📄 PDF Watermarker")
st.image("fortelogo.png", width=120)  # 👈 Add your company logo here

watermark_text = st.text_input("Enter watermark text")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file and watermark_text:
    with st.spinner("Applying watermark..."):
        result_pdf, new_filename = add_watermark(uploaded_file, watermark_text, uploaded_file.name)
        st.success("✅ Watermark added!")

        st.download_button(
            label="📥 Download Watermarked PDF",
            data=result_pdf,
            file_name=new_filename,
            mime="application/pdf"
        )

        )
