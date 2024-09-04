import xml.dom

import streamlit as st
from datetime import datetime
import pytz

from speler import Speler
import time

# Initialiseer sessievariabelen als ze nog niet bestaan
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_start' not in st.session_state:
    st.session_state.timer_start = None
if 'resterende_tijd' not in st.session_state:
    st.session_state.resterende_tijd = 5 * 60  # 5 minuten in seconden

for var in ['spelers', 'erin', 'eruit', 'erin_def', 'eruit_def', 'keeper']:
    if var not in st.session_state:
        st.session_state[var] = []


# Titel van de app
st.title("Marvilde JO8-3 Wissel Management")

# Configuratie van spelers en wissels
speler_namen = sorted(["Danielle", "Duuk", "Levi", "Bram", "Noah", "Rowdy", "Lott", "Tom", "Timme"])


doetmee = st.multiselect(
    "Welke spelers doen mee",
    speler_namen,
    default=speler_namen
)

basis = st.multiselect(
    "Welke spelers staan basis?",
    doetmee,
    max_selections=6
)

aantal_wisselspelers = len(doetmee) - 6

st.session_state.keeper = st.selectbox("Wie is keeper", basis, index=None)

# Update de keeper status van alle spelers
for speler in st.session_state.spelers:
    speler.keeper = speler.naam == st.session_state.keeper

if len(basis) != 6 or st.session_state.keeper is None:
    st.write("Zorg dat er 6 spelers en 1 keeper geselecteerd worden.")

else:
    if len(st.session_state.spelers) == 0:
        for speler_naam in speler_namen:
            st.session_state.spelers.append(
                Speler(
                    naam=speler_naam,
                    doetmee=speler_naam in doetmee,
                    in_veld=speler_naam in basis,
                    keeper=speler_naam in st.session_state.keeper,
                    n_wissels=0 if speler_naam in basis else 1,
                    laatste_wissel= None if speler_naam in basis else datetime.now(pytz.timezone('Europe/Amsterdam')).strftime("%H:%M")
                )
            )


placeholder = st.empty()

def toon_spelers():
    with placeholder.container():  # Gebruik de placeholder om de nieuwe opstelling te tonen
        col1, col2 = st.columns(2)
        with col1:
            st.header("Huidige opstelling")
            st.session_state.spelers.sort(key=lambda x: (-x.keeper, -x.n_wissels, -x.laatste_wissel_sec, x.random_nr))
            speler_nr = 1
            for speler in st.session_state.spelers:
                if speler.in_veld:
                    if speler.keeper:
                        fmt = "**"
                    elif speler_nr > 6 - aantal_wisselspelers:
                        fmt = "*"
                    else:
                        fmt = ""
                    speler_nr += 1
                    st.write(f'{fmt}{speler.naam} (Wissels: {speler.n_wissels}, Laatste wissel: {speler.laatste_wissel}){fmt}')

        with col2:
            st.header("Wisselspelers")
            for speler in st.session_state.spelers:
                if not speler.in_veld and speler.doetmee:
                    st.write(f'{speler.naam} (Wissels: {speler.n_wissels}, Laatste wissel: {speler.laatste_wissel})')

# Toon spelers bij de eerste render
toon_spelers()

# placeholder voor wissels
placeholder3 = st.empty()


def toon_wissels():
    # mogelijkheden
    eruit = [speler.naam for speler in st.session_state.spelers if speler.in_veld and not speler.keeper]
    erin = [speler.naam for speler in st.session_state.spelers if speler.doetmee and not speler.in_veld]

    with placeholder3.container():
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.eruit = st.multiselect(
                label="Wie gaan eruit?",
                options=eruit,
                max_selections=len(erin)
                # default=erin_voorstel
            )

        with col4:
            st.session_state.erin = st.multiselect(
                label="Wie komen erin?",
                options=erin,
                default=erin
            )

toon_wissels()

if st.button("Wissel"):
    if len(st.session_state.eruit) != len(st.session_state.erin):
        st.write("Selecteer evenveel invallers als wissels.")
    else:
        for speler in st.session_state.spelers:
            if speler.naam in st.session_state.eruit:
                speler.gaat_eruit()
            if speler.naam in st.session_state.erin:
                speler.komt_erin()
        toon_wissels()
        toon_spelers()


# Functie om de timer af te laten tellen
def start_timer():
    if st.session_state.timer_start is None:  # Alleen starten als er geen timer loopt
        st.session_state.timer_start = time.time()
    # Placeholder voor het updaten van de timer in de app
    # placeholder2 = st.empty()
    with placeholder2.container():
        # Timer loop
        while st.session_state.resterende_tijd > 0:
            elapsed_time = time.time() - st.session_state.timer_start
            st.session_state.resterende_tijd = max(0, 5 * 60 - int(elapsed_time))
            minutes, seconds = divmod(st.session_state.resterende_tijd, 60)
            formatted_time = f"{int(minutes)}:{int(seconds):02d}"

            # Update de placeholder met de resterende tijd
            placeholder2.title(f"Tijd tot de volgende wissel: {formatted_time}")

            # Wacht 1 seconde
            time.sleep(1)

            # Verminder de tijd met 1 seconde
            # st.session_state.tijd_in_seconden -= 1

# Functie om de timer af te laten tellen
def update_timer():
    # Bereken de verstreken tijd sinds de timer startte
    elapsed_time = time.time() - st.session_state.timer_start
    st.session_state.resterende_tijd = max(0, 5 * 60 - int(elapsed_time))  # 5 minuten

    # Als de timer op is, laat een wisselmelding zien
    if st.session_state.resterende_tijd == 0:
        st.title("Wissel nu!")

    # Toon de resterende tijd
    minutes, seconds = divmod(st.session_state.resterende_tijd, 60)
    formatted_time = f"{int(minutes)}:{int(seconds):02d}"
    st.title(f"Tijd tot de volgende wissel: {formatted_time}")

# Startknop voor de timer
if st.button("(Her)start de wisseltimer"):
    st.session_state.timer_start = time.time()  # Stel de starttijd in
    st.session_state.timer_running = True  # Zet de timer op actief
    st.session_state.resterende_tijd = 5 * 60  # Stel de resterende tijd opnieuw in op 5 minuten

placeholder2 = st.empty()

# Als de timer loopt, blijf deze updaten
if st.session_state.timer_running:
    while st.session_state.resterende_tijd > 0:
        with placeholder2.container():
            update_timer()
        time.sleep(1)
    st.session_state.timer_running = False  # Stop de timer als de tijd op is
else:
    # Toon de laatste resterende tijd wanneer de timer niet loopt
    minutes, seconds = divmod(st.session_state.resterende_tijd, 60)
    formatted_time = f"{int(minutes)}:{int(seconds):02d}"
    placeholder2.title(f"Tijd tot de volgende wissel: {formatted_time}")

# if st.button("(Her)start timer"):
#     start_timer()


    # placeholder voor session state
# placeholder4 = st.empty()
# with placeholder4.container():
#     st.write(st.session_state)
#     st.write(len(st.session_state.spelers))
    # for speler in st.session_state.spelers:
    #     st.write(speler.__dict__)
