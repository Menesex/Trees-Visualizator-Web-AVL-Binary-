import streamlit as st

st.set_page_config(
    page_title="Tree Algorithms Visualizer",
    page_icon="🌳",
    layout="centered"
)

st.title("🌳 Data Structures Visualizer")
st.subheader("Welcome to MeneDev's Tree Lab")

st.markdown("""
This educational tool allows you to explore and compare how different tree 
data structures handle information. 

### 🚀 Select a module to begin:

* **Standard Binary Search Tree (BST):** See how a basic tree grows and why it can become inefficient (unbalanced).
* **AVL Tree (Self-Balancing):** Watch the magic of automatic rotations to maintain $O(\log n)$ efficiency.

**Developed by Juan José Meneses Jaramillo (MeneDev)**
*Software & Data Engineering Student*
""")

st.info("👈 Use the sidebar on the left to navigate between the different tree types!")

# # Optional: Add a nice visual or button to go to the most popular one
# if st.button("Try the AVL Tree now! ✨"):
#     st.switch_page("pages/2_AVL_Tree.py")