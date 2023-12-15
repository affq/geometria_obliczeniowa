import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.spatial import ConvexHull

points = []
hull = []

# clear everything before loading new points
def clear():
    global points
    global hull
    points = []
    hull = []
    plt.cla()
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

def load_points():
    clear()
    try:
        file = filedialog.askopenfile(mode='r', filetypes=[('Pliki tekstowe', '*.txt')], title="Wybierz plik z punktami")
        for i, line in enumerate(file):
            points.append([float(x) for x in line.split()])
            if i > 8:
                command_line.insert(tk.END, f"{i+1}     {line}")
            else:
                command_line.insert(tk.END, f"{i+1}      {line}")
        file.close()
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawny plik.")
    except TypeError:
        pass
    command_line.insert(tk.END, "\nWczytano punkty z pliku.")
    draw_points()
    draw_bbox()
    canvas.draw()

def draw_points():
    if current_point_visibility:
        for i, point in enumerate(points):
            if current_number_visibility:
                plt.text(point[0], point[1], f"{i+1}", color=current_point_color)
            if current_point_style == "circle":
                plt.plot(point[0], point[1], "o", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "square":
                plt.plot(point[0], point[1], "s", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "triangle":
                plt.plot(point[0], point[1], "^", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "pentagon":
                plt.plot(point[0], point[1], "p", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "hexagon":
                plt.plot(point[0], point[1], "h", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "octagon":
                plt.plot(point[0], point[1], "8", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "star":
                plt.plot(point[0], point[1], "*", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "plus":
                plt.plot(point[0], point[1], "+", color=current_point_color, markersize=current_point_size)
            elif current_point_style == "x":
                plt.plot(point[0], point[1], "x", color=current_point_color, markersize=current_point_size) 
    
def draw_bbox():
    if current_bbox_visibility:
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        bbox = [min(x), min(y), max(x), max(y)]
        plt.plot([bbox[0], bbox[0], bbox[2], bbox[2], bbox[0]], [bbox[1], bbox[3], bbox[3], bbox[1], bbox[1]], color=current_bbox_color, linestyle=current_bbox_style, linewidth=current_bbox_thickness)

def calculate_hull():
    # print (points)
    return


def draw_hull():
    global hull
    if len(points) > 2:
        if current_hull_visibility:
            hull = ConvexHull(points).vertices.tolist()
            hull.append(hull[0])
            hull = [points[i] for i in hull]
            plt.plot([point[0] for point in hull], [point[1] for point in hull], color=current_hull_color, linestyle=current_hull_style, linewidth=current_hull_thickness)
    else:
        messagebox.showerror("Błąd", "Za mało punktów do wyznaczenia otoczki wypukłej.")
    return

def save_hull():
    try:
        file = filedialog.asksaveasfile(mode='w', filetypes=[('Pliki tekstowe', '*.txt')], title="Zapisz otoczkę do pliku")
        for point in hull:
            file.write(f"{point[0]} {point[1]}\n")
        file.close()
        command_line.insert(tk.END, "\nZapisano otoczkę do pliku.")
    except TypeError:
        pass
    except AttributeError:
        pass

def redraw():
    plt.cla()
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    draw_points()
    draw_bbox()
    draw_hull()
    canvas.draw()

def add_point():
    try:
        x = float(x_entry.get())
        y = float(y_entry.get())
    except ValueError:
        messagebox.showerror("Błąd", "Wpisz poprawne współrzędne.")
    
    points.append([x, y])
    redraw()
    command_line.insert(tk.END, "\nWczytano punkty z pliku.")

def on_checkbox_point_change():
    global current_point_visibility
    if points_check_var.get():
        current_point_visibility = True
        redraw()
        command_line.insert(tk.END, "\nPokazano punkty")
    else:
        current_point_visibility = False
        redraw()
        command_line.insert(tk.END, "\nUkryto punkty")

def on_spinbox_point_change():
    global current_point_size
    current_point_size = points_size_var.get()
    redraw()
    command_line.insert(tk.END, f"\nZmieniono rozmiar punktów na {points_size_var.get()}")

def on_combobox_point_change():
    global current_point_style
    current_point_style = points_style_var.get()
    redraw()
    command_line.insert(tk.END, f"\nZmieniono styl punktów na {points_style_var.get()}")

def on_color_point_change():
    global current_point_color
    color = askcolor()
    current_point_color = color[1]
    points_color_button.configure(bg=color[1])
    redraw()
    command_line.insert(tk.END, f"\nZmieniono kolor punktów na {color[1]}")

def on_checkbox_hull_change():
    global current_hull_visibility
    if hull == []:   
        hull_check_var.set(False)
        messagebox.showerror("Błąd", "Najpierw wyznacz otoczkę.")
    elif hull_check_var.get():
        current_hull_visibility = True
        redraw()
        command_line.insert(tk.END, "\nPokazano otoczkę wypukłą")
    else:
        current_hull_visibility = False
        redraw()
        command_line.insert(tk.END, "\nUkryto otoczkę wypukłą")


def on_checkbox_number_visibility_change():
    global current_number_visibility
    if points_number_visibility_var.get():
        current_number_visibility = True
        redraw()
        command_line.insert(tk.END, "\nPokazano numery punktów")
    else:
        current_number_visibility = False
        redraw()
        command_line.insert(tk.END, "\nUkryto numery punktów")

def on_color_hull_change():
    global current_hull_color
    color = askcolor()
    current_hull_color = color[1]
    hull_color_button.configure(bg=color[1])
    redraw()
    command_line.insert(tk.END, f"\nZmieniono kolor otoczki na {color[1]}")


def on_spinbox_hull_change():
    global current_hull_thickness
    current_hull_thickness = hull_size_var.get()
    redraw()
    command_line.insert(tk.END, f"\nZmieniono grubość otoczki na {hull_size_var.get()}")

def on_combobox_hull_change():
    global current_hull_style
    current_hull_style = hull_style_var.get()
    redraw()
    command_line.insert(tk.END, f"\nZmieniono styl otoczki na {hull_style_var.get()}")

def on_checkbox_bbox_change():
    global current_bbox_visibility
    if bbox_check_var.get():
        current_bbox_visibility = True
        redraw()
        command_line.insert(tk.END, "\nPokazano bbox")
    else:
        current_bbox_visibility = False
        redraw()
        command_line.insert(tk.END, "\nUkryto bbox")

def on_color_bbox_change():
    global current_bbox_color
    color = askcolor()
    current_bbox_color = color[1]
    bbox_color_button.configure(bg=color[1])
    redraw()
    command_line.insert(tk.END, f"\nZmieniono kolor bbox na {color[1]}")

def on_spinbox_bbox_change():
    global current_bbox_thickness
    current_bbox_thickness = bbox_thickness_var.get()
    redraw()
    command_line.insert(tk.END, f"\nZmieniono grubość bbox na {bbox_thickness_var.get()}")

def on_combobox_bbox_change():
    global current_bbox_style
    current_bbox_style = bbox_style_var.get()
    redraw()
    command_line.insert(tk.END, f"\nZmieniono styl bbox na {bbox_style_var.get()}")

def draw_first_hull():
    global current_hull_visibility
    current_hull_visibility = True
    redraw()
    hull_check_var.set(True)
    command_line.insert(tk.END, "\nPokazano otoczkę wypukłą")

# punkty
default_point_color = "black"
default_point_size = 2
default_point_style = "circle"
default_point_visibility = True
default_number_visibility = True

current_point_color = default_point_color
current_point_size = default_point_size
current_point_style = default_point_style
current_point_visibility = default_point_visibility
current_number_visibility = default_number_visibility

#convex hull
default_hull_color = "red"
default_hull_thickness = 2
default_hull_style = "solid"
default_hull_visibility = False

current_hull_color = default_hull_color
current_hull_thickness = default_hull_thickness
current_hull_style = default_hull_style
current_hull_visibility = default_hull_visibility

#bbox
default_bbox_color = "blue"
default_bbox_thickness = 2
default_bbox_style = "solid"
default_bbox_visibility = True

current_bbox_color = default_bbox_color
current_bbox_thickness = default_bbox_thickness
current_bbox_style = default_bbox_style
current_bbox_visibility = default_bbox_visibility

root = tk.Tk()
root.title("Wyznaczanie otoczki wypukłej")
root.geometry("1070x750")
root.resizable(False, False)


fig = plt.figure(figsize=(7,7))
plt.grid(False)
plt.xticks([])
plt.yticks([])
for spine in plt.gca().spines.values():
    spine.set_visible(False)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, padx=10, pady=10)


load_button = tk.Button(root, text="Wczytaj punkty", width=20, command=load_points)
load_button.pack(padx=10, pady=10, anchor=tk.NW)

command_line = tk.Text(root, width=40, height=10)
command_line.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.NW)

single_point_frame = tk.LabelFrame(root, text="Dodaj pojedynczy punkt")
single_point_frame.pack(side=tk.TOP, padx=10, anchor=tk.NW)

x_label = ttk.Label(single_point_frame, text="X=")
x_label.pack(side=tk.LEFT, padx=10)
x_entry = ttk.Entry(single_point_frame, width=10)
x_entry.pack(side=tk.LEFT)

y_label = ttk.Label(single_point_frame, text="Y=")
y_label.pack(side=tk.LEFT, padx=10)
y_entry = ttk.Entry(single_point_frame, width=10)
y_entry.pack(side=tk.LEFT)

add_button = tk.Button(single_point_frame, text="Dodaj punkt", width=12)
add_button.pack(side=tk.LEFT, padx=10, pady=10)
add_button.configure(command=add_point)

convex_hull_frame = tk.LabelFrame(root, text="Budowanie otoczki wypukłej")
convex_hull_frame.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.NW)

build_button = tk.Button(convex_hull_frame, text="Narysuj otoczkę", width=19)
build_button.pack(side=tk.LEFT, padx=10, pady=10)
build_button.configure(command=draw_first_hull)

save_button = tk.Button(convex_hull_frame, text="Zapisz otoczkę", width=19)
save_button.pack(side=tk.LEFT, padx=10, pady=10)
save_button.configure(command=save_hull)

drawing_parameters = tk.LabelFrame(root, text="Prezentacja")
drawing_parameters.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.NW)

points_frame = tk.LabelFrame(drawing_parameters, text="Punkty")
points_frame.pack( padx=10, pady=10, anchor=tk.NW)

#ramka na checkboxy
checkbox_frame = tk.Frame(points_frame)
checkbox_frame.pack(side=tk.TOP, padx=10)

points_check_var = tk.BooleanVar()
points_checkbutton = ttk.Checkbutton(checkbox_frame, text="Pokaż punkty", variable=points_check_var)
points_checkbutton.pack(side=tk.LEFT, padx=10)
points_checkbutton.invoke()
points_check_var.trace_add("write", lambda *args: on_checkbox_point_change())

points_number_visibility_var = tk.BooleanVar()
points_number_visibility_checkbutton = ttk.Checkbutton(checkbox_frame, text="Pokaż numery", variable=points_number_visibility_var)
points_number_visibility_checkbutton.pack(side=tk.RIGHT, padx=10)
points_number_visibility_checkbutton.invoke()
points_number_visibility_var.trace_add("write", lambda *args: on_checkbox_number_visibility_change())

points_color_button = tk.Button(points_frame, text="Kolor", width=10)
points_color_button.pack(side=tk.LEFT, padx=10, pady=10)
points_color_button.configure(command=on_color_point_change)

points_size_var = tk.IntVar()
points_size_spinbox = tk.Spinbox(points_frame, from_=1, to=10, width=10, textvariable=points_size_var)
points_size_spinbox.pack(side=tk.LEFT, padx=10, pady=10)
points_size_var.trace_add("write", lambda *args: on_spinbox_point_change())

points_style_options = ["circle", "square", "triangle", "pentagon", "hexagon", "octagon", "star", "plus", "x"]
points_style_var = tk.StringVar()
points_style_combobox = ttk.Combobox(points_frame, width=10, textvariable=points_style_var, values=points_style_options, state="readonly")
points_style_combobox.pack(side=tk.LEFT, padx=10, pady=10)
points_style_combobox.bind("<<ComboboxSelected>>", lambda *args: on_combobox_point_change())

hull_frame = tk.LabelFrame(drawing_parameters, text="Otoczka wypukła")
hull_frame.pack(side=tk.TOP, padx=10, pady=10, anchor=tk.NW)

hull_check_var = tk.BooleanVar()
hull_checkbutton = ttk.Checkbutton(hull_frame, text="Pokaż otoczkę", variable=hull_check_var)
hull_checkbutton.pack(side=tk.TOP, padx=10)
hull_check_var.trace_add("write", lambda *args: on_checkbox_hull_change())

hull_color_button = tk.Button(hull_frame, text="Kolor", width=10)
hull_color_button.pack(side=tk.LEFT, padx=10, pady=10)
hull_color_button.configure(command=on_color_hull_change)

hull_size_var = tk.IntVar()
hull_size_spinbox = tk.Spinbox(hull_frame, from_=1, to=10, width=10, textvariable=hull_size_var)
hull_size_spinbox.pack(side=tk.LEFT, padx=10, pady=10)
hull_size_var.trace_add("write", lambda *args: on_spinbox_hull_change())

hull_style_options = ["dashed", "dotted", "solid", "dashdot"]
hull_style_var = tk.StringVar()
hull_style_combobox = ttk.Combobox(hull_frame, width=10, textvariable=hull_style_var, values=hull_style_options, state="readonly")
hull_style_combobox.pack(side=tk.LEFT, padx=10, pady=10)
hull_style_combobox.bind("<<ComboboxSelected>>", lambda *args: on_combobox_hull_change())

#bbox
bbox_frame = tk.LabelFrame(drawing_parameters, text="Bbox")
bbox_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.NW)

bbox_check_var = tk.BooleanVar()
bbox_checkbutton = ttk.Checkbutton(bbox_frame, text="Pokaż bbox", variable=bbox_check_var)
bbox_checkbutton.pack(side=tk.TOP, padx=10)
bbox_checkbutton.invoke()
bbox_check_var.trace_add("write", lambda *args: on_checkbox_bbox_change())

bbox_color_button = tk.Button(bbox_frame, text="Kolor", width=10)
bbox_color_button.pack(side=tk.LEFT, padx=10, pady=10)
bbox_color_button.configure(command=on_color_bbox_change)

bbox_thickness_var = tk.IntVar()
bbox_thickness_spinbox = tk.Spinbox(bbox_frame, from_=1, to=10, width=10, textvariable=bbox_thickness_var)
bbox_thickness_spinbox.pack(side=tk.LEFT, padx=10, pady=10)
bbox_thickness_var.trace_add("write", lambda *args: on_spinbox_bbox_change())

bbox_style_options = ["dashed", "dotted", "solid", "dashdot"]
bbox_style_var = tk.StringVar()
bbox_style_combobox = ttk.Combobox(bbox_frame, width=10, textvariable=bbox_style_var, values=bbox_style_options, state="readonly")
bbox_style_combobox.pack(side=tk.LEFT, padx=10, pady=10)
bbox_style_combobox.bind("<<ComboboxSelected>>", lambda *args: on_combobox_bbox_change())

root.mainloop()