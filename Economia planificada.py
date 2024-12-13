import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# Parámetros generales
años = 20
regiones = ["Norte", "Centro", "Sur"]
desarrollo_inicial = [0.3, 0.5, 0.2]
infraestructura_inicial = [0.6, 0.4, 0.2]
inversion_infraestructura = [0.05, 0.03, 0.02]
inversion_educacion = [0.1, 0.2, 0.15]

# Parámetros de migración
atractivo_base = [0.6, 0.4, 0.5]  # Atractivo inicial de cada región
salarios_base = [1.0, 0.8, 0.6]   # Base salarial inicial
tasa_migracion = 0.1               # Proporción de población que migra

# Inicialización de población por región
poblacion_inicial = [1.0, 1.2, 0.8]
poblacion = poblacion_inicial[:]

# Lista para almacenar resultados
resultados_regionales = []
productividad = 1.0
productividad_anual = []
idh = [0.75, 0.7, 0.6]
desigualdad_inicial = [0.35, 0.4, 0.5]

for año in range(1, años + 1):
    desarrollo_regional = np.array(desarrollo_inicial) + np.array(infraestructura_inicial) * 0.05
    infraestructura_inicial = np.array(infraestructura_inicial) + np.array(inversion_infraestructura) * 0.05

    # Cálculo de migración interna
    atractivo_actual = [salarios_base[i] + desarrollo_regional[i] for i in range(len(regiones))]
    total_atractivo = sum(atractivo_actual)
    migracion = [atractivo_actual[i] / total_atractivo * tasa_migracion for i in range(len(regiones))]

    # Actualizar población considerando migración
    nueva_poblacion = [poblacion[i] + sum(migracion) * (1 if i == j else -1) for i in range(len(regiones)) for j in range(len(regiones))]
    poblacion = nueva_poblacion[:]

    productividad += productividad * 0.02
    productividad_anual.append(productividad)
    idh = [min(1.0, idh[i] + idh[i] * 0.01) for i in range(len(regiones))]
    desigualdad = [max(0.1, desigualdad_inicial[i] - 0.01) for i in range(len(regiones))]

    resultados_regionales.append({
        "Año": año,
        "Desarrollo Regional": dict(zip(regiones, desarrollo_regional.round(3))),
        "Infraestructura Regional": dict(zip(regiones, infraestructura_inicial.round(3))),
        "Población Regional": dict(zip(regiones, [round(p, 3) for p in poblacion])),
        "IDH Regional": dict(zip(regiones, [round(i, 3) for i in idh])),
        "Desigualdad Regional": dict(zip(regiones, [round(d, 3) for d in desigualdad]))
    })

# Convertir resultados a DataFrame
resultados_df = pd.DataFrame(resultados_regionales)

# Visualizaciones separadas por región y por indicador
indicadores = ["Desarrollo Regional", "Infraestructura Regional", "Población Regional", "IDH Regional", "Desigualdad Regional"]

for region in regiones:
    for indicador in indicadores:
        plt.figure(figsize=(10, 5))
        plt.plot(resultados_df['Año'], [r[indicador][region] for r in resultados_regionales], label=f"{indicador} en {region}")
        plt.xlabel('Año')
        plt.ylabel(indicador)
        plt.title(f'Evolución de {indicador} en {region}')
        plt.legend()
        plt.grid(True)
        plt.show()

# Visualización general de la productividad global
plt.figure(figsize=(12, 6))
plt.plot(resultados_df['Año'], productividad_anual, label="Productividad Global")
plt.xlabel('Año')
plt.ylabel('Productividad')
plt.title('Evolución de la Productividad Global')
plt.legend()
plt.grid(True)
plt.show()
