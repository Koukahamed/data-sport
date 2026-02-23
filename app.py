import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Force & Muscle",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide all Streamlit chrome
st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
.stDeployButton { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
</style>
""", unsafe_allow_html=True)

# Read and inject the full HTML app
with open("app.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=900, scrolling=False)
