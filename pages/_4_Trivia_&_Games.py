import streamlit as st
import random
import time

# Carica e visualizza l'icona sopra il titolo
#st.image("/workspaces/Formula-1-0/Assets/icons/Trivia.png", width=100)  # Puoi regolare la larghezza come preferisci

st.title("F1 Trivia & Games!")

st.write("""
Learn about legendary records, funny moments, and rare stats in Formula 1 history.  
Great for both fans and newcomers.
""")

# Trivia Questions (Expanded List)
questions = [
    {
        "question": "Which driver holds the record for the most Formula 1 World Championships?",
        "options": ["Michael Schumacher", "Ayrton Senna", "Sebastian Vettel", "Juan Manuel Fangio"],
        "answer": "Michael Schumacher",
        "fun_fact": "Fun Fact: Michael Schumacher holds the record for most consecutive world titles, with 5 in a row!"
    },
    {
        "question": "What year did the first Formula 1 World Championship take place?",
        "options": ["1945", "1950", "1955", "1960"],
        "answer": "1950",
        "fun_fact": "Fun Fact: The first ever F1 World Championship race took place at Silverstone in 1950!"
    },
    {
        "question": "Which team won the Constructors' Championship in 2021?",
        "options": ["Mercedes", "Red Bull Racing", "Ferrari", "McLaren"],
        "answer": "Mercedes",
        "fun_fact": "Fun Fact: Mercedes won the Constructors' Championship in 2021, marking their 8th consecutive win!"
    },
    {
        "question": "Who is the youngest driver to start a Formula 1 race?",
        "options": ["Max Verstappen", "Sebastian Vettel", "Lando Norris", "Charles Leclerc"],
        "answer": "Max Verstappen",
        "fun_fact": "Fun Fact: Max Verstappen was just 17 years old when he made his F1 debut in 2015, breaking records!"
    },
    {
        "question": "Which driver once raced in an F1 race with a broken back?",
        "options": ["Fernando Alonso", "Jenson Button", "Kimi Räikkönen", "Michael Schumacher"],
        "answer": "Fernando Alonso",
        "fun_fact": "Fun Fact: Fernando Alonso once raced with a broken back after a crash during pre-season testing. #Legend"
    },
    {
        "question": "True or False: The first Formula 1 car had no seat belts.",
        "options": ["True", "False"],
        "answer": "True",
        "fun_fact": "Fun Fact: The first F1 car was a bare-bones machine, and surprisingly, it had no seat belts for safety!"
    },
    {
        "question": "Which F1 driver once tried to drive a lawn mower?",
        "options": ["Kimi Räikkönen", "Daniel Ricciardo", "Sebastian Vettel", "Lando Norris"],
        "answer": "Kimi Räikkönen",
        "fun_fact": "Fun Fact: Kimi Räikkönen, known for his cool demeanor, once tried to drive a lawn mower during a post-race celebration. Classic Kimi!"
    },
    {
        "question": "Who was the first female driver to participate in a Formula 1 race?",
        "options": ["Lella Lombardi", "Danica Patrick", "Maria Teresa de Filippis", "Susie Wolff"],
        "answer": "Maria Teresa de Filippis",
        "fun_fact": "Fun Fact: Maria Teresa de Filippis was the first woman to race in Formula 1 in the 1950s!"
    },
    {
        "question": "Which driver has the most pole positions in Formula 1?",
        "options": ["Lewis Hamilton", "Michael Schumacher", "Ayrton Senna", "Sebastian Vettel"],
        "answer": "Lewis Hamilton",
        "fun_fact": "Fun Fact: Lewis Hamilton holds the record for the most pole positions in F1, surpassing Ayrton Senna and Michael Schumacher!"
    },
    {
        "question": "What is the nickname of the Monaco Grand Prix?",
        "options": ["The Grandest Race", "The King of F1", "The Crown Jewel", "The Race of Kings"],
        "answer": "The Crown Jewel",
        "fun_fact": "Fun Fact: The Monaco Grand Prix is often referred to as 'The Crown Jewel' of F1 due to its prestige and glitz!"
    },
    {
        "question": "Which driver famously said, 'To finish first, first you must finish'?",
        "options": ["Mario Andretti", "Ayrton Senna", "Jenson Button", "Denny Hulme"],
        "answer": "Mario Andretti",
        "fun_fact": "Fun Fact: Mario Andretti, the legendary American F1 driver, is famous for this memorable piece of racing wisdom."
    },
    {
        "question": "Which F1 driver once raced with a personalized ‘thumbs up’ helmet design?",
        "options": ["Valtteri Bottas", "Mick Schumacher", "Sebastian Vettel", "Daniel Ricciardo"],
        "answer": "Sebastian Vettel",
        "fun_fact": "Fun Fact: Sebastian Vettel's 'thumbs up' helmet became iconic during his dominant years with Red Bull Racing!"
    },
    {
        "question": "Who is the youngest-ever F1 world champion?",
        "options": ["Sebastian Vettel", "Lewis Hamilton", "Max Verstappen", "Fernando Alonso"],
        "answer": "Sebastian Vettel",
        "fun_fact": "Fun Fact: Sebastian Vettel became the youngest-ever F1 World Champion in 2010 at the age of 23!"
    },
    {
        "question": "Which F1 team has the most wins in history?",
        "options": ["Ferrari", "Mercedes", "Red Bull Racing", "McLaren"],
        "answer": "Ferrari",
        "fun_fact": "Fun Fact: Ferrari holds the record for the most wins in F1 history, having a legacy that spans over 70 years!"
    },
    {
        "question": "Which driver holds the record for the most race wins in a single season?",
        "options": ["Michael Schumacher", "Alain Prost", "Sebastian Vettel", "Nigel Mansell"],
        "answer": "Sebastian Vettel",
        "fun_fact": "Fun Fact: Sebastian Vettel won 13 races in 2013, a record for the most wins in a single F1 season!"
    },
    {
        "question": "What is the maximum number of points a driver can score in a single race, excluding sprint races?",
        "options": ["25", "30", "50", "100"],
        "answer": "26",
        "fun_fact": "Fun Fact: The maximum points a driver can earn in a regular race is 26, including the extra point for the fastest lap!"
    },
    {
        "question": "True or False: The 2020 F1 season was the first to have 17 races in a calendar year due to COVID-19 restrictions.",
        "options": ["True", "False"],
        "answer": "True",
        "fun_fact": "Fun Fact: The 2020 season was heavily affected by the pandemic, and the calendar had to be revised to a record-low number of races!"
    },
    {
        "question": "Which F1 driver is known for his famous 'shoey' celebration?",
        "options": ["Daniel Ricciardo", "Kimi Räikkönen", "Lewis Hamilton", "Sebastian Vettel"],
        "answer": "Daniel Ricciardo",
        "fun_fact": "Fun Fact: Daniel Ricciardo became famous for celebrating his podium finishes by drinking champagne from his racing shoe—#Shoey!"
    },
    {
        "question": "What is the most number of laps ever completed in a single F1 race?",
        "options": ["300", "350", "400", "500"],
        "answer": "500",
        "fun_fact": "Fun Fact: The most laps completed in an F1 race is 500, which happened during the 1954 French Grand Prix!"
    },
    {
        "question": "Who holds the record for the most Grand Prix wins without a World Championship title?",
        "options": ["Stirling Moss", "Chris Amon", "Riccardo Patrese", "Jean Alesi"],
        "answer": "Stirling Moss",
        "fun_fact": "Fun Fact: Stirling Moss is widely considered the greatest F1 driver never to win a World Championship title!"
    },
    {
        "question": "Which F1 driver has the most wins at the British Grand Prix?",
        "options": ["Lewis Hamilton", "Nigel Mansell", "Jim Clark", "Ayrton Senna"],
        "answer": "Lewis Hamilton",
        "fun_fact": "Fun Fact: Lewis Hamilton has won the British Grand Prix more times than any other driver in history!"
    },
    {
        "question": "Which circuit is known for its ‘beach’ section?",
        "options": ["Monaco", "Bahrain", "Singapore", "Australia"],
        "answer": "Bahrain",
        "fun_fact": "Fun Fact: The Bahrain Grand Prix circuit is unique for having a 'beach' section, making it stand out from the rest!"
    },
    {
        "question": "Lewis Hamilton has won 100 Formula 1 races.",
        "options": ["True", "False"],
        "answer": "True",
        "fun_fact": "He reached 100 wins at the 2021 Russian Grand Prix!"
    },
    {
        "question": "Ferrari is the only team to have competed in every Formula 1 season.",
        "options": ["True", "False"],
        "answer": "True",
        "fun_fact": "Ferrari has been part of F1 since 1950, making them the oldest and most iconic team."
    },
    {
        "question": "Sebastian Vettel won his championships with Ferrari.",
        "options": ["True", "False"],
        "answer": "False",
        "fun_fact": "He won all 4 titles with Red Bull from 2010 to 2013."
    },
    {
        "question": "Formula 1 cars use diesel engines.",
        "options": ["True", "False"],
        "answer": "False",
        "fun_fact": "They use hybrid V6 turbocharged petrol engines with electrical recovery systems."
    },
    {
        "question": "The Singapore Grand Prix is a night race.",
        "options": ["True", "False"],
        "answer": "True",
        "fun_fact": "It was the first night race in F1, debuting in 2008."
    },
    {
        "question": "Kimi Räikkönen was known as 'The Professor'.",
        "options": ["True", "False"],        
        "answer": "False",
        "fun_fact": "That was Alain Prost; Kimi was 'The Iceman' for his cool demeanor."
    }
]
# Setup session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)
if "answered" not in st.session_state:
    st.session_state.answered = False



