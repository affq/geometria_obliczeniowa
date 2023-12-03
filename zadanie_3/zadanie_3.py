import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from tkinter import ttk

polygon = []
points = []
points_inside_loaded = []
points_added_manually = []
number_of_points_added_manually = 0
points_inside = 0

default_color = "black"
default_line_width = 1
default_line_style = "solid"

default_point_inside = "green"
default_point_outside = "red"
default_point_size = 5

current_color = default_color
current_line_width = default_line_width
current_line_style = default_line_style

current_point_inside = default_point_inside
current_point_outside = default_point_outside
current_point_size = default_point_size

def bbox_check(x, y):
    x_coords = [point[0] for point in polygon]
    y_coords = [point[1] for point in polygon]
    return min(x_coords) <= x <= max(x_coords) and min(y_coords) <= y <= max(y_coords)

def check_point_location(x, y):
    return bbox_check(x, y) and polygon_check(x, y)

def polygon_check(x, y):
    counter = 0
    for i in range(len(polygon)):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        
        if (min(p1[1], p2[1]) <= y <= max(p1[1], p2[1])):
            try:
                x_cross = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
            except ZeroDivisionError:
                x_cross = p1[0]

            if x_cross == x:
                return True
            
            if x_cross > x:
                counter += 1

    return counter % 2 == 1

def reset():
    global points_inside
    polygon.clear()
    points.clear()
    points_added_manually.clear()
    points_inside = 0
    global number_of_points_added_manually
    number_of_points_added_manually = 0
    ax.clear()
    number_label.configure(text="0")
    result_label.configure(text="wynik")
    x_input.delete(0, tk.END)
    y_input.delete(0, tk.END)
    canvas.draw()

def load_polygon():
    try:
        file = filedialog.askopenfile(mode='r', filetypes=[('Pliki tekstowe', '*.txt')])
        temp = []
        for line in file:
            temp.append([float(x) for x in line.split()])
        file.close()
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawny plik.")
        return
    except TypeError:
        return
    reset()
    polygon.extend(temp)
    draw_polygon()

def load_points():
    try:
        file = filedialog.askopenfile(mode='r', filetypes=[('Pliki tekstowe', '*.txt')])
        temp = []
        for line in file:
            temp.append([float(x) for x in line.split()])
        file.close()
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawny plik.")
        return
    except TypeError:
        return
    global points_inside
    global number_of_points_added_manually
    points.clear()
    points_added_manually.clear()
    points_inside = 0
    number_of_points_added_manually = 0
    points.extend(temp)
    number_label.configure(text="0")
    result_label.configure(text="wynik")
    x_input.delete(0, tk.END)
    y_input.delete(0, tk.END)
    draw_polygon()
    try:
        draw_points()
    except ValueError:
        messagebox.showerror("Błąd", "Najpierw dodaj wielokąt.")

def draw_points():
    global points_inside
    for point in points:
        if check_point_location(point[0], point[1]):
            points_inside += 1
            points_inside_loaded.append(point)
            ax.plot(point[0], point[1], color=current_point_inside, marker='o', markersize=current_point_size)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
    number_label.configure(text=str(points_inside))
    canvas.draw()

def draw_polygon():
    ax.clear()
    ax.plot([x[0] for x in polygon], [x[1] for x in polygon], color=current_color, linewidth=current_line_width, linestyle=current_line_style)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    canvas.draw()

def check_point():
    global points_inside
    global number_of_points_added_manually

    try:
        x = float(x_input.get())
        y = float(y_input.get())
    except ValueError:
        messagebox.showerror("Błąd", "Wpisz poprawne współrzędne.")
        return

    if len(polygon) == 0:
        messagebox.showerror("Informacja", "Najpierw wczytaj wielokąt.")
        return

    points.clear()
    draw_polygon()
    # draw points added manually
    for point in points_added_manually:
        if point[2] == 1:
            ax.plot(point[0], point[1], color=current_point_inside, marker='o', markersize=current_point_size)
        else:
            ax.plot(point[0], point[1], color=current_point_outside, marker='o', markersize=current_point_size)
        ax.set_xlabel('x')
        ax.set_ylabel('y')

    if check_point_location(x, y):
        ax.plot(x, y, color=current_point_inside, marker='o', markersize=current_point_size)
        result_label.configure(text="punkt należy do wielokąta", fg="green", font=("Arial", 10, "italic"))
        if [x, y, 1] not in points_added_manually:
            points_added_manually.append([x, y, 1])
            number_of_points_added_manually += 1
        else:
            messagebox.showinfo("Informacja", "Ten punkt został już dodany.")
        number_label.configure(text=str(number_of_points_added_manually))
    else:
        ax.plot(x, y, color=current_point_outside, marker='o', markersize=current_point_size)
        points_added_manually.append([x, y, 0])
        result_label.configure(text="punkt nie należy do wielokąta", fg="red", font=("Arial", 10, "italic"))

    canvas.draw()


root = tk.Tk()
root.title("Zadanie 3")
root.geometry("950x750")

load_polygon_button = tk.Button(root, text="Wczytaj wielokąt z pliku", width=20, height=2)
load_polygon_button.grid(row=0, column=0, padx=5, pady=5, columnspan=4)
load_polygon_button.configure(command=load_polygon)

load_points_button = tk.Button(root, text="Wczytaj punkty z pliku", width=20, height=2)
load_points_button.grid(row=1, column=0, padx=5, pady=5, columnspan=4)
load_points_button.configure(command=load_points)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=4, rowspan=20, padx=5, pady=5, columnspan=8)

