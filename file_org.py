import tkinter as tk
from tkinter import filedialog

def open_file():
    file_path = filedialog.askopenfilename(title="Open Text File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, file.read())
        status_label.config(text=f"File opened: {file_path}")

def save_file():
    file_path = current_file.get()
    if file_path:
        try:
            with open(file_path, 'w') as file:
                text_content = text_widget.get("1.0", tk.END)
                file.write(text_content)
            status_label.config(text=f"File saved: {file_path}")
        except Exception as e:
            status_label.config(text=f"Error saving file: {str(e)}")
    else:
        save_as_file()
def save_as_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        current_file.set(file_path)
        save_file()
root = tk.Tk()
root.title("Text Editor")
current_file = tk.StringVar()
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)
text_widget = tk.Text(root, wrap=tk.WORD)
text_widget.pack(padx=20, pady=20, fill="both", expand=True)
status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.pack()
root.mainloop()