# Trivia section
st.subheader("F1 Trivia Time!")
# Display score
st.write(f"Current score: {st.session_state.score}")

q = st.session_state.current_question
user_answer = st.radio(q["question"], q["options"], key=q["question"])

# Button to submit answer
if st.button("Submit Answer") and not st.session_state.answered:
    if user_answer == q["answer"]:
        st.session_state.score += 1
        st.success(f"Correct! +1 Point! Your score: {st.session_state.score}")
    else:
        st.error(f"Wrong! The correct answer was **{q['answer']}**.")
    st.info(f"🔍 {q['fun_fact']}")
    st.session_state.answered = True

# Button to go to next question
if st.session_state.answered:
    if st.button("Next Question"):
        st.session_state.current_question = random.choice(questions)
        st.session_state.answered = False
        
            
# Restart trivia button
if st.button("Restart Trivia"):
    st.session_state.score = 0
    st.rerun()

st.subheader("Games!")
st.write("""
Have fun with interactive games! 
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
        time.sleep(random.uniform(0.5, 1.5))
        if st.button("✅ Cambio completato!"):
            elapsed = time.time() - st.session_state.start_time
            st.session_state.times.append(elapsed)
            st.session_state.start_time = time.time()
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.write("⛽ **Rifornimento in corso...**")
        time.sleep(random.uniform(0.5, 1.5))
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
            if reaction < 0.6:
                color = "🟢 Perfect!"
            elif reaction < 0.76:
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

