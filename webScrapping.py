#
import urllib2
import sys
from bs4 import BeautifulSoup
fecha = "22/06/2018"
fecha = sys.argv[1]
comuna = "CUR"
#INFORME DE DISTRIBUCION GENERAL
#DETALLE DE DISTRIBUCION POR COMUNAS
distribucion = "http://clasificacion.wsp.cl/indgestion02.php?comuna="
unido = "&fecha="

pagina = distribucion+comuna+unido+fecha

url = urllib2.urlopen(pagina)
html = BeautifulSoup(url,'html.parser')

columnas = html.find_all("tr")
data = []
label = []
contador = 0
for elemento in columnas:
    contador = contador + 1
    tr =  elemento.contents
    datos = []
    for valor in tr:
        if contador == 0:
            labels.append(valor)
        else :
            if valor.string != None:
                datos.append(valor.string);

    if len(datos) > 0 :
        data.append(datos)
    contador = 1
for i in data:
    print i

    #print elemento.children
    #print "Children \n "
