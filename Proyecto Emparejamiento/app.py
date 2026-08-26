import streamlit as st
import random
import os

# Configuración de ancho completo para la página
st.set_page_config(layout="wide")

st.title("🧩 Juego de Emparejar Imágenes y Nombres")

# Obtiene la ruta de la carpeta donde está este mismo archivo app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_IMAGENES = os.path.join(BASE_DIR, "imagenes")

# 1. Cargar archivos dinámicamente desde la carpeta
if not os.path.exists(CARPETA_IMAGENES):
    st.error(f"No se encuentra la carpeta '{CARPETA_IMAGENES}'. Por favor créala y añade tus fotos.")
    st.stop()

archivos = [f for f in os.listdir(CARPETA_IMAGENES) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

if not archivos:
    st.warning("No se encontraron imágenes en la carpeta.")
    st.stop()

# Crear diccionario { ruta_imagen: nombre_sin_extension }
DATOS = {
    os.path.join(CARPETA_IMAGENES, f): os.path.splitext(f)[0]
    for f in archivos
}

# Inicializar estados de la sesión
if "nombres_mezclados" not in st.session_state:
    nombres = list(DATOS.values())
    random.shuffle(nombres)
    st.session_state.nombres_mezclados = nombres

if "validado" not in st.session_state:
    st.session_state.validado = False

opciones_nombres = ["-- Selecciona --"] + st.session_state.nombres_mezclados

# 2. Renderizar en cuadrícula (grid)
NUM_COLUMNAS = 4  # Cambia a 3 o 5 según prefieras
elementos = list(DATOS.items())

with st.form("juego_form"):
    respuestas_usuario = {}

    # Procesar elementos en filas de N columnas
    for i in range(0, len(elementos), NUM_COLUMNAS):
        grupo = elementos[i:i + NUM_COLUMNAS]
        cols = st.columns(NUM_COLUMNAS)

        for idx, (img_path, nombre_correcto) in enumerate(grupo):
            pos_global = i + idx
            with cols[idx]:
                # Ancho fijo de 200px para mantener las imágenes proporcionadas y alineadas
                st.image(img_path, width=200)
                
                eleccion = st.selectbox(
                    f"Elemento {pos_global + 1}",
                    opciones_nombres,
                    key=f"select_{pos_global}"
                )
                respuestas_usuario[img_path] = eleccion

                # Validación individual
                if st.session_state.validado:
                    if eleccion == nombre_correcto:
                        st.success("✅ ¡Correcto!")
                    elif eleccion == "-- Selecciona --":
                        st.warning("⚠️ Sin responder")
                    else:
                        st.error(f"❌ Era: {nombre_correcto}")
        
        st.write("") # Espaciador entre filas

    st.markdown("---")
    submitted = st.form_submit_button("Comprobar respuestas", type="primary")
    if submitted:
        st.session_state.validado = True
        st.rerun()

# 3. Resultado global
if st.session_state.validado:
    aciertos = sum(1 for img, resp in respuestas_usuario.items() if resp == DATOS[img])
    if aciertos == len(DATOS):
        st.balloons()
        st.success(f"🎉 ¡Perfecto! Has acertado todas las parejas ({aciertos}/{len(DATOS)}).")
