import argparse
import time
import ollama
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from fpdf import FPDF

def read_code(file_path):
    """Reads the contents of a code file."""
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        messagebox.showerror(f"Error reading the file {e}")
        return None
    
def genrate_documentation(code):
    """Uses Deepseek-R1:8b that is locally installed using ollama to analyze the code complexity"""
    prompt = f"""Genrate the documentation for the following code:
    ```{code}```
    Provide a clear and consise documentation including:
    - A brief description of what the code does.
    - To explain a function / code just say what are the inputs , outputs and briefly what it do in plain english
    - Any important notes or assumptions.
    - Dependencies between functions.
    - Dependencies with other files.
    Do NOT include any intermediate reasoning or <think> blocks.
    """
    print("Generating Documentation")
    start_time=time.time()
    response=ollama.generate(
        model="deepseek-coder:6.7b",
        prompt=prompt
    )
    print("Done")
    print(f"Time taken : {time.time()-start_time:.2f} seconds")
    # print(response)  # Debugging
    if hasattr(response, "response"):
        return response.response.strip()
    else:
        return "No complexity analysis found in the response."
    
def clear_results():
    """Clear the results text area."""
    result_text.delete(1.0, tk.END)

def save_to_pdf():
    """Save the generated documentation to a pdf file."""
    content=result_text.get(1.0,tk.END).strip()
    if not content:
        messagebox.showwarning("Warning","No documentation to save!")
        return
    file_path=filedialog.asksaveasfilename(
        defaultextension="pdf",
        filetypes=[("PDF Files","*.pdf")],
        title="Save PDF As"
    )
    if file_path:
        try:
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, content)
            pdf.output(file_path)
            messagebox.showinfo("Success", "Documentation saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {e}")
def open_file():
    """Open a file dialog to select a code file and analyze it."""
    file_path=filedialog.askopenfilename(
        title="Select a Code file",
        filetypes=[("Python Files","*.py"),("Text files","*.txt"),("All Files","*.*")]
    )
    if file_path:
        code=read_code(file_path)
        if code:
            complexity_info=genrate_documentation(code)
            result_text.delete(1.0,tk.END)
            result_text.insert(tk.END,complexity_info)
root=tk.Tk()
root.title("Code Documentation Generator")
root.geometry("800x600")

open_button=tk.Button(root, text="Open Code File",command=open_file)
open_button.pack(pady=20)

result_text=scrolledtext.ScrolledText(root,wrap=tk.WORD,width=100,height=24)
result_text.pack(padx=20,pady=10)

clear_button = tk.Button(root, text="Clear Results", command=clear_results)
clear_button.pack(pady=10)

download_button = tk.Button(root, text="Download PDF", command=save_to_pdf)
download_button.pack(pady=5)

root.mainloop()