import streamlit as st
import random
import os

# Configuración de ancho completo para la página
st.set_page_config(layout="wide")


######################
# Permitir desplazamiento suave en la página
st.markdown("""
<style>
html {
    scroll-behavior: smooth;
}
</style>
""", unsafe_allow_html=True)
######################


st.title("🧩 A estudiarrrrrr")

######################
# Ancla para la parte superior de la página
st.markdown('<div id="inicio"></div>', unsafe_allow_html=True)

# Botón para bajar al pie de página
st.markdown('<a href="#pie" target="_self" style="text-decoration: none;"><button style="background-color: #4CAF50; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 20px;">⬇️ Bajar al pie de página</button></a>', unsafe_allow_html=True)

######################

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

####################

# Inicializar estados de la sesión
if "nombres_mezclados" not in st.session_state:
    nombres = list(DATOS.values())
    random.shuffle(nombres)
    st.session_state.nombres_mezclados = nombres

if "validado" not in st.session_state:
    st.session_state.validado = False

# Guardar selecciones activas para dinamizar los desplegables
if "selecciones" not in st.session_state:
    st.session_state.selecciones = {}
##################
opciones_nombres = ["-- Selecciona --"] + st.session_state.nombres_mezclados




# 2. Renderizar en cuadrícula (grid)
NUM_COLUMNAS = 5  # Cambia a 3 o 5 según prefieras
elementos = list(DATOS.items())

###########
def actualizar_seleccion(key_id):
    st.session_state.selecciones[key_id] = st.session_state[key_id]
#############

with st.form("juego_form"):
    respuestas_usuario = {}

    # Procesar elementos en filas de N columnas
   # --- 3. Renderizar en cuadrícula (grid) con opciones dinámicas ---
NUM_COLUMNAS = 5
elementos = list(DATOS.items())
respuestas_usuario = {}

# Reemplazamos 'with st.form' por un contenedor normal para permitir actualizaciones al instante
for i in range(0, len(elementos), NUM_COLUMNAS):
    grupo = elementos[i:i + NUM_COLUMNAS]
    cols = st.columns(NUM_COLUMNAS)

    for idx, (img_path, nombre_correcto) in enumerate(grupo):
        pos_global = i + idx
        key_selector = f"select_{pos_global}"
        
        with cols[idx]:
            st.markdown(f'<div class="image-card">', unsafe_allow_html=True)
            st.image(img_path)
            
            # Obtener nombres elegidos en OTRAS tarjetas
            usados = [
                v for k, v in st.session_state.selecciones.items() 
                if k != key_selector and v != "-- Selecciona --"
            ]
            
            # Filtrar opciones para dejar solo las disponibles
            opciones_disponibles = ["-- Selecciona --"] + [
                n for n in st.session_state.nombres_mezclados 
                if n not in usados
            ]
            
            # Desplegable con respuesta en tiempo real
            eleccion = st.selectbox(
                f"Elemento {pos_global + 1}",
                opciones_disponibles,
                key=key_selector,
                on_change=actualizar_seleccion,
                args=(key_selector,)
            )
            respuestas_usuario[img_path] = eleccion

            # Contenedor de validación visual
            st.markdown(f'<div class="validation-container">', unsafe_allow_html=True)
            if st.session_state.validado:
                if eleccion == nombre_correcto:
                    st.success("✅ ¡Correcto!")
                elif eleccion == "-- Selecciona --":
                    st.warning("⚠️ Sin responder")
                else:
                    st.error(f"❌ Era: {nombre_correcto}")
            
            st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Botón de comprobación fuera de un formulario
if st.button("Comprobar respuestas", type="primary"):
    st.session_state.validado = True
    st.rerun()

# 3. Resultado global
if st.session_state.validado:
    aciertos = sum(1 for img, resp in respuestas_usuario.items() if resp == DATOS[img])
    if aciertos == len(DATOS):
        st.balloons()
        st.success(f"🎉 ¡Perfecto Amore! Has acertado todas las parejas, crack, titán ¡¡ ({aciertos}/{len(DATOS)}).")

st.markdown("---")

# Ancla para la parte inferior de la página
st.markdown('<div id="pie"></div>', unsafe_allow_html=True)

# Botón para subir al inicio
st.markdown('<a href="#inicio" target="_self" style="text-decoration: none;"><button style="background-color: #008CBA; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px;">⬆️ Subir al inicio</button></a>', unsafe_allow_html=True)


