import streamlit as st

pages = [
    st.Page("pages/Sobre_Nosotros.py", title="Sobre Nosotros"),
    st.Page("pages/Chat.py", title="Chat"),
    st.Page("pages/Contactanos.py", title="Contactanos")
]

pg = st.navigation(pages)
pg.run()
