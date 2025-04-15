import streamlit as st
import time
import random

st.title("Games")
st.write("""
Have fun with interactive quizzes and games:  

- 🔧 Simulatore di pitstop  
- ⏱️ Sfida ai tempi di reazione  
- E tanto altro!
""")

# SELEZIONE GIOCO
game_choice = st.radio("Choose your Game:", ["F1 Pitstop Challenge", "Reaction Time Challenge", "Box Strategy","Formula 1 Manager Simulation"])

# ========== GIOCO 1: PITSTOP CHALLENGE ==========

def pitstop_challenge():
    st.subheader("🔧 F1 Pitstop Challenge")
    st.write("**Will you complete the perfect Pitstop?**")
    st.write("🔧 Cambio gomme → ⛽ Rifornimento → 🧠 Strategia box")

    if "step" not in st.session_state:
        st.session_state.step = 0
        st.session_state.start_time = 0.0
        st.session_state.times = []
        st.session_state.best_time = None

    def reset_game():
        st.session_state.step = 0
        st.session_state.start_time = 0.0
        st.session_state.times = []

    if st.session_state.best_time:
        st.success(f"🏆 Best Time: **{st.session_state.best_time:.2f} seconds**")

    if st.session_state.step == 0:
        if st.button("🔁 Start your Pitstop!"):
            st.session_state.step = 1
            st.session_state.start_time = time.time()
            st.rerun()

    elif st.session_state.step == 1:
        st.write("🔧 **Cambio gomme in corso...**")
        time.sleep(random.uniform(0.5, 2.5))
        if st.button("✅ Cambio completato!"):
            elapsed = time.time() - st.session_state.start_time
            st.session_state.times.append(elapsed)
            st.session_state.start_time = time.time()
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.write("⛽ **Rifornimento in corso...**")
        time.sleep(random.uniform(0.5, 2))
        if st.button("✅ Rifornimento completato!"):
            elapsed = time.time() - st.session_state.start_time
            st.session_state.times.append(elapsed)
            st.session_state.start_time = time.time()
            st.session_state.step = 3
            st.rerun()

    elif st.session_state.step == 3:
        st.write("🧠 **Box Strategy Analysis...**")
        time.sleep(random.uniform(0.5, 1.5))
        if st.button("✅ Confirmed Strategy!"):
            elapsed = time.time() - st.session_state.start_time
            st.session_state.times.append(elapsed)
            total_time = sum(st.session_state.times)

            if total_time < 4:
                st.success(f"🟢 Perfect Pitstop : **{total_time:.2f} seconds, Ferrari is waiting for you!**")
            elif total_time < 6:
                st.warning(f"🟡 Buono ma migliorabile: **{total_time:.2f} seconds**")
            else:
                st.error(f"🔴 Too Slow! **{total_time:.2f} seconds**")

            if st.session_state.best_time is None or total_time < st.session_state.best_time:
                st.session_state.best_time = total_time
                st.balloons()
                st.success("🎉 New Record!")

    if st.button("🔁 Play Again!"):
        reset_game()
        st.session_state.step = 0
        st.rerun()

# ========== GIOCO 2: REACTION TIME CHALLENGE ==========

def reaction_time_challenge():
    st.subheader("⏱️ Reaction Time Challenge")
    st.write("Click when you see the GREEN light!")

    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "can_click" not in st.session_state:
        st.session_state.can_click = False
    if "start_time" not in st.session_state:
        st.session_state.start_time = 0
    if "reaction_time" not in st.session_state:
        st.session_state.reaction_time = None
    if "best_reaction" not in st.session_state:
        st.session_state.best_reaction = None

    def start_game():
        st.session_state.game_started = True
        st.session_state.can_click = False
        st.session_state.reaction_time = None
        wait_time = random.uniform(2, 5)
        st.write("🔴 Wait for Green...")
        time.sleep(wait_time)
        st.session_state.start_time = time.time()
        st.session_state.can_click = True
        st.rerun()

    def click_now():
        if st.session_state.can_click:
            reaction = time.time() - st.session_state.start_time
            st.session_state.reaction_time = reaction
            st.session_state.can_click = False
            if (
                st.session_state.best_reaction is None
                or reaction < st.session_state.best_reaction
            ):
                st.session_state.best_reaction = reaction

    if not st.session_state.game_started:
        if st.button("🎯 Start!"):
            start_game()
    elif st.session_state.can_click:
        if st.button("🟢 CLICK!"):
            click_now()
            st.rerun()
    else:
        if st.session_state.reaction_time is None:
            st.write("🔴 Wait...")
        else:
            reaction = st.session_state.reaction_time
            if reaction < 0.25:
                color = "🟢 Perfect!"
            elif reaction < 0.4:
                color = "🟡 Not bad..."
            else:
                color = "🔴 Too Slow!"
            st.write(f"**Reaction Time:** `{reaction:.3f} s` – {color}")
            if st.session_state.best_reaction:
                st.write(f"🏆 **Best time:** `{st.session_state.best_reaction:.3f} s`")
            if st.button("🎮 Retry"):
                st.session_state.game_started = False
                st.rerun()

