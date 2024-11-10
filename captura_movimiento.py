import cv2
import numpy as np
import time
import os
from datetime import datetime

def captura_movimiento():
    
    # Carpeta para guardar capturas
    carpeta_grabaciones = os.path.join(os.getcwd(), "grabaciones")
    if not os.path.exists(carpeta_grabaciones):
        os.makedirs(carpeta_grabaciones)

    # Parámetros de configuración
    area_min = 10000  # Área mínima para activar la captura
    tiempo_espera_entre_capturas = 1
    backSub = cv2.createBackgroundSubtractorKNN()
    camara = cv2.VideoCapture(0)

    if not camara.isOpened():
        print("No es posible abrir la cámara")
        exit()

    # Tiempo del último guardado de imagen
    ultima_captura = time.time()

    while True:
        ret, frame = camara.read()
        if not ret:
            print("No es posible obtener la imagen")
            break

        # Crear máscara de primer plano para detectar movimiento
        mascara_1er_plano = backSub.apply(frame)
        
        # Calcular el área blanca en la máscara
        area_blanca = np.sum(mascara_1er_plano == 255)

        # Obtener el tiempo transcurrido desde la última captura
        tiempo_actual = time.time()
        tiempo_desde_ultima_captura = tiempo_actual - ultima_captura

        # Verificar si el área blanca es mayor al umbral
        if area_blanca > area_min:
            # Dibujar texto en la parte superior de la imagen
            fecha_hora_muestra = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(fecha_hora_muestra, font, 0.8, 2)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = 30
            cv2.putText(frame, fecha_hora_muestra, (text_x, text_y), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

            # Encontrar contornos y dibujar rectángulos alrededor del movimiento detectado
            contornos, _ = cv2.findContours(mascara_1er_plano, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contorno in contornos:
                if cv2.contourArea(contorno) > area_min:
                    x, y, w, h = cv2.boundingRect(contorno)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Guardar la imagen si ha pasado el tiempo de espera
            if tiempo_desde_ultima_captura > tiempo_espera_entre_capturas:
                nombre_archivo = os.path.join(carpeta_grabaciones, f"captura_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg")
                cv2.imwrite(nombre_archivo, frame)
                ultima_captura = tiempo_actual
                print(f"Imagen guardada como {nombre_archivo}")

        # Mostrar el video en pantalla con los destellos y la máscara de primer plano
        cv2.imshow('webcam', frame)
        cv2.imshow('mascara 1er plano', mascara_1er_plano)

        # Salir del bucle si se presiona 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    # Liberar recursos
    camara.release()
    cv2.destroyAllWindows()
