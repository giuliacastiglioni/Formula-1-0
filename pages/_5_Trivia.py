import streamlit as st
import random

# Carica e visualizza l'icona sopra il titolo
#st.image("/workspaces/Formula-1-0/Assets/icons/Trivia.png", width=100)  # Puoi regolare la larghezza come preferisci

st.title("F1 Trivia & Fun Facts")

st.write("""
Learn about legendary records, funny moments, and rare stats in Formula 1 history.  
Great for both fans and newcomers.
""")

# Trivia Questions (Expanded List)
questions = [
    {
        "question": "Which driver holds the record for the most Formula 1 World Championships?",
        "options": ["Michael Schumacher", "Lewis Hamilton", "Sebastian Vettel", "Juan Manuel Fangio"],
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

# Display score
st.write(f"🏆 Current score: {st.session_state.score}")

# Trivia section
st.subheader("🏁 F1 Trivia Time!")

q = st.session_state.current_question
user_answer = st.radio(q["question"], q["options"], key=q["question"])

# Button to submit answer
if st.button("Submit Answer") and not st.session_state.answered:
    if user_answer == q["answer"]:
        st.session_state.score += 1
        st.success(f"🎉 Correct! +1 Point! Your score: {st.session_state.score}")
    else:
        st.error(f"❌ Wrong! The correct answer was **{q['answer']}**.")
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