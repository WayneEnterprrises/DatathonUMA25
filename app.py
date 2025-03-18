import streamlit as st

pages = [
    st.Page("pages/Home.py", title="Home"),
    st.Page("pages/Chat.py", title="Chat"),
    st.Page("pages/Contact_Us.py", title="Contact Us")
]

pg = st.navigation(pages)
pg.run()