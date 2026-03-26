import streamlit as st
from graphviz import Digraph

# --- CLASE NODO AVL ---
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None
        self.altura = 1  # Los AVL necesitan rastrear su altura

# --- LÓGICA DE BALANCEO (AVL) ---
def get_altura(nodo):
    return nodo.altura if nodo else 0

def get_balance(nodo):
    return get_altura(nodo.izq) - get_altura(nodo.der) if nodo else 0

def rotar_derecha(y):
    x = y.izq
    T2 = x.der
    # Realizar rotación
    x.der = y
    y.izq = T2
    # Actualizar alturas
    y.altura = 1 + max(get_altura(y.izq), get_altura(y.der))
    x.altura = 1 + max(get_altura(x.izq), get_altura(x.der))
    return x

def rotar_izquierda(x):
    y = x.der
    T2 = y.izq
    # Realizar rotación
    y.izq = x
    x.der = T2
    # Actualizar alturas
    x.altura = 1 + max(get_altura(x.izq), get_altura(x.der))
    y.altura = 1 + max(get_altura(y.izq), get_altura(y.der))
    return y

def insertar_avl(raiz, valor):
    # 1. Inserción normal de BST
    if not raiz:
        return Nodo(valor)
    elif valor < raiz.valor:
        raiz.izq = insertar_avl(raiz.izq, valor)
    elif valor > raiz.valor:
        raiz.der = insertar_avl(raiz.der, valor)
    else:
        return raiz # No duplicados

    # 2. Actualizar altura del ancestro
    raiz.altura = 1 + max(get_altura(raiz.izq), get_altura(raiz.der))

    # 3. Obtener factor de equilibrio
    balance = get_balance(raiz)

    # 4. Casos de desequilibrio y rotaciones
    # Caso Izquierda-Izquierda
    if balance > 1 and valor < raiz.izq.valor:
        return rotar_derecha(raiz)
    # Caso Derecha-Derecha
    if balance < -1 and valor > raiz.der.valor:
        return rotar_izquierda(raiz)
    # Caso Izquierda-Derecha
    if balance > 1 and valor > raiz.izq.valor:
        raiz.izq = rotar_izquierda(raiz.izq)
        return rotar_derecha(raiz)
    # Caso Derecha-Izquierda
    if balance < -1 and valor < raiz.der.valor:
        raiz.der = rotar_derecha(raiz.der)
        return rotar_izquierda(raiz)

    return raiz

# --- VISUALIZACIÓN ---
def generar_visualizacion(nodo, dot=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='circle', style='filled', color='#2ECC71', fontname='Arial', fontcolor='white')
    if nodo:
        # Mostramos el valor y su altura/balance para aprender
        label = f"{nodo.valor}\n(h:{nodo.altura})"
        dot.node(str(nodo.valor), label)
        if nodo.izq:
            dot.edge(str(nodo.valor), str(nodo.izq.valor))
            generar_visualizacion(nodo.izq, dot)
        if nodo.der:
            dot.edge(str(nodo.valor), str(nodo.der.valor))
            generar_visualizacion(nodo.der, dot)
    return dot

# --- INTERFAZ ---
st.set_page_config(page_title="AVL Tree Master", layout="wide")
st.title("⚖️ Árbol Binario Auto-Balanceado (AVL)")

if 'raiz' not in st.session_state:
    st.session_state.raiz = None

col_controles, col_grafico = st.columns([1, 2])

with col_controles:
    val = st.number_input("Insertar valor:", value=0, step=1)
    if st.button("Insertar Nodo", use_container_width=True):
        st.session_state.raiz = insertar_avl(st.session_state.raiz, val)
    
    if st.button("Reiniciar", use_container_width=True):
        st.session_state.raiz = None
        st.rerun()
    
    st.markdown("""
    **¿Qué observar?**
    Prueba insertar `10, 20, 30`. 
    Verás que el `20` sube automáticamente para mantener el equilibrio.
    
    Made With Love By: Juan José Meneses (MeneDev)
    """)

with col_grafico:
    if st.session_state.raiz:
        st.graphviz_chart(generar_visualizacion(st.session_state.raiz))
    else:
        st.info("Agrega valores para ver la magia del balanceo.")