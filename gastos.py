from multiprocessing.connection import _ConnectionBase
from tkinter import *
import mysql.connector
import datetime
from tkinter import messagebox
from tkinter import ttk
import inicio

sesion_abierta = True
id_usuario = None

# ACLARACION: CAMBIAR LA PASSWORD DE LA BD #

class GastosApp:
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
        self.titulo = Label(self.miFrame, text="AÑADIR GASTOS", bg="#31C0E0", width=1000, height=1)
        self.titulo.config(pady=6, fg='white', font=("Arial", 12))
        self.titulo.pack(pady=20)
        # Estilo de button Verde
        ttk.Style().theme_use("clam")
        estilo_boton = ttk.Style()
        estilo_boton.configure("Custom.TButton", foreground="#15371B", font=("Helvetica", 11), padding=7)
        estilo_boton.map("Custom.TButton", background=[('!active', '#77EC8B'), ('active', '#4EC863')])
        # Estilo de button Volver
        estilo_boton_volver = ttk.Style()
        estilo_boton_volver.configure("Custom3.TButton", foreground="#15371B", font=("Helvetica", 11), padding=7)
        estilo_boton_volver.map("Custom3.TButton", background=[('!active', '#31C0E0'), ('active', '#3CBAD6')])
        # Etiqueta para mostrar el monto total
        self.monto_total_lbl = Label(self.miFrame, text=f"Monto Total: ${self.monto_total}", font=("Arial", 16), bg="#E7B9EA")
        self.monto_total_lbl.place(x=20, y=20)
        # Combobox categorías
        self.combo = ttk.Combobox(self.miFrame, state="readonly", values=["Seleccionar categoría", "alimentos", "indumentaria", "gimnasio","otro"])
        self.combo.set("Seleccionar categoría")
        self.combo.place(x=330, y=300)
        # Etiqueta y entry del monto
        self.monto_lbl = Label(self.miFrame, text="$", font=("Arial", 23), bg="#E7B9EA", width=1)
        self.monto_lbl.place(x=300, y=248)

        self.monto_entry = ttk.Entry(self.miFrame, style="TEntry", width=10)
        self.monto_entry.config(font=("Arial", 17))
        self.monto_entry.pack(pady=38)

        self.verificar_button = ttk.Button(self.miFrame, text="INGRESAR", style="Custom.TButton", command=self.ingresar_monto)
        self.verificar_button.place(x=345, y=358)

        self.boton_volver = ttk.Button(self.miFrame, text = "Volver", command = self.volver_a_inicio, style = "Custom3.TButton")
        self.boton_volver.place(x=90, y=200)

    def volver_a_inicio(self):
        ventana_inicio = inicio.InicioApp(self.root, self.id_usuario, self.db_connection)

    def ingresar_monto(self):
        monto_ingresado = self.monto_entry.get()
        tipo_movimiento = 2
        fecha_hora_actual = datetime.datetime.now()
        formato = "%Y-%m-%d %H:%M:%S"
        fecha_hora = fecha_hora_actual.strftime(formato)
    
        try:
            monto_ingresado = float(self.monto_entry.get())
            monto_ingresado = abs(monto_ingresado)
            tipo_categoria = self.combo.get()
            if tipo_categoria == "alimentos":
                tipo_categoria = 2
            elif tipo_categoria == "indumentaria":
                tipo_categoria = 3
            elif tipo_categoria == "gimnasio":
                tipo_categoria = 4
            elif tipo_categoria == "otro":
                tipo_categoria = 5
            else:
                messagebox.showerror("Error", "Por favor, seleccione una categoria valida.")
        
            # Guarda la transacción en la base de datos
            conn = mysql.connector.connect(host="localhost", user="root", password="xxxxx", database="misgastos_bd")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO movimientos (id_usuario, id_categoria, monto, fecha_hora, tipo_movimiento) VALUES (%s, %s, %s, %s, %s)", (self.id_usuario, tipo_categoria, monto_ingresado, fecha_hora, tipo_movimiento))

            # Actualiza el saldo total
            cursor.execute("UPDATE usuarios SET saldo_total = saldo_total - %s WHERE id_usuario = %s", (monto_ingresado, self.id_usuario))

            conn.commit()
            conn.close()

            self.monto_total -= monto_ingresado
            self.monto_total_lbl.config(text=f"Monto Total: ${self.monto_total}") # Muestra lo que se ingresa, no es el total
            self.monto_entry.delete(0, 'end') 

        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor numérico válido")

if __name__ == "__main__":
    root = Tk()
    usuario_actual_id = id_usuario
    app = GastosApp(root, id_usuario=usuario_actual_id, db_connection=_ConnectionBase)
    root.mainloop()