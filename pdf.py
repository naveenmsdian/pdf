import streamlit as st
from PIL import Image
from fpdf import FPDF
import io
import tempfile

# Set the title of the app
st.title("Image to PDF Converter")

# Create a file uploader for images
uploaded_files = st.file_uploader("Upload Images", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    # Display the uploaded images
    st.subheader("Uploaded Images")
    images = []
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        images.append(img)
        st.image(img, caption=uploaded_file.name, use_column_width=True)
    
    # Convert images to PDF when the button is clicked
    if st.button("Convert to PDF"):
        # Create a PDF object
        pdf = FPDF()
        pdf.set_auto_page_break(0)

        for img in images:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                img.save(temp_file.name, format='PNG')
                # Add image to PDF, ensure it fits the page size
                pdf.add_page()
                
                pdf_width = 210
                pdf_height = 297
                width, height = img.size
                aspect_ratio = width / height

                if aspect_ratio > 1:
                    new_width = pdf_width
                    new_height = pdf_width / aspect_ratio
                else:
                    new_height = pdf_height
                    new_width = pdf_height * aspect_ratio

                # Center the image on the PDF page
                x_offset = (pdf_width - new_width) / 2
                y_offset = (pdf_height - new_height) / 2

                # Add image to PDF from temporary file
                pdf.image(temp_file.name, x=x_offset, y=y_offset, w=new_width, h=new_height)

        # Save the PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            pdf.output(temp_pdf.name, 'F')
            # Read the contents of the temporary PDF file
            with open(temp_pdf.name, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
        
        # Create a download button
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="converted_images.pdf",
            mime="application/pdf"
        )
