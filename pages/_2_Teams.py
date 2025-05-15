import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Teams", page_icon="🏎️")
st.title("Constructor Performance Analysis")
st.markdown("Explore key metrics and performance trends of F1 constructors from 1950 to today.")

st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="https://preview.redd.it/b7mn2w7hnpv51.png?auto=webp&s=64a0d5e6e40d62d57363c321ec7185c63a286909" width="500">
    </div>
        """,
    unsafe_allow_html=True
)
st.markdown("<br><br>", unsafe_allow_html=True)



# Ottieni il percorso assoluto della cartella corrente
current_directory = os.getcwd()

# Crea il percorso assoluto per ogni file CSV
constructors_path = os.path.join(current_directory, 'Datasets', 'constructors.csv')
results_path = os.path.join(current_directory, 'Datasets', 'results.csv')
races_path = os.path.join(current_directory, 'Datasets', 'races.csv')
constructor_standings_path = os.path.join(current_directory, 'Datasets', 'constructor_standings.csv')

# Carica i file CSV
constructors = pd.read_csv(constructors_path)
results = pd.read_csv(results_path)
races = pd.read_csv(races_path)
constructor_standings = pd.read_csv(constructor_standings_path)

# Merge datasets
constructor_standings = constructor_standings.merge(races[['raceId', 'year']], on='raceId')
constructor_standings = constructor_standings.merge(constructors[['constructorId', 'name']], on='constructorId')



# Definizione dei periodi
periods = {
    "1950–1959": (1950, 1959),
    "1960–1980": (1960, 1980),
    "1981–1990": (1981, 1990),
    "1991–1997": (1991, 1997),
    "1998–2008": (1998, 2008),
    "2009–2014": (2009, 2014),
    "2015–2024": (2015, 2024)
}

# Selettore periodo
selected_period = st.selectbox("Select Time period", list(periods.keys()))
start_year, end_year = periods[selected_period]

# Filtro standings per periodo selezionato
filtered_standings = constructor_standings[
    (constructor_standings['year'] >= start_year) &
    (constructor_standings['year'] <= end_year)
]

# Ottieni l'ultima gara (round) per ogni anno
last_round_per_year = races.groupby('year')['round'].max().reset_index()
last_round_per_year.rename(columns={'round': 'last_round'}, inplace=True)

# Unisci con races per ottenere i raceId delle ultime gare
last_race_ids = races.merge(last_round_per_year, left_on=['year', 'round'], right_on=['year', 'last_round'])[['year', 'raceId']]

# Filtra constructor_standings per tenere solo i dati delle gare finali
final_standings = constructor_standings.merge(last_race_ids, on=['year', 'raceId'])

# Ora possiamo calcolare correttamente punti e vittorie finali per anno

# Sezione 0: Bar chart per confronto selezionati
st.subheader("Compare Constructors")

# Selezione dei team
selected_teams = st.multiselect("Select Constructors", final_standings['name'].unique())

# Filtraggio in base a team selezionati e range di anni
if selected_teams:
    filtered_df = final_standings[
        (final_standings['name'].isin(selected_teams)) &
        (final_standings['year'] >= start_year) &
        (final_standings['year'] <= end_year)
    ]

    points_by_team = filtered_df.groupby(['year', 'name'])['points'].sum().reset_index()

    # Grafico a barre
    fig4 = px.bar(points_by_team, x="year", y="points", color="name", barmode="group",
                  labels={"points": "Points", "year": "Year", "name": "Constructor"},
                  title=f"Selected Constructors: Final Points per Season ({start_year}–{end_year})")
    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)
    
# Section 1: Constructor Points (Only Point Scorers)
st.subheader("Constructor Points")

# Raggruppa per anno e nome, e somma i punti
yearly_points = final_standings.groupby(['year', 'name'])['points'].sum().reset_index()
yearly_points = yearly_points[(yearly_points['year'] >= start_year) & (yearly_points['year'] <= end_year)]

# Calcola i punti totali per ogni costruttore nel periodo
total_points = yearly_points.groupby('name')['points'].sum().reset_index()
scoring_teams = total_points[total_points['points'] > 0]['name']

# Filtra solo i team che hanno fatto almeno 1 punto
yearly_points = yearly_points[yearly_points['name'].isin(scoring_teams)]

# Crea il grafico
fig = px.line(
    yearly_points,
    x='year',
    y='points',
    color='name',
    markers=True,
    title=f"Constructor Points Trend ({start_year}–{end_year}) – Only Scoring Teams",
    labels={'points': 'Points', 'year': 'Year', 'name': 'Constructor'}
)
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)


# Section 2: Constructor Wins (Trend Line - Only Winners)
st.subheader("Constructor Wins Trend")

# Raggruppa e somma le vittorie
wins_per_year = final_standings.groupby(['year', 'name'])['wins'].sum().reset_index()
wins_per_year = wins_per_year[(wins_per_year['year'] >= start_year) & (wins_per_year['year'] <= end_year)]

# Calcola il totale delle vittorie per ciascun costruttore
total_wins = wins_per_year.groupby('name')['wins'].sum().reset_index()
winners = total_wins[total_wins['wins'] > 0]['name']

# Filtra solo i costruttori che hanno almeno una vittoria
wins_per_year = wins_per_year[wins_per_year['name'].isin(winners)]

# Crea il grafico
fig2 = px.line(
    wins_per_year,
    x='year',
    y='wins',
    color='name',
    markers=True,
    title=f"Constructor Wins Trend ({start_year}–{end_year}) – Only Winners",
    labels={'wins': 'Wins', 'year': 'Year', 'name': 'Constructor'}
)
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)





# Section 3: Final Championship Position
#st.subheader("🎯 Final Standing Positions")
#fig3 = px.bar(filtered_standings, x="year", y="position", color="name",
#              labels={"position": "Final Position", "year": "Year", "name": "Constructor"},
#              title=f"Final Championship Positions ({start_year}–{end_year})",
#              barmode="group")
#fig3.update_yaxes(autorange="reversed")
#fig3.update_layout(template="plotly_dark")
#st.plotly_chart(fig3, use_container_width=True)



# Section 5: Most Dominant per Decade
#st.subheader("👑 Dominant Constructors by Decade")
#constructor_standings['decade'] = (constructor_standings['year'] // 10) * 10
#dominant = constructor_standings.groupby(['decade', 'name'])['wins'].sum().reset_index()
#dominant = dominant.loc[dominant.groupby('decade')['wins'].idxmax()]
#fig5 = px.bar(dominant, x="decade", y="wins", color="name",
#              labels={"wins": "Total Wins", "decade": "Decade", "name": "Constructor"},
#              title="Most Successful Constructor by Decade")
#fig5.update_layout(template="plotly_dark")
#st.plotly_chart(fig5, use_container_width=True)




# Section 6: Extra Stats
st.subheader("Constructors' Championship Titles")

# Prendi solo il costruttore con più punti per anno
titles = final_standings.groupby(['year', 'name'])['points'].sum().reset_index()
winners = titles.loc[titles.groupby('year')['points'].idxmax()]

# Conta quanti titoli ha vinto ciascun costruttore
total_titles = winners['name'].value_counts().reset_index()
total_titles.columns = ['Constructor', 'Titles']

# Visualizza
st.dataframe(total_titles)