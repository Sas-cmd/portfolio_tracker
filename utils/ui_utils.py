import streamlit as st
import base64
from pathlib import Path

def customize_sidebar_with_logo():
    logo_path = Path(__file__).parent.parent / "assets" / "menu_icon.png"

    if logo_path.exists():
        with open(logo_path, "rb") as f:
            base64_logo = base64.b64encode(f.read()).decode("utf-8")
    else:
        st.warning("Sidebar logo image not found.")
        return

    st.markdown(
        f"""
        <style>
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        .custom-toggle {{
            position: fixed;
            top: 1rem;
            left: 1rem;
            width: 12px;
            height: 36px;
            z-index: 9999;
            cursor: pointer;
        }}

        .custom-toggle img {{
            width: 100%;
            height: auto;
        }}
        </style>

        <div class="custom-toggle" onclick="toggleSidebar()">
            <img src="data:image/png;base64,{base64_logo}" />
        </div>

        <script>
        function toggleSidebar() {{
            const sidebar = parent.document.querySelector('.css-1lcbmhc');
            if (sidebar) {{
                sidebar.style.display = sidebar.style.display === 'none' ? 'block' : 'none';
            }}
        }}
        </script>
        """,
        unsafe_allow_html=True
    )
