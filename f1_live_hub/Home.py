import streamlit as st

st.set_page_config(page_title="Formula 1 Live Hub", layout="wide", page_icon="🏎️")

st.markdown("<h1 style='text-align: center;'>🏁 Welcome to the Formula 1 Live Hub 🏁</h1>", unsafe_allow_html=True)

st.image("assets/f1_banner.jpg", use_column_width=True)

st.markdown("""
Explore everything about Formula 1: drivers, teams, stats, and even some fun games.  
Use the sidebar to navigate through the sections and enjoy the race! 🏎️🔥
""")

# Personalizzazione della sidebar con immagini e colori
st.sidebar.markdown("""
    <style>
        .stSidebar {
            background-color: #1f1f1f;  /* Colore scuro per la sidebar */
            color: white;
        }

        .stSidebar .st-radio > label {
            color: white;
            font-size: 16px;
            padding: 8px;
            text-transform: uppercase;
        }

        .stSidebar .st-radio .st-badge {
            background-color: #ff0000;
        }

        .stSidebar .stRadio > div > div > label {
            font-weight: bold;
        }

        .sidebar-title {
            text-align: center;
            font-size: 26px;
            color: white;
            margin-top: 20px;
        }

        .sidebar-icon {
            width: 30px;
            height: 30px;
            margin-right: 10px;
        }

        .sidebar-item {
            display: flex;
            align-items: center;
            padding: 10px;
        }

        .sidebar-item:hover {
            background-color: #ff0000;
            cursor: pointer;
        }
    </style>
    <div class="sidebar-title">Formula 1 Live Hub</div>
""", unsafe_allow_html=True)

# Aggiungi icone nella sidebar per ogni sezione
pages = {
    "Home": "Home.py",
    "Drivers": "pages/1_Drivers.py",
    "Teams": "pages/2_Teams.py",
    "Standings": "pages/3_Standings.py",
    "Races": "pages/4_Races.py",
    "Statistics": "pages/5_Statistics.py",
    "Games": "pages/6_Games.py",
    "Videos": "pages/7_Videos.py",
    "Trivia": "pages/8_Trivia.py"
}

# Creare una sidebar con icone e nomi per ogni pagina
selected_page = st.sidebar.radio("Navigate to:", list(pages.keys()), format_func=lambda page: f"🏎️ {page}")

# Carica la pagina selezionata
if selected_page == "Home":
    st.write("Welcome to the Home Page!")
else:
    exec(open(pages[selected_page]).read())

# Aggiungi una barra laterale grafica
for page_name in pages:
    icon_path = f"assets/icons/{page_name.lower()}.png"  # Supponendo di avere le icone per ciascuna sezione nella cartella assets/icons
    st.sidebar.markdown(f"""
        <div class="sidebar-item">
            <img src="{icon_path}" class="sidebar-icon" />
            <span>{page_name}</span>
        </div>
    """, unsafe_allow_html=True)
