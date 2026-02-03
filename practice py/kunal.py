"""
All-in-one Tkinter app (single-file)
Features:
- Login & Registration (sqlite3)
- Main Menu (OOP frames)
- Calculator (basic)
- Guess Number (simple)
- Advanced Guess Number (difficulty, score, restart)
- Factorial (iterative + recursive)
- Quiz Game (MCQ)
Author: Generated for Kunal
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import random
import math
from functools import partial

DB_PATH = "app_users.db"


# ---------------------- Database helpers ----------------------
def init_db():
    """Create users table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def register_user(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True, "Registered Successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        return False, f"DB Error: {e}"


def verify_user(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        row = cur.fetchone()
        conn.close()
        return bool(row)
    except Exception:
        return False


# ---------------------- App & Frames (OOP) ----------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        init_db()
        self.title("Python Multi-Tool")
        self.geometry("480x560")
        self.resizable(False, False)
        self.current_user = None

        # container for frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.frames = {}

        # create frames
        for F in (LoginFrame, RegisterFrame, MainMenuFrame,
                  CalculatorFrame, GuessGameFrame, AdvancedGuessFrame,
                  FactorialFrame, QuizFrame):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def logout(self):
        self.current_user = None
        self.show_frame("LoginFrame")


# ---------------------- Authentication Frames ----------------------
class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login", font=("Helvetica", 20)).pack(pady=20)
        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()
        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Login", command=self.try_login).pack(pady=10)
        tk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterFrame")).pack()
        tk.Button(self, text="Continue as Guest", command=self.guest_continue).pack(pady=6)

    def try_login(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Input required", "Enter username and password")
            return
        if verify_user(user, pwd):
            self.controller.current_user = user
            messagebox.showinfo("Welcome", f"Hello, {user}!")
            self.controller.show_frame("MainMenuFrame")
        else:
            messagebox.showerror("Login failed", "Incorrect username or password")

    def guest_continue(self):
        self.controller.current_user = "Guest"
        self.controller.show_frame("MainMenuFrame")


class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Register", font=("Helvetica", 20)).pack(pady=20)
        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()
        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(self, text="Register", command=self.do_register).pack(pady=10)
        tk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginFrame")).pack()

    def do_register(self):
        user = self.username.get().strip()
        pwd = self.password.get().strip()
        if not user or not pwd:
            messagebox.showwarning("Input required", "Enter username and password")
            return
        ok, msg = register_user(user, pwd)
        if ok:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame("LoginFrame")
        else:
            messagebox.showerror("Error", msg)


# ---------------------- Main Menu ----------------------
class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Main Menu", font=("Helvetica", 20)).pack(pady=16)
        self.welcome_label = tk.Label(self, text="Welcome!", font=("Helvetica", 12))
        self.welcome_label.pack(pady=6)

        btns = [
            ("Calculator", "CalculatorFrame"),
            ("Guess Number (Simple)", "GuessGameFrame"),
            ("Guess Number (Advanced)", "AdvancedGuessFrame"),
            ("Factorial", "FactorialFrame"),
            ("Quiz Game", "QuizFrame"),
        ]
        for (text, frame_name) in btns:
            tk.Button(self, text=text, width=25, command=lambda n=frame_name: controller.show_frame(n)).pack(pady=6)

        tk.Button(self, text="Logout", fg="red", command=self.logout).pack(side="bottom", pady=12)

    def tkraise(self, *args, **kwargs):
        # update welcome label before show
        user = self.controller.current_user or "Guest"
        self.welcome_label.config(text=f"Signed in as: {user}")
        super().tkraise(*args, **kwargs)

    def logout(self):
        self.controller.logout()


# ---------------------- Calculator ----------------------
class CalculatorFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Calculator", font=("Helvetica", 18)).pack(pady=8)
        self.expr = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.expr, font=("Arial", 20), justify="right")
        entry.pack(fill="x", padx=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('0', '.', 'C', '+'),
        ]
        for r, row in enumerate(buttons):
            for c, val in enumerate(row):
                action = partial(self.on_press, val)
                tk.Button(btn_frame, text=val, width=6, height=2, command=action).grid(row=r, column=c, padx=3, pady=3)

        tk.Button(self, text="=", width=28, command=self.calculate).pack(pady=6)
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenuFrame")).pack()

    def on_press(self, val):
        if val == 'C':
            self.expr.set('')
            return
        current = self.expr.get()
        self.expr.set(current + val)

    def calculate(self):
        expression = self.expr.get()
        try:
            # safe eval: only allow math operators & numbers
            # __builtins__ removed; math functions are not allowed here
            result = eval(expression, {"__builtins__": None}, {})
            self.expr.set(str(result))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {e}")


# ---------------------- Simple Guess Game ----------------------
class GuessGameFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Guess Number (1-100)", font=("Helvetica", 18)).pack(pady=8)
        self.target = random.randint(1, 100)
        self.attempts = 0

        tk.Label(self, text="Enter guess:").pack()
        self.guess_entry = tk.Entry(self)
        self.guess_entry.pack()
        tk.Button(self, text="Guess", command=self.check_guess).pack(pady=6)
        self.result_label = tk.Label(self, text="")
        self.result_label.pack(pady=6)
        tk.Button(self, text="New Number", command=self.reset).pack()
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(pady=6)

    def check_guess(self):
        val = self.guess_entry.get().strip()
        try:
            guess = int(val)
            self.attempts += 1
            if guess < self.target:
                self.result_label.config(text="Too low!")
            elif guess > self.target:
                self.result_label.config(text="Too high!")
            else:
                self.result_label.config(text=f"Correct! Attempts: {self.attempts}")
        except ValueError:
            messagebox.showwarning("Invalid", "Enter a valid integer")

    def reset(self):
        self.target = random.randint(1, 100)
        self.attempts = 0
        self.result_label.config(text="")
        self.guess_entry.delete(0, tk.END)


# ---------------------- Advanced Guess Game ----------------------
class AdvancedGuessFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Advanced Guess Game", font=("Helvetica", 18)).pack(pady=8)

        # difficulty controls
        tk.Label(self, text="Choose difficulty:").pack()
        self.difficulty = tk.StringVar(value="Easy")
        tk.OptionMenu(self, self.difficulty, "Easy", "Medium", "Hard").pack()

        tk.Button(self, text="Start Game", command=self.start_game).pack(pady=6)

        self.info_label = tk.Label(self, text="Not started")
        self.info_label.pack()
        tk.Label(self, text="Your Guess:").pack()
        self.guess_entry = tk.Entry(self)
        self.guess_entry.pack()
        tk.Button(self, text="Submit Guess", command=self.submit).pack(pady=6)

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(side="bottom", pady=8)

        # game state
        self.reset_state()

    def reset_state(self):
        self.min_val = 1
        self.max_val = 100
        self.target = None
        self.attempts = 0
        self.score = 0
        self.max_attempts = None

    def start_game(self):
        d = self.difficulty.get()
        if d == "Easy":
            self.max_attempts = 10
            self.min_val, self.max_val = 1, 50
        elif d == "Medium":
            self.max_attempts = 7
            self.min_val, self.max_val = 1, 100
        else:  # Hard
            self.max_attempts = 5
            self.min_val, self.max_val = 1, 200

        self.target = random.randint(self.min_val, self.max_val)
        self.attempts = 0
        self.score = 0
        self.info_label.config(text=f"Guess a number between {self.min_val} and {self.max_val}. Attempts allowed: {self.max_attempts}")
        self.status_label.config(text="")
        self.guess_entry.delete(0, tk.END)

    def submit(self):
        if self.target is None:
            messagebox.showinfo("Start", "Please start the game first")
            return
        try:
            g = int(self.guess_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Invalid", "Please enter an integer")
            return

        self.attempts += 1
        remaining = self.max_attempts - self.attempts
        if g == self.target:
            self.score = max(0, self.max_attempts - self.attempts + 1) * 10
            self.status_label.config(text=f"Correct! Score: {self.score}")
            # auto-start new round
            if messagebox.askyesno("Play again?", "Start a new round?"):
                self.start_game()
            else:
                self.target = None
        elif self.attempts >= self.max_attempts:
            self.status_label.config(text=f"Out of attempts! The number was {self.target}")
            self.target = None
        elif g < self.target:
            self.status_label.config(text=f"Too low! Attempts left: {remaining}")
        else:
            self.status_label.config(text=f"Too high! Attempts left: {remaining}")


# ---------------------- Factorial Frame ----------------------
class FactorialFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Factorial Calculator", font=("Helvetica", 18)).pack(pady=8)
        tk.Label(self, text="Enter non-negative integer:").pack()
        self.n_entry = tk.Entry(self)
        self.n_entry.pack()
        tk.Button(self, text="Calculate Iterative", command=self.calc_iter).pack(pady=6)
        tk.Button(self, text="Calculate Recursive", command=self.calc_rec).pack(pady=6)
        self.out_label = tk.Label(self, text="")
        self.out_label.pack(pady=8)
        tk.Button(self, text="Back to Menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(side="bottom", pady=8)

    def calc_iter(self):
        n = self._get_n()
        if n is None:
            return
        try:
            res = 1
            for i in range(1, n + 1):
                res *= i
            self.out_label.config(text=f"Factorial (iterative): {res}")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {e}")

    def calc_rec(self):
        n = self._get_n()
        if n is None:
            return
        try:
            res = self._fact_rec(n)
            self.out_label.config(text=f"Factorial (recursive): {res}")
        except RecursionError:
            messagebox.showerror("Error", "Recursion limit reached for this input")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {e}")

    def _get_n(self):
        try:
            n = int(self.n_entry.get().strip())
            if n < 0:
                messagebox.showwarning("Invalid", "Enter a non-negative integer")
                return None
            return n
        except ValueError:
            messagebox.showwarning("Invalid", "Enter a valid integer")
            return None

    def _fact_rec(self, n):
        if n == 0 or n == 1:
            return 1
        return n * self._fact_rec(n - 1)


# ---------------------- Quiz Game ----------------------
class QuizFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Quiz Game (MCQ)", font=("Helvetica", 18)).pack(pady=8)

        # sample questions (list of dicts)
        self.questions = [
            {"q": "Which language is this app written in?", "choices": ["Java", "Python", "C++", "Kotlin"], "answer": "Python"},
            {"q": "2 + 3 * 4 = ?", "choices": ["20", "14", "24", "10"], "answer": "14"},
            {"q": "Factorial of 5 is", "choices": ["120", "60", "24", "720"], "answer": "120"},
            {"q": "Tkinter is used for?", "choices": ["Web", "GUI", "Database", "Network"], "answer": "GUI"},
        ]
        self.q_index = 0
        self.score = 0

        self.question_label = tk.Label(self, text="", wraplength=420, justify="left")
        self.question_label.pack(pady=10)
        self.choice_vars = []
        self.radio_var = tk.StringVar()
        for i in range(4):
            rb = tk.Radiobutton(self, text="", variable=self.radio_var, value="", anchor="w")
            rb.pack(fill="x", padx=16, pady=2)
            self.choice_vars.append(rb)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Start Quiz", command=self.start_quiz).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Submit Answer", command=self.submit_answer).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Back to Menu", command=lambda: controller.show_frame("MainMenuFrame")).pack(pady=8)

    def start_quiz(self):
        random.shuffle(self.questions)
        self.q_index = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        if self.q_index >= len(self.questions):
            messagebox.showinfo("Quiz Completed", f"Your Score: {self.score}/{len(self.questions)}")
            return
        q = self.questions[self.q_index]
        self.question_label.config(text=f"Q{self.q_index+1}: {q['q']}")
        self.radio_var.set(None)
        choices = q["choices"][:]
        random.shuffle(choices)
        for rb, choice in zip(self.choice_vars, choices):
            rb.config(text=choice, value=choice)

    def submit_answer(self):
        if self.q_index >= len(self.questions):
            messagebox.showinfo("Quiz", "Quiz finished. Press Start Quiz to play again.")
            return
        sel = self.radio_var.get()
        if not sel:
            messagebox.showwarning("Select", "Choose an answer first")
            return
        correct = self.questions[self.q_index]["answer"]
        if sel == correct:
            self.score += 1
        self.q_index += 1
        self.show_question()


# ---------------------- Run ----------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
