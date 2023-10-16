import tkinter as tk
from tkinter import messagebox

def check_position():
    try:
        a = (float(entry_ax.get()), float(entry_ay.get()), 1)
        b = (float(entry_bx.get()), float(entry_by.get()), 1)
        p = (float(entry_px.get()), float(entry_py.get()), 1)
    except ValueError:
        messagebox.showerror('Błąd', 'Współrzędne muszą być liczbami!')
        return
    det = a[0]*b[1] + b[0]*p[1] + p[0]*a[1] - p[0]*b[1] - a[0]*p[1] - b[0]*a[1]
    vec_prod = (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])
    if det == 0:
        label_output.config(text='Punkt P leży na prostej AB')
    elif det > 0:
        label_output.config(text='Punkt P leży po prawej stronie prostej AB')
    elif det < 0:
        label_output.config(text='Punkt P leży po lewej stronie prostej AB')

    diff = vec_prod - det
    label_det.config(text=f'Wyznacznik: {det:.6f}')
    label_vec_prod.config(text=f'Iloczyn wektorowy: {vec_prod:.6f}')
    label_diff.config(text=f'Różnica: {diff:.6f}')

window = tk.Tk()
window.title('Zadanie 1')
window.geometry('700x200')

label_a = tk.Label(window, text='Podaj współrzędne punktu A:')
label_a.grid(row=0, column=0, padx=5, pady=5)

label_ax = tk.Label(window, text='X:')
label_ax.grid(row=0, column=1, padx=5, pady=5)

entry_ax = tk.Entry(window)
entry_ax.grid(row=0, column=2, padx=5, pady=5)

label_ay = tk.Label(window, text='Y:')
label_ay.grid(row=0, column=3, padx=5, pady=5)

entry_ay = tk.Entry(window)
entry_ay.grid(row=0, column=4, padx=5, pady=5)

label_b = tk.Label(window, text='Podaj współrzędne punktu B:')
label_b.grid(row=1, column=0, padx=5, pady=5)

label_bx = tk.Label(window, text='X:')
label_bx.grid(row=1, column=1, padx=5, pady=5)

entry_bx = tk.Entry(window)
entry_bx.grid(row=1, column=2, padx=5, pady=5)

label_by = tk.Label(window, text='Y:')
label_by.grid(row=1, column=3, padx=5, pady=5)

entry_by = tk.Entry(window)
entry_by.grid(row=1, column=4, padx=5, pady=5)

label_p = tk.Label(window, text='Podaj współrzędne punktu P:')
label_p.grid(row=2, column=0, padx=5, pady=5)

label_px = tk.Label(window, text='X:')
label_px.grid(row=2, column=1, padx=5, pady=5)

entry_px = tk.Entry(window)
entry_px.grid(row=2, column=2, padx=5, pady=5)

label_py = tk.Label(window, text='Y:')
label_py.grid(row=2, column=3, padx=5, pady=5)

entry_py = tk.Entry(window)
entry_py.grid(row=2, column=4, padx=5, pady=5)

button_check = tk.Button(window, text='Sprawdź położenie', command=check_position)
button_check.grid(row=3, column=1, columnspan=2)

label_output = tk.Label(window, text='')
label_output.grid(row=4, column=1, columnspan=3)

label_det = tk.Label(window, text='')
label_det.grid(row=0, column=5, columnspan=3)

label_vec_prod = tk.Label(window, text='')
label_vec_prod.grid(row=1, column=5, columnspan=3)

label_diff = tk.Label(window, text='')
label_diff.grid(row=2, column=5, columnspan=3)

window.mainloop()

entry_py = tk.Entry(window)
entry_py.grid(row=2, column=2, padx=5, pady=5)

button_check = tk.Button(window, text='Sprawdź położenie', command=check_position)
button_check.grid(row=3, column=1, columnspan=2)

label_output = tk.Label(window, text='')
label_output.grid(row=4, column=1, columnspan=3)

label_det = tk.Label(window, text='')
label_det.grid(row=0, column=3, columnspan=3)

label_vec_prod = tk.Label(window, text='')
label_vec_prod.grid(row=1, column=3, columnspan=3)

label_diff = tk.Label(window, text='')
label_diff.grid(row=2, column=3, columnspan=3)

window.mainloop()
