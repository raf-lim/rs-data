from typing import Iterable
from updaters.eu.interfaces import EsiMetric


class Esi:
    code = 'BS-ESI-I'
    name = 'ESI'


class Indu:
    code = 'BS-ICI-BAL'
    name = 'INDU'


class Serv:
    code = 'BS-SCI-BAL'
    name = 'SERV'


class Cons:
    code = 'BS-CSMCI-BAL'
    name = 'CONS'


class Reta:
    code = 'BS-RCI-BAL'
    name = 'RETA'


class Buil:
    code = 'BS-CCI-BAL'
    name = 'BUIL'


esi_metrics: Iterable[EsiMetric] = [Esi, Indu, Serv, Cons, Reta, Buil]
