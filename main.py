from tkinter import *
import mysql.connector
from tkinter import ttk
from tkinter import messagebox
import inicio
# Definir la conexión como una variable global
db_connection = None

# ACLARACION: CAMBIAR LA PASSWORD DE LA BD #
# Variable global para rastrear el estado de la sesión
sesion_abierta = False

class RegistroLoginApp:
    def __init__(self, root):
        self.root = root
        root.title("MIS GASTOS")
        root.geometry('1000x600')
        root.iconbitmap("images/icono.ico")
        # Fondo
        self.fondo = PhotoImage(file="images/fondorosa.png", format="png")
        self.lbl_fondo = Label(root, image=self.fondo, bg="#E7B9EA")
        self.lbl_fondo.place(relwidth=1, relheight=1)
        # Frame
        self.miFrame = Frame(root, width=1000, height=900, bg='#E7B9EA')
        self.miFrame.config(padx=150, pady=20)
        self.miFrame.place(x=260, y=60)
        # Logo
        self.logo = PhotoImage(file="images/logo.png", format="png")
        self.logo = self.logo.subsample(5, 5)
        self.lbl_logo = Label(self.miFrame, image=self.logo, bg="#E7B9EA")
        self.lbl_logo.pack(pady=15)
        # Estilo de entrys
        estilo = ttk.Style()
        estilo.configure("TEntry", padding=(5, 5, 5, 5))
        estilo.configure("TNotebook", background="black", fg="white")
        estilo.configure("TNotebook.Tab", background="black", foreground="black")
        # Estilo de button
        estilo_boton = ttk.Style()
        estilo_boton.configure("Custom.TButton", foreground="black", background="#BCA2C8", font=("Helvetica", 11), padding=7)

        # Variables de entrada
        self.usuario_var = StringVar()
        self.password_var = StringVar()

        # Interfaz de usuario
        self.etiqueta_usuario = Label(self.miFrame, text="Usuario:", bg='#E7B9EA', font=("Arial", 12))
        self.etiqueta_usuario.pack()
        self.entrada_usuario = ttk.Entry(self.miFrame, textvariable=self.usuario_var, font=14, style="TEntry")
        self.entrada_usuario.pack(pady=8)

        self.etiqueta_password = Label(self.miFrame, text="Password:", bg='#E7B9EA', font=("Arial", 12))
        self.etiqueta_password.pack()
        self.entrada_password = ttk.Entry(self.miFrame, textvariable=self.password_var, show="*", font=14, style="TEntry")
        self.entrada_password.pack(pady=8)

        self.boton_inicio_sesion = ttk.Button(self.miFrame, text="Iniciar Sesion", command=self.iniciar_sesion, style="Custom.TButton")
        self.boton_inicio_sesion.pack(pady=18)

        self.texto = Label(self.miFrame, text="O", bg="#E7B9EA")
        self.texto.pack()

        self.boton_registro = ttk.Button(self.miFrame, text="Registrarse", command=self.registrar_usuario, style="Custom.TButton")
        self.boton_registro.pack(pady=12)

    def registrar_usuario(self):
        usuario = self.usuario_var.get()
        password = self.password_var.get()

        if usuario and password:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="xxxxx", database="misgastos_bd")
                cursor = conn.cursor()

                # Verifica si el usuario ya existe
                cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s", (usuario,)) 
                existing_user = cursor.fetchone()

                if existing_user:
                    messagebox.showerror("Error de registro", "El usuario ya existe. Elija otro nombre de usuario.")
                else:
                    # Se realiza una insercion de un usuario nuevo
                    consulta_registro = "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)"
                    datos_registro = (usuario, password)
                    cursor.execute(consulta_registro, datos_registro)
                    id_usuario = cursor.lastrowid
                    conn.commit()
                    messagebox.showinfo("Registro exitoso", "Usuario registrado con éxito. Ya puede Iniciar sesión.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error de registro", "Ocurrió un error al registrar el usuario: {}".format(err))
            finally:
                conn.close()
        else:
            messagebox.showerror("Error de registro", "Por favor, complete todos los campos.")

    def iniciar_sesion(self):
        global sesion_abierta, id_usuario
        usuario = self.usuario_var.get()
        password = self.password_var.get()

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="xxxxx", database="misgastos_bd")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE usuario = %s AND password = %s", (usuario, password))
            usuario = cursor.fetchone()
            if usuario:
                sesion_abierta = True
                id_usuario = usuario[0]
                self.abrir_ventana_inicio()
            else:
                messagebox.showerror("Error", "Nombre de usuario o Password incorrectos.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error de inicio de sesión", "Ocurrió un error al iniciar sesión: {}".format(err))
        finally:
            conn.close()
    def obtener_id_usuario(self, usuario, password):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="xxxxx", database="misgastos_bd")
            cursor = conn.cursor()
        
            cursor.execute("SELECT id_usuario FROM usuarios WHERE usuario = %s AND password = %s", (usuario, password))
        
            result = cursor.fetchone()  # Obtiene el resultado de la consulta
        
            if result:
                id_usuario = result[0]
                return id_usuario
            else:
                return None  # No se encontró un usuario con ese usuario y contraseña

        except mysql.connector.Error as e:
            print(f"Error al obtener el ID de usuario: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def abrir_ventana_inicio(self):
        # Abre la ventana de inicio pasando la conexión a la base de datos
        ventana_inicio = inicio.InicioApp(root, id_usuario, db_connection)


if __name__ == "__main__":
    root = Tk()
    app = RegistroLoginApp(root)
    # Establecer la conexión a la base de datos
    db_connection = mysql.connector.connect(host="localhost", user="root", password="xxxxx", database="misgastos_bd")
    root.mainloop()
