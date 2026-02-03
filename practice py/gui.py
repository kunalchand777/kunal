# tkinter_factorial.py
import tkinter as tk
from tkinter import messagebox

def compute_factorial():
    try:
        n = int(entry.get())
        if n < 0:
            raise ValueError("negative")
    except Exception:
        messagebox.showerror("Error", "Please enter a non-negative integer.")
        return

    # compute factorial iteratively to avoid recursion limit
    result = 1
    for i in range(2, n+1):
        result *= i
    result_label.config(text=f"{n}! = {result}")

root = tk.Tk()
root.title("Factorial Calculator")

tk.Label(root, text="Enter n:").grid(row=0, column=0, padx=8, pady=8)
entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=8, pady=8)

compute_btn = tk.Button(root, text="Compute", command=compute_factorial)
compute_btn.grid(row=1, column=0, columnspan=2, pady=8)

result_label = tk.Label(root, text="Result will appear here")
result_label.grid(row=2, column=0, columnspan=2, pady=8)

root.mainloop()