import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica e visualizza l'icona sopra il titolo
#st.image("/workspaces/Formula-1-0/Assets/icons/helmet_1850740.png", width=100)  # Puoi regolare la larghezza come preferisci
# Titolo
st.title("Drivers")

st.write("""
Here you’ll find all the current Formula 1 drivers.  
We'll include statistics, bios, comparisons, and more.
""")



# Carica i dati (assumiamo che i CSV siano caricati in variabili dataframes)
drivers_df = pd.read_csv('/workspaces/Formula-1-0/Datasets/drivers.csv')
driver_standings_df = pd.read_csv('/workspaces/Formula-1-0/Datasets/driver_standings.csv')
results_df = pd.read_csv('/workspaces/Formula-1-0/Datasets/results.csv')
races_df = pd.read_csv('/workspaces/Formula-1-0/Datasets/races.csv')



# Funzione per estrarre i piloti che soddisfano i criteri
def get_drivers_by_period(period):
    if period == "1950-1980":
        # Piloti che hanno vinto almeno un mondiale
        # Uniamo driver_standings_df con races_df per ottenere l'anno della gara
        standings_with_year = pd.merge(driver_standings_df, races_df[['raceId', 'year']], on='raceId', how='left')
        
        # Filtro per i dati delle gare fino al 1980
        standings_per_year = standings_with_year[standings_with_year['year'] <= 1980]
        
        # Sommiamo i punti per ogni pilota in ogni stagione
        total_points_per_year = standings_per_year.groupby(['driverId', 'year'])['points'].sum().reset_index()
        
        # Troviamo il pilota con il punteggio massimo per ogni anno (vincitore del mondiale)
        world_champions = total_points_per_year.loc[total_points_per_year.groupby('year')['points'].idxmax()]
        
        # Estraiamo i driverId dei piloti che hanno vinto almeno un mondiale
        drivers = world_champions['driverId'].unique()
        
        # Numero di mondiali vinti da ciascun pilota
        world_titles = world_champions.groupby('driverId').size()
        
        criterion = "Drivers who have won at least one World Championship."
    elif period == "1981-2008":
        # Piloti con almeno 3 vittorie
        winners = driver_standings_df[driver_standings_df['wins'] >= 3]
        winners = winners[winners['raceId'].isin(races_df[races_df['year'].between(1981, 2008)]['raceId'])]
        drivers = winners['driverId'].unique()
        
        # Numero di gare vinte da ciascun pilota nel periodo 1981-2008
        race_wins = results_df[results_df['driverId'].isin(drivers) & (results_df['raceId'].isin(races_df[races_df['year'].between(1981, 2008)]['raceId']))]
        race_wins = race_wins[race_wins['positionOrder'] == 1]
        race_wins_count = race_wins.groupby('driverId').size()
        
        criterion = "Drivers who have won at least 3 races."
    elif period == "2009-2013":
        # Piloti con almeno 3 vittorie
        winners = driver_standings_df[driver_standings_df['wins'] >= 1]
        winners = winners[winners['raceId'].isin(races_df[races_df['year'].between(2009, 2013)]['raceId'])]
        drivers = winners['driverId'].unique()
        
        # Numero di gare vinte da ciascun pilota nel periodo 2009-2013
        race_wins = results_df[results_df['driverId'].isin(drivers) & (results_df['raceId'].isin(races_df[races_df['year'].between(2009, 2013)]['raceId']))]
        race_wins = race_wins[race_wins['positionOrder'] == 1]
        race_wins_count = race_wins.groupby('driverId').size()
        
        criterion = "Drivers who have won at least 1 race."
    elif period == "2014-2023":
        # Piloti che hanno ottenuto almeno un punto (quindi sono andati a punti)
        drivers_with_points = driver_standings_df[driver_standings_df['points'] > 0]
        drivers_with_points = drivers_with_points[drivers_with_points['raceId'].isin(races_df[races_df['year'].between(2014, 2023)]['raceId'])]
        drivers = drivers_with_points['driverId'].unique()

        # Numero di gare vinte da ciascun pilota nel periodo 2014-2023
        race_wins = results_df[results_df['driverId'].isin(drivers) & (results_df['raceId'].isin(races_df[races_df['year'].between(2014, 2023)]['raceId']))]
        race_wins = race_wins[race_wins['positionOrder'] == 1]
        race_wins_count = race_wins.groupby('driverId').size()

        criterion = "Drivers who have scored at least one point."

    elif period == "2024":
        # Tutti i piloti che hanno partecipato al 2024
        race_ids_2024 = races_df[races_df['year'] == 2024]['raceId']
        drivers_2024 = results_df[results_df['raceId'].isin(race_ids_2024)]['driverId'].unique()

        # Calcola i punti per ogni pilota nel 2024
        points_2024 = results_df[results_df['raceId'].isin(race_ids_2024)]
        points_2024 = points_2024.groupby('driverId')['points'].sum()

        drivers = drivers_2024
        criterion = "All drivers who participated in the 2024 season."

        # Aggiungi i punti ottenuti a ciascun pilota nel 2024
        return drivers, points_2024, criterion
    
    else:
        drivers = []
        criterion = "No criteria selected."

    return drivers, world_titles if period == "1950-1980" else race_wins_count, criterion

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
    elif period == "1998-2008":
        race_ids = races_df[races_df['year'].between(1998, 2008)]['raceId']
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

