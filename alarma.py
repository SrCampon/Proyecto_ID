import cv2
import numpy as np
import winsound
import time 

def deteccion_movimiento():

    # Parámetros de configuración
    area_min = 20000  # Área mínima para activar la alarma
    backSub = cv2.createBackgroundSubtractorKNN()
    camara = cv2.VideoCapture(0)

    # Verificar si la cámara está abierta
    if not camara.isOpened():
        print("No es posible abrir la cámara")
        exit()

    # Tiempo de inicio del programa
    inicio_programa = time.time()

    while True:
        ret, frame = camara.read()
        if not ret:
            print("No es posible obtener la imagen")
            break

        # Crear máscara de primer plano para detectar movimiento
        mascara_1er_plano = backSub.apply(frame)
        
        # Calcular el área blanca en la máscara
        area_blanca = np.sum(mascara_1er_plano == 255)

        # Obtener el tiempo transcurrido desde que comenzó el programa
        tiempo_transcurrido = time.time() - inicio_programa

        # Evitar que la alarma se active en los primeros 5 segundos
        if area_blanca > area_min and tiempo_transcurrido > 5:
            # Activar alarma de sonido
            winsound.Beep(1000, 500)

            # Crear un destello en rojo
            frame[:, :, 2] = 255  # Establece el canal rojo al máximo en todo el fotograma

            # Agregar texto en el centro de la imagen
            text = "MOVIMIENTO DETECTADO"
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_size = cv2.getTextSize(text, font, 1, 2)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            text_y = (frame.shape[0] + text_size[1]) // 2
            cv2.putText(frame, text, (text_x, text_y), font, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Encontrar contornos en la máscara de primer plano
            contornos, _ = cv2.findContours(mascara_1er_plano, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Dibujar rectángulos alrededor de los contornos detectados
            for contorno in contornos:
                if cv2.contourArea(contorno) > area_min:
                    # Obtener el rectángulo que rodea el contorno
                    x, y, w, h = cv2.boundingRect(contorno)
                    # Dibujar el rectángulo verde
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Mostrar el video en pantalla con los destellos y la máscara de primer plano
        cv2.imshow('webcam', frame)
        cv2.imshow('mascara 1er plano', mascara_1er_plano)

        # Salir del bucle si se presiona 'q'
        if cv2.waitKey(1) == ord('q'):
            break

    # Liberar recursos
    camara.release()
    cv2.destroyAllWindows()
