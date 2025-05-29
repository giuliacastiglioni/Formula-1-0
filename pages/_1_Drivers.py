import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from streamlit_extras.stylable_container import stylable_container
import requests
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import wikipediaapi

from header import show_f1_header
show_f1_header()
# Carica e visualizza l'icona sopra il titolo
#st.image("/workspaces/Formula-1-0/Assets/icons/helmet_1850740.png", width=100)  # Puoi regolare la larghezza come preferisci

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
        if st.button("Teams"):
            st.switch_page("pages/_2_Teams.py")
    with col3:
        if st.button("Circuits"):
            st.switch_page("pages/_3_Circuits.py")
    with col4:
        if st.button("Trivial & Games"):
            st.switch_page("pages/_4_Trivial_&_Games.py")



# Titolo
st.title("Drivers")

st.write("""
Here you’ll find an overview of all the Formula 1 drivers. We'll include statistics, comparisons, and more!
""")

st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="https://i.pinimg.com/originals/94/45/fb/9445fbab033edd19a32449eaaf6553eb.jpg" width="500">
    </div>
    """,
    unsafe_allow_html=True
)
# Ottieni il percorso assoluto della cartella corrente
current_directory = os.getcwd()

# Crea il percorso assoluto per ogni file CSV
drivers_path = os.path.join(current_directory, 'Datasets', 'drivers.csv')
driver_standings_path = os.path.join(current_directory, 'Datasets', 'driver_standings.csv')
results_path = os.path.join(current_directory, 'Datasets', 'results.csv')
races_path = os.path.join(current_directory, 'Datasets', 'races.csv')
qualifying_path = os.path.join(current_directory, 'Datasets', 'qualifying.csv')
circuits_path = os.path.join(current_directory, 'Datasets', 'circuits.csv')
constructors_path = os.path.join(current_directory, 'Datasets', 'constructors.csv')

# Carica i file CSV
drivers_df = pd.read_csv(drivers_path)
driver_standings_df = pd.read_csv(driver_standings_path)
results_df = pd.read_csv(results_path)
races_df = pd.read_csv(races_path)
qualifying_df = pd.read_csv(qualifying_path)
circuits_df = pd.read_csv(circuits_path)
constructors_df = pd.read_csv(constructors_path)


# Funzione per estrarre i piloti che soddisfano i criteri
#def get_drivers_by_period(period):
#    if period == "1950-1980":
#        # Piloti che hanno vinto almeno un mondiale
#        # Uniamo driver_standings_df con races_df per ottenere l'anno della gara
#        standings_with_year = pd.merge(driver_standings_df, races_df[['raceId', 'year']], on='raceId', how='left')
#        
#        # Filtro per i dati delle gare fino al 1980
#        standings_per_year = standings_with_year[standings_with_year['year'] <= 1980]
#        
#        # Sommiamo i punti per ogni pilota in ogni stagione
#        total_points_per_year = standings_per_year.groupby(['driverId', 'year'])['points'].sum().reset_index()
#        
 #       # Troviamo il pilota con il punteggio massimo per ogni anno (vincitore del mondiale)
#        world_champions = total_points_per_year.loc[total_points_per_year.groupby('year')['points'].idxmax()]
        
        # Estraiamo i driverId dei piloti che hanno vinto almeno un mondiale
#        drivers = world_champions['driverId'].unique()
        
        # Numero di mondiali vinti da ciascun pilota
#        world_titles = world_champions.groupby('driverId').size()
        
#        criterion = "Drivers who have won at least one World Championship."
#    elif period == "1981-2008":
#        # Piloti con almeno 3 vittorie
#        winners = driver_standings_df[driver_standings_df['wins'] >= 3]
#        winners = winners[winners['raceId'].isin(races_df[races_df['year'].between(1981, 2008)]['raceId'])]
#        drivers = winners['driverId'].unique()
#        
        # Numero di gare vinte da ciascun pilota nel periodo 1981-2008
#        race_wins = results_df[results_df['driverId'].isin(drivers) & (results_df['raceId'].isin(races_df[races_df['year'].between(1981, 2008)]['raceId']))]
#        race_wins = race_wins[race_wins['positionOrder'] == 1]
#        race_wins_count = race_wins.groupby('driverId').size()
        
#        criterion = "Drivers who have won at least 3 races."
#    elif period == "2009-2013":
#        # Piloti con almeno 3 vittorie
#        winners = driver_standings_df[driver_standings_df['wins'] >= 1]
#        winners = winners[winners['raceId'].isin(races_df[races_df['year'].between(2009, 2013)]['raceId'])]
#        drivers = winners['driverId'].unique()
        
        # Numero di gare vinte da ciascun pilota nel periodo 2009-2013
#        race_wins = results_df[results_df['driverId'].isin(drivers) & (results_df['raceId'].isin(races_df[races_df['year'].between(2009, 2013)]['raceId']))]
#        race_wins = race_wins[race_wins['positionOrder'] == 1]
#        race_wins_count = race_wins.groupby('driverId').size()
        
#        criterion = "Drivers who have won at least 1 race."
#    elif period == "2014-2023":
#        # Piloti che hanno ottenuto almeno un punto (quindi sono andati a punti)
#        drivers_with_points = driver_standings_df[driver_standings_df['points'] > 0]
#        drivers_with_points = drivers_with_points[drivers_with_points['raceId'].isin(races_df[races_df['year'].between(2014, 2023)]['raceId'])]
#        drivers = drivers_with_points['driverId'].unique()

        # Numero di gare vinte da ciascun pilota nel periodo 2014-2023
#        race_wins = results_df[results_df['driverId'].isin(drivers) & (results_df['raceId'].isin(races_df[races_df['year'].between(2014, 2023)]['raceId']))]
#        race_wins = race_wins[race_wins['positionOrder'] == 1]
#        race_wins_count = race_wins.groupby('driverId').size()

 #       criterion = "Drivers who have scored at least one point."

  #  elif period == "2024":
        # Tutti i piloti che hanno partecipato al 2024
#        race_ids_2024 = races_df[races_df['year'] == 2024]['raceId']
#        drivers_2024 = results_df[results_df['raceId'].isin(race_ids_2024)]['driverId'].unique()

        # Calcola i punti per ogni pilota nel 2024
#        points_2024 = results_df[results_df['raceId'].isin(race_ids_2024)]
#        points_2024 = points_2024.groupby('driverId')['points'].sum()

#        drivers = drivers_2024
#        criterion = "All drivers who participated in the 2024 season."

        # Aggiungi i punti ottenuti a ciascun pilota nel 2024
#        return drivers, points_2024, criterion
    
#    else:
#        drivers = []
#        criterion = "No criteria selected."

#    return drivers, world_titles if period == "1950-1980" else race_wins_count, criterion

def analyze_performance_by_period(period):
    # Estendere i periodi per includere più intervalli temporali
    if period == "2014-2023":
        race_ids = races_df[races_df['year'].between(2014, 2023)]['raceId']
        results_period = results_df[results_df['raceId'].isin(race_ids)]
    elif period == "2024":
        race_ids = races_df[races_df['year'] == 2024]['raceId']
        results_period = results_df[results_df['raceId'].isin(race_ids)]
    elif period == "2009-2013":
        race_ids = races_df[races_df['year'].between(2009, 2013)]['raceId']
        results_period = results_df[results_df['raceId'].isin(race_ids)]
    elif period == "1984-2008":
        race_ids = races_df[races_df['year'].between(1984, 2008)]['raceId']
        results_period = results_df[results_df['raceId'].isin(race_ids)]
    else:
        return pd.DataFrame(), pd.DataFrame()

    # Calcola la posizione media per pilota
    avg_position = results_period.groupby('driverId')['positionOrder'].mean()

    # Calcola il numero di vittorie e podi (posizione 1, 2 o 3)
    victories = results_period[results_period['positionOrder'] == 1].groupby('driverId').size()
    podiums = results_period[results_period['positionOrder'].isin([1, 2, 3])].groupby('driverId').size()

    # Unisci i dati dei piloti per ottenere i nomi e codici
    performance = pd.DataFrame({
        'Average Position': avg_position,
        'Victories': victories,
        'Podiums': podiums
    }).fillna(0)

    # Unione con il dataframe dei piloti per aggiungere il nome e il codice del pilota
    performance = performance.merge(drivers_df[['driverId', 'forename', 'surname', 'code']], on='driverId', how='left')

    # Crea una nuova colonna 'Driver' con il nome completo
    performance['Driver'] = performance['forename'] + ' ' + performance['surname']
    performance.drop(['forename', 'surname'], axis=1, inplace=True)

    # Riorganizza le colonne per avere 'Driver' prima
    performance = performance[['code', 'Driver', 'Average Position', 'Victories', 'Podiums']]

    return performance

def plot_performance(performance, period):
    st.write(f"### Victories and Podiums for {period}")
    # Filtra righe con '\N' o altri valori non numerici
    performance.replace('\\N', np.nan, inplace=True)
    performance.dropna(inplace=True)

    #st.dataframe(performance)

   
    # Grafico interattivo - vittorie e podi
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=performance['code'],
        y=performance['Victories'],
        name='Victories',
        marker_color='gold'
    ))
    fig_bar.add_trace(go.Bar(
        x=performance['code'],
        y=performance['Podiums'],
        name='Podiums',
        marker_color='red'
    ))

    fig_bar.update_layout(
        barmode='stack',
        title=f'Victories and Podiums per Driver in {period}',
        xaxis_title='Driver Code',
        yaxis_title='Count',
        title_font_size=16,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    st.plotly_chart(fig_bar, use_container_width=True)

 # Ordina per posizione media (la più bassa è la migliore)
    #performance_sorted = performance.sort_values('Average Position', ascending=True)

    # Grafico interattivo - posizione media (bar plot)
    #fig_bar = px.bar(
    #    performance_sorted,
    #    x='code',
    #    y='Average Position',
    #    title=f'Average Position per Driver in {period}',
    #    color_discrete_sequence=['red']
    #)
    #fig_bar.update_yaxes(autorange='reversed', title='Average Position')
   # fig_bar.update_xaxes(title='Driver Code')
    #fig_bar.update_layout(
    #    title_font_size=16,
    #    plot_bgcolor='rgba(0,0,0,0)',
    #    paper_bgcolor='rgba(0,0,0,0)',
    #    font=dict(color='white')
    #)
    #st.plotly_chart(fig_bar, use_container_width=True)
# Funzione per ottenere il nome del pilota
def get_driver_name(driver_id):
    driver_row = drivers_df.loc[drivers_df['driverId'] == driver_id].iloc[0]
    return f"{driver_row['forename']} {driver_row['surname']}"

# Analisi evoluzione posizione media
def analyze_driver_evolution(driver_id):
    results_driver = results_df[results_df['driverId'] == driver_id]
    results_driver = results_driver.merge(races_df[['raceId', 'year']], on='raceId')
    avg_position_per_year = results_driver.groupby('year')['positionOrder'].mean().reset_index()

    driver_name = get_driver_name(driver_id)

    fig = px.line(avg_position_per_year, x='year', y='positionOrder', markers=True,
                  title=f'Evolution of {driver_name}\'s Performance Over Time',
                  labels={'positionOrder': 'Average Finish Position', 'year': 'Year'})
    fig.update_yaxes(autorange='reversed')  # Inverti asse Y
    st.plotly_chart(fig, use_container_width=True)


# Analisi vittorie
def analyze_driver_wins(driver_id):
    results_driver = results_df[results_df['driverId'] == driver_id]
    results_driver = results_driver.merge(races_df[['raceId', 'year']], on='raceId')
    wins_per_year = results_driver[results_driver['positionOrder'] == 1].groupby('year').size().reset_index(name='wins')

    driver_name = get_driver_name(driver_id)

    fig = px.bar(wins_per_year, x='year', y='wins',
                 title=f'Number of Wins per Year for {driver_name}',
                 labels={'wins': 'Number of Wins', 'year': 'Year'},
                 color_discrete_sequence=['green'])
    st.plotly_chart(fig, use_container_width=True)


# Analisi podi
def analyze_driver_podiums(driver_id):
    results_driver = results_df[results_df['driverId'] == driver_id]
    results_driver = results_driver.merge(races_df[['raceId', 'year']], on='raceId')
    podiums_per_year = results_driver[results_driver['positionOrder'] <= 3].groupby('year').size().reset_index(name='podiums')

    driver_name = get_driver_name(driver_id)

    fig = px.bar(podiums_per_year, x='year', y='podiums',
                 title=f'Number of Podium Finishes per Year for {driver_name}',
                 labels={'podiums': 'Number of Podiums', 'year': 'Year'},
                 color_discrete_sequence=['blue'])
    st.plotly_chart(fig, use_container_width=True)


# Analisi qualifiche
def analyze_driver_qualifying(driver_id):
    driver_quali = qualifying_df[qualifying_df['driverId'] == driver_id]
    driver_quali = driver_quali.merge(races_df[['raceId', 'year']], on='raceId')
    avg_quali_per_year = driver_quali.groupby('year')['position'].mean().reset_index()

    driver_name = get_driver_name(driver_id)

    fig = px.line(avg_quali_per_year, x='year', y='position', markers=True,
                  title=f'Average Qualifying Position per Year for {driver_name}',
                  labels={'position': 'Average Qualifying Position', 'year': 'Year'},
                  color_discrete_sequence=['orange'])
    fig.update_yaxes(autorange='reversed')  # Inverti asse Y
    st.plotly_chart(fig, use_container_width=True)

# Analisi punti
def analyze_driver_points(driver_id):
    driver_results = results_df[results_df['driverId'] == driver_id]
    driver_results = driver_results.merge(races_df[['raceId', 'year']], on='raceId')
    points_per_year = driver_results.groupby('year')['points'].sum().reset_index()

    driver_name = get_driver_name(driver_id)

    fig = px.bar(points_per_year, x='year', y='points',
                 title=f'Total Points per Year for {driver_name}',
                 labels={'points': 'Points', 'year': 'Year'},
                 color_discrete_sequence=['purple'])
    st.plotly_chart(fig, use_container_width=True)

# Comparazione con compagni di squadra
def compare_driver_with_teammates(driver_id):
    driver_results = results_df[results_df['driverId'] == driver_id]
    driver_results = driver_results.merge(races_df[['raceId', 'year']], on='raceId')

    teammate_results = results_df.merge(races_df[['raceId', 'year']], on='raceId')
    teammate_results = teammate_results[teammate_results['raceId'].isin(driver_results['raceId'])]

    merged = pd.merge(driver_results[['raceId', 'constructorId']], teammate_results, on=['raceId', 'constructorId'])
    merged = merged[merged['driverId'] != driver_id]

    teammate_avg = merged.groupby('year')['positionOrder'].mean().reset_index(name='Teammates')
    driver_avg = driver_results.groupby('year')['positionOrder'].mean().reset_index(name='Driver')

    merged_df = pd.merge(driver_avg, teammate_avg, on='year')

    driver_name = get_driver_name(driver_id)

    fig = px.line(merged_df, x='year', y=['Driver', 'Teammates'],
                  title=f'{driver_name} vs. Teammates: Average Finish Position per Year',
                  labels={'value': 'Average Finish Position', 'year': 'Year', 'variable': 'Legend'},
                  markers=True)
    fig.update_yaxes(autorange='reversed')
    st.plotly_chart(fig, use_container_width=True)


def compare_drivers(period):
    # Ottieni la performance dei piloti per il periodo specificato
    performance = analyze_performance_by_period(period)

    # Escludi record con codice '\N'
    performance = performance[performance['code'] != '\\N']

    # Considera solo i piloti con almeno una vittoria
    performance = performance.copy()
    performance['Victories'] = performance['Victories'].astype(int)
    performance = performance[performance['Victories'] > 0]

    # Pie chart interattiva con Plotly
    fig = px.pie(
        performance,
        names='code',
        values='Victories',
        title=f'Victories Share per Driver in {period}',
        color_discrete_sequence=px.colors.sequential.YlOrRd
    )

    fig.update_traces(textinfo='percent+label')  # Mostra percentuali e etichette
    fig.update_layout(
        title_font_size=18,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    st.plotly_chart(fig, use_container_width=True)

def plot_driver_wins_by_circuit(driver_id):
    # Filtra le gare vinte dal pilota
    driver_wins = results_df[
        (results_df['driverId'] == driver_id) &
        (results_df['positionOrder'] == 1)
    ]

    # Unisci con races per ottenere circuitId
    wins_with_race = driver_wins.merge(races_df[['raceId', 'circuitId']], on='raceId')

    # Unisci con circuits per ottenere il nome del circuito
    wins_with_circuits = wins_with_race.merge(circuits_df[['circuitId', 'name']], on='circuitId')

    # Conta le vittorie per circuito
    wins_by_circuit = wins_with_circuits['name'].value_counts().reset_index()
    wins_by_circuit.columns = ['Circuit', 'Wins']

    # Pie chart con Plotly
    fig = px.pie(
        wins_by_circuit,
        names='Circuit',
        values='Wins',
        title=f"Wins by circuit distribution of – {get_driver_name(driver_id)}",
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label')

    total_wins = wins_by_circuit['Wins'].sum()
    st.write(f"**Total Wins:** {total_wins}")
    st.plotly_chart(fig)



def driver_timeline(driver_id, results_df, races_df, drivers_df, constructors_df, qualifying_df, year=None):
    races_df = races_df[['raceId', 'year']]
    constructors_df = constructors_df[['constructorId', 'name']]
    drivers_df['driver_name'] = drivers_df['forename'] + ' ' + drivers_df['surname']
    drivers_df['dob'] = pd.to_datetime(drivers_df['dob'])

    merged = results_df.merge(races_df, on='raceId')
    merged = merged.merge(drivers_df[['driverId', 'driver_name', 'dob']], on='driverId')
    merged = merged.merge(constructors_df, on='constructorId')

     # Dati del pilota
    pilota_df = merged[merged['driverId'] == driver_id]

    # Carriera anno per anno
    career = (
        pilota_df
        .groupby(['year', 'name'], as_index=False)
        .agg({
            'positionOrder': [
                lambda x: (x == 1).sum(),     # Vittorie
                lambda x: (x <= 3).sum(),     # Podi
                'count'                       # Gare
            ]
        })
    )
    career.columns = ['year', 'team', 'Wins', 'Podiums', 'Races']
    pilota_dob = pilota_df['dob'].iloc[0]  # Estrai la data di nascita
    career['Age'] = career['year'] - pilota_dob.year


    # Anni con più successi
    max_wins = career['Wins'].max()
    career['highlight'] = career['Wins'] == max_wins


    # Prepara dati base
    drivers_df['driver_name'] = drivers_df['forename'] + ' ' + drivers_df['surname']
    drivers_df['dob'] = pd.to_datetime(drivers_df['dob'])

    races_year_df = races_df[['raceId', 'year']]
    constructors_df = constructors_df[['constructorId', 'name']]

    merged_results = results_df.merge(races_year_df, on='raceId')
    merged_results = merged_results.merge(drivers_df[['driverId', 'driver_name', 'dob']], on='driverId')
    merged_results = merged_results.merge(constructors_df, on='constructorId')

    merged_qual = qualifying_df.merge(races_year_df, on='raceId')
    merged_qual = merged_qual.merge(drivers_df[['driverId', 'driver_name']], on='driverId')

    pilota_df = merged_results[merged_results['driverId'] == driver_id]
    pilota_name = pilota_df['driver_name'].iloc[0]

    # Filtra per anno se specificato
    if year:
        pilota_df = pilota_df[pilota_df['year'] == year]
        merged_qual = merged_qual[(merged_qual['year'] == year) & (merged_qual['driverId'] == driver_id)]

    # Calcoli metriche chiave
    wins = (pilota_df['positionOrder'] == 1).sum()
    podiums = (pilota_df['positionOrder'] <= 3).sum()
    races = pilota_df['raceId'].nunique()
    points = pilota_df['points'].sum()

    avg_qual = merged_qual['position'].mean()
    if pd.isna(avg_qual):
        avg_qual = 999  # caso no data

    data = {
        'Wins': wins,
        'Podiums': podiums,
        'Races': races,
        'Avg Qual Pos': max(0, 30 - avg_qual),  # inversione: meglio qualifiche basse
        'Total Points': points / 10  # scala down
    }

    categories = list(data.keys())
    values = list(data.values())
    values += values[:1]  # chiudo il cerchio
    
    
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill='toself',
                line=dict(color='#FF0000', width=3),  # rosso F1 e linea spessa
                marker=dict(color='#FFFFFF', size=8, line=dict(color='#FF0000', width=2)),
                name=pilota_name if not year else f"{pilota_name} - {year}"
            )
        ]
    )

    fig.update_layout(
        polar=dict(
            bgcolor='#111111',  # sfondo scuro nel plot polare
            radialaxis=dict(
                visible=True,
                range=[0, max(values)*1.2],
                gridcolor='#444444',  # grigio scuro linee griglia
                tickfont=dict(color='white'),
                linecolor='white'
            ),
            angularaxis=dict(
                tickfont=dict(color='white'),
                linecolor='white',
                gridcolor='#444444'
            )
        ),
        paper_bgcolor='#000000',  # sfondo nero attorno al grafico
        font=dict(color='white', family='Arial Black'),
        showlegend=True,
        legend=dict(
            font=dict(color='white'),
            bgcolor='#222222',
            bordercolor='white',
            borderwidth=1
        ),
        title=dict(
            text=f"Overview performance {'year ' + str(year) if year else 'career'} of {pilota_name}",
            font=dict(color='white', size=20)          
        ),
        margin=dict(t=80, b=40, l=40, r=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Each 'r' value on the radar chart corresponds to a scaled metric (e.g., wins, podiums, races) that helps visualize the driver's performance across different aspects. For average position of course the lower, the better.")

    # Tabella carriera
    st.markdown("### Driver's Annual Statistics")
    st.dataframe(
        career[['year', 'team', 'Races', 'Wins', 'Podiums', 'Age']].sort_values('year'),
        use_container_width=True
    )

    # Compagni di squadra
    st.markdown("### Teammates over the years")

    # Ricaviamo compagni
    compagni_dict = {}

    for year in pilota_df['year'].unique():
        team_annuali = pilota_df[pilota_df['year'] == year]['constructorId'].unique()
        compagni = merged[
            (merged['year'] == year) &
            (merged['constructorId'].isin(team_annuali)) &
            (merged['driverId'] != driver_id)
        ]['driver_name'].unique()
        compagni_dict[year] = sorted(set(compagni))

    # Mostra in tabella
    compagni_df = pd.DataFrame([
        {"Anno": year, "Teammates": ", ".join(names)} for year, names in compagni_dict.items()
    ]).sort_values('Anno')

    st.dataframe(compagni_df, use_container_width=True)

def age_analysis(driver_id, races_df, constructors_df):
    st.markdown("### Heatmap Age vs Wins")
    races_df = races_df[['raceId', 'year']]
    constructors_df = constructors_df[['constructorId', 'name']]
    drivers_df['driver_name'] = drivers_df['forename'] + ' ' + drivers_df['surname']
    drivers_df['dob'] = pd.to_datetime(drivers_df['dob'])

    merged = results_df.merge(races_df, on='raceId')
    merged = merged.merge(drivers_df[['driverId', 'driver_name', 'dob']], on='driverId')
    merged = merged.merge(constructors_df, on='constructorId')

     # Dati del pilota
    pilota_df = merged[merged['driverId'] == driver_id]

    # Carriera anno per anno
    career = (
        pilota_df
        .groupby(['year', 'name'], as_index=False)
        .agg({
            'positionOrder': [
                lambda x: (x == 1).sum(),     # Vittorie
                lambda x: (x <= 3).sum(),     # Podi
                'count'                       # Gare
            ]
        })
    )
    career.columns = ['year', 'team', 'Wins', 'Podiums', 'Races']
    pilota_dob = pilota_df['dob'].iloc[0]  # Estrai la data di nascita
    career['Age'] = career['year'] - pilota_dob.year


    # Anni con più successi
    max_wins = career['Wins'].max()
    career['highlight'] = career['Wins'] == max_wins
    # Heatmap: righe = età, colonne = anno, valore = vittorie
    heatmap_data = career[['year', 'Age', 'Wins']].copy()

    # Crea la heatmap con Plotly
    heatmap_fig = go.Figure(data=go.Heatmap(
        x=heatmap_data['year'],
        y=heatmap_data['Age'],
        z=heatmap_data['Wins'],
        colorscale='Reds',
        hovertemplate='year: %{x}<br>Age: %{y}<br>Wins: %{z}<extra></extra>'
    ))

    heatmap_fig.update_layout(
        title=f"Age vs Wins",
        xaxis_title='Year',
        yaxis_title='Age',
        yaxis_autorange='reversed',
        height=400
    )

    st.plotly_chart(heatmap_fig, use_container_width=True)

# Visualizza i piloti in base al periodo selezionato

    #period = st.selectbox("Select the Period", ["1950-1980", "1981-2008", "2009-2013", "2014-2023", "2024"])
    #drivers_ids, result_or_points, criterion = get_drivers_by_period(period)
    
    # Filtra i piloti dal dataframe dei piloti
    #selected_drivers = drivers_df[drivers_df['driverId'].isin(drivers_ids)]
    # Aggiungi il numero di mondiali o gare vinte per ogni pilota
    #if period == "1950-1980":
    #    world_titles = result_or_points
    #    selected_drivers['World Titles'] = selected_drivers['driverId'].map(world_titles).fillna(0).astype(int)
    #    selected_drivers = selected_drivers.sort_values(by='World Titles', ascending=False)
    #elif period in ["1981-2008", "2009-2013", "2014-2023"]:
    #    race_wins_count = result_or_points
    #    selected_drivers['Race Wins'] = selected_drivers['driverId'].map(race_wins_count).fillna(0).astype(int)
    #    selected_drivers = selected_drivers.sort_values(by='Race Wins', ascending=False)
    #elif period == "2024":
    #    selected_drivers['Points'] = selected_drivers['driverId'].map(result_or_points).fillna(0).astype(int)
    #    selected_drivers = selected_drivers.sort_values(by='Points', ascending=False)  # Ordinamento in base ai punti
    #    st.write(f"**Criteria for {period}:** {criterion}")
    #    st.dataframe(selected_drivers[['forename', 'surname', 'nationality', 'Points']])
    #    return
    # Mostra il criterio
    #st.subheader(f"**{period}:** {criterion}")
    
    # Mostra i piloti con il numero di gare vinte, mondiali o punti
    #if period == "1950-1980":
    #    st.dataframe(selected_drivers[['forename', 'surname', 'nationality', 'World Titles']])
    #elif period in ["1981-2008", "2009-2013","2014-2023"]:
    #    st.dataframe(selected_drivers[['forename', 'surname', 'nationality', 'Race Wins']])


def get_wikipedia_image_url(page_url):
    try:
        title = page_url.split('/wiki/')[-1]
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        headers = {'User-Agent': 'Formula1App/1.0 (giuliamaria2000@gmail.com)'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if 'thumbnail' in data and 'source' in data['thumbnail']:
            return data['thumbnail']['source']
    except Exception as e:
        # Logga o ignora l'errore
        print(f"Sorry! No Photo available : {e}")
    return None

def load_image_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.verify()  # verifica che l'immagine sia valida
        img = Image.open(BytesIO(response.content))  # riapre immagine per usarla
        return img
    except (requests.RequestException, UnidentifiedImageError) as e:
        print(f"Immagine non caricabile da URL {url}: {e}")
        return None

def display_drivers_by_period():
    st.title("Drivers statistics")
    period = st.selectbox("Select the Period", ["1984-2008","2009-2013","2014-2023", "2024"])
    performance = analyze_performance_by_period(period)
    analyze_performance_by_period(period)
    plot_performance(performance, period)
    compare_drivers(period)

    st.title(f"Single driver analysis")
    drivers_list = drivers_df[['driverId', 'surname']].drop_duplicates()
    drivers_list['label'] = drivers_list['surname'] + ' (' + drivers_list['driverId'].astype(str) + ')'
    driver_selected = st.selectbox("Select a Driver", drivers_list['label'].values)
    driver_id = int(driver_selected.split('(')[-1].strip(')'))

    # Recupera l'url Wikipedia del driver
    url = drivers_df.loc[drivers_df['driverId'] == driver_id, 'url'].values

    img_url = None  # definisco sempre la variabile

    if len(url) > 0 and url[0]:
        img_url = get_wikipedia_image_url(url[0])

    if img_url:
        img = load_image_from_url(img_url)
        if img:
            st.image(img, width=300)
        else:
            st.write("Sorry! No image available for this Driver!")
    else:
        st.write("Sorry! No image available for this Driver!")

    analysis_type = st.radio(
        "Choose an analysis type",
        (
            'Driver Overview',
            'Wins by circuit distribution',
            'Age vs Wins',
            'Number of Wins per Year',
            'Number of Podium Finishes per Year',
            'Average qualifying position per year',
            'Average race finish position per year',
            'Total points per year'
        )
    )

    st.markdown("---")

    # Visualizzazione grafici ecc. come prima...
    if analysis_type == 'Driver Overview':
        driver_timeline(driver_id, results_df, races_df, drivers_df, constructors_df, qualifying_df, year=None)
    elif analysis_type == 'Average race finish position per year':
        analyze_driver_evolution(driver_id)
    elif analysis_type == 'Number of Wins per Year':
        analyze_driver_wins(driver_id)
    elif analysis_type == 'Number of Podium Finishes per Year':
        analyze_driver_podiums(driver_id)
    elif analysis_type == 'Average qualifying position per year':
        analyze_driver_qualifying(driver_id)
    elif analysis_type == 'Total points per year':
        analyze_driver_points(driver_id)
    elif analysis_type == 'Comparison with teammates':
        compare_driver_with_teammates(driver_id)
    elif analysis_type == 'Wins by circuit distribution':
        plot_driver_wins_by_circuit(driver_id)
    elif analysis_type == 'Age vs Wins':
        age_analysis(driver_id, races_df, constructors_df)

# Esegui la funzione
display_drivers_by_period()

st.title("Qualifying")

st.write("""
Dive into advanced race analytics: lap times, qualifying stats, and many more.
""")

def convert_time_to_seconds(time_str):
    try:
        if pd.isna(time_str):
            return None
        if ':' in time_str:
            mins, secs = time_str.split(':')
            return float(mins) * 60 + float(secs)
        return float(time_str)
    except:
        return None

def load_and_prepare_data():

    current_directory = os.getcwd()
    drivers_path = os.path.join(current_directory, 'Datasets', 'drivers.csv')
    results_path = os.path.join(current_directory, 'Datasets', 'results.csv')
    races_path = os.path.join(current_directory, 'Datasets', 'races.csv')
    qualifying_path = os.path.join(current_directory, 'Datasets', 'qualifying.csv')

    drivers_df = pd.read_csv(drivers_path)
    results_df = pd.read_csv(results_path)
    races_df = pd.read_csv(races_path)
    qualifying_df = pd.read_csv(qualifying_path)

    qualifying_df = qualifying_df.merge(races_df[['raceId', 'year', 'name', 'round', 'circuitId']], on='raceId')
    qualifying_df = qualifying_df.merge(drivers_df[['driverId', 'code', 'forename', 'surname']], on='driverId')
    qualifying_df = qualifying_df.merge(results_df[['raceId', 'driverId', 'grid', 'positionOrder']], on=['raceId', 'driverId'], how='left')

    for q in ['q1', 'q2', 'q3']:
        qualifying_df[q] = qualifying_df[q].apply(convert_time_to_seconds)

    qualifying_df['best_time'] = qualifying_df[['q1', 'q2', 'q3']].min(axis=1)

    return qualifying_df

df = load_and_prepare_data()

# Selettore pilota
drivers_list = df['surname'].dropna().unique()
selected_driver = st.selectbox("Select a driver", sorted(drivers_list))

# Filtra i dati
driver_data = df[df['surname'] == selected_driver]
#st.markdown(f"## Qualifying Stats for {selected_driver}")

def quali_pos_over_time(driver_data):
    # Sezione 1: Posizione in Qualifica nel Tempo
    st.subheader("Qualifying Position Over Time")

    # Controllo e pulizia dei dati
    driver_data_clean = driver_data.dropna(subset=['position', 'year'])  # Elimina righe con valori mancanti
    driver_data_clean = driver_data_clean[driver_data_clean['position'].apply(lambda x: isinstance(x, (int, float)))]  # Assicurati che 'position' sia numerico

    # Se ci sono ancora dei problemi, possiamo aggiungere un controllo più approfondito
    if driver_data_clean.empty:
        st.error("I dati non sono sufficienti o ci sono problemi con il formato. Verifica i dati di input.")
    else:
        # Modifica: Coloriamo per circuito (o per anno, o per sessione)
        fig1 = px.line(driver_data_clean.sort_values("year"), 
                    x="year", 
                    y="position", 
                    color="name",  # Puoi usare "name" per il circuito o "year" per l'anno
                    markers=True,
                    title="Qualifying Position by Year and Circuit", 
                    labels={"position": "Grid Position", "year": "Year", "name": "Circuit"})

        # Invertiamo l'asse Y, poiché la posizione 1 è la migliore
        fig1.update_yaxes(autorange="reversed")

        # Aggiungiamo uno sfondo scuro e personalizzazioni per il tema
        fig1.update_layout(
            plot_bgcolor="black",  # Impostiamo lo sfondo nero per il grafico
            paper_bgcolor="black",  # Impostiamo lo sfondo nero anche fuori dal grafico
            font=dict(color="white"),  # Impostiamo il colore del testo a bianco
            title_font_size=18,    # Impostiamo una dimensione per il titolo
            xaxis_title="Year",    # Titolo per l'asse X
            yaxis_title="Grid Position",  # Titolo per l'asse Y
            xaxis=dict(tickmode='linear', tick0=2000, dtick=1),  # Per mostrare ogni anno
            hovermode="closest"    # Mostra più dettagli quando il mouse si avvicina
        )

        st.plotly_chart(fig1, use_container_width=True)


# Funzione per convertire il tempo in secondi nel formato "min:sec.msec"
def format_time(seconds):
    if pd.isna(seconds):
        return None
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    msecs = int((seconds - mins * 60 - secs) * 1000)
    return f"{mins:02}:{secs:02}.{msecs:03}"

def best_quali_time_over_time(driver_data):
    # Sezione 2: Miglior Tempo in Qualifica
    st.subheader("Best Qualifying Time Over Time")

    # Aggiungiamo le colonne formattate per Q1, Q2, Q3
    driver_data['formatted_q1'] = driver_data['q1'].apply(format_time)
    driver_data['formatted_q2'] = driver_data['q2'].apply(format_time)
    driver_data['formatted_q3'] = driver_data['q3'].apply(format_time)

    # Creiamo un dataframe per ogni sessione di qualifica separata
    q1_data = driver_data[['year', 'formatted_q1', 'round']].dropna()
    q2_data = driver_data[['year', 'formatted_q2', 'round']].dropna()
    q3_data = driver_data[['year', 'formatted_q3', 'round']].dropna()

    # Aggiungiamo una colonna per etichettare le sessioni
    q1_data['session'] = 'Q1'
    q2_data['session'] = 'Q2'
    q3_data['session'] = 'Q3'

    # Uniamo i dati delle 3 sessioni in un unico dataframe
    q1_data = q1_data.rename(columns={'formatted_q1': 'time'})
    q2_data = q2_data.rename(columns={'formatted_q2': 'time'})
    q3_data = q3_data.rename(columns={'formatted_q3': 'time'})

    all_qualifying_data = pd.concat([q1_data, q2_data, q3_data])

    # Tracciamo il grafico, ma ora usiamo la colonna 'time' per differenziare i tempi per ogni sessione
    fig2 = px.scatter(all_qualifying_data, x="year", y="time", color="session", 
                    title="Qualifying Times by Session (Q1, Q2, Q3)",
                    labels={"time": "Time (min:sec.msec)", "session": "Session"})

    # Personalizziamo il grafico
    fig2.update_traces(marker=dict(size=10))

    # Mostriamo il grafico
    st.plotly_chart(fig2, use_container_width=True)

def quali_vs_race(driver_data):
    st.subheader("Qualifying vs Race Result")

    # Rimuovi righe con dati mancanti
    driver_data_clean = driver_data.dropna(subset=['grid', 'positionOrder'])

    # Crea una colonna che indica se ha guadagnato o perso posizioni
    driver_data_clean['result'] = driver_data_clean.apply(
        lambda row: 'Gained Positions' if row['positionOrder'] < row['grid'] else 'Lost Positions',
        axis=1
    )

    # Mappa i colori per ciascun tipo di risultato
    color_map = {
        'Gained Positions': 'green',
        'Lost Positions': 'red'
    }

    # Creiamo il grafico a dispersione con legenda
    fig3 = px.scatter(driver_data_clean, x='grid', y='positionOrder',
                      color='result',
                      color_discrete_map=color_map,
                      title="Qualifying Position vs Race Finish Position",
                      labels={'grid': 'Grid Position', 'positionOrder': 'Race Finish Position', 'result': 'Result'})

    # Aggiungiamo la linea diagonale
    min_val = min(driver_data_clean['grid'].min(), driver_data_clean['positionOrder'].min())
    max_val = max(driver_data_clean['grid'].max(), driver_data_clean['positionOrder'].max())
    fig3.add_shape(
        type="line",
        x0=min_val, y0=min_val,
        x1=max_val, y1=max_val,
        line=dict(color="yellow", width=2, dash="dash")
    )

    # Invertiamo gli assi
    fig3.update_layout(
        xaxis=dict(title="Grid Position", autorange="reversed"),
        yaxis=dict(title="Race Finish Position", autorange="reversed"),
        legend_title_text='Race Outcome',
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white")
    )

    st.plotly_chart(fig3, use_container_width=True)


def distrib_of_quali_pos(driver_data):
    # Sezione 4: Distribuzione Posizioni in Qualifica
    st.subheader("Distribution of Qualifying Positions")
    fig4 = px.histogram(driver_data, x='position', nbins=20, title="Qualifying Position Histogram")
    st.plotly_chart(fig4, use_container_width=True)

def average_quali_pos_per_circuit(driver_data):
    # Sezione 5: Performance per Circuito
    st.subheader("Average Qualifying Position per Circuit")
    # Raggruppa per circuito e calcola la posizione media di qualifica
    circuit_perf = driver_data.groupby('name')['position'].mean().reset_index().sort_values('position')

    # Usa un grafico a barre verticali con circuito sull'asse X e posizione media sull'asse Y
    fig5 = px.bar(circuit_perf, x='name', y='position',
                title="Average Qualifying Position by Circuit",
                labels={'position': 'Avg Qualifying Position', 'name': 'Circuit'})

    # Inverti l'asse Y per avere il miglior circuito in basso
    fig5.update_layout(yaxis=dict(autorange="reversed"))

    # Mostra il grafico
    st.plotly_chart(fig5, use_container_width=True)


def visual_quali_data(driver_data):
        analysis_type = st.radio(
            "Choose an analysis type",
            (
                'Qualifying Position Over Time',
                'Best Qualifying Time Over Time',
                'Qualifying vs Race Result',
                'Distribution of Qualifying Positions',
                'Average Qualifying Position per Circuit',
            )
        )

        st.markdown("---")

        # Mostra il grafico corrispondente
        if analysis_type == 'Qualifying Position Over Time':
            quali_pos_over_time(driver_data)
        elif analysis_type == 'Best Qualifying Time Over Time':
            best_quali_time_over_time(driver_data)
        elif analysis_type == 'Qualifying vs Race Result':
            quali_vs_race(driver_data)
        elif analysis_type == 'Distribution of Qualifying Positions':
            distrib_of_quali_pos(driver_data)
        elif analysis_type == 'Average Qualifying Position per Circuit':
            average_quali_pos_per_circuit(driver_data)

# Esegui la funzione
visual_quali_data(driver_data)