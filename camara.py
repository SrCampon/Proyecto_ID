import cv2
from threading import Thread

class Camara:
    def __init__(self):
        self.cap = None
        self.running = False

    def iniciar_camara(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        thread = Thread(target=self.mostrar_video)
        thread.start()

    def mostrar_video(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imshow("Videovigilancia en Vivo", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.detener_camara()
            else:
                break

    def detener_camara(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
