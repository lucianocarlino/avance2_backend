from Backend.app.core.MEF.mef import MEF
import utilities 
import numpy as np

def simulation(hectares: float, tramps:int | None = None, insecticide_eggs: bool = True, prev_larvaes: int = None) -> int:
    """
    Simulate the number of tramps in a given area of hectares.
    
    :param hectares: The number of hectares to simulate.
    :param tramps: The number of tramps to simulate, if known.
    :return: The number of tramps simulated.
    """
    days_to_simulate = 243 #Represents 8 months, from August to March
    day = 1
    acumulated_carpogrades = 0
    larvaes = 0
    adults = 0 
    eggs = 0
    days_applied = 0
    totals_cap = 0
    evolute_poblation = True

    # Simulate the carpogrades to start the third-generation moths
    u = utilities.parte_central_cuadrado(utilities.get_seed(5), 5, 1)
    third_generation_carpogrades = 750 + 50 * u

    mean_temperatures_table = {
        ("Agosto", 31) : ("Septiembre", 3.3, 19.4),
        ("Septiembre", 61) : ("Octubre", 6.8, 22.8),
        ("Octubre", 92) : ("Noviembre", 9.7, 26.4),
        ("Noviembre", 122) : ("Diciembre", 12.3, 29.3),
        ("Diciembre", 153) : ("Enero", 13.4, 30.7),
        ("Enero", 184) : ("Febrero", 12.3, 29.5),
        ("Febrero", 212) : ("Agosto", 9.6, 26.3)
    }

    # Lambda function to toggle evolute_poblation
    toggle_evolute_poblation = lambda: not evolute_poblation

    carpogrades_table = {
        ("Larvas diapausantes", 90): ("Vuelos", toggle_evolute_poblation),
        ("Vuelos", 250): ("Larvas", toggle_evolute_poblation),
        ("Larvas", 450): ("Vuelos", toggle_evolute_poblation),
        ("Vuelos", third_generation_carpogrades): ("Larvas", toggle_evolute_poblation),
        ("Larvas", 1750): ("Vuelos", toggle_evolute_poblation),
    }

    # If tramps is not provided, simulate the number of tramps
    if tramps is None:
        tramps = utilities.simulate_tramps(hectares)

    mean_temperatures_mef = MEF("Agosto", mean_temperatures_table, 9.6, 26.3)
    carpogrades_mef = MEF("Larvas diapausantes", carpogrades_table)

    # Main simulation loop
    while day <= days_to_simulate:
        
        #MEF to get the mean temperatures whitout using ifs
        mean_temperatures_mef.transition(day)

        #Carpogrades calculus
        max_temp = np.random.normal(loc=mean_temperatures_mef.min_mean, scale=5)
        min_temp = np.random.normal(loc=mean_temperatures_mef.max_mean, scale=5)

        carpogrados = ((max_temp - min_temp)/2) - 10

        if carpogrados > 0:
            acumulated_carpogrades += carpogrados

        #MEF to get the poblation state
        carpogrades_mef.transition(day)

        #Evolute poblation 
        if carpogrades_mef.state == "Vuelos" and evolute_poblation:
            adults = larvaes
            totals_cap = utilities.read_tramps(day, tramps, adults)
            eggs = utilities.update_population(totals_cap)
            evolute_poblation = False

        
        if carpogrades_mef.state == "Larvas" and evolute_poblation:
            if days_applied == 0:
                larvaes = utilities.egg_eclosion(eggs, insecticide_eggs)
            if days_applied < 2:
                utilities.preventive_measures(larvaes, days_applied)
                days_applied += 1
                evolute_poblation = False

        day += 1
    return tramps