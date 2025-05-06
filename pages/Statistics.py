import streamlit as st
import pandas as pd
import plotly.express as px
import os
# Carica e visualizza l'icona sopra il titolo
#st.image("/workspaces/Formula-1-0/Assets/icons/Statistics.png", width=100)  # Puoi regolare la larghezza come preferisci

st.title("Statistics - Qualifing")

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
st.markdown(f"## Qualifying Stats for {selected_driver}")

# Sezione 1: Posizione in Qualifica nel Tempo
st.subheader("📅 Qualifying Position Over Time")

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

# Sezione 2: Miglior Tempo in Qualifica
st.subheader("⏱️ Best Qualifying Time Over Time")

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

# Sezione 3: Qualifica vs Risultato Gara
st.subheader("🔁 Qualifying vs Race Result")

# Creiamo un grafico a dispersione per confrontare la posizione di grid e la posizione finale
fig3 = px.scatter(driver_data, x='grid', y='positionOrder', color='name', 
                  title="Qualifying Position vs Race Finish Position",
                  labels={'grid': 'Grid Position', 'positionOrder': 'Race Finish Position'})

# Aggiungiamo linee di riferimento sulla diagonale per visualizzare la corrispondenza
fig3.add_shape(
    type="line",
    x0=driver_data['grid'].min(), y0=driver_data['grid'].min(),
    x1=driver_data['grid'].max(), y1=driver_data['grid'].max(),
    line=dict(color="Red", width=2, dash="dash")
)

# Personalizzazione grafico
fig3.update_layout(
    xaxis=dict(title="Grid Position", autorange="reversed"),  # Invertiamo l'asse X per mostrare la miglior posizione a sinistra
    yaxis=dict(title="Race Finish Position", autorange="reversed"),  # Invertiamo l'asse Y per mostrare la miglior posizione in alto
    showlegend=False
)

st.plotly_chart(fig3, use_container_width=True)


# Sezione 4: Distribuzione Posizioni in Qualifica
st.subheader("📊 Distribution of Qualifying Positions")
fig4 = px.histogram(driver_data, x='position', nbins=20, title="Qualifying Position Histogram")
st.plotly_chart(fig4, use_container_width=True)

# Sezione 5: Performance per Circuito
st.subheader("🏟️ Average Qualifying Position per Circuit")
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