frame = tk.Frame(root, bd=1, relief=tk.SOLID)
frame.grid(row=3, column=0, padx=20, pady=20, columnspan=4)

point_label = tk.Label(frame, text="Wpisz współrzędne punktu:", font=("Calibri", 12, "bold"))
point_label.grid(row=0, column=0, padx=10, pady=20, columnspan=4)

# x_label = tk.Label(frame, text="x:")
# x_label.grid(row=1, column=0, padx=5, pady=5)

x_input = tk.Entry(frame, width=10)
x_input.grid(row=1, column=1, padx=5, pady=5)

# y_label = tk.Label(frame, text="y:")
# y_label.grid(row=1, column=2, padx=5, pady=5)

y_input = tk.Entry(frame, width=10)
y_input.grid(row=1, column=2, padx=5, pady=5)

check_point_button = tk.Button(frame, text="Sprawdź położenie punktu", width=20, height=2)
check_point_button.grid(row=2, column=0, padx=5, pady=20, columnspan=4)
check_point_button.configure(command=check_point)

result_label = tk.Label(frame, text="wynik", font=("Calibri", 12), fg="blue")
result_label.grid(row=3, column=0, padx=5, pady=5, columnspan=4)

amount_label = tk.Label(root, text="Liczba punktów należących do wielokąta: ", font=("Calibri", 12, "bold"))
amount_label.grid(row=6, column=0, padx=5, pady=5, columnspan=4)

number_label = tk.Label(root, text="0", font =("Calibri", 20, "bold"))
number_label.grid(row=7, column=0, padx=5, pady=5, columnspan=4)


# powinna istnieć możliwość konfigurowania parametrów rysunku, tzn.: kolory, grubości i style
# linii,


def redraw():
    ax.clear()
    if polygon:
        ax.plot([x[0] for x in polygon], [x[1] for x in polygon], color=current_color, linewidth=current_line_width, linestyle=current_line_style)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    if points:
        for point in points_inside_loaded:
            if check_point_location(point[0], point[1]):
                ax.plot(point[0], point[1], color=current_point_inside, marker='o', markersize=current_point_size)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
            else:
                ax.plot(point[0], point[1], color=current_point_outside, marker='o', markersize=current_point_size)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
    if points_added_manually:
        for point in points_added_manually:
            if point[2] == 1:
                ax.plot(point[0], point[1], color=current_point_inside, marker='o', markersize=current_point_size)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
            else:
                ax.plot(point[0], point[1], color=current_point_outside, marker='o', markersize=current_point_size)
                ax.set_xlabel('x')
                ax.set_ylabel('y')
    canvas.draw()

# zmiana koloru linii
def change_color():
    global current_color
    color = askcolor()
    if color[1]:
        current_color = color[1]
        redraw()

# zmiana grubości linii
def change_line_width(event):
    global current_line_width
    current_line_width = int(line_width.get())
    redraw()

# zmiana stylu linii
def change_line_style(event):
    global current_line_style
    current_line_style = line_style.get()
    redraw()

frame2 = tk.Frame(root)
frame2.grid(row=21, column=4, columnspan=8, padx=5, pady=5)

color_button = tk.Button(frame2, text="Zmień kolor linii", width=20, height=2)
color_button.grid(row=0, column=0, padx=20, pady=5)
color_button.configure(command=change_color)

line_width = ttk.Combobox(frame2, width=20, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
line_width.grid(row=0, column=3, padx=5, pady=5)
line_width.current(0)
line_width.set("Wybierz grubość linii")
line_width.bind("<<ComboboxSelected>>", change_line_width)

line_style = ttk.Combobox(frame2, width=20, values=["solid", "dashed", "dashdot", "dotted"])
line_style.grid(row=0, column=7, padx=20, pady=5)
line_style.current(0)
line_style.set("Wybierz styl linii")
line_style.bind("<<ComboboxSelected>>", change_line_style)

# kolor punktów wewnątrz wielokąta
def change_point_inside():
    global current_point_inside
    color = askcolor()
    if color[1]:
        current_point_inside = color[1]
        redraw()

# kolor punktów na zewnątrz wielokąta
def change_point_outside():
    global current_point_outside
    color = askcolor()
    if color[1]:
        current_point_outside = color[1]
        redraw()

# rozmiar punktów
def change_point_size(event):
    global current_point_size
    current_point_size = int(point_size.get())
    redraw()

frame3 = tk.Frame(root)
frame3.grid(row=22, column=4, columnspan=8, padx=5, pady=5)

point_inside_button = tk.Button(frame3, text="Zmień kolor punktów \n wewnątrz wielokąta", width=20, height=2)
point_inside_button.grid(row=0, column=0, padx=20, pady=5)
point_inside_button.configure(command=change_point_inside)

point_outside_button = tk.Button(frame3, text="Zmień kolor punktów \n na zewnątrz wielokąta", width=20, height=2)
point_outside_button.grid(row=0, column=3, padx=20, pady=5)
point_outside_button.configure(command=change_point_outside)

point_size = ttk.Combobox(frame3, width=20, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
point_size.grid(row=0, column=6, padx=5, pady=5)
point_size.current(0)
point_size.set("Wybierz rozmiar punktów")
point_size.bind("<<ComboboxSelected>>", change_point_size)

root.resizable(False, False)

root.mainloop()