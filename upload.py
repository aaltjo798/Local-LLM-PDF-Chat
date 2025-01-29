import os
import json
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tkinter import messagebox

def upload_pdf(file_path, vault_dir):
    """Upload a new PDF, process it, and save the chunks"""
    try:
        # Extract text from PDF
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_text(text)
        
        # Save chunks as JSON
        filename = os.path.basename(file_path).replace('.pdf', '.json')
        filepath = os.path.join(vault_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(text_chunks, f)

        return text_chunks

    except Exception as e:
        raise Exception(f"Error uploading PDF: {str(e)}")

def refresh_pdf_list(vault_dir):
    """Refresh the list of PDFs in the vault directory"""
    pdfs = [f for f in os.listdir(vault_dir) if f.endswith('.json')]
    return pdfs
