import streamlit as st

pages = [
    st.Page("pagesFiles/Home.py", title="Home"),
    st.Page("pagesFiles/Chat.py", title="Chat"),
    st.Page("pagesFiles/Contact_Us.py", title="Contact Us")
]

pg = st.navigation(pages)
pg.run()