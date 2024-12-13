import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parámetros del modelo de economía planificada
n_periodos = 20
sectores = ['Manufactura', 'Servicios', 'Agricultura']
regiones = ['Norte', 'Centro', 'Sur']

# Inicialización de variables
productividad = {sector: [1.0] for sector in sectores}
idhs = []
desigualdad = []
poblacion = {region: [5 + np.random.uniform(-0.5, 0.5)] for region in regiones}
redistribucion = 0.02  # Nivel de redistribución inicial
ineficiencia_burocratica = 0.01  # Ineficiencia en asignación
innovacion = 0.03  # Incremento base en productividad por innovación

# Factores externos
impactos_externos = [1 if i % 5 != 0 else 0.9 for i in range(1, n_periodos + 1)]

# Simulación
for t in range(1, n_periodos + 1):
    # Ajuste de productividad por sector
    for sector in sectores:
        innovacion_actual = innovacion * (1 - ineficiencia_burocratica)
        productividad[sector].append(productividad[sector][-1] * (1 + innovacion_actual) * impactos_externos[t-1])

    # Cálculo del IDH promedio
    idh_promedio = 0.7 + 0.001 * t - desigualdad[-1] * 0.1 if t > 1 else 0.7
    idhs.append(idh_promedio)

    # Ajuste de desigualdad (suavización por redistribución)
    nueva_desigualdad = (desigualdad[-1] if t > 1 else 0.45) * (1 - redistribucion)
    desigualdad.append(nueva_desigualdad)

    # Población por regiones
    for region in regiones:
        crecimiento = 0.02 * (1 + np.random.uniform(-0.01, 0.01))  # Crecimiento poblacional variable
        nueva_poblacion = poblacion[region][-1] * (1 + crecimiento)
        poblacion[region].append(nueva_poblacion)

# Consolidar resultados
resultados = pd.DataFrame({
    'Año': np.arange(1, n_periodos + 1),
    'Productividad Global': [np.mean([productividad[sector][t] for sector in sectores]) for t in range(n_periodos)],
    'Productividad Manufactura': productividad['Manufactura'][1:],
    'Productividad Servicios': productividad['Servicios'][1:],
    'Productividad Agricultura': productividad['Agricultura'][1:],
    'IDH': idhs,
    'Desigualdad': desigualdad,
    'Poblacion': [{region: poblacion[region][t] for region in regiones} for t in range(n_periodos)]
})

# Visualización de resultados
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Productividad Global
axs[0].plot(resultados['Año'], resultados['Productividad Global'], label='Productividad Global')
axs[0].set_title('Productividad Global')
axs[0].set_xlabel('Año')
axs[0].set_ylabel('Productividad')
axs[0].legend()

# IDH
axs[1].plot(resultados['Año'], resultados['IDH'], label='IDH', color='green')
axs[1].set_title('IDH Promedio')
axs[1].set_xlabel('Año')
axs[1].set_ylabel('IDH')
axs[1].legend()

# Desigualdad
axs[2].plot(resultados['Año'], resultados['Desigualdad'], label='Desigualdad', color='red')
axs[2].set_title('Desigualdad Promedio')
axs[2].set_xlabel('Año')
axs[2].set_ylabel('Desigualdad')
axs[2].legend()

plt.tight_layout()
plt.show()

# Exportar resultados
print(resultados.head())
