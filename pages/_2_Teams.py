import streamlit as st
import pandas as pd
import plotly.express as px
import os
import random
from matplotlib.colors import to_rgb, to_hex
from streamlit_extras.stylable_container import stylable_container


st.set_page_config(page_title="Teams", page_icon="🏎️")

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
        if st.button("Drivers"):
            st.switch_page("pages/_1_Drivers.py")
    with col3:
        if st.button("Circuits"):
            st.switch_page("pages/_3_Circuits.py")
    with col4:
        if st.button("Trivial & Games"):
            st.switch_page("pages/_4_Trivial_&_Games.py")



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
drivers_path = os.path.join(current_directory, 'Datasets', 'drivers.csv')

# Carica i file CSV
constructors = pd.read_csv(constructors_path)
results = pd.read_csv(results_path)
races = pd.read_csv(races_path)
constructor_standings = pd.read_csv(constructor_standings_path)
drivers = pd.read_csv(drivers_path)

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
                  title=f"Selected Constructors: Final Points per Season ({start_year}–{end_year})",
                  #color_discrete_sequence=px.colors.sequential.YlOrRd
                  )
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


# Drivers belonging to the different Constructors teams
st.subheader("Drivers belonging to the different Constructors teams")

# 1. Unisci results con races per avere anno per ogni risultato
results_with_year = results.merge(races[['raceId', 'year']], on='raceId')

# 2. Filtra per anni nel periodo selezionato
results_filtered = results_with_year[
    (results_with_year['year'] >= start_year) &
    (results_with_year['year'] <= end_year)
]

# 3. Raggruppa per driverId, constructorId e estrai anni unici in cui ha corso in quel team nel periodo
driver_years = (
    results_filtered.groupby(['driverId', 'constructorId'])['year']
    .apply(lambda years: sorted(years.unique()))
    .reset_index()
)

# 4. Trasforma la lista anni in stringa per tooltip
driver_years['years_str'] = driver_years['year'].apply(lambda ylist: ", ".join(map(str, ylist)))

# 5. Aggiungi nomi pilota e team
driver_years = driver_years.merge(drivers[['driverId', 'forename', 'surname']], on='driverId')
driver_years = driver_years.merge(constructors[['constructorId', 'name']], on='constructorId')

# 6. Seleziona team da visualizzare
team_list = sorted(driver_years['name'].unique())

# Funzione per schiarire/scurire un colore (factor >1 schiarisce, <1 scurisce)
def adjust_color_lightness(color_hex, factor):
    rgb = to_rgb(color_hex)
    rgb_adjusted = tuple(min(max(c * factor, 0), 1) for c in rgb)
    return to_hex(rgb_adjusted)

# Colori ufficiali team famosi F1
team_colors = {
    "Alfa Romeo": "#E10600",
    "Ferrari": "#E10600",
    "Mercedes": "#00D2BE",
    "Red Bull": "#1E41FF",
    "McLaren": "#FF8700",
    "Alpine": "#2293D1",
    "Aston Martin": "#006F62",
    "Williams": "#005AFF",
}

# Seleziona team da visualizzare
team_list = sorted(driver_years['name'].unique())
selected_team = st.selectbox("Select Constructor Team", team_list)

# Colore base del team o colore random se non noto
if selected_team in team_colors:
    main_team_color = team_colors[selected_team]
else:
    main_team_color = random.choice(list(team_colors.values()))


# Filtra i piloti del team selezionato
team_drivers = driver_years[driver_years['name'] == selected_team]

# Lista anni del periodo selezionato
year_range = list(range(start_year, end_year + 1))

# Costruisci matrice presenza (1 se ha corso per il team quell'anno, altrimenti 0)
heatmap_data = []
pilot_names = []

for _, row in team_drivers.iterrows():
    years = row['year']
    name = f"{row['forename']} {row['surname']}"
    pilot_names.append(name)
    row_presence = [1 if y in years else 0 for y in year_range]
    heatmap_data.append(row_presence)

# DataFrame per heatmap
df_heatmap = pd.DataFrame(heatmap_data, index=pilot_names, columns=year_range)

# Crea heatmap con Plotly (senza legenda color)
fig = px.imshow(
    df_heatmap,
    labels=dict(x="Year", y="Driver"),
    color_continuous_scale=["#111111", main_team_color],  # nero = assente, colore team = presente
    aspect="auto"
)

# Rimuovi barra colore
fig.update_coloraxes(showscale=False)

# Layout grafico
fig.update_layout(
    title=f"{selected_team} drivers in selected period ({start_year}-{end_year})",
    xaxis_title="Year",
    yaxis_title="Driver",
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(color='white'),
    height=500,
    margin=dict(t=60, l=100, r=20, b=40)
)

# Mostra grafico
st.plotly_chart(fig, use_container_width=True)

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


st.markdown("""Data source: https://ergast.com/mrd/ 
            """)