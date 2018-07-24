import folium
import os
import pandas as pd
from folium import plugins
#df = pd.read_csv("gps/msectorc1_0606gps.txt", sep='\xb0')
#print df.describe
rutsEncontrados = []
def convertirHora(hora,sesgo):
    posibilidades = []
    Hora = hora.split(":")
    hora = int(Hora[0])
    minuto = int(Hora[1])
    segundo = int(Hora[2])
    i = 0
    while i < sesgo :
        if segundo == 59:
            segundo = 0
            if minuto == 59 :
                hora = hora + 1
                minuto = 0
            else :
                minuto = minuto + 1

        else :
            segundo = segundo + 1
        data = [hora,minuto,segundo]
        i = i + 1
        posibilidades.append(data)
    i = 0
    hora = int(Hora[0])
    minuto = int(Hora[1])
    segundo = int(Hora[2])
    while i < sesgo :
        if segundo == 0:
            segundo = 59
            if minuto == 0 :
                hora = hora - 1
                minuto = 59
            else :
                minuto = minuto - 1
        else :
            segundo = segundo - 1
        i = i + 1
        if hora >= 12:
            hora = hora - 12
        data = [hora,minuto,segundo]
        posibilidades.append(data)
    return posibilidades

def buscar(dia,hora,sesgo,file):
    contador = 0
    dias = dia.split("-")
#    print dias
    dia = int(dias[0])
    mes = int(dias[1])
    year = int(dias[2])

    gps = open("gps/"+str(file),"r")
    for texto in gps:
        if str(texto[:10]) == "Trackpoint" :
            #print "Si es trackpoint"
            v =  texto.split("\t")
            if len(v) > 8:
                fecha = v[2].split(" ")
                if len(fecha) > 1:
                    Dias = fecha[0].split("-")
                    Mes = int(Dias[0])
                    Dia = int(Dias[1])
                    Year = int(Dias[2])
                    h = fecha[1].split(":")

                    if int(h[0]) >= 12:
                        valor = int(h[0]) - 12
                    else :
                        valor = h[0]
                    Hora = ""+str(valor)+":"+str(h[1])+":"+str(h[2])
                    #print v[1]

                    if(dia == Dia and mes==Mes):
                        lista = convertirHora(hora,sesgo)

                        for elemento in lista:

                            newHora = str(elemento[0])+":"+str(elemento[1])+":"+str(elemento[2])
                            if newHora == Hora:
                                return v[1]
                        #return v[1]


