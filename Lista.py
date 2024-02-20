import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os

class PipoShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PipoShop")
        self.root.configure(bg="white")

        # Configuración de la geometría de la ventana
        window_width = 400
        window_height = 300
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Conexión a la base de datos
        self.connection = sqlite3.connect("usuarios.db")
        self.cursor = self.connection.cursor()
        self.crear_tabla_usuarios()

        # Marco principal
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(expand=True, fill="both")

        # Etiqueta de bienvenida
        self.welcome_label = ttk.Label(self.main_frame, text="¡Bienvenido a PipoShop!", font=("Helvetica", 20), background="white")
        self.welcome_label.pack(pady=20)

        # Botón de Registrarse
        self.register_button = ttk.Button(self.main_frame, text="Registrarse", command=self.registrarse)
        self.register_button.config(style='RoundButton.TButton')
        self.register_button.pack(pady=10)

        # Botón de Iniciar sesión
        self.login_button = ttk.Button(self.main_frame, text="Iniciar sesión", command=self.iniciar_sesion)
        self.login_button.config(style='RoundButton.TButton')
        self.login_button.pack(pady=10)

        # Estilo para los botones redondeados
        self.style = ttk.Style()
        self.style.configure('RoundButton.TButton', foreground="black", background="lightgrey", borderwidth=0, bordercolor="white", border=0, focuscolor="none")
        self.style.map('RoundButton.TButton', background=[('active', 'lightgrey')])

    def crear_tabla_usuarios(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')
        self.connection.commit()

    def registrarse(self):
        messagebox.showinfo("Registrarse", "Introduce tus datos para registrarte:")
        registro_window = tk.Toplevel(self.root)
        registro_window.title("Registro")
        registro_window.geometry("300x200")
        registro_window.configure(bg="white")

        registro_frame = tk.Frame(registro_window, bg="white")
        registro_frame.pack(expand=True, fill="both")

        nombre_label = ttk.Label(registro_frame, text="Nombre:", background="white")
        nombre_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        nombre_entry = ttk.Entry(registro_frame)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        email_label = ttk.Label(registro_frame, text="Email:", background="white")
        email_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        email_entry = ttk.Entry(registro_frame)
        email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        password_label = ttk.Label(registro_frame, text="Contraseña:", background="white")
        password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        password_entry = ttk.Entry(registro_frame, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        registrar_button = ttk.Button(registro_frame, text="Registrar", command=lambda: self.procesar_registro(nombre_entry.get(), email_entry.get(), password_entry.get(), registro_window))
        registrar_button.grid(row=3, columnspan=2, pady=10)

    def procesar_registro(self, nombre, email, password, window):
        try:
            self.cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)", (nombre, email, password))
            self.connection.commit()
            messagebox.showinfo("Registro exitoso", f"Bienvenido, {nombre}! Tu cuenta ha sido registrada con éxito.")
            window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El correo electrónico ya está en uso.")

    def iniciar_sesion(self):
        messagebox.showinfo("Iniciar Sesión", "Introduce tus datos para iniciar sesión:")
        login_window = tk.Toplevel(self.root)
        login_window.title("Iniciar Sesión")
        login_window.geometry("300x150")
        login_window.configure(bg="white")

        login_frame = tk.Frame(login_window, bg="white")
        login_frame.pack(expand=True, fill="both")

        email_label = ttk.Label(login_frame, text="Email:", background="white")
        email_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        email_entry = ttk.Entry(login_frame)
        email_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        password_label = ttk.Label(login_frame, text="Contraseña:", background="white")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        password_entry = ttk.Entry(login_frame, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        login_button = ttk.Button(login_frame, text="Iniciar Sesión", command=lambda: self.procesar_inicio_sesion(email_entry.get(), password_entry.get(), login_window))
        login_button.grid(row=2, columnspan=2, pady=10)

    def procesar_inicio_sesion(self, email, password, window):
        self.cursor.execute("SELECT * FROM usuarios WHERE email = ? AND password = ?", (email, password))
        usuario = self.cursor.fetchone()
        if usuario:
            messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {usuario[1]}!")
            window.destroy()
            self.abrir_mercado()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_mercado(self):
        self.root.destroy()
        os.system('python mercado.py')

def main():
    root = tk.Tk()
    app = PipoShopApp(root)

    # Centrar ventana
    center_window(root)

    root.mainloop()

def center_window(window):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x_coordinate = (screen_width - window_width) // 2
    y_coordinate = (screen_height - window_height) // 2
    window.geometry(f"+{x_coordinate}+{y_coordinate}")

if __name__ == "__main__":
    main()
