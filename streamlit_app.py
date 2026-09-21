import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tienda Fiorella", page_icon="🛍️", layout="wide")

# Configurar número de WhatsApp para la pasarela de pedidos (cambia esto por tu número con código de país)
TELEFONO_WHATSAPP = "584120000000"  # Ejemplo: 58 (Venezuela) + tu número

st.title("🛒 Tienda Fiorella - Catálogo en Línea")
st.write("Agrega productos a tu carrito y finaliza tu pedido al instante.")

sheet_url = "https://docs.google.com/spreadsheets/d/1vlc6XBbc4Wq_lr-H9MxbtQBoj7J3Yp2H7HWQL18VZ-8/export?format=csv"

@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv(sheet_url)

# Inicializar el carrito de compras en la sesión de Streamlit
if "carrito" not in st.session_state:
    st.session_state.carrito = []

try:
    df = load_data()
    
    # Diseño de dos columnas estilo E-commerce (Productos a la izquierda, Carrito estilo Walmart a la derecha)
    col_catalogo, col_carrito = st.columns([2, 1])

    with col_catalogo:
        st.subheader("Catálogo de Productos")
        cols = st.columns(2)
        for index, row in df.iterrows():
            c = cols[index % 2]
            with c:
                nombre = row.get("Nombre", "Sin nombre")
                precio = row.get("Precio", 0)
                imagen = row.get("Imagen", "")
                descripcion = row.get("Descripción", "")
                
                st.subheader(nombre)
                if pd.notna(imagen):
                    st.image(imagen, use_container_width=True)
                st.write(f"**Precio:** ${precio}")
                if pd.notna(descripcion):
                    st.write(descripcion)
                
                # Botón estilo Walmart para agregar al carrito
                if st.button(f"Agregar 🛒", key=f"add_{index}خرى_{nombre}"):
                    st.session_state.carrito.append({
                        "nombre": nombre,
                        "precio": float(precio) if pd.notna(precio) else 0.0
                    })
                    st.success(f"¡Agregado al carrito!")
                st.divider()

    with col_carrito:
        st.markdown("### 🛍️ Tu Carrito de Compras")
        
        if not st.session_state.carrito:
            st.info("Tu carrito está vacío. ¡Agrega productos!")
        else:
            total = 0
            for i, item in enumerate(st.session_state.carrito):
                st.write(f"- **{item['nombre']}**: ${item['precio']}")
                total += item['precio']
            
            st.markdown("---")
            st.markdown(f"### **Total a Pagar: ${total:.2f}**")
            
            # Botón para vaciar carrito
            if st.button("🗑️ Vaciar Carrito"):
                st.session_state.carrito = []
                st.rerun()

            st.markdown("---")
            st.subheader("💳 Finalizar Pedido")
            
            nombre_cliente = st.text_input("Tu Nombre:")
            direccion_cliente = st.text_input("Dirección de Entrega:")
            
            if st.button("🚀 Enviar Pedido por WhatsApp"):
                if not nombre_cliente:
                    st.warning("Por favor ingresa tu nombre para continuar.")
                else:
                    # Construir mensaje para WhatsApp
                    detalle = f"Hola, quiero hacer un pedido:%0A*Cliente:* {nombre_cliente}%0A*Dirección:* {direccion_cliente}%0A%0A*Productos:*%0A"
                    for item in st.session_state.carrito:
                        detalle += f"- {item['nombre']} (${item['precio']})%0A"
                    detalle += f"%0A*Total:* ${total:.2f}"
                    
                    url_whatsapp = f"https://wa.me/{TELEFONO_WHATSAPP}?text={detalle}"
                    st.markdown(f'<meta http-equiv="refresh" content="0;url={url_whatsapp}">', unsafe_allow_html=True)
                    st.success("¡Redirigiendo a WhatsApp para procesar tu pago y pedido!")

except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
