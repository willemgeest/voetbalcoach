from datetime import datetime
from time import gmtime, strftime, time
from typing import Optional

import pytz


class Speler:
    def __init__(
            self,
            naam: str,
            doetmee: bool,
            n_wissels: int,
            in_veld: bool,
            keeper: bool,
            laatste_wissel: Optional[str]
    ):
        self.laatste_wissel = laatste_wissel
        self.naam = naam
        self.doetmee = doetmee
        self.n_wissels = n_wissels
        self.in_veld = in_veld
        self.keeper = keeper
        self.laatste_wissel_sec = 0


    def gaat_eruit(self):
        self.n_wissels += 1
        self.in_veld = False
        self.laatste_wissel = datetime.now(pytz.timezone('Europe/Amsterdam')).strftime("%H:%M")
        self.laatste_wissel_sec = int(time())

    def komt_erin(self):
        self.in_veld = True





