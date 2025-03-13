import streamlit as st
from pages.Login import login_form

st.set_page_config(page_title="Bienvenido a ArkhamMed", page_icon=":bat:", layout="centered", initial_sidebar_state="collapsed")

if "authenticated" not in st.session_state or st.session_state.authenticated == False:
    login_form()

else:
    st.markdown("<h2 style='text-align: center; font-weight: bold;'>Presentación del equipo</h2>", unsafe_allow_html=True)
    
    st.write(f"Bienvenido {st.session_state['username']} al equipo ArkhamMed de la Universidad de Málaga. En este espacio, combinamos la innovación en inteligencia artificial con la excelencia en el ámbito médico para ofrecer soluciones avanzadas en asistencia clínica. Como parte de nuestro equipo, te sumerges en un entorno donde la tecnología de vanguardia y el conocimiento médico se fusionan para transformar la atención al paciente. Prepárate para una experiencia inmersiva en la que cada interacción es un paso más hacia el futuro de la salud digital.")

    st.image("assets/logoDatathon.png", caption="Arkham Analytics",use_container_width=True)

    st.markdown("<h2 style='text-align: center; font-weight: bold;'>Conócenos</h2>", unsafe_allow_html=True)

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
