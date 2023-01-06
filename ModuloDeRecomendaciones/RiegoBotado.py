import ModuloDeRecomendaciones.HumedadAprovechable as HumedadAprovechable
import ModuloDeRecomendaciones.Hargreaves as Hargreaves

#Umbral de riego (%)
ur = 40

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

def tiempoDeRiego(ti):
    #tiempo que se demora el agua de riego en infiltrar (minutos)
    #ti = 0
    #obtenemos la eto
    tr = (5/4)*ti
    return tr
