import pandas as pd 
import numpy as np
import os

#datos necesarios

poblacion = pd.read_csv('./content/poblacion.csv', encoding = 'latin-1')
esperanza = pd.read_csv('./content/esperanza_de_vida.csv', encoding = 'latin-1')
hogares = pd.read_csv('./content/hogares_viviendas_superficie.csv', encoding = 'latin-1')

#Mostrar las primeras 5 filas 
poblacion.head()

#Mostrar las Ultimas 5 filas
poblacion.tail()

#Mostrar la cantidad de filas y columnas 
poblacion.shape

# Muestro los tipos de datos quer contiene mi dataset
poblacion.dtypes

# Obtenemos un resumen estadistico del dataframe
poblacion.describe

#Filtro los datos del csv POBLACION, excluyendo Total pais
poblacion_filtrado = poblacion[poblacion['provincia'] != 'Total País']
poblacion_filtrado

#Con la funcion merge combinamos los DataFrames, pobla_filtrado y hogares, en un nuevo dataFrame llamadom "poblac_superf".
#La combinacion se hara donde los valores de la columna provincia coincidan entre ambos DataFrames
poblac_superficie = pd.merge(poblacion_filtrado, hogares, left_on=['provincia'], right_on='provincia', how='left') # how-left ("Union por la izquierda")
poblac_superficie

#Calculo la densidad, usando la superficie + la poblacion total
poblac_superficie['densidad_de_poblacion'] = poblac_superficie['poblacion_total'] / poblac_superficie['superficie_km2']
poblac_superficie

# Busco algun dato faltante en mi dataset
poblac_superficie.isnull().sum()

# Crearemos una nueva columna ('fuera_de_rango'), que tomara del dataframe 'poblac_superf', los datos de la columna 'densidad_de_poblacion', resta la media del (promedio) de todos los 
# Valores en la columna densidad_de_poblacion, utilizando np.mean y lo dividimos por la desviacion estandar calculada, aplicando np. std a 'densidad_de poblacion'. Esto estandariza 
#los valores, convirtiendolos en una media llamada z-socre, el z-scoore indica cuantas desviaciones estandar esta un valor por encima o por debajo de la media.

poblac_superficie['fuera_de_rango'] = (poblac_superficie['densidad_de_poblacion'] - np.mean(poblac_superficie['densidad_de_poblacion']) ) / np.std(poblac_superficie['densidad_de_poblacion'])
poblac_superficie

#Calculo del percentil de la columna densidad de poblacion.
#El percentil 99 del valor por debajo del cual se encuentra el 99% de los datos. Esto significa que solo el 1% de los datos
#son mayores que este valor

p99 = np.percentile(poblac_superficie['fuera_de_rango'], 99)
p99

poblac_superficie[poblac_superficie['fuera_de_rango'] >= p99]

#Calcular el promedio
promedio = poblac_superficie['fuera_de_rango'].mean()
promedio