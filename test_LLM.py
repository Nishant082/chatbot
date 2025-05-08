import tkinter as tk
from tkinter import scrolledtext
import tkinter.filedialog as filedialog
import os
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import os
from gen_ai import GENAi

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("MINI chatbot")
        self.window.geometry("800x600")
        self.gen = GENAi()
        self.full_image_path=None
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        input_frame = tk.Frame(self.window)
        input_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        prompt_label = tk.Label(input_frame, text="Enter your prompt:")
        prompt_label.pack(anchor="w")
        
        self.input_text = tk.Text(input_frame, height=4, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True)

        self.gen_btn = tk.Button(input_frame, text="Generate", command=self.generate_response, padx=10, pady=5)
        self.gen_btn.pack(pady=10)
        self.input_text.bind("<Control-Return>", lambda event: self.generate_response())
        
        response_label = tk.Label(self.window, text="Response:")
        response_label.pack(anchor="w", padx=10)
        
        self.output_text = scrolledtext.ScrolledText(self.window, height=20, wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        pdf_frame = tk.Frame(self.window)
        pdf_frame.pack(fill=tk.X, expand=False, padx=10, pady=5)
        
        self.pdf_path_var = tk.StringVar()
        self.pdf_path_var.set("No PDF selected")

        pdf_select_btn = tk.Button(pdf_frame, text="Select PDF", command=self.select_pdf)
        pdf_select_btn.pack(side=tk.LEFT, padx=(0, 10))

        pdf_path_label = tk.Label(pdf_frame, textvariable=self.pdf_path_var)
        pdf_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.pdf_button = tk.Button(pdf_frame, text="Summarize PDF", command=self.summarize_selected_pdf,padx=10, pady=5)
        self.pdf_button.pack(side=tk.RIGHT, padx=(10, 0))

        image_selection_frame = tk.Frame(self.window)
        image_selection_frame.pack(fill=tk.X, expand=False, padx=10, pady=5)

        self.image_path_var = tk.StringVar()
        self.image_path_var.set("No image selected")

        image_select_btn = tk.Button(image_selection_frame, text="Select Image", command=self.select_image)
        image_select_btn.pack(side=tk.LEFT, padx=(0, 10))

        image_path_label = tk.Label(image_selection_frame, textvariable=self.image_path_var)
        image_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        image_gen_btn = tk.Button(image_selection_frame, text="Generate with Image", 
                                command=self.generate_with_image,
                                padx=10, pady=5)
        image_gen_btn.pack(side=tk.RIGHT, padx=(10, 0))

        self.image_frame = tk.Frame(self.window)
        self.image_preview = tk.Label(self.image_frame)
        self.image_preview.pack(pady=5)


    def generate_response(self):
        prompt = self.input_text.get("1.0", tk.END).strip()
        if prompt:
            self.gen_btn.config(text="Generating...", state=tk.DISABLED)
            self.window.update()
            self.gen.gen(prompt, self.output_text)
            self.gen_btn.config(text="Generate", state=tk.NORMAL)
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Please enter a prompt first.")

    def select_pdf(self):
        pdf_path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if pdf_path:
            self.pdf_path_var.set(os.path.basename(pdf_path))
            self.full_pdf_path = pdf_path

    def summarize_selected_pdf(self):
        if hasattr(self, 'full_pdf_path') and self.full_pdf_path:
            self.pdf_button.config(text="Summarizing...", state=tk.DISABLED)
            self.window.update()
            self.gen.summarize_pdf(self.full_pdf_path, self.output_text)
            self.pdf_button.config(text="Summarize PDF", state=tk.NORMAL)
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Please select a PDF file first.")

    def select_image(self):
        image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        if image_path:
            self.image_path_var.set(os.path.basename(image_path))
            self.full_image_path = image_path
            self.display_selected_image(image_path)

    def display_selected_image(self, image_path):
        try:
            img = Image.open(image_path)
            img = self.resize_image(img, 200)  
            photo = ImageTk.PhotoImage(img)
            self.image_preview.config(image=photo)
            self.image_preview.image = photo  
            self.image_frame.pack(fill=tk.X, expand=False, padx=10, pady=5)
        except Exception as e:
            print(f"Error displaying image: {e}")

    def resize_image(self, img, max_size):
        width, height = img.size
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        return img.resize((new_width, new_height), Image.LANCZOS)

    def generate_with_image(self):
        if hasattr(self, 'full_image_path') and self.full_image_path:
            prompt = self.input_text.get("1.0", tk.END).strip()
            if prompt:
                self.gen_btn.config(text="Generating...", state=tk.DISABLED)
                self.window.update()
                self.gen.gen_with_image(prompt, self.full_image_path, self.output_text)
                self.gen_btn.config(text="Generate", state=tk.NORMAL)
            else:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, "Please enter a prompt first.")
        else:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Please select an image first.")

if __name__ == "__main__":
    gui = GUI()