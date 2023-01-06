import pandas as pd

pathArchivo = 'ModuloDeRecomendaciones/HumedadAprovechable.xlsx'

#Para utilizar esta funcion se necesita lo siguiente
#tipoDeSuelo => tipo de suelo del predio
#prof => profundidad de las raices (cm) / profundidad de mojamiento
#pred => porcentaje de pedregosidad
def calcularHumedadAprovechable(tipoDeSuelo, prof, pred):
    #hat = humedad - teorica
    hat = 0
    #cc = 
    cc = 0
    #pmp = 
    pmp = 0

    #cargar archivo con valores de ha
    archivo = pd.read_excel(pathArchivo, sheet_name='Hoja1')
    pivote = archivo.iloc[:, 0]
    i=0
    largo = len(pivote)
    while(i<largo):
        if(pivote[i] == tipoDeSuelo):
            #extraer valor de kc
            columna = archivo.iloc[:, 1]
            cc = columna[i]
            columna = archivo.iloc[:, 2]
            pmp = columna[i]
            columna = archivo.iloc[:, 3]
            hat = columna[i]
            break
        i=i+1
    #determinar si usar el valor de ha por defecto o calcularlo
    if(prof==0):
        ha = hat
    else:
        #calcular valor de ha
        ha = ((cc-pmp)/100)*prof*(1-(pred/100))

    #devolver el resultado
    return ha
    