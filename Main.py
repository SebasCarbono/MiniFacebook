import streamlit as st
import networkx as nx
from pyvis.network import Network
import pandas as pd
import random

st.set_page_config(page_title="Mini Facebook con Grafos", layout="wide")

# -----------------------------
# 1. CREACIÓN DEL GRAFO
# -----------------------------

# Puedes cambiar esta lista por tu propia red
usuarios = ["Ana","Luis","Carlos","Marta","Sofía","Javier","Paula","Andrés","Lucía","Tomás"]

# Crear grafo
G = nx.Graph()
G.add_nodes_from(usuarios)

# Aristas aleatorias (solo para demo)
for _ in range(18):
    a, b = random.sample(usuarios, 2)
    G.add_edge(a, b)

# -----------------------------
# 2. CÁLCULO DE JACCARD
# -----------------------------

def recomendar_usuario(G, usuario):
    candidatos = []
    vecinos = set(G.neighbors(usuario))

    # Comparamos usuario con cada otro nodo NO conectado
    for otro in G.nodes():
        if otro == usuario:
            continue
        if otro in vecinos:
            continue

        vecinos_u = set(G.neighbors(usuario))
        vecinos_v = set(G.neighbors(otro))

        inter = vecinos_u & vecinos_v
        union = vecinos_u | vecinos_v

        jaccard = len(inter) / len(union) if union else 0
        candidatos.append((otro, jaccard))

    # Ordenar por similitud
    candidatos.sort(key=lambda x: x[1], reverse=True)
    return candidatos


# -----------------------------
# 3. VISUALIZACIÓN DEL GRAFO
# -----------------------------

def crear_visualizacion(G):
    net = Network(height="600px", width="100%", bgcolor="#0e1117", font_color="white")

    # Convertir grafo
    net.from_nx(G)

    # Forzar diseño bonito
    net.repulsion(node_distance=120, central_gravity=0.2)

    return net


# -----------------------------
# 4. INTERFAZ STREAMLIT
# -----------------------------

st.title("Mini Facebook basado en Grafos y Coeficiente de Jaccard")
st.write("Explora amistades y recomendaciones usando teoría de grafos.")

col1, col2 = st.columns([1,1])

with col1:
    st.subheader("Selecciona un usuario")
    selected_user = st.selectbox("Usuario", usuarios)

    st.subheader("Amigos actuales")
    amigos = list(G.neighbors(selected_user))
    if amigos:
        st.write(amigos)
    else:
        st.write("Este usuario no tiene amigos aún.")

    st.subheader("Recomendaciones (Jaccard)")
    recomendaciones = recomendar_usuario(G, selected_user)

    df = pd.DataFrame(recomendaciones, columns=["Usuario", "Similitud"])
    st.dataframe(df)

with col2:
    st.subheader("Visualización del grafo")
    grafo = crear_visualizacion(G)
    grafo.save_graph("grafo.html")
    html_file = open("grafo.html", "r").read()
    st.components.v1.html(html_file, height=600)
