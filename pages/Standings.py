import streamlit as st

# Carica e visualizza l'icona sopra il titolo
st.image("/workspaces/Formula-1-0/Assets/icons/Standings.png", width=100)  # Puoi regolare la larghezza come preferisci

st.title("Standings")

st.write("""
Live or updated standings for both drivers and constructors.  
Charts and progress tracking will be displayed here.
""")