# Funzione Box Strategy aggiornata senza countdown
def box_strategy():
    st.subheader("🧠 Box Strategy")
    st.write("Test your race engineering instincts! Choose the best pit strategy in dynamic race scenarios. Can you make the smartest calls under pressure?")

    # Modalità Hard
    mode = st.radio("Select difficulty:", ["Easy", "Hard"], key="mode_select")
    
    # Scenari in modalità Hard
    hard_scenarios = [
        {
            "situation": "Light rain is starting, and the Safety Car is on track.",
            "options": ["Stay out on slicks", "Pit for intermediates", "Pit for full wets"],
            "correct": 1
        },
        {
            "situation": "You're on soft tires in hot conditions, and they're heavily degraded.",
            "options": ["Extend the stint", "Pit for hard tires", "Pit for intermediates"],
            "correct": 1
        },
        {
            "situation": "Virtual Safety Car deployed; your pit window is open.",
            "options": ["Pit immediately", "Wait a lap", "Skip the stop"],
            "correct": 0
        },
        {
            "situation": "Heavy rain expected within two laps.",
            "options": ["Pit for intermediates now", "Stay out and wait", "Pit now for full wets"],
            "correct": 2
        },
        {
            "situation": "You just pitted for mediums, but a full Safety Car is deployed the next lap.",
            "options": ["Pit again and lose position", "Stay out and maintain track position", "Switch to softs now"],
            "correct": 1
        },
        {
            "situation": "The track is drying after heavy rain, and you're the first to pit.",
            "options": ["Pit for softs", "Pit for mediums", "Pit for hard tires"],
            "correct": 0
        },
        {
            "situation": "You're in the lead, but your tire wear is extremely high.",
            "options": ["Stay out for another lap", "Pit for softs", "Pit for hard tires"],
            "correct": 1
        },
        {
            "situation": "A rival team is undercutting you by pitting a lap earlier.",
            "options": ["Stay out", "Pit to cover the undercut", "Wait to see what they do"],
            "correct": 1
        },
        {
            "situation": "A full Safety Car is on track and you’re about to enter the pits.",
            "options": ["Pit now and gain position", "Stay out and gamble", "Wait for the Safety Car to finish a lap"],
            "correct": 0
        },
        {
            "situation": "The rain has stopped but the track is still damp.",
            "options": ["Pit for intermediates", "Pit for softs", "Stay out and push on slicks"],
            "correct": 1
        }
    ]

    # Impostazioni per la modalità facile (meno scenari)
    easy_scenarios = hard_scenarios[:5]

    # Scenari da usare in base alla modalità scelta
    scenarios = hard_scenarios if mode == "Hard" else easy_scenarios

    # Inizializza la sessione
    if "box_scenarios" not in st.session_state:
        st.session_state.box_scenarios = random.sample(scenarios, len(scenarios))
        st.session_state.current_box_question = 0
        st.session_state.box_score = 0
        st.session_state.box_feedback = ""
        st.session_state.box_done = False
        st.session_state.quiz_started = False  # Indica se il quiz è stato avviato, solo se non esiste

    # Se il quiz è stato avviato
    if not st.session_state.box_done:
        if not st.session_state.quiz_started:
            st.session_state.quiz_started = True  # Segna che il quiz è iniziato

        # Mostra la domanda e le opzioni
        q = st.session_state.box_scenarios[st.session_state.current_box_question]
        st.write(f"### Scenario {st.session_state.current_box_question + 1} of {len(scenarios)}")
        st.info(f"**Race Situation:** _{q['situation']}_")
        choice = st.radio("What would you do?", q["options"], key=f"box_q{st.session_state.current_box_question}")

        # Mostra la conferma della scelta
        if st.button("✅ Confirm Strategy"):
            if q["options"].index(choice) == q["correct"]:
                st.success("🎯 Perfect strategy call!")
                st.session_state.box_score += 1
                st.session_state.box_feedback = "✅ That was the ideal move for maximizing race pace and minimizing time loss."
            else:
                st.error("❌ That strategy wasn't optimal.")
                correct_option = q["options"][q["correct"]]
                st.session_state.box_feedback = f"📌 The best strategy would have been: **{correct_option}**."
            
            st.session_state.current_box_question += 1

            # Se il quiz è finito
            if st.session_state.current_box_question == len(scenarios):
                st.session_state.box_done = True
            st.rerun()

    else:
        # Feedback finale quando il quiz è completato
        st.success(f"🏁 You've completed all the scenarios! Your score: **{st.session_state.box_score}/{len(scenarios)}**")

        if st.session_state.box_score == len(scenarios):
            st.balloons()
            st.markdown("### 🏆 Excellent strategist! The pit wall needs you.")
        elif st.session_state.box_score >= len(scenarios) // 2:
            st.markdown("### 👍 Solid strategy skills! Keep refining your race instincts.")
        else:
            st.markdown("### 🤔 Strategy needs work. Try again and trust the data!")

        # Aggiungi un pulsante per ripartire da zero
        if st.button("🔁 Play Again"):
            # Reset delle variabili di sessione
            for key in list(st.session_state.keys()):
                if key.startswith("box_"):
                    del st.session_state[key]
            st.session_state.box_done = False
            st.session_state.current_box_question = 0
            st.rerun()

