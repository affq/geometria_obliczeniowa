import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_data():
    '''
    Get data from entries and return them as floats.
    '''
    try:
        Ax = float(entry_Ax.get())
        Ay = float(entry_Ay.get())
        Bx = float(entry_Bx.get())
        By = float(entry_By.get())
        Cx = float(entry_Cx.get())
        Cy = float(entry_Cy.get())
        Dx = float(entry_Dx.get())
        Dy = float(entry_Dy.get())
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne dane.")
        return

    return Ax, Ay, Bx, By, Cx, Cy, Dx, Dy

def calculate():
    '''
    Calculate the intersection point of two lines and return its coordinates or None if there is no intersection point.
    '''
    try:
        Ax, Ay, Bx, By, Cx, Cy, Dx, Dy = get_data()
    except TypeError:
        return None, None

    try:
        t1 = ((Cx - Ax) * (Dy - Cy) - (Cy - Ay) * (Dx - Cx)) / ((Bx - Ax) * (Dy - Cy) - (By - Ay) * (Dx - Cx))
        t2 = ((Cx - Ax) * (By - Ay) - (Cy - Ay) * (Bx - Ax)) / ((Bx - Ax) * (Dy - Cy) - (By - Ay) * (Dx - Cx))
    except ZeroDivisionError:
        messagebox.showerror("Błąd", "Brak punktu przecięcia")
        return None, None
    
    # sprawdź czy punkt przecięcia należy do obu odcinków
    if 0 <= t1 <= 1:
        if 0 <= t2 <= 1:
            # oblicz współrzędne punktu przecięcia
            Px = Ax + t1 * (Bx - Ax)
            Py = Ay + t1 * (By - Ay)

            # wyświetl współrzędne punktu przecięcia w inputach
            entry_Px.configure(state="normal")
            entry_Px.delete(0, tk.END)
            entry_Px.insert(0, Px)
            entry_Px.configure(state="readonly")
            entry_Py.configure(state="normal")
            entry_Py.delete(0, tk.END)
            entry_Py.insert(0, Py)
            entry_Py.configure(state="readonly")
        else:
            # punkt przecięcia nie należy do odcinka CD
            Px, Py = None, None
            entry_Px.configure(state="normal")
            entry_Px.delete(0, tk.END)
            entry_Px.insert(0, "Brak punktu przecięcia")
            entry_Px.configure(state="readonly")
            entry_Py.configure(state="normal")
            entry_Py.delete(0, tk.END)
            entry_Py.insert(0, "Brak punktu przecięcia")
            entry_Py.configure(state="readonly")
    else:
        # punkt przecięcia nie należy do odcinka AB
        Px, Py = None, None
        entry_Px.configure(state="normal")
        entry_Px.delete(0, tk.END)
        entry_Px.insert(0, "Brak punktu przecięcia")
        entry_Px.configure(state="readonly")
        entry_Py.configure(state="normal")
        entry_Py.delete(0, tk.END)
        entry_Py.insert(0, "Brak punktu przecięcia")
        entry_Py.configure(state="readonly")
    
    if Px is None or Py is None:
        messagebox.showerror("Błąd", "Brak punktu przecięcia")
        return None, None

    return Px, Py

def load():
    '''
    Load data from a file and put them into entries.
    '''
    file = filedialog.askopenfile(mode="r", filetypes=[("Pliki tekstowe", "*.txt")])
    if file is not None:
        try:
            data = np.loadtxt(file, delimiter=",")
            entry_Ax.delete(0, tk.END)
            entry_Ax.insert(0, data[0])
            entry_Ay.delete(0, tk.END)
            entry_Ay.insert(0, data[1])
            entry_Bx.delete(0, tk.END)
            entry_Bx.insert(0, data[2])
            entry_By.delete(0, tk.END)
            entry_By.insert(0, data[3])
            entry_Cx.delete(0, tk.END)
            entry_Cx.insert(0, data[4])
            entry_Cy.delete(0, tk.END)
            entry_Cy.insert(0, data[5])
            entry_Dx.delete(0, tk.END)
            entry_Dx.insert(0, data[6])
            entry_Dy.delete(0, tk.END)
            entry_Dy.insert(0, data[7])

        except (ValueError, IndexError, TypeError):
            messagebox.showerror("Błąd", "Niepoprawne dane")
            return

