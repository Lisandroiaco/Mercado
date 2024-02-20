import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import string

class PipoShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PipoShop")
        self.root.configure(bg="white")

        # Conexión a la base de datos
        self.connection = sqlite3.connect("productos.db")
        self.cursor = self.connection.cursor()
        self.crear_tabla_productos()
        self.crear_tabla_mensajes()

        # Marco principal
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.pack(expand=True, fill="both")

        # Botón de búsqueda
        self.search_button = ttk.Button(self.main_frame, text="Buscar", command=self.buscar)
        self.search_button.pack(pady=10)

        # Cuadro de búsqueda
        self.search_entry = ttk.Entry(self.main_frame)
        self.search_entry.pack()

        # Resultados de búsqueda
        self.results_label = ttk.Label(self.main_frame, text="Resultados de búsqueda:", font=("Helvetica", 14), background="white")
        self.results_label.pack(pady=10)

        # Listado de productos
        self.product_listbox = tk.Listbox(self.main_frame, selectmode="single")
        self.product_listbox.pack(expand=True, fill="both")
        self.product_listbox.bind("<<ListboxSelect>>", self.mostrar_producto_seleccionado)

        # Botón de comprar
        self.buy_button = ttk.Button(self.main_frame, text="Comprar", command=self.comprar)
        self.buy_button.pack(pady=10)

        # Botón de chatear
        self.chat_button = ttk.Button(self.main_frame, text="Chatear", command=self.abrir_chat)
        self.chat_button.pack(pady=10)

        # Agregar objetos predeterminados
        self.agregar_objetos_predeterminados()

    def crear_tabla_productos(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                            id INTEGER PRIMARY KEY,
                            nombre TEXT NOT NULL,
                            precio REAL NOT NULL)''')
        self.connection.commit()

    def crear_tabla_mensajes(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mensajes (
                            id INTEGER PRIMARY KEY,
                            producto_id INTEGER NOT NULL,
                            mensaje TEXT NOT NULL,
                            FOREIGN KEY (producto_id) REFERENCES productos(id))''')
        self.connection.commit()

    def buscar(self):
        query = self.search_entry.get()
        self.product_listbox.delete(0, tk.END)  # Limpiar la lista de resultados antes de agregar nuevos elementos
        self.cursor.execute("SELECT id, nombre FROM productos WHERE nombre LIKE ?", ('%' + query + '%',))
        productos = self.cursor.fetchall()
        for producto in productos:
            self.product_listbox.insert(tk.END, producto[1])

    def mostrar_producto_seleccionado(self, event):
        seleccion = self.product_listbox.curselection()
        if seleccion:
            nombre_producto = self.product_listbox.get(seleccion[0])

    def comprar(self):
        seleccion = self.product_listbox.curselection()
        if seleccion:
            producto_id = self.cursor.execute("SELECT id FROM productos WHERE nombre=?", (self.product_listbox.get(seleccion[0]),)).fetchone()[0]
            messagebox.showinfo("Compra realizada", f"Has comprado el producto con ID {producto_id}")

    def abrir_chat(self):
        seleccion = self.product_listbox.curselection()
        if seleccion:
            producto_id = self.cursor.execute("SELECT id FROM productos WHERE nombre=?", (self.product_listbox.get(seleccion[0]),)).fetchone()[0]
            ChatWindow(self.root, producto_id, self.cursor, self.connection)

    def agregar_objetos_predeterminados(self):
        for _ in range(5):
            nombre = ''.join(random.choices(string.ascii_letters, k=10))
            precio = round(random.uniform(10, 1000), 2)
            self.cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
            self.connection.commit()

class ChatWindow:
    def __init__(self, root, producto_id, cursor, connection):
        self.root = root
        self.producto_id = producto_id
        self.cursor = cursor
        self.connection = connection

        # Ventana de chat
        self.chat_window = tk.Toplevel(root)
        self.chat_window.title("Chat con Vendedor")
        self.chat_window.geometry("400x600")

        # Lista de mensajes
        self.message_listbox = tk.Listbox(self.chat_window, bg="white", fg="black", height=25, width=60, font=("Arial", 12), selectmode="browse")
        self.message_listbox.pack(side="top", fill="both", expand=True)

        # Cuadro de entrada del mensaje
        self.message_entry = ttk.Entry(self.chat_window, font=("Arial", 12))
        self.message_entry.pack(side="left", fill="x", expand=True)

        # Botón de enviar mensaje
        self.send_button = ttk.Button(self.chat_window, text="Enviar", command=self.enviar_mensaje)
        self.send_button.pack(side="right")

        # Cargar mensajes anteriores
        self.cargar_mensajes_anteriores()

    def cargar_mensajes_anteriores(self):
        self.cursor.execute("SELECT mensaje FROM mensajes WHERE producto_id=?", (self.producto_id,))
        mensajes = self.cursor.fetchall()
        for mensaje in mensajes:
            self.message_listbox.insert(tk.END, mensaje[0])

    def enviar_mensaje(self):
        mensaje = self.message_entry.get()
        self.cursor.execute("INSERT INTO mensajes (producto_id, mensaje) VALUES (?, ?)", (self.producto_id, mensaje))
        self.connection.commit()
        self.message_entry.delete(0, tk.END)
        self.message_listbox.insert(tk.END, f"Yo: {mensaje}")

def main():
    root = tk.Tk()
    app = PipoShopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
