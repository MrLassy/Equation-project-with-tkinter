import tkinter as tk 
from sympy import symbols, Eq, solve, pretty, sympify, SympifyError, Mul
import random

app = tk.Tk()
app.title("Math - Equation")
app.geometry("800x400")

equation = None
# Option gestion
selected_option = tk.StringVar(value="Facile")

# Déclaration des radiobutton
rb1 = tk.Radiobutton(app, text="Facile", variable=selected_option, value="Facile")
rb2 = tk.Radiobutton(app, text="Moyen", variable=selected_option, value="Moyen")
rb3 = tk.Radiobutton(app, text="Difficile", variable=selected_option, value="Difficile")

#Widget 
rb1.pack(anchor="w", padx=20, pady=5)
rb2.pack(anchor="w", padx=20, pady=5)
rb3.pack(anchor="w", padx=20, pady=5)


def genere_equation():
    global equation
    
    
    option = selected_option.get()
    # Equation 
    x = symbols('x')

    if option == "Facile":
        a = random.randint(1, 9)
        b = random.randint(0, 10)
        c = random.randint(-10, 10)
        equation = Eq(a*x + b, c)
    elif option == "Moyen":

        a = random.randint(2, 9)
        b = random.randint(1 , 5)
        d = random.randint(-1, 10)
        c =random.randint(-1, 10)
        equation = Eq(Mul(a ,( x * b + d ), evaluate=False), c)
    else :
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(-10, 10)        
        equation = Eq( a*x**2 + b * x + c, 0)
            
    format = pretty(equation, use_unicode=True)
    label_equation.config(text=format)

    entry.delete(0 , tk.END)
    label_solution.config(text="")
    button2.config(state="normal")


def solve_equation():
    
    solution = list(solve(equation))
    user_solution = entry.get()
    try :   
        if sympify(user_solution) in solution :
            label_solution.config(text="Réponse correct", font=("Arial", 12), fg="green")
            button2.config(state="disabled")
        else :
            label_solution.config(text=f"It is a bad answer\nGood answer: {solution}", font=("Arial", 12), fg="red") 
            button2.config(state="disabled")
    except (SympifyError, SyntaxError, TypeError) :
        if not user_solution.strip():
            label_solution.config(text="Champ vide", font=("Arial", 12), fg="red")     
        else :
            label_solution.config(text="Entrée incorrect", font=("Arial", 12), fg="red")                       




label_equation = tk.Label(app,font=("Consolas", 12))
label_equation.pack(pady=5)

entry = tk.Entry(app, width=25, font=("Arial", 12))
entry.pack(pady=20)


label_solution= tk.Label(app)
label_solution.pack(pady=10)


button1 = tk.Button(app, text="Commencer une nouvelle partie" , command=genere_equation)
button1.pack(pady=0)


button2 = tk.Button(app, text="Confirmer la réponse", command=solve_equation, state="normal")
button2.pack(pady=20)

genere_equation()
app.mainloop()