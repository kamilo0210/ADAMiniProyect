#estadisticas.py
from collections import Counter

def promedio(values):
    return sum(values) / len(values) if values else 0

def mediana(sorted_vals):
    n = len(sorted_vals)
    if n == 0:
        return 0
    mid = n // 2
    if n % 2 == 1:
        return sorted_vals[mid]
    return (sorted_vals[mid - 1] + sorted_vals[mid]) // 2

def moda(values):
    cnt = Counter(values)
    most_common = cnt.most_common()
    if not most_common:
        return None
    max_freq = most_common[0][1]
    modes = [val for val, freq in most_common if freq == max_freq]
    return min(modes)  # Si hay empate, regresa el menor valor modal

def extremismo(values):
    """Proporción de opiniones completamente desfavorables (0) o favorables (10)."""
    extremes = sum(1 for v in values if v in (0, 10))
    return extremes / len(values) if values else 0

def consenso(values):
    """Proporción de opiniones iguales a la moda."""
    m = moda(values)
    if m is None:
        return 0
    return values.count(m) / len(values) if values else 0
