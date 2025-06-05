from MEF.mef import MEF
import utilities 
import generators
import numpy as np
import json

def simulation(hectares: float, cost_per_hectare: float, tramps:int | None = None, insecticide_eggs: bool = True, prev_larvaes: int = None) -> str:
    """
    Simulate the number of tramps in a given area of hectares.

    :param hectares: The number of hectares to simulate.
    :param tramps: The number of tramps to simulate, if known.
    :return: The simulation result as a JSON string.
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
    generation = 0
    cost_per_hectare = 0.5  
    total_hectare_cost = hectares * cost_per_hectare
    data = {
        "aplicacionInsecticidas": [{}],
        "acumulacionCarpogrados": [{}],
        "analisisEconomico": [{}],
        "eficaciaPrograma": [{}],
    }

    # Simulate the carpogrades to start the third-generation moths
    u = generators.parte_central_cuadrado(generators.get_seed(5), 5, 1)
    third_generation_carpogrades = 750 + 100 * u["resultado"][0]

    mean_temperatures_table = {
        #(Estado, evento) : (Estado siguiente, accion)
        ("Agosto", 31) : ("Septiembre", 3.3, 19.4),
        ("Septiembre", 61) : ("Octubre", 6.8, 22.8),
        ("Octubre", 92) : ("Noviembre", 9.7, 26.4),
        ("Noviembre", 122) : ("Diciembre", 12.3, 29.3),
        ("Diciembre", 153) : ("Enero", 13.4, 30.7),
        ("Enero", 184) : ("Febrero", 12.3, 29.5),
        ("Febrero", 212) : ("Agosto", 9.6, 26.3)
    }

    # Lambda function to activate evolute_poblation, lambda por que es en una sola linea
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

        max_temp_daily = 0
        min_temp_daily = 0
        
        #MEF to get the mean temperatures whitout using ifs
        mean_temperatures_mef.transition(day)

        #Durante el dia mido tres veces la temperatura
        for i in range(3):
            max_temp_daily += np.random.normal(loc=mean_temperatures_mef.max_mean, scale=5)
            min_temp_daily += np.random.normal(loc=mean_temperatures_mef.min_mean, scale=5)

        #Carpogrades calculus
        #Promedio
        max_temp = max_temp_daily / 3
        min_temp = min_temp_daily / 3
        print(f"max_temp_daily: {max_temp}, min_temp_daily: {min_temp}")

        #Calculo de carpogrados
        carpogrados = ((max_temp - min_temp)/2) - 10

        if carpogrados > 0:
            acumulated_carpogrades += carpogrados

        #MEF to get the poblation state
        carpogrades_mef.transition(acumulated_carpogrades)

        #Evolute poblation 
        if carpogrades_mef.state == "Vuelos" and evolute_poblation:
            adults = larvaes
            totals_cap += utilities.read_tramps(day, tramps, adults) #Todos los dias
            # eggs = utilities.update_population(totals_cap) #Al final
            evolute_poblation = False
            generation += 1

        
        if carpogrades_mef.state == "Larvas" and evolute_poblation:
            larvaes_prev = larvaes
            if days_applied == 0:
                eggs = utilities.update_population(totals_cap)
                larvaes = utilities.egg_eclosion(eggs, insecticide_eggs)
            if days_applied < 2:
                utilities.preventive_measures(larvaes, days_applied)
                days_applied += 1
                larvaes = evolute_poblation = False
            generation += 1

        print(f"day: {day}, carpogrades: {carpogrados}, carpogrados acumulados {acumulated_carpogrades}, state: {carpogrades_mef.state}, month: {mean_temperatures_mef.state}, larvaes: {larvaes}, adults: {adults}, eggs: {eggs}, tramps: {tramps}, totals_cap: {totals_cap}, generation: {generation}")
        day += 1

    data = json.dumps(data)
    return data

simulation(hectares=10, cost_per_hectare=5, tramps=5, insecticide_eggs=True, prev_larvaes=500)