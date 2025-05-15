import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import os

# Ottieni il percorso assoluto della cartella corrente
current_directory = os.getcwd()

# Crea il percorso assoluto per ogni file CSV
drivers_path = os.path.join(current_directory, 'Datasets', 'drivers.csv')
driver_standings_path = os.path.join(current_directory, 'Datasets', 'driver_standings.csv')
results_path = os.path.join(current_directory, 'Datasets', 'results.csv')
races_path = os.path.join(current_directory, 'Datasets', 'races.csv')
circuits_path = os.path.join(current_directory, 'Datasets', 'circuits.csv')


# Carica i file CSV
drivers = pd.read_csv(drivers_path)
results = pd.read_csv(results_path)
races = pd.read_csv(races_path)
circuits = pd.read_csv(circuits_path)

# Merge races with circuits
races_with_circuits = races.merge(circuits, on="circuitId", suffixes=('_race', '_circuit'))

st.title("F1 Circuits & Races: Stats and Fun Facts")

st.header("Global Circuit Overview")

# Most used circuits
#most_used = races_with_circuits['name_circuit'].value_counts().reset_index()
#most_used.columns = ['Circuit', 'Hosted GPs']
#st.subheader("🏁 Most Frequently Used Circuits")
#st.dataframe(most_used.head(10))

# Circuit map with tooltip
st.subheader("Interactive Circuit Map with Info")

unique_circuits = circuits.drop_duplicates(subset='circuitId')

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
            get_color='[200, 30, 0, 160]',
            get_radius=40000,
            pickable=True,
        )
    ],
    tooltip={"text": "{name}\n{location}, {country}"}
)

st.pydeck_chart(circuit_map)

# First race per circuit
#st.subheader("📆 First Grand Prix on Each Circuit")
#first_race = races_with_circuits.groupby('name_circuit')['year'].min().reset_index()
#first_race.columns = ['Circuit', 'First GP Year']
#st.dataframe(first_race.sort_values('First GP Year'))

# Longevity
st.subheader("Longest Active Circuits")
lifespan = races_with_circuits.groupby('name_circuit')['year'].agg(['min', 'max'])
lifespan['Years Active'] = lifespan['max'] - lifespan['min']
lifespan = lifespan.reset_index().sort_values('Years Active', ascending=False)
lifespan.columns = ['Circuit', 'First Year', 'Last Year', 'Years Active']
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

    #st.markdown("Years with races on this circuit:")
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
    st.subheader("Wins Distribution of Top 10 Drivers on This Circuit")
    fig = px.bar(
        winner_counts.head(10),
        x='Driver',
        y='Wins',
        color='Driver',
        text='Wins',
        title='Top 10 Most Frequent Winners on This Circuit'
    )
    fig.update_layout(xaxis_title='Driver', yaxis_title='Number of Wins', showlegend=False)
    st.plotly_chart(fig)

