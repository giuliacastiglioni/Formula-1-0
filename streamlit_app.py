import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from header import show_f1_header

# Impostazioni di base per Streamlit
st.set_page_config(page_title="Formula 1 For Fans", layout="wide", page_icon="🏎️")

show_f1_header()

# Pulsanti F1 in alto
with stylable_container(
    key="f1-menu",
    css_styles="""
    div[data-testid="stHorizontalBlock"] > div {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        padding: 1rem 0;
        background-color: #1a1a1a;  /* sfondo scuro per contrasto */
        border-bottom: 3px solid #e10600; /* linea rossa sotto */
    }

    button {
        background-color: #e10600; /* F1 red */
        color: white;
        font-weight: 700;
        font-size: 17px;
        padding: 0.7rem 1.6rem;
        border: none;
        border-radius: 30px;
        box-shadow: 0 6px 12px rgba(225, 6, 0, 0.6);
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.15s ease;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    button:hover {
        background-color: #ff3b3b;
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255, 59, 59, 0.8);
    }

    button:focus {
        outline: none;
        box-shadow: 0 0 8px 3px #ff3b3b;
    }
    """
):
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Drivers"):
            st.switch_page("pages/_1_Drivers.py")
    with col2:
        if st.button("Teams"):
            st.switch_page("pages/_2_Teams.py")
    with col3:
        if st.button("Circuits"):
            st.switch_page("pages/_3_Circuits.py")
    with col4:
        if st.button("Trivial & Games"):
            st.switch_page("pages/_4_Trivial_&_Games.py")




# Importa il font da Google Fonts
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather&display=swap');
        
        .title {
            font-family: 'Georgia', sans-serif;
            font-size: 14px;
            color: white;
            margin-top: 10px;
            text-align: center;
        }


    </style>
