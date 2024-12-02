from pathlib import Path
import cv2
import numpy as np
from tkinter import Tk, filedialog, Button, Label, Frame, OptionMenu, StringVar, Canvas, Scrollbar,Toplevel
from PIL import Image, ImageTk
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import time
import os
import gc
import psutil
import pyautogui

# Variables globales
images = []
original_img_labels = []
processed_img_labels = []
time_label = None
after_label = None
before_label=None
Speed_label=None
filters = ["Canny", "GaussianBlur", "Laplacian", "Sobel", "Mean", "Median","UnsharpMask","Rotate","SobelWithOrientation"]
# Obtener el número de hilos basado en los núcleos de la CPU
num_workers = 2

# Función para cargar y decodificar una imagen
def cargar_imagen(filepath):
    try:
        img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            return img
    except Exception as e:
        time_label.config(text=f"Error al leer la imagen {filepath}: {e}")
        print(f"Error al leer la imagen {filepath}: {e}")
    return None


# Función para seleccionar imágenes en paralelo
def seleccionar_imagenes():
    global images, original_img_labels, processed_img_labels

    # Seleccionar rutas y normalizarlas
    filepaths = [os.path.normpath(fp) for fp in filedialog.askopenfilenames(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])]

    if not filepaths:
        return

    # Paralelizar la carga de imágenes
    with ThreadPoolExecutor(max_workers=num_workers) as pool:
        images = [img for img in pool.map(cargar_imagen, filepaths) if img is not None]

    # Limpiar imágenes y etiquetas anteriores
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    original_img_labels.clear()
    processed_img_labels.clear()

    time_label.config(text="")

    # Mostrar las imágenes originales
    for idx, img in enumerate(images):
        mostrar_imagen(img, original_img_labels, "Original", idx, 0)


# Función para aplicar filtros en paralelo
def aplicar_filtro_paralelo():
    global images, processed_img_labels, time_label

    if not images:
        time_label.config(text=f"Selecciona las imágenes primero")
        return

    cpu_before = psutil.cpu_percent(interval=1)  # Medir uso antes de la ejecución
    start_time = time.time()
    filtro_seleccionado = filtro_var.get()
    batch_size = 10  # Número de imágenes por lote
    results = []
    # Procesar imágenes en paralelo
    with ThreadPoolExecutor(max_workers=num_workers) as pool:  # Usamos ProcessPoolExecutor
        # Procesar por lotes
        for i in range(0, len(images), batch_size):
            lote = images[i:i+batch_size]
            resultados_lote = list(pool.map(lambda img: procesar_imagen(img, filtro_seleccionado), lote))
            results.extend(resultados_lote)

    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=1)  # Medir uso de CPU después de la ejecución
    tiempo_transcurrido = end_time - start_time
    speedup =  cpu_after - cpu_before 
    time_label.config(text=f"Tiempo de procesamiento: {tiempo_transcurrido:.2f} segundos, con {num_workers} hilos")
    

    before_label.config(text=f"Uso de CPU antes: {cpu_before} ")
    after_label.config(text=f"Uso de CPU después: {cpu_after} ")
    speed_label.config(text=f"Diferencia en CPU: {speedup} ")

    # Mostrar las imágenes procesadas
    for idx, img in enumerate(results):
        mostrar_imagen(img, processed_img_labels, "Transformada", idx, 1)

    gc.collect()

# Filtro de Enfoque (Unsharp Mask)
def unsharp_mask(img, sigma=2.0, strength=2.5):
    blurred = cv2.GaussianBlur(img, (5, 5), sigma)
    sharpened = cv2.addWeighted(img, 1 + strength, blurred, -strength, 0)
    return sharpened

# Transformaciones Geométricas: Rotación, Escalado y Recorte
def rotar_imagen(img, angulo):
    (h, w) = img.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h))
    return rotated


# Filtro Sobel con orientación
def sobel_con_orientacion(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    magnitud = cv2.magnitude(sobel_x, sobel_y)
    direccion = cv2.phase(sobel_x, sobel_y, angleInDegrees=True)
    sobel_edges = cv2.convertScaleAbs(magnitud)
    return sobel_edges, direccion

# Función para procesar una imagen
def procesar_imagen(img, filtro, angulo=0, escala=1.0, x=0, y=0, w=100, h=100):
    try:
        if filtro == "Canny":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            processed_img = cv2.Canny(gray_img, 100, 200)
        elif filtro == "GaussianBlur":
            processed_img = cv2.GaussianBlur(img, (21, 21), 0)
        elif filtro == "Laplacian":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray_img, cv2.CV_64F)
            processed_img = cv2.convertScaleAbs(laplacian)
        elif filtro == "Sobel":
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
            processed_img = cv2.magnitude(sobel_x, sobel_y)
            processed_img = cv2.convertScaleAbs(processed_img)
        elif filtro == "Mean":
            processed_img = cv2.blur(img, (21, 21))
        elif filtro == "Median":
            processed_img = cv2.medianBlur(img, 21)
        elif filtro == "UnsharpMask":
            processed_img = unsharp_mask(img)
        elif filtro == "Rotate":
            processed_img = rotar_imagen(img, 50)
        elif filtro == "SobelWithOrientation":
            processed_img, _ = sobel_con_orientacion(img)
        else:
            processed_img = img

        return processed_img
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
        return None  # Devolver None si ocurre un error

