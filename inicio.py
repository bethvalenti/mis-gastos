from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import messagebox
import ingresos
import gastos
import movimientos

sesion_abierta = True
id_usuario = None

# ACLARACION: CAMBIAR LA PASSWORD DE LA BD #
class InicioApp:
    def __init__(self, root, id_usuario, db_connection):
        self.root = root
        self.id_usuario = id_usuario
        self.db_connection = db_connection  # Almacena la conexión a la base de datos
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
        # LOGO
        self.logo = PhotoImage(file="images/logo.png", format="png")
        self.logo = self.logo.subsample(5, 5)
        self.lbl_logo = Label(self.miFrame, image=self.logo, bg="#E7B9EA")
        self.lbl_logo.pack(pady=15)
        # Estilo de button Verde
        ttk.Style().theme_use("clam")
        estilo_boton = ttk.Style()
        estilo_boton.configure("Custom.TButton", foreground="#15371B", font=("Helvetica", 11), padding=7)
        estilo_boton.map("Custom.TButton", background=[('!active', '#8DDC9A'), ('active', '#6CD77E')])
        # Estilo button cerrar sesion
        estilo_boton_cerrarsesion = ttk.Style()
        estilo_boton_cerrarsesion.configure("Custom2.TButton", foreground="white", font=("Helvetica", 11), padding=7)
        estilo_boton_cerrarsesion.map("Custom2.TButton", background=[('!active', '#CA1024'), ('active', '#AE0A1B')])

        self.nombre_usuario = Label(self.miFrame, text = "hola, ", bg="#31C0E0", width = 1000, height = 1)
        self.nombre_usuario.config(pady = 6, fg = 'white', font = ("Arial",12))
        self.nombre_usuario.pack(pady = 20)

        # Etiqueta del monto
        self.monto_total_lbl = Label(self.miFrame, text="$", pady=12, padx=15, bg="#E7B9EA")
        self.monto_total_lbl.config(fg='black', font=("Arial", 30), cursor="hand2")
        self.monto_total_lbl.pack()
        self.monto_total_lbl.bind("<Enter>", self.mostrar_tooltip)
        self.monto_total_lbl.bind("<Leave>", self.ocultar_tooltip)
        self.monto_total_lbl.bind("<Button-1>", self.abrir_ventana_movimientos)  # Agregar evento clic
        # Frame contenedor de botones
        self.botones = Frame(self.miFrame, bg = "#E7B9EA", width = 600, height = 70)
        self.botones.pack(pady = 40)
        # BOTON Agregar Ingreso
        self.button_ingreso = ttk.Button(self.botones, text = "AGREGAR INGRESO", command = self.abrir_ventana_ingreso, style = "Custom.TButton")
        self.button_ingreso.place(x = 95, y = 2)
        # BOTON Agregar Gasto
        self.button_gasto = ttk.Button(self.botones, text = "AGREGAR GASTO", command = self.abrir_ventana_gasto, style = "Custom.TButton")
        self.button_gasto.place(x = 340, y = 2)
        # BOTON CERRAR SESION
        self.boton_cerrar_sesion = ttk.Button(self.miFrame, text = "Cerrar sesion", command = self.cerrar_sesion, style = "Custom2.TButton")
        self.boton_cerrar_sesion.pack(pady = 5)
         
        # Conectar a la base de datos y obtener el monto total
        conn = mysql.connector.connect(host="localhost", user="root", password="xxxxx", database="misgastos_bd")
        cursor = conn.cursor()
        # Verifica si ya hay un registro en la tabla
        cursor.execute("SELECT saldo_total FROM usuarios WHERE id_usuario = %s", (self.id_usuario,))
        row = cursor.fetchone()
        if row is None:
            # Valor inicial para saldo_total con el nombre de usuario actual
            saldo_total = 0.0
            usuario = self.nombre_usuario.cget("text")  # Utiliza el nombre de usuario almacenado en self.nombre_usuario
            cursor.execute("INSERT INTO usuarios (saldo_total, usuario) VALUES (%s, %s)", (saldo_total, usuario))
        conn.commit()
        # Obtener el monto total
        cursor.execute("SELECT saldo_total FROM usuarios WHERE id_usuario = %s", (self.id_usuario,))
        #saldo_total = cursor.fetchone()[0]
        row = cursor.fetchone()
        if row is not None:
            saldo_total = row[0]
        else:
            saldo_total = 0.0  # Otra acción por defecto en caso de que no haya datos
        self.monto_total_lbl.config(text=f"${saldo_total}")

        #Obtener nombre usuario
        cursor.execute("SELECT usuario FROM usuarios WHERE id_usuario = %s", (self.id_usuario,))
        result = cursor.fetchone()
        if result is not None:
            usuario = result[0]
            self.nombre_usuario.config(text=f"Hola, {usuario}, este es tu sueldo total:")

        # Cerrar la conexión
        conn.close()

    def abrir_ventana_ingreso(self):
        ventana_ingresos = ingresos.IngresosApp(self.root, self.id_usuario, self.db_connection)

    def abrir_ventana_gasto(self):
        ventana_gastos = gastos.GastosApp(self.root, self.id_usuario, self.db_connection)
        
    def abrir_ventana_movimientos(self, event):
        ventana_movimientos = movimientos.MovimientosApp(self.root, self.id_usuario, self.db_connection)
        
    def mostrar_tooltip(self, event):
        self.tooltip = Toplevel(self.root)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
        label = Label(self.tooltip, text="Ver movimientos", bg="lightyellow", relief="solid", borderwidth=1)
        label.pack()

    def ocultar_tooltip(self, event):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def cerrar_sesion(self):
        global id_usuario
        id_usuario = None
        self.root.destroy()
        
def abrir_ventana_inicio():
    global id_usuario, sesion_abierta
    if sesion_abierta:
        root = Tk()
        ventana_inicio = InicioApp(root, id_usuario)
        root.mainloop()
    else:
        messagebox.showerror("Error", "La sesión está cerrada. Inicie sesión para continuar.")

if __name__ == "__main__":
    abrir_ventana_inicio()