""", unsafe_allow_html=True)

# Intestazione dell'app con il nuovo font
st.markdown("<h1 class='title'> Welcome to the Formula 1 Live Hub </h1>", unsafe_allow_html=True)



# Descrizione
st.markdown("""Embark on a journey through the world of Formula 1! Use the menu above to dive into the high-speed action, legendary drivers, iconic teams, and unforgettable moments of this thrilling sport!""")



# Aggiungi alcune frasi iconiche della Formula 1 con CSS personalizzato per la grafica
st.markdown("""
    <style>
        /* Stile per le citazioni */
        .quote {
            font-family: 'Georgia', serif;
            font-size: 24px;
            color: #ff0000;  /* Colore rosso per le frasi */
            font-style: italic;
            text-align: center;  /* Centra il testo */
            margin: 20px 0;  /* Aggiungi spazio sopra e sotto le citazioni */
            padding: 10px;
            border-left: 5px solid #ff0000;  /* Linea laterale rossa */
            background-color: #000;  /* Sfondo nero per evidenziare le citazioni */
            color: white;  /* Testo bianco per contrasto */
        }

        /* Impostazioni per le immagini con didascalie */
        .image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin: 30px 0;
        }

        .image-container img {
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.5); /* Ombra leggera intorno alle immagini */
            width: 70%;  /* Riduci la larghezza delle immagini */
        }

        .image-container p {
            font-family: 'Georgia', sans-serif;
            font-size: 14px;
            color: white;
            margin-top: 10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Aggiungi le frasi iconiche
st.markdown('<div class="quote">"Sono i sogni a far vivere l’uomo. Il destino è in buona parte nelle nostre mani, sempre che sappiamo chiaramente quel che vogliamo e siamo decisi ad ottenerlo." – Enzo Ferrari</div>', unsafe_allow_html=True)

# Foto 1: Leggenda della Formula 1
st.markdown('<div class="image-container"><img src="https://adrianchambersmotorsports.com.au/wp-content/uploads/2022/09/Monza-track.jpg" alt="Formula 1" /><p>Formula 1 - Monza</p></div>', unsafe_allow_html=True)

# Una frase iconica di un pilota
st.markdown('<div class="quote">"I am not a magician, I am just a good driver." – Ayrton Senna</div>', unsafe_allow_html=True)

# Foto 2: Pilota leggenda
st.markdown('<div class="image-container"><img src="https://th.bing.com/th/id/R.e7d96b2d8766810fd96b5eb04acbe1e3?rik=FGC4GI9bozY%2bVg&pid=ImgRaw&r=0" alt="Ayrton Senna" /><p>Ayrton Senna - A legendary driver</p></div>', unsafe_allow_html=True)

# Una citazione famosa sulla velocità
st.markdown('<div class="quote">"Se lo puoi sognare, lo puoi fare." – Ferrari</div>', unsafe_allow_html=True)

# Foto 3: Auto Ferrari
st.markdown('<div class="image-container"><img src="https://cdn-8.motorsport.com/images/amp/6zQ7yKJY/s1000/ferrari-engine-1.jpg" alt="Ferrari" /><p>Ferrari - Power and tradition</p></div>', unsafe_allow_html=True)

# Una frase celebre da Michael Schumacher
st.markdown('<div class="quote">"You have to be able to push the limits." – Michael Schumacher</div>', unsafe_allow_html=True)

# Foto 4: Michael Schumacher in azione
st.markdown('<div class="image-container"><img src="https://imgr1.auto-motor-und-sport.de/F1-Michael-Schumacher-169FullWidthArticleGalleryOverlay-77e61a-304621.jpg" alt="Michael Schumacher" /><p>Michael Schumacher - The Kaiser of Formula 1</p></div>', unsafe_allow_html=True)

# Aggiungi una citazione da Niki Lauda
st.markdown('<div class="quote">"I don\'t fear death. I fear not trying." – Niki Lauda</div>', unsafe_allow_html=True)

# Foto 5: Niki Lauda
st.markdown('<div class="image-container"><img src="https://gpkingdom.it/wp-content/uploads/2024/02/lauda-1024x683.jpg" alt="Niki Lauda" /><p>Niki Lauda - A true fighter</p></div>', unsafe_allow_html=True)

# Aggiungi una citazione di James Hunt
st.markdown('<div class="quote">"I’m a racer. I don’t think about anything else." – James Hunt</div>', unsafe_allow_html=True)

# Foto 6: James Hunt
st.markdown('<div class="image-container"><img src="https://cdn.shopify.com/s/files/1/1566/2889/files/niki_lauda.jpg?v=1647363481" alt="James Hunt" /><p>James Hunt - The ultimate racer</p></div>', unsafe_allow_html=True)

# Citazione leggendaria di Enzo Ferrari
st.markdown('<div class="quote">"Non si può descrivere la passione, la si può solo vivere." – Enzo Ferrari</div>', unsafe_allow_html=True)

# Foto 7: Enzo Ferrari
st.markdown('<div class="image-container"><img src="https://th.bing.com/th/id/R.d48d51658a43b82ced61e7725f8f629a?rik=8GSLeT8ZUU3S%2bA&riu=http%3a%2f%2fwww.thefamouspeople.com%2fprofiles%2fimages%2fenzo-ferrari-2.jpg&ehk=lvQlZHzS006qkMY4C7u7Xp5ZXw%2bEyklaX41MUclV1Ys%3d&risl=&pid=ImgRaw&r=0" /><p>Enzo Ferrari - The genius behind the Ferrari legacy</p></div>', unsafe_allow_html=True)

# Citazione di Lewis Hamilton (famoso pilota)
st.markdown('<div class="quote">"I don’t really believe in limits. I believe in endless possibilities." – Lewis Hamilton</div>', unsafe_allow_html=True)

# Foto 8: Lewis Hamilton
st.markdown('<div class="image-container"><img src="https://www.autohebdo.fr/app/uploads/2024/07/DPPI_00124013_2016-753x494.jpg" alt="Lewis Hamilton" /><p>Lewis Hamilton - A legend in the making</p></div>', unsafe_allow_html=True)

# Citazione di Sir Frank Williams
st.markdown('<div class="quote">"The team is everything. If you are not part of the team, you don’t matter." – Sir Frank Williams</div>', unsafe_allow_html=True)

# Foto 9: Sir Frank Williams
st.markdown('<div class="image-container"><img src="https://cdn-autosprint.corrieredellosport.it/images/2021/11/28/155231939-88ed7035-6c88-4347-8249-a0008c7cd7b4.jpg" alt="Sir Frank Williams" /><p>Sir Frank Williams - A legend of Formula 1</p></div>', unsafe_allow_html=True)

# Citazione di Jean Todt
st.markdown('<div class="quote">"It’s all about the team. We have to fight together, win together, and lose together." – Jean Todt</div>', unsafe_allow_html=True)

# Foto 10: Jean Todt
st.markdown('<div class="image-container"><img src="https://www.repstatic.it/content/nazionale/img/2019/07/30/213747138-68b8a4ac-0af2-4d04-81ee-b133be205f73.jpg" alt="Jean Todt" /><p>Jean Todt - Mastermind of Ferrari\'s success</p></div>', unsafe_allow_html=True)

# Aggiungi più immagini e citazioni per arricchire ulteriormente la pagina

# Separa le immagini e i testi con un po' di spazio
st.write("<br>", unsafe_allow_html=True)

st.markdown("""Data source: https://ergast.com/mrd/ 
            """)
