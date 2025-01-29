import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import ollama
from ttkthemes import ThemedTk
from datetime import datetime
from upload import upload_pdf, refresh_pdf_list  # Import functions from upload.py

class ModernPDFChatApp:
    def __init__(self):
        self.root = ThemedTk(theme="azure")
        self.root.title("PDF Chat")
        self.root.geometry("1000x700")

        # Custom colors
        self.colors = {
            'primary': '#cefdff',
            'secondary': '#cefdff',
            'text': '#333333',
            'bg': '#cefdff',
            'sidebar': '#cefdff'
        }

        # Styles
        self.style = ttk.Style()
        self.configure_styles()

        # Vault directory
        self.vault_dir = "pdf_vault"
        os.makedirs(self.vault_dir, exist_ok=True)

        # Initialize
        self.text_chunks = []
        self.current_file = None
        self.loading_indicator = None
        self.setup_layout()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        self.style.configure("Primary.TButton", padding=10, background=self.colors['primary'], foreground='white')
        self.style.configure("Secondary.TButton", padding=8, background=self.colors['secondary'])
        self.style.configure("Chat.TFrame", background=self.colors['bg'])
        self.style.configure("Sidebar.TFrame", background=self.colors['sidebar'])

    def setup_layout(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="10")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Left sidebar
        sidebar = ttk.Frame(main_container, style="Sidebar.TFrame", width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)

        # App title
        title_frame = ttk.Frame(sidebar, style="Sidebar.TFrame")
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(
            title_frame,
            text="PDF Chat",
            font=("Segoe UI", 16, "bold"),
            background=self.colors['sidebar']
        )
        title_label.pack(side=tk.LEFT, padx=10)

        # Upload button
        upload_btn = ttk.Button(sidebar, text="Upload PDF", style="Secondary.TButton", command=self.upload_pdf)
        upload_btn.pack(pady=(0, 10), padx=10, fill=tk.X)

        # PDF list with custom styling
        list_frame = ttk.Frame(sidebar, style="Sidebar.TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        # Add a label above the list
        list_label = ttk.Label(list_frame, text="Your PDFs", font=("Segoe UI", 11, "bold"), background=self.colors['sidebar'])
        list_label.pack(anchor=tk.W, pady=(0, 5))

        # Custom styled listbox
        self.pdf_listbox = tk.Listbox(list_frame, background=self.colors['bg'], foreground=self.colors['text'], 
                                      selectbackground=self.colors['primary'], selectforeground='white', 
                                      font=("Segoe UI", 10), borderwidth=0, highlightthickness=1, 
                                      highlightcolor=self.colors['primary'])
        self.pdf_listbox.pack(fill=tk.BOTH, expand=True)
        self.pdf_listbox.bind('<<ListboxSelect>>', self.load_selected_pdf)

        # Right chat area
        chat_frame = ttk.Frame(main_container, style="Chat.TFrame")
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Chat display with custom styling
        self.chat_display = tk.Text(chat_frame, wrap=tk.WORD, font=("Segoe UI", 10), background=self.colors['bg'], 
                                    foreground=self.colors['text'], padx=10, pady=10, borderwidth=0, 
                                    highlightthickness=1, highlightcolor=self.colors['primary'])
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Modern scrollbar for chat
        chat_scrollbar = ttk.Scrollbar(self.chat_display, orient="vertical", command=self.chat_display.yview)
        chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_display.configure(yscrollcommand=chat_scrollbar.set)

        # Input area with modern styling
        input_frame = ttk.Frame(chat_frame, style="Chat.TFrame")
        input_frame.pack(fill=tk.X)

        self.user_input = ttk.Entry(input_frame, font=("Segoe UI", 14), style="Chat.TEntry")
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.user_input.bind('<Return>', self.send_message)

        send_btn = ttk.Button(input_frame, text="Send", style="Secondary.TButton", command=self.send_message)
        send_btn.pack(side=tk.RIGHT)

        # Initialize PDF list
        self.refresh_pdf_list()

    def refresh_pdf_list(self):
        """Refresh the list of PDFs in the vault"""
        pdfs = refresh_pdf_list(self.vault_dir)
        self.pdf_listbox.delete(0, tk.END)
        for pdf in pdfs:
            self.pdf_listbox.insert(tk.END, pdf)

    def show_loading_indicator(self):
        """Show a modern loading indicator"""
        if self.loading_indicator is None:
            self.loading_indicator = ttk.Label(self.chat_display, text="Processing...", font=("Segoe UI", 10, "italic"), 
                                               foreground=self.colors['primary'], background=self.colors['text'])
            self.loading_indicator.place(relx=0.5, rely=0.95, anchor="center")

    def hide_loading_indicator(self):
        """Hide the loading indicator"""
        if self.loading_indicator:
            self.loading_indicator.place_forget()
            self.loading_indicator = None

    def upload_pdf(self):
        """Upload a new PDF and process it"""
        file_path = filedialog.askopenfilename(title="Select PDF", filetypes=[("PDF files", "*.pdf")])
        
        if not file_path:
            return
        
        try:
            # Show loading indicator
            self.show_loading_indicator()

            # Upload and process PDF
            text_chunks = upload_pdf(file_path, self.vault_dir)

            # Refresh PDF list
            self.refresh_pdf_list()

            # Hide loading indicator
            self.hide_loading_indicator()

            messagebox.showinfo("Success", f"PDF uploaded with {len(text_chunks)} chunks")

        except Exception as e:
            self.hide_loading_indicator()
            messagebox.showerror("Error", str(e))

    def load_selected_pdf(self, event):
        """Load context from selected PDF"""
        try:
            selection = self.pdf_listbox.curselection()
            if not selection:
                return
            
            filename = self.pdf_listbox.get(selection[0])
            filepath = os.path.join(self.vault_dir, filename)
            
            with open(filepath, 'r') as f:
                self.text_chunks = json.load(f)
            
            self.current_file = filename
            self.display_message("System", f"Loaded {filename} with {len(self.text_chunks)} chunks")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def send_message(self, event=None):
        """Send message and get AI response"""
        user_msg = self.user_input.get()
        if not user_msg or not self.text_chunks:
            return
        
        # Display user message
        self.display_message("You", user_msg)
        self.user_input.delete(0, tk.END)
        
        # Show loading indicator
        self.show_loading_indicator()

        # Start the AI call in a separate thread
        threading.Thread(target=self.get_ai_response, args=(user_msg,), daemon=True).start()

    def get_ai_response(self, user_msg):
        """Get AI response using ollama and update the chat"""
        # Prepare context
        context = " ".join(self.text_chunks[:5])
        
        try:
            response = ollama.chat(
                model='llama3.1:8b',
                messages=[{
                    'role': 'system', 
                    'content': f'Context from PDF: {context}'
                },{
                    'role': 'user', 
                    'content': user_msg
                }]
            )
            
            # Update chat display
            self.root.after(0, self.hide_loading_indicator)
            self.root.after(0, self.display_message, "Assistant", response['message']['content'])
        
        except Exception as e:
            self.root.after(0, self.hide_loading_indicator)
            self.root.after(0, self.display_message, "Error", str(e))

    def display_message(self, sender, message):
        """Display messages with improved formatting"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.tag_configure("sender", font=("Segoe UI", 10, "bold"))
        self.chat_display.tag_configure("timestamp", font=("Segoe UI", 8), foreground="gray")
        self.chat_display.tag_configure("message", font=("Segoe UI", 10))
        
        self.chat_display.insert(tk.END, f"{sender} ", "sender")
        self.chat_display.insert(tk.END, f"{timestamp}\n", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n", "message")
        self.chat_display.see(tk.END)

    def run(self):
        self.root.mainloop()

def main():
    app = ModernPDFChatApp()
    app.run()

if __name__ == "__main__":
    main()
