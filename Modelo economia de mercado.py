import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parámetros iniciales
años = 20
regiones = ["Norte", "Centro", "Sur"]
infraestructura_inicial = [0.7, 0.5, 0.3]
inversion_privada = [0.1, 0.08, 0.05]
inversion_educacion = [0.05, 0.03, 0.02]
desigualdad_inicial = [0.25, 0.35, 0.5]

# Parámetros económicos
elasticidades_sector = {"manufactura": 0.4, "servicios": 0.5, "agricultura": 0.1}
incentivo_innovacion = 0.1
choques_externos = {5: -0.05, 10: 0.1, 15: -0.02}

# Crecimiento de la población y IDH
poblacion_inicial = [6, 5, 3]
tasa_crecimiento_poblacion = [0.012, 0.015, 0.01]
idhs_iniciales = [0.8, 0.7, 0.6]

# Lista para almacenar resultados
resultados_regionales = []
productividad = {"manufactura": 1.0, "servicios": 1.0, "agricultura": 1.0}

# Iteración principal
for año in range(1, años + 1):
    # Inversión privada impulsa infraestructura
    infraestructura_actual = [
        infraestructura_inicial[i] + inversion_privada[i] * infraestructura_inicial[i]
        for i in range(len(regiones))
    ]

    # Ajuste de productividad por sector
    for sector in productividad.keys():
        productividad[sector] += incentivo_innovacion * np.mean(infraestructura_actual)

        # Influencia intersectorial
        intersectorial = sum(
            elasticidades_sector[other] * productividad[other]
            for other in productividad if other != sector
        ) * 0.03
        productividad[sector] += intersectorial

    # Impacto en IDH
    idh_actual = [
        min(1.0, idhs_iniciales[i] + 0.003 * infraestructura_actual[i] + 0.002 * inversion_educacion[i])
        for i in range(len(regiones))
    ]

    # Ajuste de desigualdad sin redistribución fiscal
    desigualdad_actual = [
        max(
            0.1,
            desigualdad_inicial[i] + 0.01 * (1 - infraestructura_actual[i])
        ) for i in range(len(regiones))
    ]

    # Choques externos
    if año in choques_externos:
        for sector in productividad.keys():
            productividad[sector] *= (1 + choques_externos[año])

    # Población dinámica
    poblacion_actual = [
        poblacion_inicial[i] * (1 + tasa_crecimiento_poblacion[i])
        for i in range(len(regiones))
    ]

    # Registro de resultados
    resultados_regionales.append({
        "Año": año,
        "Productividad Global": round(sum(productividad.values()) / len(productividad), 3),
        "Productividad Manufactura": round(productividad["manufactura"], 3),
        "Productividad Servicios": round(productividad["servicios"], 3),
        "Productividad Agricultura": round(productividad["agricultura"], 3),
        "IDH": {region: round(idh_actual[i], 3) for i, region in enumerate(regiones)},
        "Desigualdad": {region: round(desigualdad_actual[i], 3) for i, region in enumerate(regiones)},
        "Poblacion": {region: round(poblacion_actual[i], 3) for i, region in enumerate(regiones)}
    })

# Convertir resultados a DataFrame y mostrarlo
resultados_df = pd.DataFrame(resultados_regionales)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(resultados_df)

# Visualización
variables_a_graficar = ["IDH", "Desigualdad"]

for region in regiones:
    plt.figure(figsize=(12, 6))
    for variable in variables_a_graficar:
        if variable in ["IDH", "Desigualdad"]:
            plt.plot(resultados_df['Año'], [r[variable][region] for r in resultados_regionales], label=variable)

    plt.xlabel('Año')
    plt.ylabel('Valor')
    plt.title(f'Evolución de Indicadores en {region} - Economía de Mercado')
    plt.legend()
    plt.grid(True)
    plt.show()

# Gráfica de productividad global
plt.figure(figsize=(14, 7))
plt.plot(resultados_df['Año'], resultados_df['Productividad Global'], label="Productividad Global")
plt.xlabel('Año')
plt.ylabel('Productividad')
plt.title('Evolución de la Productividad Global - Economía de Mercado')
plt.legend()
plt.grid(True)
plt.show()
