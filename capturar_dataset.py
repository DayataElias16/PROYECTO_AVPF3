"""
Captura del dataset - APF3 (detector de POWER BANK)

Teclas:
    p -> guarda POSITIVA (solo lo que está dentro del recuadro azul)
    n -> guarda NEGATIVA (toda la escena, SIN power bank)
    q -> salir

Las carpetas 'p' y 'n' se crean en la carpeta desde donde ejecutes el script.
Si ya tienen imágenes, continúa la numeración sin borrar nada.
"""

import os

import cv2


FUENTE = "http://10.255.199.62:4747/video"   # IP que muestra DroidCam (o 0 para webcam)
ANCHO, ALTO = 90, 60                        # tamaño final de cada positiva (proporción 2:1)
FRACCION_RECUADRO = 0.5                      # ancho del recuadro respecto al ancho de la imagen


os.makedirs("p", exist_ok=True)
os.makedirs("n", exist_ok=True)

cap = cv2.VideoCapture(FUENTE)
if not cap.isOpened():
    raise SystemExit("No se pudo abrir la cámara. Revisa la IP de DroidCam y que el celular y la PC estén en el mismo Wi-Fi.")

count_p = len(os.listdir("p"))
count_n = len(os.listdir("n"))

print("p = POSITIVA (power bank dentro del recuadro azul)")
print("n = NEGATIVA (escena SIN power bank)")
print("q = salir")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    bw = int(w * FRACCION_RECUADRO)
    bh = int(bw * ALTO / ANCHO)              # mismo aspecto que la imagen final: no se deforma
    x1, y1 = (w - bw) // 2, (h - bh) // 2
    x2, y2 = x1 + bw, y1 + bh

    limpio = frame.copy()                    # copia sin dibujos para guardar
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(frame, f"Pos: {count_p} | Neg: {count_n}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Captura dataset - Power bank", frame)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord("p"):
        recorte = cv2.resize(limpio[y1:y2, x1:x2], (ANCHO, ALTO))
        cv2.imwrite(f"p/powerbank_{count_p:03d}.jpg", recorte)
        count_p += 1
    elif tecla == ord("n"):
        escena = cv2.resize(limpio, (320, int(320 * h / w)))
        cv2.imwrite(f"n/fondo_{count_n:03d}.jpg", escena)
        count_n += 1
    elif tecla == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
