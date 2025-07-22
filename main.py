import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
from tkcalendar import DateEntry

# -------------- Pomodoro Class (Non-blocking UI) --------------
class Pomodoro:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x200")
        self.minutes = tk.IntVar(value=25)
        self.seconds = tk.IntVar(value=0)
        self.timer_running = False

        ttk.Label(root, text="Pomodoro Timer", font=("Helvetica", 16)).pack(pady=10)
        self.timer_display = ttk.Label(root, text="", font=("Helvetica", 24))
        self.timer_display.pack()

        ttk.Button(root, text="Start Work", command=self.start_work).pack(pady=5)
        ttk.Button(root, text="Take Break", command=self.start_break).pack()

        self.update_display()

    def update_display(self):
        self.timer_display.config(
            text=f"{self.minutes.get():02}:{self.seconds.get():02}"
        )

    def countdown(self):
        if self.timer_running:
            min_val = self.minutes.get()
            sec_val = self.seconds.get()

            if min_val == 0 and sec_val == 0:
                self.timer_running = False
                messagebox.showinfo("Done", "Time's up!")
                return

            if sec_val == 0:
                self.minutes.set(min_val - 1)
                self.seconds.set(59)
            else:
                self.seconds.set(sec_val - 1)

            self.update_display()
            self.root.after(1000, self.countdown)

    def start_work(self):
        self.minutes.set(25)
        self.seconds.set(0)
        self.timer_running = True
        self.countdown()

    def start_break(self):
        self.minutes.set(5)
        self.seconds.set(0)
        self.timer_running = True
        self.countdown()

# -------------- Main Task App (Launcher) --------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("400x300")
        ttk.Label(root, text="Welcome!", font=("Helvetica", 18)).pack(pady=20)

        ttk.Button(root, text="Pomodoro Timer", command=self.open_pomodoro).pack(pady=5)
        ttk.Button(root, text="Todo List", command=self.open_todo).pack(pady=5)
        ttk.Button(root, text="Note-Taking", command=self.open_note).pack(pady=5)

    def open_pomodoro(self):
        pomodoro_window = tk.Toplevel(self.root)
        Pomodoro(pomodoro_window)

    def open_todo(self):
        def add_task():
            task = entry.get().strip()
            date = cal.get_date()
            if task:
                tasks_listbox.insert(tk.END, f"{date}: {task}")
                entry.delete(0, tk.END)

        def delete_task():
            selected = tasks_listbox.curselection()
            if selected:
                tasks_listbox.delete(selected)

        win = tk.Toplevel(self.root)
        win.title("Todo List")
        win.geometry("400x400")

        cal = DateEntry(win)
        cal.pack(pady=5)

        entry = ttk.Entry(win, width=30)
        entry.pack(pady=5)

        ttk.Button(win, text="Add Task", command=add_task).pack()
        ttk.Button(win, text="Delete Task", command=delete_task).pack(pady=5)

        tasks_listbox = tk.Listbox(win, height=10)
        tasks_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

    def open_note(self):
        def open_file():
            file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file:
                with open(file, "r") as f:
                    text.delete("1.0", tk.END)
                    text.insert(tk.END, f.read())

        def save_file():
            file = filedialog.asksaveasfilename(defaultextension=".txt")
            if file:
                with open(file, "w") as f:
                    f.write(text.get("1.0", tk.END))

        win = tk.Toplevel(self.root)
        win.title("Notes")
        win.geometry("400x400")

        text = tk.Text(win, wrap=tk.WORD)
        text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        frame = ttk.Frame(win)
        frame.pack()

        ttk.Button(frame, text="Open", command=open_file).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Save", command=save_file).grid(row=0, column=1, padx=5)

# -------------- Authentication Window --------------
class SimpleAuthentication:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x350")
        self.users = {"admin": "admin123"}

        ttk.Label(root, text="Login", font=("Helvetica", 18)).pack(pady=10)

        self.username = ttk.Entry(root)
        self.password = ttk.Entry(root, show="*")

        ttk.Label(root, text="Username").pack(pady=5)
        self.username.pack()

        ttk.Label(root, text="Password").pack(pady=5)
        self.password.pack()

        ttk.Button(root, text="Login", command=self.login).pack(pady=10)

        ttk.Separator(root).pack(pady=10, fill=tk.X)

        ttk.Label(root, text="New? Sign Up below").pack()
        self.new_username = ttk.Entry(root)
        self.new_password = ttk.Entry(root, show="*")

        ttk.Label(root, text="New Username").pack(pady=5)
        self.new_username.pack()

        ttk.Label(root, text="New Password").pack(pady=5)
        self.new_password.pack()

        ttk.Button(root, text="Sign Up", command=self.signup).pack(pady=10)

    def login(self):
        u, p = self.username.get(), self.password.get()
        if self.users.get(u) == p:
            messagebox.showinfo("Login", "Login Successful!")
            self.root.destroy()
            main = tk.Tk()
            App(main)
            main.mainloop()
        else:
            messagebox.showerror("Error", "Invalid credentials.")

    def signup(self):
        u, p = self.new_username.get(), self.new_password.get()
        if u in self.users:
            messagebox.showerror("Error", "User already exists!")
        elif u and p:
            self.users[u] = p
            messagebox.showinfo("Success", "Account created!")
        else:
            messagebox.showwarning("Warning", "Enter valid username & password.")


if __name__ == "__main__":
    root = tk.Tk()
    ttk.Style().theme_use('clam')  # Use modern style
    SimpleAuthentication(root)
    root.mainloop()
