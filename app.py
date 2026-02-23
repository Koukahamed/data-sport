import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Force & Muscle",
    page_icon="🏋️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stHeader"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
.stDeployButton { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stMain"] > div { padding: 0 !important; }
iframe { border: none !important; display: block !important; }
</style>
<script>
// Resize iframe to full viewport height
window.addEventListener('message', function(e) {
    const iframes = window.document.querySelectorAll('iframe');
    iframes.forEach(function(iframe) {
        iframe.style.height = window.innerHeight + 'px';
        iframe.style.width = '100%';
        iframe.style.position = 'fixed';
        iframe.style.top = '0';
        iframe.style.left = '0';
        iframe.style.zIndex = '9999';
    });
});
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const iframes = document.querySelectorAll('iframe');
        iframes.forEach(function(iframe) {
            iframe.style.height = window.innerHeight + 'px';
            iframe.style.width = '100%';
            iframe.style.position = 'fixed';
            iframe.style.top = '0';
            iframe.style.left = '0';
            iframe.style.zIndex = '9999';
            iframe.style.border = 'none';
        });
    }, 100);
});
window.addEventListener('resize', function() {
    const iframes = document.querySelectorAll('iframe');
    iframes.forEach(function(iframe) {
        iframe.style.height = window.innerHeight + 'px';
    });
});
</script>
""", unsafe_allow_html=True)

with open("app.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=900, scrolling=False)
