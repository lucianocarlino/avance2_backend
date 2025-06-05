import math

import numpy as np
from app.core.exceptions import ApplyProduct, HighMalePercent
import generators

def simulate_tramps(hectares: int):
    Tramps = 0
    hectare = 0
    while hectare <= hectares:
        Tramps = Tramps + 1
        u = generators.parte_central_cuadrado(generators.get_seed(5), 5, 1)
        distance_to_tramp = 2 + 2 * u
        u = generators.parte_central_cuadrado(generators.get_seed(5), 5, 1)
        hectare = hectare + ((distance_to_tramp * -1) * math.log(u))

def read_tramps(days: int, tramps: int | None = None, adults: int | None = None) -> int:
    t = 0
    totals_cap = 0
    if ((days % 7) == 0):
        while t < tramps:
            u = generators.parte_central_cuadrado(generators.get_seed(5), 5, 1)
            capt_percent = 40 + 10 * u
            male_capt = int((adults / tramps) * capt_percent)
            totals_cap = totals_cap + male_capt
            if male_capt > 5:
                raise HighMalePercent()
            t += 1
    return totals_cap

def preventive_measures(larvaes:int, days_applied: int) -> int:
    while days_applied < 2:
        print("Aplicar producto preventivo") #TODO Esto no va asi
        larvaes = int(larvaes * 0.1)    
    print("Finalizar aplicación de producto preventivo")
    return larvaes

def egg_eclosion(eggs: int, insecticide_eggs: bool) -> int:
    if insecticide_eggs:
        u = generators.parte_central_cuadrado(generators.get_seed(5), 5, 1)
        eclosion_percent = 5 + 5 * u
    else:
        eclosion_percent = np.random.normal(loc=95, scale=2)
    larvaes = int((eggs * eclosion_percent) / 100)
    return larvaes

def update_population(totals_cap: int):
    u = generators.parte_central_cuadrado(generators.get_seed(5), 5, 1)
    male_percent = 40 + 10 * u 
    adults = totals_cap / male_percent
    female = adults - totals_cap
    H = 0
    eggs = 0
    while H < female:
        egg_per_female = np.random.poisson(lam=44)
        eggs += egg_per_female
        H += 1
    return eggs
