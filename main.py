import tkinter as tk
from PIL import Image, ImageTk
import os
import subprocess
from camara import Camara  # Importamos la clase Camara para manejar la cámara

# Función que se ejecuta al presionar el botón de iniciar videovigilancia
def iniciar_videovigilancia():
    print("Videovigilancia iniciada")
    # Crear una instancia de la clase Camara y llamar a su método para iniciar la cámara
    camara = Camara()  # Instanciar la cámara
    camara.iniciar_camara()  # Iniciar la cámara

# Función para abrir la carpeta de grabaciones
def mostrar_grabaciones():
    carpeta_grabaciones = os.path.join(os.getcwd(), "grabaciones")  # Ruta de la carpeta
    if not os.path.exists(carpeta_grabaciones):
        os.makedirs(carpeta_grabaciones)  # Crear la carpeta si no existe
    # Abrir la carpeta en el explorador de archivos
    if os.name == 'nt':  # Windows
        os.startfile(carpeta_grabaciones)
    elif os.name == 'posix':  # macOS o Linux
        subprocess.call(["open" if os.uname().sysname == "Darwin" else "xdg-open", carpeta_grabaciones])

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("InstaWatch")
ventana.geometry("400x300")  # Tamaño de la ventana

# Cargar y redimensionar la imagen de fondo
imagen_fondo = Image.open("recursos/rec.png")  # Cambia "fondo.png" por la ruta de tu imagen de fondo
imagen_fondo_resized = imagen_fondo.resize((400, 300))  # Ajustar el tamaño de la imagen al tamaño de la ventana
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo_resized)  # Convertir para tkinter

# Colocar la imagen de fondo en un Label que ocupe toda la ventana
label_fondo = tk.Label(ventana, image=imagen_fondo_tk)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Hacer que el fondo cubra toda la ventana

# Cargar y redimensionar la imagen del ícono
imagen_icono = Image.open("recursos/camara_seguridad.png")  # Cambia "camara_seguridad.png" por la ruta de tu imagen
imagen_icono_resized = imagen_icono.resize((60, 60))  # Redimensiona la imagen del ícono
imagen_logo = ImageTk.PhotoImage(imagen_icono_resized)

# Colocar el ícono encima del botón
label_imagen = tk.Label(ventana, image=imagen_logo)  # Agregar fondo blanco o transparente si se necesita
label_imagen.pack(pady=30)

# Crear el botón "Iniciar videovigilancia"
boton_iniciar = tk.Button(ventana, text="Iniciar Videovigilancia", font=("Arial", 14), command=iniciar_videovigilancia)
boton_iniciar.pack(pady=20)

# Crear el botón para visualizar las grabaciones realizadas
boton_grabaciones = tk.Button(ventana, text="Ver grabaciones", font=("Arial", 14), command=mostrar_grabaciones)
boton_grabaciones.pack(pady=10)

# Traer los elementos al frente para que se vean sobre el fondo
label_imagen.lift()
boton_iniciar.lift()
boton_grabaciones.lift()

# Ejecutar la aplicación
ventana.mainloop()
