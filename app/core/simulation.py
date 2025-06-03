import utilities 

def simulation(hectares: int, tramps:int | None = None) -> int:
    """
    Simulate the number of tramps in a given area of hectares.
    
    :param hectares: The number of hectares to simulate.
    :param tramps: The number of tramps to simulate, if known.
    :return: The number of tramps simulated.
    """
    days_to_simulate = 243 #Represents 8 months, from August to March
    day = 0

    # If tramps is not provided, simulate the number of tramps
    if tramps is None:
        tramps = utilities.simulate_tramps(hectares)

    # Simulate the carpogrades to start the third-generation moths
    u = utilities.parte_central_cuadrado(utilities.get_seed(5), 5, 1)
    third_generation_carpogrades = 750 + 50 * u

    # Main simulation loop
    while day < days_to_simulate:
        

    return tramps