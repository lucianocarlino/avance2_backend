import sys
import time
import numpy as np
import requests

def parte_central_cuadrado(seed: int, digits: int, total: int):
    j=1
    random_numbers = []
    M = seed
    if (10**digits > sys.maxsize):
        return {
            "estado": 0,
            "mensaje": "La cantidad de dígitos es demasiado grande",
            "resultado": []
        }
    while (j<=total):
        X = M**2
        if ((len(str(X))) - digits) % 2 != 0:
            X = X * 10
        limits = (len(str(X)) - digits) // 2 
        M = int(str(X)[limits:limits + digits])
        random_numbers.append(M/10**digits)
        j += 1
    return {
        "estado": 1,
        "mensaje": "",
        "resultado": random_numbers
    }

def lehmer(seed: int, t: int, total: int):
    if (len(str(t)) >= len(str(seed))):
        return {
            "estado": 0,
            "mensaje": "El valor de t no puede ser mayor o igual que el valor de seed",
            "resultado": []
        }
    j = 1
    random_numbers = []
    M = seed
    k = len(str(t))
    n = len(str(seed))
    while (j <= total):
        nt = M * t
        M = int(str(nt)[k:]) - int(str(nt)[:k])
        random_numbers.append(float(f"0.{M}"))
        j += 1
    return {
        "estado": 1,
        "mensaje": "",
        "resultado": random_numbers
    }

def congruencial_mixto(seed: int, a: int, c: int, m: int, total: int):
    if (m <= 0):
        return {
            "estado": 0,
            "mensaje": "El valor del modulo debe ser mayor que cero",
            "resultado": []
        }
    if (a <= 0):
        return {
            "estado": 0,
            "mensaje": "El valor de la constante multiplicativa debe ser mayor que cero",
            "resultado": []
        }
    if (c < 0):
        print("El valor de la constante aditiva debe ser mayor o igual que cero")
        return {
            "estado": 0,
            "mensaje": "El valor de la constante aditiva debe ser mayor o igual que cero",
            "resultado": []
        }
    j = 1
    random_numbers = []
    M = seed
    while(j <= total):
        M = (a * M + c) % m
        random_numbers.append(M/m)
        j += 1
    return {
        "estado": 1,
        "mensaje": "",
        "resultado": random_numbers
    }

def congruencial_multiplicativo(seed: int, a: int, m: int, total: int, decimals: int = 4):
    if (m <= 0):
        return {
            "estado": 0,
            "mensaje": "El valor del modulo debe ser mayor que cero",
            "resultado": []
        }
    if (a <= 0):
        return {
            "estado": 0,
            "mensaje": "El valor de la constante multiplicativa debe ser mayor que cero",
            "resultado": []
        }
    j = 1
    random_numbers = []
    M = seed
    while(j <= total):
        M = (a * M) % m
        random_numbers.append(round(M/m, decimals))
        j += 1
    return {
        "estado": 1,
        "mensaje": "",
        "resultado": random_numbers
    }

def congruencial_adivito(seed: list[int], m: int, total: int, decimals: int = 4):
    if (m <= 0):
        return {
            "estado": 0,
            "mensaje": "El valor del modulo debe ser mayor que cero",
            "resultado": []
        }
    j = 1
    random_numbers = []
    seed_array = seed
    while(j <= total):
        M = seed[j-1] + seed[-1]
        M = M % m
        seed_array.append(M)
        random_numbers.append(round(M/m, decimals))
        j += 1
    return {
        "estado": 1,
        "mensaje": "",
        "resultado": random_numbers
    }

def get_seed(digits: int):
    before_input = time.time()
    response = requests.get('https://argentina.gob.ar')
    after_input = time.time()
    seed = int(str(int((((after_input - before_input) * response.elapsed.total_seconds()) % 1) * (10**17)))[::-1][:digits])
    return seed
