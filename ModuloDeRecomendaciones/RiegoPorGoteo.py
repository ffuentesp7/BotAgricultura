import ModuloDeRecomendaciones.HumedadAprovechable as HumedadAprovechable
import ModuloDeRecomendaciones.Hargreaves as Hargreaves

#es la eficiencia del sistema (Ef), la que en riego por goteo tiene un máximo teórico de 90%
ef = 90
#Umbral de riego (%)
ur = 20

def frecuenciaDeRiego(ha, etc):
    #obtener la ha (humedad aprovechable)
    #ha = HumedadAprovechable.calcularHumedadAprovechable()
    #humedad de deficid en mm 
    hd = (ur/100)*ha*10
    #obtenemos la eto
    #etc = Hargreaves.calcularEvotranspiracion()
    #Frecuencia de riego
    fr = etc/hd
    return fr

def tiempoDeRiego(dh, ds, qe, etc):
    #distancia entre plantas
    #dh = 0
    #distancia entre geteo
    #ds = 0
    #densidad de emisores por hectárea
    ne = 10000/(dh*ds)
    #litros por hora por gotero
    #qe = 0
    #es la precipitación bruta del sistema (mm/h). 
    pp = qe*ne/10000
    #obtenemos la eto
    #etc = Hargreaves.calcularEvotranspiracion()
    #tiempo de riego (h)
    tr = etc/(pp*(ef/100))
    return tr