todos = []
location = "lector/"
coordenadas = []
archivos = []
rutas = []
ruts = []
sectores = []
mapa = 0
for file in os.listdir(location):
    rendicion = []
    archivos.append(folium.Map(
        location=[-34.9926116,-71.2527959],
        zoom_start=13
    ))
    lector = open("lector/"+file,"r")
    nombreSector = file.split("_")
    fechaCarpeta = nombreSector[1][0:2]
    if not os.path.exists("rendiciones/"+fechaCarpeta):
        os.makedirs("rendiciones/"+fechaCarpeta)
    nombreSector = nombreSector[0]
    nombreSector = nombreSector[1:]



    archivo = file.replace("lector","gps")
    print file
    print archivo
    sesgo = 22
    Ruts = []
    for texto in lector:
        palabras = texto.split(",")
        c = 0
        for i in range(len(palabras)):
            if  i == 0:
                existe = palabras[i].find("-")
            if existe > 0 and len(palabras[0]) < 12 and len(palabras[0]) > 8:

                rut = palabras[0]
                ruts.append(rut)
                Ruts.append(rut)
                print rut
                palabras[2].replace(" ", "")
                hora = palabras[2].split("AM")

                if len(hora)<2:
                    hora = palabras[2].split("PM")

                dia = hora[1]
                hora = hora[0]

                dia = dia.replace("/","-")
                dia = dia.replace("\n","")
                gps = buscar(dia,hora,sesgo,archivo)
                if gps != None :
                    rutsEncontrados.append(rut)
                    dato = [gps, rut]
                    rendicion.append(dato)


            c = c + 1
            print len(Ruts)
    lista_nueva = []
    for i in rendicion:
        if i not in lista_nueva:
            lista_nueva.append(i)
        if i not in todos:
            todos.append(i)
    multihogar = []
    contador = 0
    lapromedio = 0
    lopromedio = 0
    circulo = folium.Circle(
        radius=1000,
        location=[lapromedio, lopromedio],
        popup='Sector',
        color='crimson',
        fill=False,
    )
    for i in lista_nueva:

        if contador == 0:
            registro = folium.Map(
                location=[-34.9926116,-71.2527959],
                zoom_start=16
            )
            m = folium.Map(
                location=[-34.9926116,-71.2527959],
                zoom_start=13
            )
        contador = contador + 1
        ubicacion = i[0].split(" ")
        latitud = ubicacion[0].replace("S","-")
        longitud = ubicacion[1].replace("W","-")
        rut = i[1]
        folium.Marker([float(latitud),float(longitud)],icon=folium.Icon(color='red',icon='info-sign'), popup='<i>'+rut+'</i>').add_to(archivos[mapa])
        folium.Marker([float(latitud),float(longitud)],icon=folium.Icon(color='red',icon='info-sign'), popup='<i>'+rut+'</i>').add_to(m)
        data = [latitud,longitud,rut]
        lapromedio = lapromedio + float(latitud)
        lopromedio = lopromedio + float(longitud)
        coordenada = [float(latitud),float(longitud)]
        coordenadas.append(coordenada)
        multihogar.append(data)


    if contador > 0:
        lapromedio = lapromedio / contador
        lopromedio = lopromedio / contador
        print lapromedio
        print lopromedio
        folium.PolyLine(
            smooth_factor=50,
            locations=coordenadas,
            color='green',
            weight=5
            ).add_to(registro)
        folium.features.Circle(location=[lapromedio, lopromedio], radius=1500,
                        popup='Sector',
                        color='black',
                        fill=True,
                        fill_color='#07131d'
                        ).add_to(archivos[mapa])
        #circulo = folium.Circle(
        #    radius=1000,
        #    location=[lapromedio, lopromedio],
        #    popup='Sector',
        #    color='crimson',
        #    fill=False,
        #)
        #circulo.add_to(archivos[mapa])

        #sectores[mapa].add_to(archivos[mapa])
        #m.save("rendiciones/poligono"+file+".html")
        plug = plugins.TimestampedGeoJson({
            'type': 'FeatureCollection',
        }, period='PT1M', add_last_point=True)

        plug.add_to(archivos[mapa])
        archivos[mapa].save("rendiciones/"+fechaCarpeta+"/"+nombreSector+".html")

        mapa = mapa + 1

    for i in todos:
        if contador == 0:
            m = folium.Map(
                location=[lapromedio, lopromedio],
                zoom_start=13,
                tiles='Stamen Terrain'
            )
        contador = contador + 1
        ubicacion = i[0].split(" ")
        latitud = ubicacion[0].replace("S","-")
        longitud = ubicacion[1].replace("W","-")
        rut = i[1]
        folium.Marker([float(latitud),float(longitud)], popup='<i>'+rut+'</i>').add_to(m)
        #folium.Marker([float(latitud),float(longitud)], popup='<i>'+rut+'</i>').add_to(registros)
        data = [latitud,longitud,rut]
    registro.save("rendiciones/"+fechaCarpeta+"/registros.html")
    plug.add_to(m)
    m.save("rendiciones/"+fechaCarpeta+"/todos.html")

print "cantidad total de documentos entregados : "+str(len(todos))


############################
#print multihogar
lista_ruts = []
print "largo ruts"
print len(ruts)
for i in ruts:
    if i not in lista_ruts:
        print i
        lista_ruts.append(i)
print "cantidad de ruts "+str(len(lista_ruts))
#noEncontrados = []
#print rutsEncontrados
#for i in lista_ruts:
    #if i not in rutsEncontrados:
#        print i
#        noEncontrados.append(i)

#print len(lista_ruts)
#print len(noEncontrados)
