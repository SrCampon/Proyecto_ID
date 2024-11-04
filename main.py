import cv2
import datetime

# Inicializar la captura de video
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
ret, frame2 = cap.read()

# Configurar el codec y el archivo de salida
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None
recording = False

while cap.isOpened():
    # Calcular la diferencia entre frames consecutivos
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Verificar si se detecta movimiento
    for contour in contours:
        if cv2.contourArea(contour) < 5000:  # Ajusta el umbral según tus necesidades
            continue
        if not recording:
            # Iniciar la grabación
            recording = True
            filename = f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
            out = cv2.VideoWriter(filename, fourcc, 20.0, (frame1.shape[1], frame1.shape[0]))
        
        # Dibujar un rectángulo alrededor del movimiento detectado
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if recording:
        out.write(frame1)
        if len(contours) == 0:
            # Si no hay movimiento, detener la grabación
            recording = False
            out.release()

    # Mostrar el frame procesado
    cv2.imshow('Motion Detection', frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    # Salir al presionar 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if out is not None and out.isOpened():
    out.release()
cv2.destroyAllWindows()
