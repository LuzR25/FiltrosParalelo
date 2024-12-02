from pathlib import Path
import cv2
import numpy as np
from tkinter import Tk, filedialog, Button, Label, Frame, OptionMenu, StringVar, Canvas, Scrollbar
from PIL import Image, ImageTk
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import time
import os
import gc
import psutil

# Variables globales
images = []
original_img_labels = []
processed_img_labels = []
time_label = None
after_label = None
before_label=None
Speed_label=None
filters = ["Canny", "GaussianBlur", "Laplacian", "Sobel", "Mean", "Median"]
# Obtener el número de hilos basado en los núcleos de la CPU
num_workers = os.cpu_count()

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

    # Procesar imágenes en paralelo
    with ThreadPoolExecutor(max_workers=num_workers) as pool:
        results = list(pool.map(lambda img: procesar_imagen(img, filtro_seleccionado), images))

    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=1)  # Medir uso de CPU después de la ejecución
    tiempo_transcurrido = end_time - start_time
    speedup = cpu_after - cpu_before
    time_label.config(text=f"Tiempo de procesamiento: {tiempo_transcurrido:.2f} segundos, con {num_workers} hilos")
    

    before_label.config(text=f"Uso de CPU antes: {cpu_before} ")
    after_label.config(text=f"Uso de CPU después: {cpu_after} ")
    speed_label.config(text=f"Uso total de CPU: {speedup} ")

    # Mostrar las imágenes procesadas
    for idx, img in enumerate(results):
        mostrar_imagen(img, processed_img_labels, "Transformada", idx, 1)

    gc.collect()


# Función para procesar una imagen
def procesar_imagen(img, filtro):
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
        else:
            processed_img = img

        return processed_img
    except Exception as e:
        time_label.config(text=f"Error en el procesamiento: {e}")
        print(f"Error al procesar la imagen: {e}")
        return None  # Devolver None si ocurre un error


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

    def abrir_imagen(event):
        cv2.imshow(f"{tipo} {idx+1}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    label.bind("<Button-1>", abrir_imagen)
    labels.append(label)

    canvas_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

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

    speed_label = Label(root, text="Uso total estimado del CPU: 0%", font=("Arial", 12))
    speed_label.pack(pady=8)

    frame_controles = Frame(root)
    frame_controles.pack(pady=10)

    Button(frame_controles, text="Seleccionar imágenes", command=seleccionar_imagenes).pack(side="left", padx=5)

    filtro_var = StringVar(root)
    filtro_var.set(filters[0])
    OptionMenu(frame_controles, filtro_var, *filters).pack(side="left", padx=5)

    Button(frame_controles, text="Aplicar filtro", command=lambda: aplicar_filtro_paralelo()).pack(side="left", padx=5)

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