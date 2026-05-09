import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from weasyprint import HTML
import io
import base64

def ejecutar_motor_geotecnia(datos_input):
    # Procesamiento de DataFrame
    df = pd.DataFrame(datos_input)
    
    # Cálculo de Curva Proctor (Ajuste Polinómico)
    coef = np.polyfit(df['Punto'], df['Densidad_Seca'], 2)
    p = np.poly1d(coef)
    
    # Búsqueda de Óptimos
    x_max = -coef[1] / (2 * coef[0])
    y_max = p(x_max)
    
    return x_max, y_max, df
