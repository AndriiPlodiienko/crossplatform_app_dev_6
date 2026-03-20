import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog, filedialog, colorchooser


# ================= MODEL =================
class ModelApp:
    def __init__(self):
        self.profile = {
            "name": "",
            "age": 0,
            "mode": "",
            "level": 0,
            "color": None,
            "file": None
        }
        self.notify = lambda data: None

    def set_profile(self, key, value):
        self.profile[key] = value
        self.notify(self.profile)

    def get_profile(self):
        return self.profile


# ================= CUSTOM DIALOG =================
class CustomDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.result = None

        self.title("Додаткові налаштування")
        self.grab_set()

        tk.Label(self, text="Рівень (Scale):").pack()

        self.scale = tk.Scale(self, from_=1, to=10, orient="horizontal")
        self.scale.pack()

        tk.Label(self, text="Режим:").pack()

        self.combo = ttk.Combobox(self, values=["Easy", "Normal", "Hard"], state="readonly")
        self.combo.current(0)
        self.combo.pack()

        tk.Button(self, text="OK", command=self.ok).pack()
        tk.Button(self, text="Cancel", command=self.cancel).pack()

    def ok(self):
        self.result = (self.scale.get(), self.combo.get())
        self.destroy()

    def cancel(self):
        self.destroy()


# ================= VIEW =================
class ViewApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # callbacks (заглушки)
        self.on_name = lambda: None
        self.on_age = lambda: None
        self.on_mode = lambda: None
        self.on_custom = lambda: None
        self.on_file = lambda: None
        self.on_save = lambda: None
        self.on_dir = lambda: None
        self.on_color = lambda: None
        self.on_save_profile = lambda: None

        tk.Label(self, text="Створення профілю", font=("Arial", 14)).pack()

        tk.Button(self, text="Ввести ім’я", command=lambda: self.on_name()).pack(fill="x")
        tk.Button(self, text="Ввести вік", command=lambda: self.on_age()).pack(fill="x")
        tk.Button(self, text="Вибрати режим", command=lambda: self.on_mode()).pack(fill="x")
        tk.Button(self, text="Додаткові налаштування", command=lambda: self.on_custom()).pack(fill="x")

        tk.Button(self, text="Вибрати файл", command=lambda: self.on_file()).pack(fill="x")
        tk.Button(self, text="Зберегти файл", command=lambda: self.on_save()).pack(fill="x")
        tk.Button(self, text="Вибрати папку", command=lambda: self.on_dir()).pack(fill="x")
        tk.Button(self, text="Вибрати колір", command=lambda: self.on_color()).pack(fill="x")

        tk.Button(self, text="Зберегти профіль", command=lambda: self.on_save_profile()).pack(fill="x")

        self.label = tk.Label(self, text="",fg="black", bg="white")
        self.label.pack(fill="x")

    def update_view(self, data):
        self.label.config(text=str(data))
        if data["color"]:
            self.label.config(bg=data["color"][1])


# ================= CONTROLLER =================
class ControllerApp:
    def __init__(self, root):
        self.model = ModelApp()
        self.view = ViewApp(root)
        self.view.pack(fill="both")

        self.model.notify = self.view.update_view

        # binding
        self.view.on_name = self.set_name
        self.view.on_age = self.set_age
        self.view.on_mode = self.set_mode
        self.view.on_custom = self.custom_settings
        self.view.on_file = self.open_file
        self.view.on_save = self.save_file
        self.view.on_dir = self.choose_dir
        self.view.on_color = self.choose_color
        self.view.on_save_profile = self.save_profile

    # ===== simpledialog =====
    def set_name(self):
        name = simpledialog.askstring("Ім’я", "Введіть ім’я:")
        if name:
            self.model.set_profile("name", name)

    def set_age(self):
        age = simpledialog.askinteger("Вік", "Введіть вік:")
        if age is None:
            messagebox.showwarning("Увага", "Вік не введено")
        elif age < 0:
            messagebox.showerror("Помилка", "Некоректний вік")
        else:
            self.model.set_profile("age", age)

    def set_mode(self):
        mode = simpledialog.askstring("Режим", "Введіть режим (User/Admin):")
        if mode:
            self.model.set_profile("mode", mode)

    # ===== custom dialog =====
    def custom_settings(self):
        dialog = CustomDialog(self.view)
        self.view.wait_window(dialog)

        if dialog.result:
            level, mode = dialog.result
            self.model.set_profile("level", level)
            self.model.set_profile("mode", mode)

    # ===== filedialog =====
    def open_file(self):
        file = filedialog.askopenfilename()
        if file:
            self.model.set_profile("file", file)

    def save_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt")
        if file:
            self.model.set_profile("file", file)

    def choose_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            messagebox.showinfo("Папка", f"Обрано: {directory}")

    # ===== color =====
    def choose_color(self):
        color = colorchooser.askcolor()
        if color:
            self.model.set_profile("color", color)

    # ===== messagebox =====
    def save_profile(self):
        result = messagebox.askyesnocancel("Збереження", "Зберегти профіль?")

        if result is True:
            messagebox.showinfo("OK", "Профіль збережено")
        elif result is False:
            retry = messagebox.askretrycancel("Повторити?", "Спробувати ще?")
            if retry:
                self.save_profile()
        else:
            messagebox.showwarning("Скасовано", "Операцію скасовано")


# ================= MAIN =================
if __name__ == "__main__":
    root = tk.Tk()
    root.title("MVC Profile App")
    app = ControllerApp(root)
    root.mainloop()