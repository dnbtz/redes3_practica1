import sys
import rrdtool
import time
tiempo_actual = int(time.time())
tiempo_final = tiempo_actual - 86400
tiempo_inicial = tiempo_final -25920000


def grafica(agente):
    file = "%s.rrd" % agente
    while 1:
        ret = rrdtool.graph( "%s.png" % agente,
                         "--start",'1582775880',
                         "--end","1582776000",
                         "--vertical-label=Bytes/s",
                         "DEF:inoctets="+file+":inoctets:AVERAGE",
                         "DEF:outoctets="+file+":outoctets:AVERAGE",
                         "AREA:inoctets#00FF00:In traffic",
                         "LINE1:outoctets#0000FF:Out traffic\r")

        time.sleep(10)