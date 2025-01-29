Chat-with-PDF-with-Local-LLM
A Python-based chatbot application that allows users to interact with PDF documents using a local language model (LLM). Upload PDFs, extract text, and chat with AI about the content — all offline!

Features
Upload and store PDFs locally.
Extract text from PDFs and split into chunks for AI-based conversation.
Chat with the extracted content using a local LLM.
Fully offline, ensuring privacy and efficiency.
Technologies
Python
Tkinter (for the GUI)
PyPDF2 (for PDF text extraction)
Langchain (for text chunking)
Local LLM (e.g., Ollama)
Installation
Clone the repository:

bash
Kopioi
Muokkaa
git clone https://github.com/your-username/Chat-with-PDF-with-Local-LLM.git
cd Chat-with-PDF-with-Local-LLM
Install dependencies:

bash
Kopioi
Muokkaa
pip install -r requirements.txt
Run the application:

bash
Kopioi
Muokkaa
python main.py
Usage
Launch the app.
Upload a PDF file by clicking the "Upload PDF" button.
After processing, interact with the extracted PDF content through the chat interface.
The app uses a local LLM for generating responses based on the PDF content.
Requirements
Python 3.x
PyPDF2
Langchain
Tkinter
Ollama (or another local LLM)
License
MIT License
