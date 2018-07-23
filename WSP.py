import MySQLdb
import urllib2
import sys
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

db = MySQLdb.connect("192.99.150.93","oficinap_corellana","oficinapostal2018*","oficinap_oficinaPostal" )
query = db.cursor()

def insert(sector,pendientes,entregados,total,fecha):
    try:
        sql = "insert into distribucion values (null,'"+str(sector)+"',"+str(pendientes)+","+str(entregados)+","+str(total)+",'"+fecha+"')"
        query.execute(sql)
        db.commit()
    except Exception as e:
        print e
        db.rollback()
        raise


def buscar(fecha,comuna):
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
    # Sector , Pendientes , Entregados
    contador = 0
    comunas = []
    totales = []
    pendientes = []
    entregados = []
    for i in data:
        if contador == 1:
            print i
        if contador == 2:
            comuna = i[1]
            comunas.append(comuna)
            pendiente = i[2]
            pendientes.append(pendiente)
            entregado = i[4]
            entregados.append(entregado)
            # 3 y 5 son porcentajes
            total = i[6]
            totales.append(total)
            print " \n"
            #print i
            #print "\n"
            print "Comuna :"+str(comuna)
            print "pendientes :"+str(pendiente)
            print "entregados :"+str(entregados)
            print "total : " +str(total)
            insert(comuna,pendiente,entregado,total,fecha)
            contador = 0
            print " \n"
        else:
            contador = contador + 1

        #print elemento.children
        #print "Children \n "

for mes in range(12):
    for dia in range(31):
        fecha = str(dia)+"/"+str(mes)+"/2018"
        comuna = "CUR"
        if fecha == "11/07/2018":
            break
        buscar(fecha,comuna)

#y_pos = np.arange(len(comunas))

#totales = map(int, totales)
#entregados = map(int, entregados)
#pendientes = map(int, pendientes)
#totales.sort()
#print totales
#bar_width = 0.35
#opacity = 0.8
#plt.bar(y_pos, totales, align='center',alpha=opacity,color="g")
#plt.xticks(y_pos, comunas)
#plt.ylabel('Comunas')
#plt.title("totales por comunas")

#plt.show()
