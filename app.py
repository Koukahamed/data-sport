import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Force & Muscle", page_icon="🏋️", layout="centered")

# Cacher le header Streamlit
st.markdown("""
<style>
[data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none !important; }
.block-container { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

with open("app.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=850, scrolling=False)
