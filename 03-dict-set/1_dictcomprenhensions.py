# Una lista de tuplas
DIAL_CODES = [
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
    (62, 'Indonesia'),
    (55, 'Brazil'),
    (92, 'Pakistan'),
    (880, 'Bangladesh'),
    (234, 'Nigeria'),
    (7, 'Russia'),
    (81, 'Japan'),
]

# Creamos un diccionario a partir de la lista de tuplas
d1 = dict(DIAL_CODES)
print(f"d1: {d1}\n")
# Podemos crear una lista con los keys, y otra con los values
print(f"d1 (keys): {list(d1.keys())}\n")
print(f"d1 (values): {list(d1.values())}\n")
print(f"d1 (items): {list(d1.items())}\n\n")

# El diccionario mantiene el orden con el que se insertan los registros
d3 = dict(sorted(DIAL_CODES, key=lambda x: x[1]))
print(f"d3: {d3}\n\n")
# Pero son el mismo diccionario
assert d1 == d3

# Podemos crear comprenhensions
country_dial = {country: code for code, country in DIAL_CODES}
country_dial_u = {code: country.upper() for country, code in sorted(country_dial.items()) if code < 70}

print(f'{country_dial}\n{country_dial_u}\n\n')
