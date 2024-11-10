import tkinter as tk
from PIL import Image, ImageTk
import os, subprocess
import threading
from alarma import deteccion_movimiento
from captura_movimiento import captura_movimiento


#--------- FUNCIONALIDADES APLICACIÓN ------------------------------------------------

def activar_alarma():
    # Crear un hilo para ejecutar el código de la alarma sin bloquear la GUI
    threading.Thread(target=deteccion_movimiento).start()

def captar_movimientos():
    print("Captando movimientos")
    threading.Thread(target=captura_movimiento).start()


def mostrar_grabaciones():
    carpeta_grabaciones = os.path.join(os.getcwd(), "grabaciones")  # Ruta de la carpeta
    os.startfile(carpeta_grabaciones) # Abrir la carpeta en el explorador de archivos


#-------- INTERFAZ GRÁFICA DE USUARIO (GUI) ------------------------------------------

# Crear la ventana de inicio
ventana = tk.Tk()
ventana.title("InstaWatch")
ventana.geometry("400x300")

# Cargar y redimensionar la imagen de fondo
imagen_fondo = Image.open("recursos/rec.png")  
imagen_fondo_resized = imagen_fondo.resize((400, 300))  
imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo_resized) 

# Colocar la imagen de fondo en un Label que ocupe toda la ventana
label_fondo = tk.Label(ventana, image=imagen_fondo_tk)
label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

# Cargar y redimensionar la imagen del ícono
imagen_icono = Image.open("recursos/camara_seguridad.png")
imagen_icono_resized = imagen_icono.resize((60, 60))
imagen_logo = ImageTk.PhotoImage(imagen_icono_resized)

# Colocar el ícono encima del botón
label_imagen = tk.Label(ventana, image=imagen_logo)  
label_imagen.pack(pady=30)

# Crear el botón "Iniciar videovigilancia"
boton_iniciar = tk.Button(ventana, text="Activar Alarma", font=("Arial", 14), command=activar_alarma)
boton_iniciar.pack(pady=5)

# Crear el botón "activar alarma"
boton_iniciar = tk.Button(ventana, text="Captar Movimientos", font=("Arial", 14), command=captar_movimientos)
boton_iniciar.pack(pady=5)

# Crear el botón para visualizar las grabaciones realizadas
boton_grabaciones = tk.Button(ventana, text="Ver capturas", font=("Arial", 14), command=mostrar_grabaciones)
boton_grabaciones.pack(pady=5)

# Traer los elementos al frente para que se vean sobre el fondo
label_imagen.lift()
boton_iniciar.lift()
boton_grabaciones.lift()

# Ejecutar la aplicación
ventana.mainloop()
