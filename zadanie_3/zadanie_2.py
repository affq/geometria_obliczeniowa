# Zadanie polega na napisaniu programu, który będzie wyznaczał punkt przecięcia dwóch
# odcinków, z których każdy jest dany przez współrzędne dwóch punktów. Ilustrację zadania
# przedstawia rys. 4.
# Rysunek 4. Ilustracja zadania przecięcia dwóch prostych określonych dwoma punktami
# 2.1 METODA ROZWIĄZANIA ZADANIA
# Z punktu widzenia wzorów rozwiązujących, to zadanie jest szczególnym przypadkiem
# ogólnego zadania polegającego na wyznaczeniu punktu przecięcia dwóch prostych. Do rozwiązania
# zadania wykorzystujemy równanie parametryczne prostej, w którym każdy punkt na prostej daje
# się wyrazić w funkcji punktu początkowego, końcowego i pewnego parametru rzeczywistego 𝑡.
# Parametryczne równanie prostej przechodzącej przez punkty A i B ma postać:
# 𝑋 = 𝑋𝐴 + 𝑡 ∗ 𝛥𝑋𝐴𝐵,
# 𝑌 = 𝑌𝐴 + 𝑡 ∗ 𝛥𝑌𝐴𝐵,
# gdzie 𝑡 ∈ (−∞, ∞). Przy czym na uwagę zasługuje fakt, że w punkcie A parametr 𝑡 = 0 natomiast
# w punkcie B parametr 𝑡 = 1. Rozwiązanie zadania możemy przedstawić następującymi wzorami:
# 𝑋𝑃 = 𝑋𝐴 + 𝑡1𝛥𝑋𝐴𝐵,
# 𝑌𝑃 = 𝑌𝐴 + 𝑡1𝛥𝑌𝐴𝐵
#  lub 𝑋𝑃 = 𝑋𝐶 + 𝑡2𝛥𝑋𝐶𝐷,
# 𝑌𝑃 = 𝑌𝐶 + 𝑡2𝛥𝑌𝐶𝐷,
# gdzie:
# 𝑡1 =
# 𝛥𝑋𝐴𝐶𝛥𝑌𝐶𝐷−𝛥𝑌𝐴𝐶𝛥𝑋𝐶𝐷
# 𝛥𝑋𝐴𝐵𝛥𝑌𝐶𝐷−𝛥𝑌𝐴𝐵𝛥𝑋𝐶𝐷
# , 𝑡2 =
# 𝛥𝑋𝐴𝐶𝛥𝑌𝐴𝐵−𝛥𝑌𝐴𝐶𝛥𝑋𝐴𝐵
# 𝛥𝑋𝐴𝐵𝛥𝑌𝐶𝐷−𝛥𝑌𝐴𝐵𝛥𝑋𝐶𝐷
# .
# O ile jednak w ogólnym zadaniu wyznaczenia współrzędnych punktu przecięcia prostych
# wystarczające jest obliczenie parametrów parametry 𝑡1 i 𝑡2 a następnie współrzędnych punktu
# przecięcia, to w zadaniu wyznaczenia współrzędnych punkty przecięcia odcinków należy
# dodatkowo sprawdzić czy wyznaczony punkt przecięcia należy do obu odcinków (co jest konieczne
# do uznania go za rozwiązanie).
# Rysunek 5. Różne położenie punktu przecięcia dwóch prostych w stosunku do odcinków
# 6
# W celu sprawdzenia przynależności do odcinków możemy wykorzystać parametry 𝑡1 i 𝑡2, na
# podstawie których, można stwierdzić czy punkt przecięcia będzie należał do obu przecinanych
# odcinków. Ma to miejsce, jeżeli: (0 ≤ 𝑡1 ≤ 1) i (0 ≤ 𝑡2 ≤ 1).

# 2.2 ĆWICZENIE 2 – WYMAGANIA DO PROGRAMU
# 1. Program może być napisany w dowolnym środowisku programistycznym.
# 2. Program powinien mieć możliwość wprowadzania danych z klawiatury jak i odczytu danych
# z pliku tekstowego, a także mieć możliwość zapisania wyników do pliku tekstowego.
# 3. Program powinien realizować prezentację graficzną analizowanych punktów i odcinków wraz
# z punktem ich przecięcia:
# a. pierwsza prezentacja powinna być dopasowana do widoczności wszystkich punktów,
# b. punkty na rysunku powinny być opisana swoimi oznaczeniami (A,B,C,D,P),
# c. powinna istnieć możliwość konfigurowania parametrów rysunku, tzn.: kolory, grubości
# i style linii, widoczność ukrycie oznaczeń punktów.
# 4. Czas na wykonanie ćwiczenia: 4 zajęcia. Program powinien być oddany na koniec szóstych
# zajęć, w przypadku nieoddania wystawiana jest ocena negatywna.

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import math
import os

# import figurecanvastkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.colorchooser import askcolor

# stworzenie okna
root = tk.Tk()
root.title("Zadanie 2")
root.geometry("800x600")
root.resizable(False, False)
root.configure(background="black")

# stworzenie ramki
frame = tk.Frame(root)
frame.pack()

# stworzenie ramki do wykresu
frame_plot = tk.Frame(root)
frame_plot.pack(side=RIGHT)

# stworzenie ramki do przycisków
frame_buttons = tk.Frame(root)
frame_buttons.pack(side=LEFT)

# stworzenie ramki do wprowadzania danych
frame_input = tk.Frame(root)
frame_input.pack(side=LEFT)

# stworzenie ramki do wyświetlania danych
frame_output = tk.Frame(root)
frame_output.pack(side=LEFT)

