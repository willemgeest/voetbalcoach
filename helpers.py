from speler import Speler
from typing import List
import random

def voorstel_wissels(spelers: List[Speler], n: int):
    # keeper kan nooit gewisseld worden
    spelers = [speler for speler in spelers if not speler.keeper]
    # sorteer op aantal wissels, laatste wissel
    spelers = sorted(spelers, key=lambda x: (x.n_wissels, x.laatste_wissel, random.random()))
    # return de eerste n speler namen
    return [speler.naam for speler in spelers][:n]

