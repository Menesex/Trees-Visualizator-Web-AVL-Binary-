import streamlit as st
from graphviz import Digraph

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    elif value > root.value:
        root.right = insert(root.right, value)
    return root

def search_node(root, value):
    if root is None or root.value == value:
        return root
    if value < root.value:
        return search_node(root.left, value)
    return search_node(root.right, value)

def get_inorder(root, result_list):
    if root:
        get_inorder(root.left, result_list)
        result_list.append(root.value)
        get_inorder(root.right, result_list)
    return result_list

def generate_viz(node, dot=None):
    if dot is None:
        dot = Digraph()
        dot.attr('node', shape='circle', style='filled', color='lightblue')
    if node:
        dot.node(str(node.value), str(node.value))
        if node.left:
            dot.edge(str(node.value), str(node.left.value))
            generate_viz(node.left, dot)
        else:
            invisible_id = f"inv_left_{node.value}"
            dot.node(invisible_id, label="", style="invis")
            dot.edge(str(node.value), invisible_id, style="invis")
        if node.right:
            dot.edge(str(node.value), str(node.right.value))
            generate_viz(node.right, dot)
        else:
            invisible_id = f"inv_right_{node.value}"
            dot.node(invisible_id, label="", style="invis")
            dot.edge(str(node.value), invisible_id, style="invis")
    return dot

st.set_page_config(page_title="BST Visualizer", layout="wide")

st.title("🌳 Binary Search Tree (BST) Visualizer")

if 'bst_root' not in st.session_state:
    st.session_state.bst_root = None

with st.sidebar:
    st.header("Controls")
    val = st.number_input("Node Value:", value=0, step=1)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Insert Node", use_container_width=True):
            st.session_state.bst_root = insert(st.session_state.bst_root, val)
    with col_btn2:
        if st.button("Reset Tree", use_container_width=True):
            st.session_state.bst_root = None
            st.rerun()
    
    st.markdown("---")
    st.markdown("Made With Love By: Juan José Meneses (MeneDev)")

col_viz, col_info = st.columns([2, 1])

with col_viz:
    if st.session_state.bst_root:
        st.subheader("Tree Structure")
        st.graphviz_chart(generate_viz(st.session_state.bst_root))
    else:
        st.info("The tree is empty. Add nodes from the sidebar.")

with col_info:
    st.subheader("Tree Analysis")
    if st.session_state.bst_root:
        inorder_list = get_inorder(st.session_state.bst_root, [])
        st.write("**In-Order Traversal:**")
        st.code(" -> ".join(map(str, inorder_list)))
        
        st.write("**Properties:**")
        st.write(f"- Total nodes: {len(inorder_list)}")
        st.write(f"- Minimum value: {min(inorder_list)}")
        st.write(f"- Maximum value: {max(inorder_list)}")
    else:
        st.info("Add nodes to see analysis")