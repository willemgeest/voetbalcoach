import streamlit as st
from datetime import datetime
import pytz

from speler import Speler
from helpers import voorstel_wissels
import time

# Initialiseer sessievariabelen als ze nog niet bestaan
if 'tijd_in_seconden' not in st.session_state:
    st.session_state.tijd_in_seconden = 300

for var in ['spelers', 'erin', 'eruit', 'erin_def', 'eruit_def', 'keeper']:
    if var not in st.session_state:
        st.session_state[var] = []


# placeholder voor session state
placeholder4 = st.empty()
with placeholder4.container():
    st.write(st.session_state)
    st.write(len(st.session_state.spelers))
    # for speler in st.session_state.spelers:
    #     st.write(speler.__dict__)




# Titel van de app
st.title("Marvilde JO8-3 Wissel Management")

# Configuratie van spelers en wissels
speler_namen = ("Danielle", "Duuk", "Levi", "Bram", "Noah", "Rowdy", "Lott", "Tom", "Timme")


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
            st.session_state.spelers.sort(key=lambda x: x.keeper, reverse=True)
            for speler in st.session_state.spelers:
                if speler.in_veld:
                    bold = "**" if speler.keeper else ""
                    st.write(f'{bold}{speler.naam} (Wissels: {speler.n_wissels}, Laatste wissel: {speler.laatste_wissel}){bold}')

        with col2:
            st.header("Wisselspelers")
            for speler in st.session_state.spelers:
                if not speler.in_veld:
                    st.write(f'{speler.naam} (Wissels: {speler.n_wissels}, Laatste wissel: {speler.laatste_wissel})')

# Toon spelers bij de eerste render
toon_spelers()

placeholder2 = st.empty()
# Functie om de timer af te laten tellen
def start_timer():
    with placeholder2.container():
         # Placeholder voor het updaten van de timer in de app

        # Timer loop
        while st.session_state.tijd_in_seconden > 0:
            minutes, seconds = divmod(st.session_state.tijd_in_seconden, 60)
            formatted_time = f"{int(minutes)}:{int(seconds):02d}"

            # Update de placeholder met de resterende tijd
            placeholder2.title(f"Tijd tot de volgende wissel: {formatted_time}")

            # Wacht 1 seconde
            time.sleep(1)

            # Verminder de tijd met 1 seconde
            st.session_state.tijd_in_seconden -= 1


# placeholder voor wissels
placeholder3 = st.empty()

def toon_wissels():
    # mogelijkheden
    eruit = [speler.naam for speler in st.session_state.spelers if speler.in_veld]
    erin = [speler.naam for speler in st.session_state.spelers if
            not speler.in_veld and speler.doetmee]
    # default
    erin_voorstel = voorstel_wissels(
           spelers=[speler for speler in st.session_state.spelers if speler.in_veld],
            n=len(erin))
# else:
    #     st.session_state.eruit_def = st.session_state.eruit

    with placeholder3.container():
        col3, col4 = st.columns(2)
        with col3:
            st.session_state.eruit = st.multiselect(
                label="Wie gaan eruit?",
                options=eruit,
                default=erin_voorstel
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
        start_timer()


