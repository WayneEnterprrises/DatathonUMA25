import streamlit as st

st.set_page_config(page_title="Sobre Nosotros", page_icon=":bat:")

import streamlit as st

import streamlit as st

st.markdown(
    """
    <style>
        /* Estilo general del menú */
        [data-testid="stSidebar"] {
            background-color: #1E1E1E; /* Color de fondo oscuro */
            padding: 20px;
            border-radius: 10px; /* Bordes redondeados */
            box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.2);
        }

        /* Estilo del texto dentro del menú */
        [data-testid="stSidebar"] * {
            color: #ffffff !important; /* Texto en blanco */
            font-size: 16px !important;
            font-weight: bold;
        }

        /* Estilo de los selectores (dropdowns, inputs) */
        [data-baseweb="select"] {
            background-color: #333333 !important;
            color: #ffffff !important;
            border-radius: 5px;
        }

        /* Estilo de los botones */
        button[kind="primary"] {
            background-color: #6200EA !important; /* Morado */
            color: white !important;
            border-radius: 5px;
        }

        /* Hover en botones */
        button[kind="primary"]:hover {
            background-color: #3700B3 !important; /* Un morado más oscuro */
        }

        /* Mejorar el diseño de los inputs */
        input {
            background-color: #333333 !important;
            color: white !important;
            border: none !important;
            border-radius: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Presentación del Equipo")

st.write("Equipo ArkhamMed de la Universidad de Málaga, Ingenieros del Software del plan de estudios de la UMA-ETSII 2010")

st.image("assets/logoDatathon.png", caption=" Arkham Analytics", use_column_width=True)

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
