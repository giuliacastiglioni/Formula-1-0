import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import os
from streamlit_extras.stylable_container import stylable_container

from header import show_f1_header
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
        if st.button("Home"):
            st.switch_page("streamlit_app.py")
    with col2:
        if st.button("Drivers "):
            st.switch_page("pages/_1_Drivers.py")
    with col3:
        if st.button("Teams"):
            st.switch_page("pages/_3_Teams.py")
    with col4:
        if st.button("Trivial & Games"):
            st.switch_page("pages/_4_Trivial_&_Games.py")



# Ottieni il percorso assoluto della cartella corrente
current_directory = os.getcwd()

# Crea il percorso assoluto per ogni file CSV
drivers_path = os.path.join(current_directory, 'Datasets', 'drivers.csv')
driver_standings_path = os.path.join(current_directory, 'Datasets', 'driver_standings.csv')
results_path = os.path.join(current_directory, 'Datasets', 'results.csv')
races_path = os.path.join(current_directory, 'Datasets', 'races.csv')
circuits_path = os.path.join(current_directory, 'Datasets', 'circuits.csv')
lap_times_path = os.path.join(current_directory, 'Datasets', 'lap_times.csv')


# Carica i file CSV
drivers = pd.read_csv(drivers_path)
results = pd.read_csv(results_path)
races = pd.read_csv(races_path)
circuits = pd.read_csv(circuits_path)
lap_times = pd.read_csv(lap_times_path)

# Merge races with circuits
races_with_circuits = races.merge(circuits, on="circuitId", suffixes=('_race', '_circuit'))

st.title("F1 Circuits & Races: Stats and Fun Facts")

