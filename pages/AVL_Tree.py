import streamlit as st
from graphviz import Digraph

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

def get_height(node):
    return node.height if node else 0

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x

def rotate_left(x):
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y

def insert_avl(root, value):
    if not root:
        return Node(value)
    if value < root.value:
        root.left = insert_avl(root.left, value)
    elif value > root.value:
        root.right = insert_avl(root.right, value)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and value < root.left.value:
        return rotate_right(root)
    if balance < -1 and value > root.right.value:
        return rotate_left(root)
    if balance > 1 and value > root.left.value:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if balance < -1 and value < root.right.value:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    
    return root

def generate_avl_viz(node, dot=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='circle', style='filled', color='#2ECC71', fontcolor='white')
    if node:
        label = f"{node.value}\n(h:{node.height})"
        dot.node(str(node.value), label)
        if node.left:
            dot.edge(str(node.value), str(node.left.value))
            generate_avl_viz(node.left, dot)
        if node.right:
            dot.edge(str(node.value), str(node.right.value))
            generate_avl_viz(node.right, dot)
    return dot

st.set_page_config(page_title="AVL Tree Visualizer", layout="wide")

st.title("⚖️ Self-Balancing AVL Tree")

if 'avl_root' not in st.session_state:
    st.session_state.avl_root = None

with st.sidebar:
    st.header("Controls")
    val = st.number_input("Node Value:", value=0, step=1)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Insert Node", use_container_width=True):
            st.session_state.avl_root = insert_avl(st.session_state.avl_root, val)
    with col_btn2:
        if st.button("Reset Tree", use_container_width=True):
            st.session_state.avl_root = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("**What to observe?**")
    st.markdown("Try inserting `10, 20, 30`.")
    st.markdown("You'll see `20` automatically rise to maintain balance.")
    st.markdown("---")
    st.markdown("Made With Love By: Juan José Meneses (MeneDev)")

col_viz, col_info = st.columns([2, 1])

with col_viz:
    if st.session_state.avl_root:
        st.subheader("Tree Structure")
        st.graphviz_chart(generate_avl_viz(st.session_state.avl_root))
    else:
        st.info("The tree is empty. Add nodes to see the auto-balancing magic!")

with col_info:
    st.subheader("Tree Information")
    if st.session_state.avl_root:
        def count_nodes(node):
            if not node:
                return 0
            return 1 + count_nodes(node.left) + count_nodes(node.right)
        
        total_nodes = count_nodes(st.session_state.avl_root)
        st.write(f"**Total nodes:** {total_nodes}")
        
        if total_nodes > 0:
            st.write("**Insert a sequence like:**")
            st.code("10, 20, 30, 40, 50")
            st.write("Watch how AVL keeps it balanced!")