import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Teams", page_icon="🏎️")
st.title("Constructor Performance Analysis")
st.markdown("Explore key metrics and performance trends of F1 constructors from 1950 to today.")

# Load data
constructors = pd.read_csv("/workspaces/Formula-1-0/Datasets/constructors.csv")
constructor_standings = pd.read_csv("/workspaces/Formula-1-0/Datasets/constructor_standings.csv")
races = pd.read_csv("/workspaces/Formula-1-0/Datasets/races.csv")

# Merge datasets
constructor_standings = constructor_standings.merge(races[['raceId', 'year']], on='raceId')
constructor_standings = constructor_standings.merge(constructors[['constructorId', 'name']], on='constructorId')

# Definizione dei periodi
periods = {
    "1950–1959": (1950, 1959),
    "1960–1990": (1960, 1990),
    "1991–2009": (1991, 2009),
    "2010–2024": (2010, 2024)
}

# Selettore periodo
selected_period = st.selectbox("Select time period", list(periods.keys()))
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

# Section 1: Grafico punti finali
st.subheader("📈 Constructor Points")
yearly_points = final_standings.groupby(['year', 'name'])['points'].sum().reset_index()
yearly_points = yearly_points[(yearly_points['year'] >= start_year) & (yearly_points['year'] <= end_year)]

fig = px.line(yearly_points, x='year', y='points', color='name',
              title=f"Constructor Points at End of Season ({start_year}–{end_year})",
              labels={'points': 'Points', 'year': 'Year', 'name': 'Constructor'})
fig.update_layout(template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)


# Section 2: Vittorie stagionali finali
st.subheader("🏆 Constructor Wins per Season")
wins_per_year = final_standings.groupby(['year', 'name'])['wins'].sum().reset_index()
wins_per_year = wins_per_year[(wins_per_year['year'] >= start_year) & (wins_per_year['year'] <= end_year)]

fig2 = px.bar(wins_per_year, x="year", y="wins", color="name", barmode="group",
              labels={"wins": "Wins", "year": "Year", "name": "Constructor"},
              title=f"Wins by Constructor at End of Season ({start_year}–{end_year})")
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)


# Section 3: Final Championship Position
st.subheader("🎯 Final Standing Positions")
fig3 = px.line(filtered_standings, x="year", y="position", color="name",
               labels={"position": "Final Position", "year": "Year", "name": "Constructor"},
               title=f"Final Positions by Constructor ({start_year}–{end_year})")
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(template="plotly_dark")
st.plotly_chart(fig3, use_container_width=True)

# Sezione 4: Bar chart per confronto selezionati
st.subheader("🔍 Compare Constructors")

selected_teams = st.multiselect("Select Constructors", final_standings['name'].unique())

if selected_teams:
    filtered_df = final_standings[final_standings['name'].isin(selected_teams)]
    points_by_team = filtered_df.groupby(['year', 'name'])['points'].sum().reset_index()

    fig4 = px.bar(points_by_team, x="year", y="points", color="name", barmode="group",
                  labels={"points": "Points", "year": "Year", "name": "Constructor"},
                  title=f"Selected Constructors: Final Points per Season ({start_year}–{end_year})")
    fig4.update_layout(template="plotly_dark")
    st.plotly_chart(fig4, use_container_width=True)


# Section 5: Most Dominant per Decade
st.subheader("👑 Dominant Constructors by Decade")
constructor_standings['decade'] = (constructor_standings['year'] // 10) * 10
dominant = constructor_standings.groupby(['decade', 'name'])['wins'].sum().reset_index()
dominant = dominant.loc[dominant.groupby('decade')['wins'].idxmax()]
fig5 = px.bar(dominant, x="decade", y="wins", color="name",
              labels={"wins": "Total Wins", "decade": "Decade", "name": "Constructor"},
              title="Most Successful Constructor by Decade")
fig5.update_layout(template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

# Section 6: Extra Stats
st.subheader("🤔 Interesting Stats")

# 🏅 Total Titles
total_titles = constructor_standings[constructor_standings['position'] == 1].groupby('name').size().sort_values(ascending=False)
st.markdown("### 🏅 Constructors' Championship Titles")
st.dataframe(total_titles.rename("Titles"))

# 🌎 Most Consistent
most_consistent = constructor_standings.groupby('name')['position'].mean().sort_values()
st.markdown("### 🌎 Most Consistent Constructors (Avg. Final Position)")
st.dataframe(most_consistent.rename("Avg Position").round(2))

# 🧮 Average Points per Season (Filtered)
avg_points = filtered_standings.groupby('name')['points'].mean().sort_values(ascending=False)
st.markdown(f"### 🧮 Average Points per Season ({start_year}–{end_year})")
st.dataframe(avg_points.rename("Avg Points").round(2))

# 📈 Biggest Year-over-Year Improvement
improvement_df = filtered_standings.pivot_table(index='year', columns='name', values='points')
delta = improvement_df.diff().dropna()
max_improvements = delta.max().sort_values(ascending=False).head(10)
st.markdown(f"### 📈 Biggest Year-over-Year Improvements ({start_year}–{end_year})")
st.dataframe(max_improvements.rename("Max Point Gain").round(1))
