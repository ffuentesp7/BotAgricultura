import pandas as pd
import ModuloDeConexionDeBaseDeDatos.ConexionFirebase

pathArchivo = 'ModuloDeRecomendaciones/RadiacionSolar.xlsx'

#Para utilizar esta funcion se necesita lo siguiente
#latitud => Latitud en la cual esta ubicada el predio
#mes => mes actual de la pregunta
def calcularEvotranspiracion(mes, latitud):

    datos = ModuloDeConexionDeBaseDeDatos.ConexionFirebase.getTemperatura("curico")
    temperaturaPromedio = datos["temperatura"]
    temperaturaBaja = datos["temperaturaMenor"]
    temperaturaAlta = datos["temperaturaMayor"]

    r0 = 0

    if(latitud<=0):
        archivo = pd.read_excel(pathArchivo, sheet_name='Sur')
        latitud = latitud*-1
    else:
        archivo = pd.read_excel(pathArchivo, sheet_name='Norte')
    pivote = archivo.iloc[:, 0]
    columna = archivo.iloc[:, mes]
    i=0
    largo = len(pivote)
    while(i<largo):
        if(int(pivote[i]) <= latitud):
            r0 = float(columna[i])
            break
        i=i+1
    eto = 0.0023*(temperaturaPromedio+17.78)*r0*(temperaturaAlta-temperaturaBaja)**0.5
    return eto
        
