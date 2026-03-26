import streamlit as st
from graphviz import Digraph

# --- CLASE NODO ---
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

# --- LÓGICA DEL ÁRBOL ---
def insertar(raiz, valor):
    if raiz is None:
        return Nodo(valor)
    if valor < raiz.valor:
        raiz.izq = insertar(raiz.izq, valor)
    elif valor > raiz.valor:
        raiz.der = insertar(raiz.der, valor)
    return raiz

def buscar_nodo(raiz, valor):
    if raiz is None or raiz.valor == valor:
        return raiz
    if valor < raiz.valor:
        return buscar_nodo(raiz.izq, valor)
    return buscar_nodo(raiz.der, valor)

# --- RECORRIDOS ---
def get_inorder(raiz, lista):
    if raiz:
        get_inorder(raiz.izq, lista)
        lista.append(raiz.valor)
        get_inorder(raiz.der, lista)
    return lista

# --- VISUALIZACIÓN CON GRAPHVIZ ---
def generar_visualizacion(nodo, dot=None):
    if dot is None:
        # Creamos el grafo con atributos estéticos
        dot = Digraph(comment='Arbol Binario')
        dot.attr('node', shape='circle', style='filled', color='skyblue', fontname='Arial')

    if nodo is not None:
        dot.node(str(nodo.valor), str(nodo.valor))
        
        if nodo.izq:
            dot.edge(str(nodo.valor), str(nodo.izq.valor))
            generar_visualizacion(nodo.izq, dot)
        else:
            # Nodos invisibles para mantener la simetría (Opcional)
            id_invisible = f"inv_izq_{nodo.valor}"
            dot.node(id_invisible, label="", style="invis")
            dot.edge(str(nodo.valor), id_invisible, style="invis")

        if nodo.der:
            dot.edge(str(nodo.valor), nodo.der.valor.__str__())
            generar_visualizacion(nodo.der, dot)
        else:
            id_invisible = f"inv_der_{nodo.valor}"
            dot.node(id_invisible, label="", style="invis")
            dot.edge(str(nodo.valor), id_invisible, style="invis")
            
    return dot

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Visualizador de Árboles Pro", layout="wide")
st.title("🌳 Visualizador de Árbol Binario de Búsqueda")

# Inicializar sesión
if 'raiz' not in st.session_state:
    st.session_state.raiz = None

# Sidebar para controles
with st.sidebar:
    st.header("Controles")
    nuevo_valor = st.number_input("Valor del nodo:", value=0, step=1)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Insertar", use_container_width=True):
            st.session_state.raiz = insertar(st.session_state.raiz, nuevo_valor)
    with col_btn2:
        if st.button("Limpiar", use_container_width=True):
            st.session_state.raiz = None
            st.rerun()

# Layout principal
col_viz, col_info = st.columns([2, 1])

with col_viz:
    if st.session_state.raiz:
        st.subheader("Estructura del Árbol")
        grafico = generar_visualizacion(st.session_state.raiz)
        # Streamlit tiene soporte nativo para objetos de Graphviz
        st.graphviz_chart(grafico)
    else:
        st.info("El árbol está vacío. Agrega nodos desde el panel lateral.")

with col_info:
    st.subheader("Análisis Lógico")
    if st.session_state.raiz:
        in_order_list = get_inorder(st.session_state.raiz, [])
        st.write("**Recorrido In-Order:**")
        st.code(" -> ".join(map(str, in_order_list)))
        
        st.write("**Propiedades:**")
        st.write(f"- Total de nodos: {len(in_order_list)}")
        st.write(f"- Valor mínimo: {min(in_order_list)}")
        st.write(f"- Valor máximo: {max(in_order_list)}")