def draw():
    '''
    Draw the plot.
    '''
    try:
        Px, Py = calculate()
    except TypeError:
        return

    if Px is None or Py is None:
        return
    
    Ax, Ay, Bx, By, Cx, Cy, Dx, Dy = get_data()
        
    ax.clear()

    ax.plot([Ax, Bx], [Ay, By], color="black", linewidth=1)
    ax.plot([Cx, Dx], [Cy, Dy], color="black", linewidth=1)

    ax.plot(Ax, Ay, marker="o", color="black")
    ax.plot(Bx, By, marker="o", color="black")
    ax.plot(Cx, Cy, marker="o", color="black")
    ax.plot(Dx, Dy, marker="o", color="black")
    ax.plot(Px, Py, marker="o", color="red")

    ax.text(Ax, Ay, "A", fontsize=10)
    ax.text(Bx, By, "B", fontsize=10)
    ax.text(Cx, Cy, "C", fontsize=10)
    ax.text(Dx, Dy, "D", fontsize=10)
    ax.text(Px, Py, "P", fontsize=10)

    canvas.draw()

def save():
    '''
    Save the intersection point to a text file.
    '''
    Px, Py = calculate()
    if Px is None or Py is None:
        return
    
    file = filedialog.asksaveasfile(mode="w", filetypes=[("Pliki tekstowe", "*.txt")])
    if file is not None:
        file.write(str(Px) + ", " + str(Py))
        file.close()
    else:
        messagebox.showerror("Błąd", "Niepoprawny plik")
        return
    
def change_color_line(line_index):
    try:
        color = askcolor()
        ax.lines[line_index].set_color(color[1])
        canvas.draw()
    except IndexError:
        if color[0] is None:
            return
        messagebox.showerror("Błąd", f"Linia {line_index+1} nie istnieje.")
        return
    
def change_width_line1(event):
    '''
    Change the width of the first line.
    '''
    try:
        width = combo_line1.get()
        ax.lines[0].set_linewidth(width)
        canvas.draw()
    except IndexError:
        messagebox.showerror("Błąd", "Linia 1 nie istnieje.")
        combo_line1.set("Wybierz grubość linii 1")
        return
    finally:
        combo_line1.selection_clear()
        root.focus()

def change_width_line2(event):
    '''
    Change the width of the second line.
    '''
    try:
        width = combo_line2.get()
        ax.lines[1].set_linewidth(width)
        canvas.draw()
    except IndexError:
        messagebox.showerror("Błąd", "Linia 2 nie istnieje.")
        combo_line2.set("Wybierz grubość linii 2")
        return
    finally:
        combo_line2.selection_clear()
        root.focus()

def change_style_line1(event):
    '''
    Change the style of the first line.
    '''
    try:
        style = combo_line1_style.get()
        ax.lines[0].set_linestyle(style)
        canvas.draw()
    except IndexError:
        messagebox.showerror("Błąd", "Linia 1 nie istnieje.")
        combo_line1_style.set("Wybierz styl linii 1")
        return
    finally:
        combo_line1_style.selection_clear()
        root.focus()

def change_style_line2(event):
    '''
    Change the style of the second line.
    '''
    try:
        style = combo_line2_style.get()
        ax.lines[1].set_linestyle(style)
        canvas.draw()
    except IndexError:
        messagebox.showerror("Błąd", "Linia 2 nie istnieje.")
        combo_line2_style.set("Wybierz styl linii 2")
        return
    finally:
        combo_line2_style.selection_clear()
        root.focus()

