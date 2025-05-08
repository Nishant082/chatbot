import google.generativeai as genai
import tkinter as tk
from pypdf import PdfReader
from key import *


class GENAi:
    def __init__(self):
        self.api = genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

    def gen(self, prompt, output_widget):
        try:
            response = self.model.generate_content(prompt)
            output_widget.config(state=tk.NORMAL) 
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, response.text)
            output_widget.config(state=tk.DISABLED) 
        except Exception as e:
            output_widget.config(state=tk.NORMAL)
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, f"Error: {str(e)}")
            output_widget.config(state=tk.DISABLED)

    def extract_pdf_text(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

    def summarize_pdf(self, pdf_path, output_widget):
        try:
            pdf_text = self.extract_pdf_text(pdf_path)
            prompt = f"Please summarize the following document concisely:\n\n{pdf_text[:25000]}"
            response = self.model.generate_content(prompt)
            output_widget.config(state=tk.NORMAL) 
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, response.text)
            output_widget.config(state=tk.DISABLED) 

        except Exception as e:
            output_widget.config(state=tk.NORMAL)
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, f"Error: {str(e)}")
            output_widget.config(state=tk.DISABLED) 
        

    def gen_with_image(self, prompt, image_path, output_widget):
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            response = self.model.generate_content([
                prompt,  
                {"mime_type": "image/jpeg", "data": image_bytes}  
            ])

            output_widget.config(state=tk.NORMAL) 
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, response.text)
            output_widget.config(state=tk.DISABLED) 

        except Exception as e:
            output_widget.config(state=tk.NORMAL)
            output_widget.delete(1.0, tk.END)
            output_widget.insert(tk.END, f"Error: {str(e)}")
            output_widget.config(state=tk.DISABLED) 