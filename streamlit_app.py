import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tienda Fiorella", page_icon="🛍️", layout="wide")

st.title("🛒 Tienda Fiorella - Inventario en Vivo")
st.write("Catálogo actualizado directamente desde Google Sheets.")

sheet_url = "https://docs.google.com/spreadsheets/d/1vlc6XBbc4Wq_lr-H9MxbtQBoj7J3Yp2H7HWQL18VZ-8/export?format=csv"

@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv(sheet_url)

try:
    df = load_data()
    cols = st.columns(3)
    for index, row in df.iterrows():
        col = cols[index % 3]
        with col:
            # Usamos "Nombre" que es como se llama tu columna en el Google Sheet
            st.subheader(row.get("Nombre", "Sin nombre"))
            if "Imagen" in row and pd.notna(row["Imagen"]):
                st.image(row["Imagen"], use_container_width=True)
            st.write(f"**Precio:** ${row.get('Precio', 'Consultar')}")
            
            # Mostramos la descripción o categoría si deseas
            if "Descripción" in row and pd.notna(row["Descripción"]):
                st.write(f"{row.get('Descripción')}")
                
            st.button(f"Comprar {row.get('Nombre', '')}", key=f"btn_{index}")
            st.divider()
            
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
    st.info("Asegúrate de que tu Google Sheet tenga permisos públicos de lectura o esté publicado como CSV.")
