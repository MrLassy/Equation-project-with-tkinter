import customtkinter as ctk
from tkinter import TclError
from sympy import symbols, Eq, solve, pretty, sympify, SympifyError, Mul
import os
import random


class JeuEquation():

    def __init__(self):
        self.app = ctk.CTk()
        self.equation = None
        self.temps = 31
        self.timer_id = None

        # Déclaration des widgets 
        self.label_equation = ctk.CTkLabel(self.app, font=ctk.CTkFont(family="Consolas", size=15))
        self.label_solution = ctk.CTkLabel(self.app)
        self.timer_label = ctk.CTkLabel(self.app, font=ctk.CTkFont(family="Arial", size=15))
        self.button_generate = ctk.CTkButton(self.app, text="Nouvelle partie", command=self.genere_equation, font=ctk.CTkFont(family="Arial", size=15))
        self.button_reponse = ctk.CTkButton(self.app, text="Confirmer la réponse", command=self.solve_equation, font=ctk.CTkFont(family="Arial", size=15))
        self.selected_option = ctk.StringVar(value="Facile")
        self.selected_timer = ctk.BooleanVar(value=False)
        self.entry = ctk.CTkEntry(self.app, width=190, font=ctk.CTkFont(family="Arial", size=15), placeholder_text="Entrez votre réponse...")


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
            d = random.randint(-10, 10)
            self.equation = Eq( Mul((a*x + b),(c*x + d), evaluate=False), 0)
            self.temps = 91

        format = pretty(self.equation, use_unicode=True)

        self.label_equation.configure(text=format)

        self.entry.delete(0 , ctk.END)
        self.label_solution.configure(text="")
        self.button_reponse.configure(state="normal")

        timer_option = self.selected_timer.get()
        if self.timer_id:
            self.app.after_cancel(self.timer_id)
        if timer_option :
            self.timer()
        

    def solve_equation(self):
        solution = list(solve(self.equation))
        user_solutions = self.entry.get()
        solutions_list = [us.strip() for us in user_solutions.split(",")]

        try :
        
            if sympify(solutions_list) == solution :
                self.label_solution.configure(text="Réponse correct", font=ctk.CTkFont(family="Arial", size=15), text_color="green")

            else :
                self.label_solution.configure(text=f"It is a bad answer\nGood answer: {solution}", font=ctk.CTkFont(family="Arial", size=15) ,text_color="red")

            self.button_reponse.configure(state="disabled")
        except (SympifyError, SyntaxError, TypeError) :

            if not user_solutions.strip():
                self.label_solution.configure(text="Champ vide", font=ctk.CTkFont(family="Arial", size=15), text_color="red")
            else :
                self.label_solution.configure(text="Entrée incorrect", font=ctk.CTkFont(family="Arial", size=15), text_color="red") 


    def timer(self):
        if not self.timer_label.winfo_exists() :
            return

        option = self.selected_timer.get()
        if option :
            try :
                if self.temps > 0 :
                    self.temps -= 1
                    self.timer_label.configure(text=f"Temps restant: {self.temps} s", text_color="white")
                    self.timer_id = self.timer_label.after(1000, self.timer)
                else :

                    self.timer_label.configure(text="Temps écoulé !!", text_color="red")
                    self.button_reponse.configure(state="disabled") 
            except TclError :
                pass   
        else :
            self.timer_label.configure(text="")         


    def on_closing(self):
    
        if self.timer_id:
            self.app.after_cancel(self.timer_id)
        self.app.quit()    
        self.app.destroy()

    def start(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.app.geometry("560x475")
        self.app.title("Math - Equation")

        # Widget des button-radio 
        rb1 = ctk.CTkRadioButton(self.app, text="Facile", variable=self.selected_option, value="Facile")
        rb2 = ctk.CTkRadioButton(self.app, text="Moyen", variable=self.selected_option, value="Moyen")
        rb3 = ctk.CTkRadioButton(self.app, text="Difficile", variable=self.selected_option, value="Difficile")
        check_timer = ctk.CTkCheckBox(self.app, text="Timer", variable=self.selected_timer)

        # Mis en page des Widgets 
        rb1.pack(anchor="w", padx=20, pady=5)
        rb2.pack(anchor="w", padx=20, pady=5)        
        rb3.pack(anchor="w", padx=20, pady=5)
        check_timer.pack(anchor="n")

        self.label_equation.pack(pady=15)
        self.entry.pack(pady=10)
        self.label_solution.pack(pady=10)
        self.button_generate.pack(pady=5)
        self.button_reponse.pack(pady=5)

        self.timer_label.pack(anchor="w", pady=15)

        self.genere_equation()
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app.mainloop()


app = JeuEquation()
app.start()
os.system("clear")
print("Fin du programme !!!")