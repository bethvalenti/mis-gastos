from multiprocessing.connection import _ConnectionBase
from tkinter import *
import mysql.connector
import datetime
from tkinter import messagebox
from tkinter import ttk
import inicio

sesion_abierta = True
id_usuario = None


class MovimientosApp:
    def __init__(self, root, id_usuario, db_connection):
        self.root = root
        self.id_usuario = id_usuario
        self.db_connection = db_connection  # Almacena la conexión a la base de datos
        self.monto_total = 0  
        root.title("MIS GASTOS")
        root.geometry('1000x600')
        root.iconbitmap("images/icono.ico")
        # Fondo
        self.fondo = PhotoImage(file="images/fondorosa.png", format="png")
        self.lbl_fondo = Label(root, image=self.fondo, bg="#E7B9EA")
        self.lbl_fondo.place(relwidth=1, relheight=1)
        # Frame
        self.miFrame = Frame(root, bg='#E7B9EA')
        self.miFrame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        # Logo
        self.logo = PhotoImage(file="images/logo.png", format="png")
        self.logo = self.logo.subsample(5, 5)
        self.lbl_logo = Label(self.miFrame, image=self.logo, bg="#E7B9EA")
        self.lbl_logo.pack(pady=15)
        # Título
        self.titulo = Label(self.miFrame, text="MOVIMIENTOS", bg="#31C0E0", width=1000, height=1)
        self.titulo.config(pady=6, fg='white', font=("Arial", 12))
        self.titulo.pack(pady=20)
        # Estilo de button Volver
        estilo_boton_volver = ttk.Style()
        estilo_boton_volver.configure("Custom3.TButton", foreground="#15371B", font=("Helvetica", 11), padding=7)
        estilo_boton_volver.map("Custom3.TButton", background=[('!active', '#31C0E0'), ('active', '#3CBAD6')])

        self.boton_volver = ttk.Button(self.miFrame, text = "Volver", command = self.volver_a_inicio, style = "Custom3.TButton")
        self.boton_volver.place(x=40, y=200)
        # Estilo personalizado para el encabezado
        style = ttk.Style()
        style.configure("Treeview.Heading", background="light blue", font=("Arial", 12))

        self.tree = ttk.Treeview(self.miFrame, columns=("Fecha y Hora", "Monto", "Categoría"), show="headings")
        self.tree.heading("Fecha y Hora", text="Fecha y Hora")
        self.tree.heading("Monto", text="Monto")
        self.tree.heading("Categoría", text="Categoría")

        self.tree.column("Fecha y Hora", width=140)
        self.tree.column("Monto", width=100)
        self.tree.column("Categoría", width=140)
        self.tree.pack(pady=20, padx=20)

        # Crea un scrollbar vertical
        scrollbar = Scrollbar(self.miFrame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.place(x=600, y=240, height=200)

        self.tree.configure(yscrollcommand=scrollbar.set)

        # Carga movimientos en el Treeview
        self.cargar_movimientos()
        

    def volver_a_inicio(self):
        ventana_inicio = inicio.InicioApp(self.root, self.id_usuario, self.db_connection)


    def cargar_movimientos(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="xxxxx", database="misgastos_bd")
            cursor = conn.cursor()

            # Consulta para obtener los movimientos del usuario actual, incluyendo la descripción de la categoría
            cursor.execute("SELECT m.fecha_hora, m.monto, m.tipo_movimiento, c.descripcion FROM movimientos AS m JOIN categoria AS c ON m.id_categoria = c.id_categoria WHERE m.id_usuario = %s ORDER BY fecha_hora DESC", (self.id_usuario,))
            movimientos = cursor.fetchall()

            # Borra los elementos anteriores del Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            for movimiento in movimientos:
                fecha_hora, monto, tipo_movimiento, categoria = movimiento
                signo = "+" if tipo_movimiento == 1 else "-"
                self.tree.insert("", "end", values=(fecha_hora, f"{signo} $ {monto}", categoria))
                
            cursor.close()

        except mysql.connector.Error as e:
            print(f"Error al cargar los movimientos: {e}")

if __name__ == "__main__":
    root = Tk()
    usuario_actual_id = id_usuario
    app = MovimientosApp(root, id_usuario=usuario_actual_id, db_connection=_ConnectionBase)
    root.mainloop()