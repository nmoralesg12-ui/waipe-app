import streamlit as st
from database import *

# ✅ CREA TABLAS AUTOMÁTICAMENTE (ARREGLA ERROR)
crear_tablas()

st.set_page_config(page_title="WAIPE", layout="centered")

st.title("📱 WAIPE")

# =========================
# CONTROL DE PAGINAS
# =========================
if "pagina" not in st.session_state:
    st.session_state.pagina = "menu"

# =========================
# MENU
# =========================
if st.session_state.pagina == "menu":

    if st.button("📦 Materia Prima"):
        st.session_state.pagina = "Materia"

    if st.button("👷 Reparto"):
        st.session_state.pagina = "Reparto"

    if st.button("📦 Empaque"):
        st.session_state.pagina = "Empaque"

    if st.button("💰 Entrega"):
        st.session_state.pagina = "Entrega"

# =========================
# MATERIA PRIMA
# =========================
elif st.session_state.pagina == "Materia":

    st.subheader("Materia Prima")

    blanco = st.number_input("Blanco", min_value=0.0)
    color = st.number_input("Color", min_value=0.0)

    if st.button("Guardar"):
        limpiar_materia_prima()
        guardar_materia_prima(blanco, color)
        st.success("✅ Guardado correctamente")

    if st.button("Ver resumen"):
        b, c = obtener_materia_total()
        st.info(f"Blanco: {b} | Color: {c}")

    if st.button("Volver"):
        st.session_state.pagina = "menu"

# =========================
# REPARTO
# =========================
elif st.session_state.pagina == "Reparto":

    st.subheader("Reparto")

    aldea = st.selectbox("Aldea", ["LOS OCOTES","LOS LLANOS"])

    trabajadores = obtener_trabajadores_por_aldea(aldea)
    trabajadores = [t for t in trabajadores if t[0] not in (None,"","None")]

    trabajadores.sort(key=lambda x: x[1], reverse=True)

    nombres = [t[0] for t in trabajadores]

    nombre = st.selectbox("Trabajador", nombres) if nombres else None

    pendiente = st.number_input(
        "Pendiente",
        value=float(obtener_pendiente(nombre)) if nombre else 0.0,
        min_value=0.0
    )

    tipo = st.selectbox(
        "Tipo",
        ["color","blanco"],
        index=0 if obtener_tipo(nombre)=="color" else 1
    )

    entregado = st.number_input("Entregado", min_value=0.0)
    nuevo = st.number_input("Nuevo", min_value=0.0)

    if st.button("Guardar"):

        if nombre:

            if entregado > pendiente:
                st.error("❌ No puedes entregar más de lo que debe")
            else:
                restante = pendiente - entregado
                total = restante + nuevo

                pago = entregado * (2.5 if tipo=="color" else 3)

                guardar_trabajador(nombre, aldea, total, tipo)

                st.success(f"✅ Pago Q{pago}")
                st.info(f"Pendiente nuevo: {total}")

    nuevo_nombre = st.text_input("Nuevo trabajador")

    if st.button("Agregar trabajador"):
        if nuevo_nombre.strip():
            guardar_trabajador(nuevo_nombre, aldea, 0, "color")
            st.success("✅ Trabajador agregado")

    if st.button("Eliminar trabajador"):
        if nombre:
            eliminar_trabajador(nombre)
            st.warning("🗑 Eliminado")

    st.subheader("📋 Lista de trabajadores")

    for n, p in trabajadores:
        tipo_trab = obtener_tipo(n)

        if p > 100:
            st.error(f"{n} → Q{p} → {tipo_trab}")
        elif p > 50:
            st.warning(f"{n} → Q{p} → {tipo_trab}")
        else:
            st.success(f"{n} → Q{p} → {tipo_trab}")

    if st.button("Volver"):
        st.session_state.pagina = "menu"

# =========================
# EMPAQUE
# =========================
elif st.session_state.pagina == "Empaque":

    st.subheader("Empaque")

    tipo = st.selectbox("Tipo", ["granel","boleado"])
    waipe = st.selectbox("Waipe", ["color","blanco"])

    cantidad = st.number_input("Cantidad", min_value=0.0)

    if st.button("Guardar"):

        stock = obtener_empaque(tipo, waipe)

        if tipo == "granel":
            guardar_empaque(tipo, waipe, cantidad)
            st.success("✅ Guardado correctamente")
            st.info(f"Bolsas: {stock} → {stock + cantidad}")

        else:
            bolas_viejas = stock * 50
            bolas_nuevas = cantidad * 50

            guardar_empaque(tipo, waipe, cantidad)

            st.success("✅ Guardado correctamente")
            st.info(f"Bolas: {bolas_viejas} → {bolas_viejas + bolas_nuevas}")

    if st.button("Volver"):
        st.session_state.pagina = "menu"

# =========================
# ENTREGA
# =========================
elif st.session_state.pagina == "Entrega":

    st.subheader("Entrega")

    tipo = st.selectbox("Tipo", ["granel","boleado"])
    waipe = st.selectbox("Waipe", ["color","blanco"])

    cantidad = st.number_input("Cantidad", min_value=0.0)

    if st.button("Vender"):

        stock = obtener_empaque(tipo, waipe)

        if stock <= 0:
            st.error("❌ No hay stock disponible")

        elif tipo == "granel":

            disponible = stock

            if cantidad > disponible:
                st.error(f"❌ Solo tienes {disponible} bolsas disponibles")
            else:
                precio = 6.5 if waipe == "color" else 9.5
                total = cantidad * 75 * precio

                reducir_empaque(tipo, waipe, cantidad)

                st.success(f"✅ Venta Q{total}")
                st.info(f"Bolsas restantes: {disponible - cantidad}")

        else:

            disponible = stock * 50

            if cantidad > disponible:
                st.error(f"❌ Solo tienes {disponible} bolas disponibles")
            else:
                precio = 6.5 if waipe == "color" else 9.5
                total = cantidad * precio

                reducir_empaque(tipo, waipe, cantidad / 50)

                st.success(f"✅ Venta Q{total}")
                st.info(f"Bolas restantes: {disponible - cantidad}")

    if st.button("Volver"):
        st.session_state.pagina = "menu"
