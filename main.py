zrtvu3-codex/buscar-nuevas-implementaciones
"""Entry point to run the PaintApp."""
from paint_app.app import main

if __name__ == "__main__":
    main()

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk  # Importar para mostrar imágenes en el canvas
from tkinter import colorchooser, filedialog, messagebox  # Importar el selector de colores, cuadro de diálogo de archivos y mensajes
import os

# Configuración inicial
ICON_SIZE = 30  # Tamaño del icono (30x30 píxeles)

# Función para cargar la imagen híbrida
def load_hybrid_icon():
    try:
        img = Image.open("modoHibrido.png").convert("RGBA")
        ratio = min(ICON_SIZE/img.width, ICON_SIZE/img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        final_img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
        position = ((ICON_SIZE - new_size[0]) // 2, (ICON_SIZE - new_size[1]) // 2)
        final_img.paste(img, position)
        return ctk.CTkImage(light_image=final_img, dark_image=final_img, size=(ICON_SIZE, ICON_SIZE))
    except FileNotFoundError:
        img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, ICON_SIZE//2, ICON_SIZE], fill="#333333")
        draw.rectangle([ICON_SIZE//2, 0, ICON_SIZE, ICON_SIZE], fill="#CCCCCC")
        return ctk.CTkImage(light_image=img, dark_image=img, size=(ICON_SIZE, ICON_SIZE))

# Alternar modo oscuro/claro
def toggle_mode():
    ctk.set_appearance_mode("dark" if switch.get() else "light")


# Cargar y redimensionar la imagen del círculo de colores
def load_color_circle_image():
    img = Image.open("color_circle.png")  # Asegúrate de que la imagen esté en el mismo directorio
    img = img.resize((30, 30), Image.Resampling.LANCZOS)  # Ajusta el tamaño según sea necesario
    return ctk.CTkImage(light_image=img, dark_image=img, size=(30, 30))

# Crear ventana principal
root = ctk.CTk()
root.title("Paint App")
root.geometry("1100x600")
root.resizable(False, False)

# Cargar imagen híbrida
hybrid_icon = load_hybrid_icon()

color_circle_image = load_color_circle_image()

# Frame superior (barra de herramientas)
top_frame = ctk.CTkFrame(root, height=80)
top_frame.pack(fill="x", padx=5, pady=5)

top_frame.configure(cursor="hand2")

# Contenedor izquierdo (modo y herramientas)
left_panel = ctk.CTkFrame(top_frame, fg_color="transparent")
left_panel.pack(side="left", padx=10)

# Interruptor de modo oscuro/claro
switch = ctk.CTkSwitch(left_panel, text="Modo Oscuro", command=toggle_mode)
switch.pack(pady=5)

# Mostrar icono híbrido
icon_label = ctk.CTkLabel(left_panel, text="", image=hybrid_icon, fg_color="transparent")
icon_label.pack(pady=5)

# Contenedor derecho (herramientas de dibujo)
tools_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
tools_frame.pack(side="left", padx=10)

# Contenedor derecho para opciones de archivo
file_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
file_frame.pack(side="right", padx=10)

tools_frame.grid_columnconfigure(0, weight=1)
tools_frame.grid_columnconfigure(1, weight=1)

tools_label = ctk.CTkLabel(tools_frame, text="Herramientas:")
tools_label.grid(row=0, column=0, columnspan=2, pady=5)

# Botones de herramientas
pencil_btn = ctk.CTkButton(tools_frame, text="Lápiz", width=80, corner_radius=5)
pencil_btn.grid(row=1, column=0, padx=5, pady=5)

eraser_btn = ctk.CTkButton(tools_frame, text="Goma", width=80, corner_radius=5)
eraser_btn.grid(row=1, column=1, padx=5, pady=5)

# Menú desplegable

def change_brush_size(choice):
    global brush_size
    sizes= {"pequeño" : 5, "Mediano" : 10, "Grande" : 15, "Enorme" : 50}
    brush_size =sizes.get(choice, 5) # Valor por defecto 5


brush_size=5
tool_options = ["Pequeño", "Mediano", "Grande", "Enorme"]
tool_size = ctk.StringVar(value=tool_options[0])
tool_menu = ctk.CTkComboBox(tools_frame, values=tool_options, variable=tool_size, command=change_brush_size)
tool_menu.grid(row=1, column=2, padx=10, pady=5)

# Variable global para el color actual
current_color = "black"  # Color predeterminado

# Función para elegir un color
def choose_color():
    global current_color
    color_code = colorchooser.askcolor(title="Selecciona un color")[1]  # Obtener el código hexadecimal del color
    if color_code:  # Si se selecciona un color
        current_color = color_code
        color_btn.configure(fg_color=current_color)  # Cambiar el color del botón para reflejar el color seleccionado

# Botón con la imagen del círculo de colores
color_btn = ctk.CTkButton(
    tools_frame,
    text="",  # Sin texto
    image=color_circle_image,  # Asignar la imagen
    width=30,  # Ajustar el ancho al tamaño de la imagen
    height=30,  # Ajustar la altura al tamaño de la imagen
    corner_radius=30,  # Igual al tamaño del botón para hacerlo circular
    command=choose_color,  # Función para abrir el selector de colores
    fg_color="transparent",  # Fondo transparente
    hover_color="#bababa"  # Color al pasar el mouse
)

color_btn.grid(row=1, column=3, padx=5, pady=5)

# Función para cargar una imagen en el canvas
def upload_image():
    file_path = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    if file_path:  # Si se selecciona un archivo
        img = Image.open(file_path)  # Abrir la imagen seleccionada
        img.thumbnail((canvas.winfo_width(), canvas.winfo_height()))  # Redimensionar la imagen para que quepa en el canvas
        img_tk = ImageTk.PhotoImage(img)  # Convertir la imagen a un formato compatible con tkinter
        

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        img_width = img.width
        img_height = img.height

        x_center = (canvas_width - img_width) // 2
        y_center = (canvas_height - img_height) // 2

        canvas.create_image(x_center, y_center, anchor="nw", image=img_tk)  # Dibujar imagen centrada
        canvas.image = img_tk  # Guardar referencia para evitar el garbage collector


# Guardar el dibujo actual como imagen PNG
def save_project():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", "*.png")],
        title="Guardar dibujo"
    )
    if file_path:
        ps_temp = file_path + ".ps"
        canvas.postscript(file=ps_temp, colormode="color")
        img = Image.open(ps_temp)
        img.save(file_path, "png")
        os.remove(ps_temp)


# Abrir una imagen existente en el lienzo
def open_project():
    file_path = filedialog.askopenfilename(
        title="Abrir imagen",
        filetypes=[("PNG", "*.png"), ("Todos", "*.*")]
    )
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((canvas.winfo_width(), canvas.winfo_height()))
        img_tk = ImageTk.PhotoImage(img)
        canvas.delete("all")
        x_center = (canvas.winfo_width() - img.width) // 2
        y_center = (canvas.winfo_height() - img.height) // 2
        canvas.create_image(x_center, y_center, anchor="nw", image=img_tk)
        canvas.image = img_tk

# Botones para abrir y guardar archivos
open_btn = ctk.CTkButton(file_frame, text="Abrir", width=80, corner_radius=5, command=open_project)
open_btn.pack(side="left", padx=5, pady=5)
save_btn = ctk.CTkButton(file_frame, text="Guardar", width=80, corner_radius=5, command=save_project)
save_btn.pack(side="left", padx=5, pady=5)




# Botón para subir una imagen
upload_btn = ctk.CTkButton(
    tools_frame,
    text="Subir Imagen",
    width=100,
    corner_radius=5,
    command=upload_image
)
upload_btn.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

# Área de dibujo
canvas_frame = ctk.CTkFrame(root)
canvas_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

canvas = ctk.CTkCanvas(canvas_frame, bg="white", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Variables de dibujo
current_tool = "pencil"
prev_point = None

def start_drawing(event):
    global prev_point
    prev_point = (event.x, event.y)
    

def draw(event):
    global prev_point
    if prev_point:
        color = current_color if current_tool == "pencil" else "white"
        canvas.create_line(prev_point[0], prev_point[1], event.x, event.y, fill=color, width=brush_size, capstyle="round", smooth=True)
        prev_point = (event.x, event.y)
        

def stop_drawing(event):
    global prev_point
    prev_point = None


# Eventos del lienzo
canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)

def set_pencil():
    global current_tool
    current_tool = "pencil"
    canvas.configure(cursor="pencil")

def set_eraser():
    global current_tool
    current_tool = "eraser"
    canvas.configure(cursor="dotbox")

# Asignar funciones a botones
pencil_btn.configure(command=set_pencil)
eraser_btn.configure(command=set_eraser)



# Iniciar aplicación
root.mainloop()
main
