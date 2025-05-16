import streamlit as st
def show_f1_header():
    # HTML e CSS per barra superiore
    st.markdown(
        """
        <style>
        .f1-header {
            background-color: #e10600; /* Colore rosso F1 */
            padding: 10px 0;
            text-align: center;
        }
        .f1-header img {
            height: 40px;
        }
        </style>

        <div class="f1-header">
            <img src="https://upload.wikimedia.org/wikipedia/commons/3/33/F1.svg" alt="F1 Logo">
        </div>
        """,
        unsafe_allow_html=True
    )
