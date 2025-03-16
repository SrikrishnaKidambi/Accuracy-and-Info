import argparse
import time
import ollama
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def read_code(file_path):
    """Reads the contents of a code file."""
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        messagebox.showerror(f"Error reading the file {e}")
        return None
    
def analyze_complexity(code):
    """Uses Deepseek-R1:8b that is locally installed using ollama to analyze the code complexity"""
    prompt = f"""Analyse the time complexity and space complexity of the following code and provide only the final consice answer:
    ```{code}```
    Provide a consice answer like:
    - Time Complexity: O(...)
    - Space Complexity: O(...)
    - Explanation: (short explanation,max 2-3 sentences)
    Strictly follow the above format time comeplexity in one line , in the next line space complexity and in the next line start explanation which can be for 2-3 lines, just given some 2-3 line reasoning in the explanation but don't give any reasoning in Time Complexity: or Space Complexity:
    Do NOT include any intermediate reasoning or <think> blocks.
    """
    print("Analysing")
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

def open_file():
    """Open a file dialog to select a code file and analyze it."""
    file_path=filedialog.askopenfilename(
        title="Select a Code file",
        filetypes=[("Python Files","*.py"),("Text files","*.txt"),("All Files","*.*")]
    )
    if file_path:
        code=read_code(file_path)
        if code:
            complexity_info=analyze_complexity(code)
            result_text.delete(1.0,tk.END)
            result_text.insert(tk.END,complexity_info)
root=tk.Tk()
root.title("Code Complexity Analyzer")
root.geometry("600x400")

open_button=tk.Button(root, text="Open Code File",command=open_file)
open_button.pack(pady=20)

result_text=scrolledtext.ScrolledText(root,wrap=tk.WORD,width=70,height=15)
result_text.pack(padx=20,pady=10)

clear_button = tk.Button(root, text="Clear Results", command=clear_results)
clear_button.pack(pady=10)

root.mainloop()