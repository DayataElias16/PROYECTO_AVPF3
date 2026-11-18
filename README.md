# Detector de power bank con Haar Cascade y OpenCV

**Avance de Proyecto Final 3 (AVPF-3) – Visión Computacional aplicada a Ingeniería Civil**
Universidad Tecnológica del Perú (UTP) – Piura
Autora: Elías Ramírez, Dáyata

Detector en tiempo real de un **power bank** usando un clasificador Haar Cascade entrenado con un dataset propio. Se ejecuta en Python con OpenCV y toma el video del celular mediante DroidCam.

## Contenido del repositorio

```
PowerBank_APF3/
├── APF3_EliasRamirez.py        # detector en tiempo real
├── cascade.xml                 # modelo entrenado (9 etapas)
├── entrenamiento/
│   ├── capturar_dataset.py     # script para capturar el dataset con DroidCam
│   ├── p/                      # 219 imágenes positivas
│   ├── n/                      # 172 imágenes negativas
│   ├── pos.lst, neg.lst        # listas generadas por Cascade Trainer GUI
│   └── classifier/             # etapas, parámetros y log del entrenamiento
└── capturas/                   # capturas de resultados (detecciones, falsos positivos, etc.)
```

## Dataset

Construido personalmente, sin datasets descargados.

| Tipo | Cantidad | Descripción |
|---|---|---|
| Positivas (`p/`) | 219 | Power bank dentro de un recuadro guía (100×50 px y 90×60 px), con distintos fondos, distancias, iluminación y con o sin mano |
| Negativas (`n/`) | 172 | Escenas de 320×180 px sin power bank: paredes, pisos, mesas, cajas, textiles, objetos oscuros y personas |

## Entrenamiento

Herramienta: **Cascade Trainer GUI 3.3.1**

| Parámetro | Valor |
|---|---|
| Característica | HAAR |
| Tamaño de muestra | 36×24 |
| Positivas usadas | 153 |
| Negativas por etapa | 1000 |
| Etapas solicitadas / completadas | 10 / 9 |

El entrenamiento terminó con el mensaje *Required leaf false alarm rate achieved* y generó `cascade.xml`.

## Requisitos

- Python 3.x
- OpenCV: `pip install opencv-python`
- App DroidCam en el celular (o una webcam), con el celular y la PC en la misma red Wi-Fi

## Uso

1. Abre DroidCam en el celular y revisa la IP que muestra.
2. En `APF3_EliasRamirez.py`, ajusta la IP en `FUENTE_POR_DEFECTO`. Con webcam usa `"0"`.
3. Ejecuta:

```
python APF3_EliasRamirez.py
```

Otras opciones:

```
python APF3_EliasRamirez.py --fuente 0                  # webcam de la PC
python APF3_EliasRamirez.py --carpeta imagenes_prueba/  # evalúa imágenes sueltas
```

**Teclas:** `q` salir, `s` guardar captura en `capturas/`.
**Deslizadores:** `vecinos` (más alto, menos falsos positivos) y `scale x10`.

## Resultados

- El detector marca un cuadro con la etiqueta «Power bank» cuando el objeto está cerca de la cámara y con buen contraste.
- Hay **falsos positivos** sobre texturas del fondo (piso, manta, madera).
- Hay **falsos negativos** cuando el power bank refleja luz o está muy girado.
- Los cuadros a veces incluyen la mano que sostiene el objeto.

## Limitaciones y mejoras

- Dataset pequeño para un clasificador Haar.
- Las primeras 100 positivas tienen proporción 2:1 y las demás 3:2, lo que deforma parte de las muestras al redimensionarlas a 36×24.
- Objeto negro y liso, con pocos contrastes que Haar pueda aprovechar.
- Mejoras: más imágenes, negativas con más texturas, recortes más ajustados, *hard negative mining*, más etapas y modelos modernos como YOLO.

## Aplicación en Ingeniería Civil

El mismo flujo sirve para detectar equipos de protección, contar materiales en almacén, localizar herramientas y apoyar la supervisión de obra, siempre entrenando con imágenes tomadas en condiciones reales de campo.