# Funzione per visualizzare i grafici con uno stile adatto
def plot_performance(performance, period):
    st.write(f"### Average Position, Victories and Podiums for {period}")
    st.dataframe(performance)

    # Line chart per visualizzare la posizione media nel tempo per ciascun pilota
    st.write("**Average Position (Lower is Better)**")
    fig, ax = plt.subplots(figsize=(10, 6))
    performance.set_index('code')['Average Position'].plot(kind='line', color='red', marker='o', ax=ax)
    ax.set_title(f'Average Position per Driver in {period}', fontsize=16)
    ax.set_ylabel('Average Position', fontsize=12)
    ax.set_xlabel('Driver Code', fontsize=12)
    ax.grid(True, linestyle='--', color='white', alpha=0.3)
    st.pyplot(fig)

    # Bar chart per il numero di vittorie e podi
    fig, ax = plt.subplots(figsize=(10, 6))
    performance.set_index('code')[['Victories', 'Podiums']].plot(kind='bar', stacked=True, color=['gold', 'silver'], ax=ax)
    ax.set_title(f'Victories and Podiums per Driver in {period}', fontsize=16)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_xlabel('Driver Code', fontsize=12)
    ax.grid(True, linestyle='--', color='white', alpha=0.3)
    st.pyplot(fig)

# Funzione per analizzare l'evoluzione di un pilota nel tempo
def analyze_driver_evolution(driver_id):
    results_driver = results_df[results_df['driverId'] == driver_id]
    results_driver = results_driver.merge(races_df[['raceId', 'year']], on='raceId')
    avg_position_per_year = results_driver.groupby('year')['positionOrder'].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    avg_position_per_year.plot(kind='line', marker='o', color='red', ax=ax)
    ax.set_title(f'Evolution of Driver {driver_id} Performance Over Time', fontsize=16)
    ax.set_ylabel('Average Position', fontsize=12)
    ax.set_xlabel('Year', fontsize=12)
    ax.grid(True, linestyle='--', color='white', alpha=0.3)
    st.pyplot(fig)


def compare_drivers(period):
    # Ottieni la performance dei piloti per il periodo specificato
    performance = analyze_performance_by_period(period)
    
    # Crea un grafico a barre per le vittorie
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Ordina i piloti in base al numero di vittorie
    performance.sort_values(by='Victories', ascending=False, inplace=True)
    
    # Usa il 'code' dei piloti come etichetta per l'asse X
    performance['Victories'].plot(kind='bar', color='gold', ax=ax)
    
    # Imposta il titolo, etichette degli assi e altre proprietà del grafico
    ax.set_title(f'Victories per Driver in {period}', fontsize=16)
    ax.set_ylabel('Victories', fontsize=12)
    ax.set_xlabel('Driver (Code)', fontsize=12)
    
    # Aggiungi i codici dei piloti all'asse X
    ax.set_xticks(range(len(performance)))
    ax.set_xticklabels(performance['code'], rotation=45, ha='right', fontsize=10)
    
    # Aggiungi una griglia e imposta il suo stile
    ax.grid(True, linestyle='--', color='white', alpha=0.3)
    
    # Mostra il grafico
    st.pyplot(fig)
    
# Visualizza i piloti in base al periodo selezionato
def display_drivers_by_period():
    period = st.selectbox("Select the Period", ["1950-1980", "1981-2008", "2009-2013", "2014-2023", "2024"])
    drivers_ids, result_or_points, criterion = get_drivers_by_period(period)
    
    # Filtra i piloti dal dataframe dei piloti
    selected_drivers = drivers_df[drivers_df['driverId'].isin(drivers_ids)]
    # Aggiungi il numero di mondiali o gare vinte per ogni pilota
    if period == "1950-1980":
        world_titles = result_or_points
        selected_drivers['World Titles'] = selected_drivers['driverId'].map(world_titles).fillna(0).astype(int)
        selected_drivers = selected_drivers.sort_values(by='World Titles', ascending=False)
    elif period in ["1981-2008", "2009-2013", "2014-2023"]:
        race_wins_count = result_or_points
        selected_drivers['Race Wins'] = selected_drivers['driverId'].map(race_wins_count).fillna(0).astype(int)
        selected_drivers = selected_drivers.sort_values(by='Race Wins', ascending=False)
    elif period == "2024":
        selected_drivers['Points'] = selected_drivers['driverId'].map(result_or_points).fillna(0).astype(int)
        selected_drivers = selected_drivers.sort_values(by='Points', ascending=False)  # Ordinamento in base ai punti
        st.write(f"**Criteria for {period}:** {criterion}")
        st.dataframe(selected_drivers[['forename', 'surname', 'nationality', 'Points']])
        return
    # Mostra il criterio
    st.write(f"**Criteria for {period}:** {criterion}")
    
    # Mostra i piloti con il numero di gare vinte, mondiali o punti
    if period == "1950-1980":
        st.dataframe(selected_drivers[['forename', 'surname', 'nationality', 'World Titles']])
    elif period in ["1981-2008", "2009-2013","2014-2023"]:
        st.dataframe(selected_drivers[['forename', 'surname', 'nationality', 'Race Wins']])

    # Visualizza le statistiche in una sezione separata
    st.title("Drivers statistics")
    # Scegli il periodo per analizzare le performance
    period = st.selectbox("Select the Period", ["1998-2008","2009-2013","2014-2023", "2024"])
    performance = analyze_performance_by_period(period)
    analyze_performance_by_period(period)
    plot_performance(performance, period)
    compare_drivers(period)
    # Scegli il pilota per analizzare l'evoluzione
    driver_name = st.selectbox("Select a Driver", drivers_df['forename'] + ' ' + drivers_df['surname'])
    driver_id = drivers_df[drivers_df['forename'] + ' ' + drivers_df['surname'] == driver_name].iloc[0]['driverId']
    analyze_driver_evolution(driver_id)
    

# Esegui la funzione
display_drivers_by_period()



