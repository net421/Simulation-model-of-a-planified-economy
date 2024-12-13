import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parámetros iniciales
años = 20
regiones = ["Norte", "Centro", "Sur"]
desarrollo_inicial = [0.3, 0.5, 0.2]
infraestructura_inicial = [0.6, 0.4, 0.2]
inversion_infraestructura = [0.05, 0.03, 0.02]
inversion_educacion = [0.08, 0.12, 0.1]

# Parámetros para sectores económicos
impacto_tecnologia = {"manufactura": 0.1, "servicios": 0.08, "agricultura": 0.03}
demanda_intersectorial = {"manufactura": 0.4, "servicios": 0.5, "agricultura": 0.1}
redistribucion_fiscal = 0.02  # Moderada
tasa_mejora_idh = 0.005
desigualdad_inicial = [0.35, 0.4, 0.5]

# Población inicial y crecimiento base
poblacion_inicial = [5, 4, 3]
tasa_crecimiento_poblacion = [0.01, 0.012, 0.008]

# Parámetros de innovación
inversion_tecnologia = [0.1, 0.15, 0.1]
choques_externos = {5: -0.05, 10: 0.1, 15: -0.02}

# Lista para almacenar resultados
resultados_regionales = []
productividad = {"manufactura": 1.0, "servicios": 1.0, "agricultura": 1.0}
idh = [0.75, 0.7, 0.65]

# Iteración principal
for año in range(1, años + 1):
    desarrollo_regional = np.array(desarrollo_inicial) + np.array(infraestructura_inicial) * 0.1
    infraestructura_inicial = np.array(infraestructura_inicial) + np.array(inversion_infraestructura) * 0.05

    # Ajuste de productividad por sector
    for sector in productividad.keys():
        impacto = impacto_tecnologia[sector] * np.mean(inversion_tecnologia)
        productividad[sector] += productividad[sector] * impacto

        # Influencia intersectorial
        intersectorial = sum(
            demanda_intersectorial[other] * productividad[other]
            for other in productividad if other != sector
        ) * 0.02
        productividad[sector] += intersectorial

    # Impacto en IDH
    idh = [
        min(1.0, idh[i] + idh[i] * tasa_mejora_idh + 0.005 * inversion_educacion[i])
        for i in range(len(regiones))
    ]

    # Ajuste de desigualdad con redistribución fiscal
    desigualdad_regional = [
        max(
            0.1,
            desigualdad_inicial[i] - redistribucion_fiscal * (inversion_educacion[i] + 0.01 * productividad["servicios"])
        )
        for i in range(len(regiones))
    ]

    # Choques externos
    if año in choques_externos:
        for sector in productividad.keys():
            productividad[sector] *= (1 + choques_externos[año])

    # Población dinámica
    poblacion = [
        poblacion_inicial[i] * (1 + tasa_crecimiento_poblacion[i] + 0.005 * desarrollo_regional[i])
        for i in range(len(regiones))
    ]

    resultados_regionales.append({
        "Año": año,
        "Productividad Global": round(sum(productividad.values()) / len(productividad), 3),
        "Productividad Manufactura": round(productividad["manufactura"], 3),
        "Productividad Servicios": round(productividad["servicios"], 3),
        "Productividad Agricultura": round(productividad["agricultura"], 3),
        "IDH": {region: round(idh[i], 3) for i, region in enumerate(regiones)},
        "Desigualdad": {region: round(desigualdad_regional[i], 3) for i, region in enumerate(regiones)},
        "Poblacion": {region: round(poblacion[i], 3) for i, region in enumerate(regiones)}
    })

# Convertir resultados a DataFrame y mostrarlo
resultados_df = pd.DataFrame(resultados_regionales)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
print(resultados_df)

# Visualizaciones por región y variable
variables_a_graficar = ["Productividad Manufactura", "Productividad Servicios", "Productividad Agricultura", "IDH", "Desigualdad"]

for region in regiones:
    plt.figure(figsize=(12, 6))
    for variable in variables_a_graficar:
        if variable == "IDH" or variable == "Desigualdad":
            plt.plot(resultados_df['Año'], [r[variable][region] for r in resultados_regionales], label=variable)
        else:
            plt.plot(resultados_df['Año'], resultados_df[variable], label=variable)

    plt.xlabel('Año')
    plt.ylabel('Valor')
    plt.title(f'Evolución de Indicadores en {region} - Economía Mixta')
    plt.legend()
    plt.grid(True)
    plt.show()

# Gráfica de productividad global
plt.figure(figsize=(14, 7))
plt.plot(resultados_df['Año'], resultados_df['Productividad Global'], label="Productividad Global")
plt.xlabel('Año')
plt.ylabel('Productividad')
plt.title('Evolución de la Productividad Global - Economía Mixta')
plt.legend()
plt.grid(True)
plt.show()
