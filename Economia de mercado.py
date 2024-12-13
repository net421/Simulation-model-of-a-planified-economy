import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parámetros generales
años = 20
sectores = ["Tecnología", "Manufactura", "Servicios"]
crecimiento_inicial = [0.05, 0.03, 0.04]
inversion_privada = [0.1, 0.08, 0.09]
demanda_inicial = [1.0, 1.2, 1.1]
oferta_inicial = [1.0, 1.0, 1.0]

# Inicialización de precios y producción por sector
precios_iniciales = [100, 80, 90]
produccion_inicial = [1.0, 1.0, 1.0]
precios = precios_iniciales[:]
produccion = produccion_inicial[:]

# Lista para almacenar resultados
resultados_sectoriales = []

for año in range(1, años + 1):
    # Actualización de la demanda y la oferta
    demanda = np.array(demanda_inicial) * (1 + np.array(crecimiento_inicial))
    oferta = np.array(oferta_inicial) * (1 + np.array(inversion_privada))
    
    # Ajuste de precios basado en la oferta y la demanda
    precios = precios * (demanda / oferta)
    
    # Actualización de la producción basada en la inversión privada
    produccion = produccion * (1 + np.array(inversion_privada))
    
    resultados_sectoriales.append({
        "Año": año,
        "Precios": dict(zip(sectores, precios.round(2))),
        "Producción": dict(zip(sectores, produccion.round(2))),
        "Demanda": dict(zip(sectores, demanda.round(2))),
        "Oferta": dict(zip(sectores, oferta.round(2)))
    })

# Convertir resultados a DataFrame
resultados_df = pd.DataFrame(resultados_sectoriales)

# Visualizaciones separadas por sector y por indicador
indicadores = ["Precios", "Producción", "Demanda", "Oferta"]

for sector in sectores:
    for indicador in indicadores:
        plt.figure(figsize=(10, 5))
        plt.plot(resultados_df['Año'], [r[indicador][sector] for r in resultados_sectoriales], label=f"{indicador} en {sector}")
        plt.xlabel('Año')
        plt.ylabel(indicador)
        plt.title(f'Evolución de {indicador} en {sector}')
        plt.legend()
        plt.grid(True)
        plt.show()
