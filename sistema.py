import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import tkinter as tk
from tkinter import ttk

# Cargar el CSV de productos
df = pd.read_csv('productos.csv')

# Asegurarse de que la columna 'descripcion' no tenga valores nulos
df = df.dropna(subset=['descripcion'])

# Lista de stopwords en español
stopwords_es = ["de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un", "para", "con", "no", "una", "su", "al", "es", "lo", "como", "más", "pero", "sus"]

# Crear una matriz TF-IDF para las descripciones de los productos
vectorizer = TfidfVectorizer(stop_words=stopwords_es)
tfidf_matrix = vectorizer.fit_transform(df['descripcion'])

# Calcular la similitud de coseno entre las descripciones de los productos
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Función para obtener recomendaciones basadas en contenido con porcentaje de similitud
def get_product_recommendations(product_id, cosine_similarities=cosine_similarities):
    # Obtener las similitudes de coseno para el producto en cuestión
    sim_scores = list(enumerate(cosine_similarities[product_id]))

    # Ordenar los productos por similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Imprimir el producto del cual se están haciendo las recomendaciones
    print(f'Recomendaciones para el producto con ID {product_id}\n')

    # Obtener las recomendaciones con porcentaje de similitud
    recommendations = []
    for i in sim_scores[1:6]:  # Tomar los 5 productos más similares
        similar_product_id = i[0]
        similar_product = df['producto'].iloc[similar_product_id]
        similar_product_price = df['precio'].iloc[similar_product_id]
        similarity_percentage = i[1] * 100  # Convertir a porcentaje
        recommendations.append((similar_product_id, similar_product, similar_product_price, similarity_percentage))

    return recommendations

# Funciones de los botones
def llenar_Tabla_Resultados():
    # Obtener el ID del producto desde la entrada_Producto
    product_id_to_recommend_for = int(entrada_Producto.get())
    recommendations = get_product_recommendations(product_id_to_recommend_for)
    for similar_product_id, similar_product, similar_product_price, similarity_percentage in recommendations:
        tabla.insert("", "end", text=similar_product_id, values=(similar_product, similar_product_price, f"{similarity_percentage:.2f}%"))
    entrada_Producto["state"] = "disable"
    boton_Buscar["state"] = "disable"
    boton_Limpiar["state"] = "normal"

def limpiar_Tabla_Resultados():
    for resultados in tabla.get_children():
        tabla.delete(resultados)
    entrada_Producto["state"] = "normal"
    boton_Buscar["state"] = "normal"
    boton_Limpiar["state"] = "disable"

# Declaracion y diseño de componentes para la UI
ventana = tk.Tk()
ventana.geometry("1050x800")
ventana.title("Sistema Recomendador")

# Cuadro BD
frame = tk.Frame(master=ventana, bg="lightblue")
label_BD = tk.Label(frame, text="BD de Prodcutos", bg="lightblue", font="consolas 18 bold", anchor=tk.W)
label_BD.pack(side=tk.TOP, padx=10, pady=10)

tabla1 = ttk.Treeview(frame, columns=("Col1", "Col2", "Col3"))
tabla1.heading("#0", text="Indice")
tabla1.heading("Col1", text="Producto")
tabla1.heading("Col2", text="Precio")
tabla1.heading("Col3", text="Descripción")
tabla1.column("#0", width=100, anchor="center")
tabla1.column("Col1", width=300, anchor="center")
tabla1.column("Col2", width=100, anchor="center")
tabla1.column("Col3", width=300, anchor="center")
tabla1.pack(side=tk.BOTTOM, padx=10, pady=10)

frame.pack(pady=10)

# Cuadro buscador
frame1 = tk.Frame(master=ventana, bg="lightblue")
label_Texto = tk.Label(frame1, text="Ingresa el ID del Producto:", bg="lightblue", font="consolas 18 bold", anchor=tk.W)
label_Texto.pack(side=tk.LEFT, padx=10, pady=10)
entrada_Producto = tk.Entry(frame1, bg="white", fg="black", font="consolas 18  bold", relief=tk.SUNKEN, width=50, justify=tk.LEFT, state="normal")
entrada_Producto.pack(side=tk.LEFT, padx=10, pady=10)

frame1.pack(pady=10)

# Cuadro boton buscar y limpiar
frame2 = tk.Frame(master=ventana, bg="lightblue")
boton_Buscar = tk.Button(frame2, text="Buscar", bg="orange", font="consolas 18 bold", width=10, state="normal", command=llenar_Tabla_Resultados)
boton_Buscar.pack(side=tk.LEFT, padx=20, pady=20)
boton_Limpiar = tk.Button(frame2, text="Limpiar", bg="grey", font="consolas 18 bold", width=10, state="disable", command=limpiar_Tabla_Resultados)
boton_Limpiar.pack(side=tk.LEFT, padx=20, pady=20)

frame2.pack(pady=10)

# Cuadro Tabla Resultados
frame3 = tk.Frame(master=ventana, bg="lightblue")
label_Resultados = tk.Label(frame3, text="Resultados", bg="lightblue", font="consolas 18 bold", anchor=tk.W)
label_Resultados.pack(side=tk.TOP, padx=10, pady=10)

tabla = ttk.Treeview(frame3, columns=("Col1", "Col2", "Col3"))
tabla.heading("#0", text="Indice")
tabla.heading("Col1", text="Producto")
tabla.heading("Col2", text="Precio")
tabla.heading("Col3", text="Porcentaje de Similitud")
tabla.column("#0", width=100, anchor="center")
tabla.column("Col1", width=300, anchor="center")
tabla.column("Col2", width=150, anchor="center")
tabla.column("Col3", width=150, anchor="center")
tabla.pack(side=tk.BOTTOM, padx=10, pady=10)

frame3.pack(pady=10)

# Funcion BD
def llenar_Tabla_BD():
    for i, row, in df.iterrows():
        tabla1.insert("", "end", text = i, values=(row['producto'], row['precio'], row['descripcion']))

llenar_Tabla_BD()

# Ventana
ventana.mainloop()