"""
APF3 - Visión Computacional aplicada a Ingeniería Civil
Detector de POWER BANK con Haar Cascade (OpenCV)

Autor: Elías Ramírez, Dáyata
Universidad Tecnológica del Perú (UTP) - Piura

Uso:
    Ejecutar con F5 en IDLE o con:  python APF3_EliasRamirez.py
    Por defecto usa la cámara del celular (DroidCam).

Teclas:
    q -> salir
    s -> guardar captura en la carpeta 'capturas'
Deslizadores de la ventana:
    vecinos   -> más alto = menos falsos positivos
    scale x10 -> factor de escala x10 (12 = 1.2)
"""

import argparse
import os
import time

import cv2


FUENTE_POR_DEFECTO = "http://10.255.199.62:4747/video"   # IP de DroidCam
ETIQUETA = "Power bank"
TAM_MIN = (36, 24)      # tamaño mínimo de detección (igual al de muestra del entrenamiento)
COLOR = (0, 200, 0)     # BGR (verde)
# -----------------------------------------------


def cargar_modelo(ruta_xml):
    """Carga el clasificador en cascada generado con Cascade Trainer GUI."""
    clasificador = cv2.CascadeClassifier(ruta_xml)
    if clasificador.empty():
        raise FileNotFoundError(f"No se pudo cargar el modelo: {ruta_xml}")
    return clasificador


def detectar(clasificador, frame, scale=1.2, vecinos=5):
    """Devuelve los rectángulos (x, y, w, h) donde se detecta el objeto."""
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gris = cv2.equalizeHist(gris)   # reduce el efecto de la iluminación
    return clasificador.detectMultiScale(
        gris, scaleFactor=scale, minNeighbors=vecinos, minSize=TAM_MIN
    )


def dibujar(frame, cajas):
    """Dibuja rectángulo y etiqueta sobre cada detección."""
    for (x, y, w, h) in cajas:
        cv2.rectangle(frame, (x, y), (x + w, y + h), COLOR, 2)
        (tw, th), _ = cv2.getTextSize(ETIQUETA, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(frame, (x, y - th - 10), (x + tw + 6, y), COLOR, -1)
        cv2.putText(frame, ETIQUETA, (x + 3, y - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    return frame


def modo_tiempo_real(clasificador, fuente, args):
    """Detección en vivo con DroidCam o webcam."""
    if isinstance(fuente, str) and fuente.isdigit():
        fuente = int(fuente)
    cap = cv2.VideoCapture(fuente)
    if not cap.isOpened():
        raise RuntimeError(f"No se pudo abrir la fuente de video: {fuente}")

    os.makedirs("capturas", exist_ok=True)
    ventana = "APF3 - Detector de power bank"
    cv2.namedWindow(ventana)
    cv2.createTrackbar("vecinos", ventana, args.vecinos, 40, lambda x: None)
    cv2.createTrackbar("scale x10", ventana, int(args.scale * 10), 15, lambda x: None)

    t_prev = time.time()
    n_capt = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        vec = max(1, cv2.getTrackbarPos("vecinos", ventana))
        sc = max(11, cv2.getTrackbarPos("scale x10", ventana)) / 10
        cajas = detectar(clasificador, frame, sc, vec)
        frame = dibujar(frame, cajas)

        t_now = time.time()
        fps = 1.0 / max(t_now - t_prev, 1e-6)
        t_prev = t_now
        cv2.putText(frame, f"FPS: {fps:.1f}  Detecciones: {len(cajas)}", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow(ventana, frame)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord("q"):
            break
        if tecla == ord("s"):
            n_capt += 1
            ruta = os.path.join("capturas", f"captura_{n_capt:03d}.jpg")
            cv2.imwrite(ruta, frame)
            print("Captura guardada:", ruta)

    cap.release()
    cv2.destroyAllWindows()


def modo_carpeta(clasificador, carpeta, args):
    """Procesa imágenes de prueba y guarda los resultados para el análisis
    (aciertos, falsos positivos y falsos negativos se anotan a mano en el informe)."""
    salida = "resultados"
    os.makedirs(salida, exist_ok=True)
    extensiones = (".jpg", ".jpeg", ".png", ".bmp")
    archivos = sorted(f for f in os.listdir(carpeta) if f.lower().endswith(extensiones))

    print(f"{'imagen':40s} detecciones")
    for nombre in archivos:
        img = cv2.imread(os.path.join(carpeta, nombre))
        if img is None:
            continue
        cajas = detectar(clasificador, img, args.scale, args.vecinos)
        cv2.imwrite(os.path.join(salida, nombre), dibujar(img, cajas))
        print(f"{nombre:40s} {len(cajas)}")
    print(f"\nImágenes con resultados guardadas en '{salida}/'")


def main():
    ap = argparse.ArgumentParser(description="Detector de power bank (Haar Cascade)")
    ap.add_argument("--modelo", default="cascade.xml", help="ruta del cascade.xml")
    ap.add_argument("--fuente", default=FUENTE_POR_DEFECTO, help="índice de cámara o URL de DroidCam")
    ap.add_argument("--carpeta", help="carpeta con imágenes de prueba (modo evaluación)")
    ap.add_argument("--scale", type=float, default=1.2, help="scaleFactor de detectMultiScale")
    ap.add_argument("--vecinos", type=int, default=5, help="minNeighbors (más alto = menos falsos positivos)")
    args = ap.parse_args()

    clasificador = cargar_modelo(args.modelo)
    if args.carpeta:
        modo_carpeta(clasificador, args.carpeta, args)
    else:
        modo_tiempo_real(clasificador, args.fuente, args)


if __name__ == "__main__":
    main()
