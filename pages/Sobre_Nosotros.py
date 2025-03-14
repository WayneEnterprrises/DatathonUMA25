import streamlit as st
from pages.Login import login_form

st.set_page_config(page_title="Sobre Nosotros", page_icon=":bat:", layout="centered")

if "authenticated" not in st.session_state or st.session_state.authenticated == False:
    login_form()
else:
    st.title("Presentación del Equipo")
    st.write(f"Bienvenido {st.session_state['username']} al equipo ArkhamMed de la Universidad de Málaga")

    st.image("assets/logoDatathon.png", caption="Arkham Analytics", use_container_width=True)

    st.markdown("<h2 style='text-align: center; font-weight: bold;'>Sobre nosotros</h2>", unsafe_allow_html=True)

    equipo = [
        {
            "nombre": "Ángel Nicolás Escaño López",
            "github": "https://github.com/JustBeWell",
            "linkedin": "https://www.linkedin.com/in/angel-nicolas-escaño-lopez-32031426b/",
        },
        {
            "nombre": "José Canto Peral",
            "github": "https://github.com/Anon2148",
            "linkedin": "https://www.linkedin.com/in/jose-c-ln/",
        },
        {
            "nombre": "Diego Sicre Cortizo",
            "github": "https://github.com/DiegoSicre",
            "linkedin": "https://www.linkedin.com/in/diego-sicre-cortizo-b1897b233/",
        }
    ]

    for miembro in equipo:
        st.markdown(
            f"""
            <h2 style="text-align: center;">{miembro['nombre']}</h2>
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                <a href="{miembro['github']}" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="40" style="margin-right: 10px;">
                </a>
                <a href="{miembro['linkedin']}" target="_blank">
                    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="40" style="margin-left: 10px;">
                </a>
            </div>
            <hr>
            """,
            unsafe_allow_html=True
        )