# Carpeta de destino para guardar las imágenes procesadas
def seleccionar_carpeta_destino():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta de destino")
    return carpeta



# Función para guardar la imagen procesada
def guardar_imagen(img, nombre_archivo="imagen_procesada", formato="jpg"):
    try:
        carpeta_destino = seleccionar_carpeta_destino()
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        ruta_archivo = os.path.join(carpeta_destino, f"{nombre_archivo}.{formato}")
        cv2.imwrite(ruta_archivo, img)
        print(f"Imagen guardada en: {ruta_archivo}")
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")


# Función para mostrar una imagen en la interfaz gráfica
def mostrar_imagen(img, labels, tipo, idx=None, columna=0):
    img_resized = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img_resized.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(img_resized)

    label = Label(canvas_frame, image=img_tk)
    label.image = img_tk
    label.grid(row=2*idx, column=columna, padx=10, pady=10)

    texto = Label(canvas_frame, text=f"{tipo} {idx+1}", font=("Arial", 12))
    texto.grid(row=2*idx + 1, column=columna, pady=5)

    # Función para abrir y visualizar una imagen procesada
    def abrir_imagen(event):
        try:
            #img, tipo, idx
            # Obtener las dimensiones de la pantalla
            screen_width, screen_height = pyautogui.size()

            # Obtener las dimensiones de la imagen
            img_height, img_width = img.shape[:2]

            # Calcular el factor de escala (asegurándonos de que no exceda el tamaño de la pantalla)
            scale_factor = min(screen_width / img_width, screen_height / img_height, 1)

            # Redimensionar la imagen proporcionalmente
            new_width = int(img_width * scale_factor) - 100
            new_height = int(img_height * scale_factor) - 100
            resized_img = cv2.resize(img, (new_width, new_height))

            # Mostrar la imagen redimensionada
            cv2.imshow(f"{tipo} {idx+1}", resized_img)

            key = cv2.waitKey(0)
            if key == ord('g'):  # Presionar 'g' para guardar
                guardar_imagen(img, nombre_archivo=f"{tipo}_{idx+1}")

            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error al abrir la imagen: {e}")

    label.bind("<Button-1>", abrir_imagen)
    labels.append(label)

    canvas_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Agregar un botón "Más" para abrir una pestaña con información del programa
def mostrar_info():
    info_window = Toplevel(root)
    info_window.title("Información del programa")
    info_window.geometry("800x300")

    Label(info_window, text="Procesamiento de Imágenes Paralelo", font=("Arial", 16)).pack(pady=10)
    Label(info_window, text=(
        "Este programa aplica filtros de procesamiento de imágenes en paralelo.\n"
        "Características principales:\n"
        "- Carga de imágenes en paralelo.\n"
        "- Aplicación de filtros como Canny, Sobel, GaussianBlur, etc.\n"
        "- Medición del uso de CPU y tiempo de procesamiento.\n"
        "- Puedes observar mejor una imagen dando clic sobre ella.\n"
        "- Para guardar imágenes puedes presionar la tecla 'g'."
    ), font=("Arial", 12), justify="left").pack(pady=10)

    Button(info_window, text="Cerrar", command=info_window.destroy).pack(pady=10)

# Configuración de la interfaz gráfica
def configurar_interfaz():
    global time_label, filtro_var, canvas, canvas_frame, before_label, after_label, speed_label

    root = Tk()
    root.title("Procesamiento de Imágenes Paralelo")

    # Establecer las dimensiones mínimas de la ventana
    root.minsize(500, 800)  # Establece el tamaño mínimo a 800x600 píxeles

    time_label = Label(root, text="", font=("Arial", 12))
    time_label.pack(pady=5)

    before_label = Label(root, text="Uso de CPU antes: 0%", font=("Arial", 12))
    before_label.pack(pady=6)

    after_label = Label(root, text="Uso de CPU después 0%:", font=("Arial", 12))
    after_label.pack(pady=7)

    speed_label = Label(root, text="Diferencia en CPU: 0%", font=("Arial", 12))
    speed_label.pack(pady=8)

    frame_controles = Frame(root)
    frame_controles.pack(pady=10)

    Button(frame_controles, text="Seleccionar imágenes", command=seleccionar_imagenes).pack(side="left", padx=5)

    filtro_var = StringVar(root)
    filtro_var.set(filters[0])
    OptionMenu(frame_controles, filtro_var, *filters).pack(side="left", padx=5)

    Button(frame_controles, text="Aplicar filtro", command=lambda: aplicar_filtro_paralelo()).pack(side="left", padx=5)

    Button(frame_controles, text="Más", command=mostrar_info).pack(side="left", padx=5)

    canvas = Canvas(root)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvas_frame = Frame(canvas)
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    return root


# Ejecutar la interfaz
if __name__ == '__main__':
    root = configurar_interfaz()
    root.mainloop()