def hide_points():
    '''
    Hide or show points A, B, C, D and P and their labels.
    '''
    try:
        if var.get() == 1:
            for i in range(5):
                ax.texts[i].set_visible(False)
            for x in range(2, 7):
                ax.lines[x].set_marker("")
        else:
            for i in range(5):
                ax.texts[i].set_visible(True)
            for x in range(2, 7):
                ax.lines[x].set_marker("o")
        canvas.draw()
    except IndexError:
        if var.get() == 1:
            var.set(0)
        messagebox.showerror("Błąd", "Brak punktów do ukrycia.")
        return

def clear():
    '''
    Clear the plot.
    '''
    ax.clear()
    canvas.draw()

def save_plot():
    """
    Saves the plot as a PNG file.
    """
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Pliki PNG", "*.png")])
    if filename:
        fig.savefig(filename)
    else:
        messagebox.showerror("Błąd", "Niepoprawny plik.")

root = tk.Tk()
root.title("Zadanie 2")
root.geometry("1030x600")
root.resizable(False, False)

fig = plt.figure(figsize=(6, 4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=5, rowspan=7, columnspan=5, padx=5, pady=5)

# punkt A
label_A = tk.Label(root, text="Punkt A")
label_A.grid(row=0, column=0, padx=5, pady=5)
label_Ax = tk.Label(root, text="x:")
label_Ax.grid(row=0, column=1, padx=5, pady=5)
entry_Ax = tk.Entry(root)
entry_Ax.grid(row=0, column=2, padx=5, pady=5)
label_Ay = tk.Label(root, text="y:")
label_Ay.grid(row=0, column=3, padx=5, pady=5)
entry_Ay = tk.Entry(root)
entry_Ay.grid(row=0, column=4, padx=5, pady=5)

# punkt B
label_B = tk.Label(root, text="Punkt B")
label_B.grid(row=1, column=0, padx=5, pady=5)
label_Bx = tk.Label(root, text="x:")
label_Bx.grid(row=1, column=1, padx=5, pady=5)
entry_Bx = tk.Entry(root)
entry_Bx.grid(row=1, column=2, padx=5, pady=5)
label_By = tk.Label(root, text="y:")
label_By.grid(row=1, column=3, padx=5, pady=5)
entry_By = tk.Entry(root)
entry_By.grid(row=1, column=4, padx=5, pady=5)

# punkt C
label_C = tk.Label(root, text="Punkt C")
label_C.grid(row=2, column=0, padx=5, pady=5)
label_Cx = tk.Label(root, text="x:")
label_Cx.grid(row=2, column=1, padx=5, pady=5)
entry_Cx = tk.Entry(root)
entry_Cx.grid(row=2, column=2, padx=5, pady=5)
label_Cy = tk.Label(root, text="y:")
label_Cy.grid(row=2, column=3, padx=5, pady=5)
entry_Cy = tk.Entry(root)
entry_Cy.grid(row=2, column=4, padx=5, pady=5)

# punkt D
label_D = tk.Label(root, text="Punkt D")
label_D.grid(row=3, column=0, padx=5, pady=5)
label_Dx = tk.Label(root, text="x:")
label_Dx.grid(row=3, column=1, padx=5, pady=5)
entry_Dx = tk.Entry(root)
entry_Dx.grid(row=3, column=2, padx=5, pady=5)
label_Dy = tk.Label(root, text="y:")
label_Dy.grid(row=3, column=3, padx=5, pady=5)
entry_Dy = tk.Entry(root)
entry_Dy.grid(row=3, column=4, padx=5, pady=5)

# punkt P
label_P = tk.Label(root, text="Punkt P")
label_P.grid(row=5, column=0, padx=5, pady=5)
label_Px = tk.Label(root, text="x:")
label_Px.grid(row=5, column=1, padx=5, pady=5)
entry_Px = tk.Entry(root, state="readonly")
entry_Px.grid(row=5, column=2, padx=5, pady=5)
label_Py = tk.Label(root, text="y:")
label_Py.grid(row=5, column=3, padx=5, pady=5)
entry_Py = tk.Entry(root, state="readonly")
entry_Py.grid(row=5, column=4, padx=5, pady=5)

# przycisk oblicz
button_calculate = tk.Button(root, text="Oblicz")
button_calculate.grid(row=4, column=2, padx=5, pady=5, sticky="nsew", columnspan=3)
button_calculate.configure(command=draw)

# przycisk wczytaj
button_load = tk.Button(root, text="Wczytaj dane z pliku")
button_load.grid(row=6, column=1, padx=5, pady=5, columnspan=2)
button_load.configure(command=load)

# przycisk zapisz
button_save = tk.Button(root, text="Zapisz wynik jako plik tekstowy")
button_save.grid(row=6, column=3, padx=5, pady=5, columnspan=2)
button_save.configure(command=save)

# przyciski do zmiany koloru linii 1
button_color_line1 = tk.Button(root, text="Zmień kolor linii 1")
button_color_line1.grid(row=8, column=5, padx=5, pady=5)
button_color_line1.configure(command=lambda: change_color_line(0))

# przyciski do zmiany koloru linii 2
button_color_line2 = tk.Button(root, text="Zmień kolor linii 2")
button_color_line2.grid(row=8, column=7, padx=5, pady=5)
button_color_line2.configure(command=lambda: change_color_line(1))

# combobox do zmiany grubości linii 1
combo_line1 = ttk.Combobox(root, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
combo_line1.grid(row=9, column=5, padx=5, pady=5)
combo_line1.set("Wybierz grubość linii 1")
combo_line1.bind("<<ComboboxSelected>>", change_width_line1)

# label do grubości linii
label_thickness = tk.Label(root, text="<-------------------Grubość linii------------------->")
label_thickness.grid(row=9, column=6, padx=5, pady=5)

# combobox do zmiany grubości linii 2
combo_line2 = ttk.Combobox(root, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
combo_line2.grid(row=9, column=7, padx=5, pady=5)
combo_line2.set("Wybierz grubość linii 2")
combo_line2.bind("<<ComboboxSelected>>", change_width_line2)

# combobox do zmiany stylu linii 1
combo_line1_style = ttk.Combobox(root, values=["solid", "dashed", "dashdot", "dotted"])
combo_line1_style.grid(row=10, column=5, padx=5, pady=5)
combo_line1_style.set("Wybierz styl linii 1")
combo_line1_style.bind("<<ComboboxSelected>>", change_style_line1)

# label do stylu linii
label_style = tk.Label(root, text="<-------------------Styl linii------------------->")
label_style.grid(row=10, column=6, padx=5, pady=5)

# combobox do zmiany stylu linii 2
combo_line2_style = ttk.Combobox(root, values=["solid", "dashed", "dashdot", "dotted"])
combo_line2_style.grid(row=10, column=7, padx=5, pady=5)
combo_line2_style.set("Wybierz styl linii 2")
combo_line2_style.bind("<<ComboboxSelected>>", change_style_line2)

# checkbox do ukrycia punktów
var = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="Ukryj punkty", variable=var)
checkbutton.grid(row=8, column=6, padx=5, pady=5)
checkbutton.configure(command=hide_points)

# przycisk do wyczyszczenia wykresu
button_clear = tk.Button(root, text="Wyczyść wykres")
button_clear.grid(row=11, column=5, padx=5, pady=5)
button_clear.configure(command=clear)

# przycisk do wyjścia z programu
button_exit = tk.Button(root, text="X Zamknij")
button_exit.grid(row=13, column=7, padx=0, pady=5)
button_exit.configure(command=root.destroy)

# przycisk do zapisu wykresu
button_save_plot = tk.Button(root, text="Zapisz jako plik PNG")
button_save_plot.grid(row=11, column=7, padx=5, pady=5)
button_save_plot.configure(command=save_plot)

# wyświetl okno
root.mainloop()