# stworzenie ramki do wykresu
frame_plot = tk.Frame(root)
frame_plot.pack(side=RIGHT)

# ramka na przyciski do zmiany koloru, grubosci i stylu linii oraz ukrycia oznaczen punktow
frame_buttons_plot = tk.Frame(root)
frame_buttons_plot.pack(side=RIGHT)



# stworzenie miejsc na wspolrzedne oraz podpisy
label_xa = Label(frame_input, text="xa", bg="black", fg="white")
label_xa.grid(row=0, column=0)
label_ya = Label(frame_input, text="ya", bg="black", fg="white")
label_ya.grid(row=1, column=0)
label_xb = Label(frame_input, text="xb", bg="black", fg="white")
label_xb.grid(row=2, column=0)
label_yb = Label(frame_input, text="yb", bg="black", fg="white")
label_yb.grid(row=3, column=0)
label_xc = Label(frame_input, text="xc", bg="black", fg="white")
label_xc.grid(row=4, column=0)
label_yc = Label(frame_input, text="yc", bg="black", fg="white")
label_yc.grid(row=5, column=0)
label_xd = Label(frame_input, text="xd", bg="black", fg="white")
label_xd.grid(row=6, column=0)
label_yd = Label(frame_input, text="yd", bg="black", fg="white")
label_yd.grid(row=7, column=0)

# stworzenie miejsc na wprowadzanie danych
entry_xa = Entry(frame_input, width=10)
entry_xa.grid(row=0, column=1)
entry_ya = Entry(frame_input, width=10)
entry_ya.grid(row=1, column=1)
entry_xb = Entry(frame_input, width=10)
entry_xb.grid(row=2, column=1)
entry_yb = Entry(frame_input, width=10)
entry_yb.grid(row=3, column=1)
entry_xc = Entry(frame_input, width=10)
entry_xc.grid(row=4, column=1)
entry_yc = Entry(frame_input, width=10)
entry_yc.grid(row=5, column=1)
entry_xd = Entry(frame_input, width=10)
entry_xd.grid(row=6, column=1)
entry_yd = Entry(frame_input, width=10)
entry_yd.grid(row=7, column=1)

# stworzenie miejsc na wyświetlanie danych
entry_xp = Entry(frame_output, width=10,)
entry_xp.grid(row=9, column=1)
entry_yp = Entry(frame_output, width=10,)
entry_yp.grid(row=10, column=1)

# stworzenie przyciskow zmiany koloru, grubosci, stylu linii oraz ukrycia oznaczen punktow

def change_color(x):
    color = askcolor()
    return color

#PRZYCISK ZMIANY KOLORU, po którym wyświetla się paleta wyboru koloru z askcolor
color_button_1 = Button(frame_buttons_plot, text="Zmień kolor linii AB", bg="black", fg="white", command= change_color(1))
color_button_1.grid(row=0, column=0)

color_button_2 = Button(frame_buttons_plot, text="Zmień kolor linii CD", bg="black", fg="white", command= change_color(2))
color_button_2.grid(row=1, column=0)


# dodaj wykres do ramki
fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

# tworzenie wykresu po wcisnieciu przycisku oblicz
def plot(color_1, color_2):
    try:
        xa = float(entry_xa.get())
        ya = float(entry_ya.get())
        xb = float(entry_xb.get())
        yb = float(entry_yb.get())
        xc = float(entry_xc.get())
        yc = float(entry_yc.get())
        xd = float(entry_xd.get())
        yd = float(entry_yd.get())
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadzono niepoprawne dane")
        return

    try:
        t1 = ((xc - xa) * (yd - yc) - (yc - ya) * (xd - xc)) / ((xb - xa) * (yd - yc) - (yb - ya) * (xd - xc))
        t2 = ((xc - xa) * (yb - ya) - (yc - ya) * (xb - xa)) / ((xb - xa) * (yd - yc) - (yb - ya) * (xd - xc))
    except ZeroDivisionError:
        entry_xp.delete(0, END)
        entry_yp.delete(0, END)
        messagebox.showerror("Błąd", "Nie można dzielić przez zero")
        return

    if 0 <= t1 <= 1 and 0 <= t2 <= 1:
        xp = xa + t1 * (xb - xa)
        yp = ya + t1 * (yb - ya)
        entry_xp.delete(0, END)
        entry_yp.delete(0, END)
        entry_xp.insert(0, xp)
        entry_yp.insert(0, yp)
    else:
        entry_xp.delete(0, END)
        entry_yp.delete(0, END)
        messagebox.showerror("Błąd", "Odcinki nie przecinają się")
        return

    # tworzenie wykresu - podpisz każdy punkt

    ax.clear()

    plt.plot(xa, ya, 'ro')
    plt.annotate('A', (xa, ya))
    plt.plot(xb, yb, 'ro')
    plt.annotate('B', (xb, yb))
    plt.plot(xc, yc, 'ro')
    plt.annotate('C', (xc, yc))
    plt.plot(xd, yd, 'ro')
    plt.annotate('D', (xd, yd))
    plt.plot(xp, yp, 'ro')
    plt.annotate('P', (xp, yp))

    # tworzenie wykresu - podpisz każdy odcinek
    plt.plot([xa, xb], [ya, yb], label='AB', color=color_1)
    plt.plot([xc, xd], [yc, yd], label='CD', color=color_2)
    
    plt.legend()

    # tworzenie wykresu - podpisz punkt przecięcia
    plt.plot(xp, yp, 'ro')
    plt.annotate('P', (xp, yp))

    canvas.draw()

# przycisk oblicz
button_calculate = Button(frame_buttons, text="Oblicz", bg="black", fg="white", command = plot)
button_calculate.grid(row=0, column=0)

root.mainloop()