import math
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
