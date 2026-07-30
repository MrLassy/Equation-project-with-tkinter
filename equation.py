import tkinter as tk 
from tkinter import TclError
from sympy import symbols, Eq, solve, pretty, sympify, SympifyError, Mul
import random


class JeuEquation():

    def __init__(self):
        self.app = tk.Tk()
        self.equation = None
        self.temps = 31
        self.timer_id = None

        # Déclaration des widgets 
        self.label_equation = tk.Label(self.app, font=("Consolas", 12))
        self.label_solution = tk.Label(self.app)
        self.timer_label = tk.Label(self.app, font=("Arial", 12))
        self.buttton_generate = tk.Button(self.app, text="Nouvelle partie", command=self.genere_equation, font=("Arial", 12))
        self.buttton_reponse = tk.Button(self.app, text="Confirmer la réponse", command=self.solve_equation, font=("Arial", 12))
        self.selected_option = tk.StringVar(value="Facile")
        self.entry = tk.Entry(self.app, width=25, font=("Arial", 12))


    def genere_equation(self) :
        option = self.selected_option.get()        
        x = symbols('x')

        if option == "Facile":
            a = random.randint(1, 9)
            b = random.randint(0, 10)
            c = random.randint(-10, 10)
            self.equation = Eq(a*x + b, c)
            self.temps = 31

        elif option == "Moyen":

            a = random.randint(2, 9)
            b = random.randint(1 , 5)
            d = random.randint(-1, 10)
            c =random.randint(-1, 10)
            self.equation = Eq(Mul(a ,( x * b + d ), evaluate=False), c)
            self.temps = 61

        else :
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            c = random.randint(-10, 10)
            self.equation = Eq( a*x**2 + b * x + c, 0)
            self.temps = 91

        format = pretty(self.equation, use_unicode=True)

        self.label_equation.config(text=format)

        self.entry.delete(0 , tk.END)
        self.label_solution.config(text="")
        self.buttton_reponse.config(state="normal")

        if self.timer_id:
            self.app.after_cancel(self.timer_id)
        self.timer()


    def solve_equation(self):
        solution = list(solve(self.equation))
        user_solution = self.entry.get()

        try :

            if sympify(user_solution) in solution :
                self.label_solution.config(text="Réponse correct", font=("Arial", 12), fg="green")

            else :
                self.label_solution.config(text=f"It is a bad answer\nGood answer: {solution}", font=("Arial", 12), fg="red")

            self.buttton_reponse.config(state="disabled")
        except (SympifyError, SyntaxError, TypeError) :

            if not user_solution.strip():
                self.label_solution.config(text="Champ vide", font=("Arial", 12), fg="red")
            else :
                self.label_solution.config(text="Entrée incorrect", font=("Arial", 12), fg="red") 


    def timer(self):
        if not self.timer_label.winfo_exists() :
            return

        try :
            if self.temps > 0 :
                self.temps -= 1
                self.timer_label.config(text=f"Temps restant: {self.temps} s", fg="black")
                self.timer_id = self.timer_label.after(1000, self.timer)
            else :

                self.timer_label.config(text="Temps écoulé !!", fg="red")
                self.buttton_reponse.config(state="disabled") 
        except TclError :
            pass        

    def on_closing(self):
    
        if self.timer_id:
            self.app.after_cancel(self.timer_id)
        self.app.quit()    
        self.app.destroy()

    def start(self):
        self.app.geometry("800x400")
        self.app.title("Math - Equation")

        # Widget des button-radio 
        rb1 = tk.Radiobutton(self.app, text="Facile", variable=self.selected_option, value="Facile")
        rb2 = tk.Radiobutton(self.app, text="Moyen", variable=self.selected_option, value="Moyen")
        rb3 = tk.Radiobutton(self.app, text="Difficile", variable=self.selected_option, value="Difficile")

        # Mis en page des Widgets 
        rb1.pack(anchor="w", padx=20, pady=5)
        rb2.pack(anchor="w", padx=20, pady=5)        
        rb3.pack(anchor="w", padx=20, pady=5)

        self.label_equation.pack(pady=15)
        self.entry.pack(pady=10)
        self.label_solution.pack(pady=15)
        self.buttton_generate.pack(pady=5)
        self.buttton_reponse.pack(pady=5)

        self.timer_label.pack(anchor="w", pady=15)

        self.genere_equation()
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()


app = JeuEquation()
app.start()