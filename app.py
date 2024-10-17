import streamlit as st  
import pypandoc  
from PyPDF2 import PdfMerger  
import os  
import tempfile  
  
def convert_word_to_pdf(input_file, output_file):  
    try:  
        # Convert DOCX to PDF using pypandoc  
        pypandoc.convert_file(input_file, 'pdf', outputfile=output_file)  
        return output_file  
    except Exception as e:  
        st.error(f"Error converting file: {e}")  
        return None  
  
def merge_pdfs(pdf_list, output_file):  
    merger = PdfMerger()  
    for pdf in pdf_list:  
        merger.append(pdf)  
    merger.write(output_file)  
    merger.close()  
    return output_file  
  
def main():  
    st.title("Word to PDF Converter and Merger")  
  
    word_file = st.file_uploader("Upload a Word document", type=["docx"])  
    pdf_file = st.file_uploader("Upload a PDF to merge with", type=["pdf"])  
  
    if word_file and pdf_file:  
        with tempfile.TemporaryDirectory() as tmpdirname:  
            word_path = os.path.join(tmpdirname, word_file.name)  
            pdf_path = os.path.join(tmpdirname, pdf_file.name)  
  
            # Save uploaded files to temporary directory  
            with open(word_path, "wb") as f:  
                f.write(word_file.getbuffer())  
            with open(pdf_path, "wb") as f:  
                f.write(pdf_file.getbuffer())  
  
            output_pdf_file = os.path.join(tmpdirname, "merged_document.pdf")  
              
            # Convert the uploaded Word file to PDF  
            with st.spinner("Converting Word to PDF..."):  
                converted_pdf = convert_word_to_pdf(word_path, os.path.join(tmpdirname, "converted.pdf"))  
              
            if converted_pdf:  
                # Merge the converted PDF with the uploaded PDF  
                with st.spinner("Merging PDFs..."):  
                    merged_pdf = merge_pdfs([converted_pdf, pdf_path], output_pdf_file)  
                  
                st.success("PDFs have been successfully merged!")  
                with open(output_pdf_file, "rb") as f:  
                    st.download_button(  
                        label="Download