st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="https://i.pinimg.com/736x/72/3e/9c/723e9c40b7f54e3d917ae43185667654--office-office-office-decor.jpg" width="400">
    </div>
        """,
    unsafe_allow_html=True
)

st.header("Global Circuit Overview")

# Most used circuits
#most_used = races_with_circuits['name_circuit'].value_counts().reset_index()
#most_used.columns = ['Circuit', 'Hosted GPs']
#st.subheader("🏁 Most Frequently Used Circuits")
#st.dataframe(most_used.head(10))
# --- costruzione lifespan ---
# Longevity
lifespan = races_with_circuits.groupby('name_circuit')['year'].agg(['min', 'max'])
lifespan['Years Active'] = lifespan['max'] - lifespan['min']
lifespan = lifespan.reset_index().sort_values('Years Active', ascending=False)
lifespan.columns = ['Circuit', 'First Year', 'Last Year', 'Years Active']
#st.dataframe(lifespan)
# 1. Miglior tempo per giro in lap_times
fastest_laps = lap_times.loc[lap_times.groupby('raceId')['milliseconds'].idxmin()].copy()

# 2. Aggiungi circuitoId tramite races
fastest_laps = fastest_laps.merge(races[['raceId', 'circuitId']], on='raceId', how='left')

# 3. Tieni solo il miglior giro per ogni circuito
best_lap_per_circuit = fastest_laps.loc[fastest_laps.groupby('circuitId')['milliseconds'].idxmin()].copy()

# 4. Aggiungi nome circuito
best_lap_per_circuit = best_lap_per_circuit.merge(circuits[['circuitId', 'name']], on='circuitId', how='left')

# 5. Aggiungi nome pilota
best_lap_per_circuit = best_lap_per_circuit.merge(drivers[['driverId', 'forename', 'surname']], on='driverId', how='left')
best_lap_per_circuit['Driver'] = best_lap_per_circuit['forename'] + ' ' + best_lap_per_circuit['surname']

# 6. Converti millisecondi in tempo leggibile
def ms_to_time(ms):
    if pd.isna(ms): return None
    seconds = ms / 1000
    minutes = int(seconds // 60)
    remaining = seconds % 60
    return f"{minutes}:{remaining:06.3f}"

best_lap_per_circuit['Best Lap Time'] = best_lap_per_circuit['milliseconds'].apply(ms_to_time)

# 7. Seleziona solo le colonne necessarie
best_lap_summary = best_lap_per_circuit[['name', 'Best Lap Time', 'Driver']]
best_lap_summary.columns = ['Circuit', 'Best Lap Time', 'Driver']

# 8. Unisci con la tabella lifespan
lifespan = lifespan.merge(best_lap_summary, on='Circuit', how='left')


# --- merge con unique_circuits e aggiunta colore ---
unique_circuits = circuits.drop_duplicates(subset='circuitId')
unique_circuits = unique_circuits.merge(
    lifespan[['Circuit', 'Last Year']],
    left_on='name',
    right_on='Circuit',
    how='left'
)
unique_circuits['is_active'] = unique_circuits['Last Year'] == 2024
unique_circuits['color'] = unique_circuits['is_active'].apply(
    lambda active: [0, 200, 0, 160] if active else [200, 0, 0, 160]
)

# --- definizione della mappa ---
circuit_map = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=unique_circuits['lat'].mean(),
        longitude=unique_circuits['lng'].mean(),
        zoom=1.2,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=unique_circuits,
            get_position='[lng, lat]',
            get_color='color',
            get_radius=40000,
            pickable=True,
        )
    ],
    tooltip={"text": "{name}\n{location}, {country}"}
)

st.pydeck_chart(circuit_map)

# --- poi puoi mostrare la tabella lifespan ---
st.dataframe(lifespan)


# Races with same name on different circuits
#st.subheader("🔁 Races with Same Name but Different Circuits")
#same_name_diff_circuit = races.groupby('name')['circuitId'].nunique().reset_index()
#same_name_diff_circuit = same_name_diff_circuit[same_name_diff_circuit['circuitId'] > 1]
#same_name_diff_circuit.columns = ['GP Name', 'Different Circuits']
#st.dataframe(same_name_diff_circuit.sort_values('Different Circuits', ascending=False))

# Circuit selector
st.header("Circuit Details")
selected_circuit = st.selectbox("Select a circuit:", circuits['name'].sort_values().unique())

if selected_circuit:
    c_info = circuits[circuits['name'] == selected_circuit].iloc[0]
    c_races = races[races['circuitId'] == c_info['circuitId']]
    race_ids = c_races['raceId'].tolist()

    st.subheader(f"Info about {selected_circuit}")
    st.markdown(f"""
    - **Location**: {c_info['location']}, {c_info['country']}
    - **Lat/Lon**: {c_info['lat']}, {c_info['lng']}
    - **Altitude**: {c_info['alt']} m
    - **Total GPs Hosted**: {len(c_races)}
    - **First GP**: {c_races['year'].min()}
    - **Last GP**: {c_races['year'].max()}
    - [Wikipedia Link]({c_info['url']})
    """)

   # st.markdown("Years with races on this circuit:")
    #st.write(sorted(c_races['year'].unique()))

    # Most frequent winners
    st.subheader("Most Frequent Winners on this Circuit")
    wins_on_circuit = results[
        (results['raceId'].isin(race_ids)) & 
        (results['positionOrder'] == 1)
    ]

    wins_merged = wins_on_circuit.merge(drivers, on='driverId')
    winner_counts = wins_merged.groupby(['forename', 'surname']).size().reset_index(name='Wins')
    winner_counts = winner_counts.sort_values('Wins', ascending=False)

    st.dataframe(winner_counts.head(10))

    # Add histogram
    #st.subheader("Wins Distribution of Top 10 Drivers on This Circuit")
    #fig = px.bar(
    #    winner_counts.head(10),
    #    x='Driver',
    #    y='Wins',
    #    color='Driver',
     #   text='Wins',
    #    title='Top 10 Most Frequent Winners on This Circuit'
    #)
    #fig.update_layout(xaxis_title='Driver', yaxis_title='Number of Wins', showlegend=False)
    #st.plotly_chart(fig)

