# Paint application module
import os
from pathlib import Path
import customtkinter as ctk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk, ImageGrab


ASSETS_DIR = Path(__file__).resolve().parent / 'assets'
ICON_SIZE = 30


class PaintApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Paint App")
        self.root.geometry("1100x600")
        self.root.resizable(False, False)

        self.current_color = "black"
        self.brush_size = 5
        self.current_tool = "pencil"
        self.prev_point = None

        self._build_ui()

    def _build_ui(self):
        top_frame = ctk.CTkFrame(self.root, height=80)
        top_frame.pack(fill="x", padx=5, pady=5)
        top_frame.configure(cursor="hand2")

        left_panel = ctk.CTkFrame(top_frame, fg_color="transparent")
        left_panel.pack(side="left", padx=10)

        self.switch = ctk.CTkSwitch(left_panel, text="Modo Oscuro", command=self._toggle_mode)
        self.switch.pack(pady=5)

        icon_label = ctk.CTkLabel(left_panel, text="", image=self._load_hybrid_icon(), fg_color="transparent")
        icon_label.pack(pady=5)

        tools_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        tools_frame.pack(side="left", padx=10)
        tools_frame.grid_columnconfigure(0, weight=1)
        tools_frame.grid_columnconfigure(1, weight=1)

        tools_label = ctk.CTkLabel(tools_frame, text="Herramientas:")
        tools_label.grid(row=0, column=0, columnspan=2, pady=5)

        self.pencil_btn = ctk.CTkButton(tools_frame, text="Lápiz", width=80, corner_radius=5, command=self.set_pencil)
        self.pencil_btn.grid(row=1, column=0, padx=5, pady=5)
        self.eraser_btn = ctk.CTkButton(tools_frame, text="Goma", width=80, corner_radius=5, command=self.set_eraser)
        self.eraser_btn.grid(row=1, column=1, padx=5, pady=5)

        tool_options = ["Pequeño", "Mediano", "Grande", "Enorme"]
        self.tool_size = ctk.StringVar(value=tool_options[0])
        tool_menu = ctk.CTkComboBox(tools_frame, values=tool_options, variable=self.tool_size, command=self.change_brush_size)
        tool_menu.grid(row=1, column=2, padx=10, pady=5)

        color_circle_image = self._load_color_circle_image()
        color_btn = ctk.CTkButton(
            tools_frame,
            text="",
            image=color_circle_image,
            width=30,
            height=30,
            corner_radius=30,
            command=self.choose_color,
            fg_color="transparent",
            hover_color="#bababa",
        )
        color_btn.grid(row=1, column=3, padx=5, pady=5)

        file_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        file_frame.pack(side="right", padx=10)

        open_btn = ctk.CTkButton(file_frame, text="Abrir", width=80, corner_radius=5, command=self.open_project)
        open_btn.pack(side="left", padx=5, pady=5)
        save_btn = ctk.CTkButton(file_frame, text="Guardar", width=80, corner_radius=5, command=self.save_project)
        save_btn.pack(side="left", padx=5, pady=5)

        canvas_frame = ctk.CTkFrame(self.root)
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        self.canvas = ctk.CTkCanvas(canvas_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

    def _toggle_mode(self):
        ctk.set_appearance_mode("dark" if self.switch.get() else "light")

    def _load_hybrid_icon(self):
        path = ASSETS_DIR / "modoHibrido.png"
        try:
            img = Image.open(path).convert("RGBA")
            ratio = min(ICON_SIZE / img.width, ICON_SIZE / img.height)
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

    def _load_color_circle_image(self):
        path = ASSETS_DIR / "color_circle.png"
        img = Image.open(path)
        img = img.resize((30, 30), Image.Resampling.LANCZOS)
        return ctk.CTkImage(light_image=img, dark_image=img, size=(30, 30))

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Selecciona un color")[1]
        if color_code:
            self.current_color = color_code

    def change_brush_size(self, choice):
        sizes = {"Pequeño": 5, "Mediano": 10, "Grande": 15, "Enorme": 50}
        self.brush_size = sizes.get(choice, 5)

    def start_drawing(self, event):
        self.prev_point = (event.x, event.y)

    def draw(self, event):
        if self.prev_point:
            color = self.current_color if self.current_tool == "pencil" else "white"
            self.canvas.create_line(
                self.prev_point[0], self.prev_point[1], event.x, event.y,
                fill=color, width=self.brush_size, capstyle="round", smooth=True
            )
            self.prev_point = (event.x, event.y)

    def stop_drawing(self, _event):
        self.prev_point = None

    def set_pencil(self):
        self.current_tool = "pencil"
        self.canvas.configure(cursor="pencil")

    def set_eraser(self):
        self.current_tool = "eraser"
        self.canvas.configure(cursor="dotbox")

    def save_project(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
            title="Guardar dibujo",
        )
        if file_path:
            self.root.update()
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            img = ImageGrab.grab(bbox=(x, y, x1, y1))
            img.save(file_path, "PNG")

    def open_project(self):
        file_path = filedialog.askopenfilename(
            title="Abrir imagen",
            filetypes=[("PNG", "*.png"), ("Todos", "*.*")]
        )
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()))
            img_tk = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            x_center = (self.canvas.winfo_width() - img.width) // 2
            y_center = (self.canvas.winfo_height() - img.height) // 2
            self.canvas.create_image(x_center, y_center, anchor="nw", image=img_tk)
            self.canvas.image = img_tk

    def run(self):
        self.root.mainloop()


def main():
    app = PaintApp()
    app.run()


if __name__ == "__main__":
    main()