# Dati dei piloti (Esempio)
drivers = [
    "Max Verstappen", "Lewis Hamilton", "Charles Leclerc", "Lando Norris", 
    "George Russell", "Oscar Piastri", "Kimi Antonelli", "Fernando Alonso", 
    "Carlos Sainz", "Pierre Gasly"
]

gomme = ["Soft", "Medium", "Hard"]
assetti = ["High Downforce", "Low Downforce"]

# Nuovi eventi casuali
eventi_casuali = [
    "Safety car", "Unexpected Rain", "Technical failure", "No event", 
    "Perfect pit stop strategy", "Team pit stop error", "Tires overheating", "Strong wind"
]

# Funzione per scegliere il pilota, la strategia delle gomme e l'assetto
def simulazione_gara():
    st.title("Formula 1 Manager Simulation")

    # Seleziona pilota
    pilota_scelto = st.selectbox("Choose your driver:", drivers)
    
    # Seleziona le gomme
    gomme_scelte = st.selectbox("Choose tire strategy:", gomme)
    
    # Seleziona l'assetto
    assetto_scelto = st.selectbox("Choose car setup:", assetti)

    # Bottone per far partire la simulazione
    if st.button("🏁 Start Race"):
        evento = random.choice(eventi_casuali)

        # Calcolo risultato base
        if evento == "Safety car":
            risultato = f"Safety car deployment! You gain 5 positions."
        elif evento == "Unexpected Rain":
            if gomme_scelte == "Soft":
                risultato = f"Sudden rain! The soft tires lost grip, you lost 3 positions!"
            elif gomme_scelte == "Hard":
                risultato = f"Sudden rain! Hard tires held well, you gain 3 positions!"
            else:
                risultato = f"Medium tires are perfect for the rain, you maintain your position."
        elif evento == "Technical failure":
            risultato = f"Technical failure during the race, you lose 4 positions."
        elif evento == "Perfect pit stop strategy":
            risultato = f"Perfect pit stop strategy! You gain 6 positions."
        elif evento == "Team pit stop error":
            risultato = f"Team pit stop error! You lose 5 positions."
        elif evento == "Tires overheating":
            risultato = f"Tires overheating! You lose 2 positions due to reduced speed."
        elif evento == "Strong wind":
            risultato = f"Strong wind affects stability! You gain 1 position but your pace is slower."
        else:
            risultato = f"No major events! You gain 2 positions through a great strategy."

        # Commento tecnico extra
        if gomme_scelte == "Soft" and assetto_scelto == "Low Downforce":
            risultato += f" Your low downforce setup with soft tires made your car very fast on straights but unstable in corners."
        elif gomme_scelte == "Hard" and assetto_scelto == "High Downforce":
            risultato += f" The hard tires with high downforce gave you great stability but lacked speed."
        else:
            risultato += f" A balanced setup gave you consistent performance."

        # Mostra risultati solo dopo il bottone
        st.success(f"🌀 **Race Event:** {evento}")
        st.info(f"📊 **Result:** {risultato}")
    # Pulsante per fare di nuovo la simulazione (Play Again)
    if st.button("Play Again"):
        st.rerun()  # Ricarica la pagina per iniziare una nuova simulazione





# LANCIA IL GIOCO SELEZIONATO
if game_choice == "F1 Pitstop Challenge":
    pitstop_challenge()
elif game_choice == "Reaction Time Challenge":
    reaction_time_challenge()
elif game_choice == "Box Strategy":
    box_strategy()
elif game_choice == "Formula 1 Manager Simulation":
    simulazione_gara()

