import folium
import os
import json
from folium import plugins
#total = input("Cantidad total de documentos : ")
total  = 28
x = 0
errores = []
while x != 0:
    print ("Ingrese el codigo de error (Ingrese 0 para dejar de ingresar)")
    x = input("Codigo :")

    if x == 0:
        print ("Gracias, Comienza el proceso de datos.\nTrabajando...")
        break
    else:
        codigo = x
        cantidad = input("Cantidad :")
        data = [codigo,cantidad]
        errores.append(data)
rutsEncontrados = []
def crearJson(datos):
    from easydict import EasyDict as edict
    listaDatos = []
    for data in datos:
        ubicacion = data[0].split(" ")
        latitud = ubicacion[0].replace("S","-")
        longitud = ubicacion[1].replace("W","-")
        cuerpo = '{"type": "Feature", "properties": {"@id": "node/3578353919", "addr:city": "Curico", "addr:country": "Chile","name": "'+str(data[1])+'"}, "geometry": {"type": "Point", "coordinates": ['+str(longitud)+','+str(latitud)+']}}'
        listaDatos.append(eval(cuerpo))
    x = edict({"type": "FeatureCollection", "generator": "Cristopher Orellana", "copyright": "protected by oficinapostalchile.cl", "timestamp": "2018-07-30T19:03:02Z", "features": listaDatos })
    return x
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
        if minuto < 10 :
            data = [hora,"0"+str(minuto),segundo]
        else :
            data = [hora,minuto,segundo]
        posibilidades.append(data)
    return posibilidades

def buscar(dia,hora,sesgo,file,flag):
    contador = 0
    dias = dia.split("-")
#    print (dias
    dia = int(dias[0])
    mes = int(dias[1])
    year = int(dias[2])

    gps = open("gps/"+str(file),"r")
    for texto in gps:
        if str(texto[:10]) == "Trackpoint" and flag == 0:
            #print ("Si es trackpoint"
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
                    #print (v[1]

                    if(dia == Dia and mes==Mes):
                        lista = convertirHora(hora,sesgo)
                        for elemento in lista:
                            newHora = str(elemento[0])+":"+str(elemento[1])+":"+str(elemento[2])
                            if newHora == Hora:
                                return v[1]

        if str(texto[:10]) == "Trackpoint" and flag == 1:
            #print ("Si es trackpoint"
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

                    #print (v[1]

                    if(dia == Dia and mes==Mes):

                        lista = convertirHora(hora,sesgo)
                        print lista

                        for elemento in lista:
                            print "elemento"
                            print elemento
                            newHora = str(elemento[0])+":"+str(elemento[1])+":"+str(elemento[2])
                            print newHora+" res"
                            print hora+" ant"
                            print "hora del doc gps"
                            print Hora
                            #print v[1]
                            if newHora == Hora:
                                return v[1]

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
    print (file)
    print (archivo)
    sesgo = 12
    Ruts = []
    for texto in lector:
        palabras = texto.split(",")
        c = 0
        for i in range(len(palabras)):
            if  i == 0:
                existe = palabras[i].find("-")
            if existe > 0 and len(palabras[0]) < 12 and len(palabras[0]) > 8:
                rut = palabras[0]
                print rut
                ruts.append(rut)
                Ruts.append(rut)
                palabras[2].replace(" ", "")
                hora = palabras[2].split("AM")

                if len(hora)<2:
                    hora = palabras[2].split("PM")

                dia = hora[1]
                hora = hora[0]

                dia = dia.replace("/","-")
                dia = dia.replace("\n","")
                flag = 0
                gps = buscar(dia,hora,sesgo,archivo,flag)
                if gps != None :
                    rutsEncontrados.append(rut)
                    dato = [gps, rut, hora]
                    rendicion.append(dato)
                else :
                    print "esste rut no lo encontre"
                    print rut
                    print "######"
            c = c + 1

    lista_nueva = []
    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    for i in rendicion:
        if i not in lista_nueva:
            print i
            lista_nueva.append(i)
        if i not in todos:
            todos.append(i)
    print "$$$$$"
    print len(lista_nueva)
    x = input("pausa")

    print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    multihogar = []
    contador = 0
    lapromedio = 0
    lopromedio = 0
    circulo = folium.Circle(
        radius=1000,
        location=[lapromedio, lopromedio],
        color='crimson',
        fill=False,
    )
    from Folium import plugins
    #plugins.Search(states, search_zoom=6, geom_type='Polygon').add_to(m)
    x = crearJson(lista_nueva)
    plugins.Search(x, search_zoom=20).add_to(archivos[mapa])
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
        hora = i[2]
        folium.Marker([float(latitud),float(longitud)],icon =folium.Icon(color='red'), popup='<div><p>Cliente : '+rut+'</p><p>Latitud : '+latitud+'</p><p>Longitud : '+longitud+'</p><p>Hora : '+hora+'</p></div>').add_to(archivos[mapa])
        folium.Marker([float(latitud),float(longitud)],icon =folium.Icon(color='red'), popup='<div><p>Cliente : '+rut+'</p><p>Latitud : '+latitud+'</p><p>Longitud : '+longitud+'</p><p>Hora : '+hora+'</p></div>').add_to(m)
        data = [latitud,longitud,rut]
        lapromedio = lapromedio + float(latitud)
        lopromedio = lopromedio + float(longitud)
        coordenada = [float(latitud),float(longitud)]
        coordenadas.append(coordenada)
        multihogar.append(data)


    if contador > 0:
        lapromedio = lapromedio / contador
        lopromedio = lopromedio / contador
        print (lapromedio )
        print (lopromedio )
        folium.PolyLine(
            smooth_factor=50,
            locations=coordenadas,
            color='green',
            weight=5
            ).add_to(registro)
        folium.features.Circle(location=[lapromedio, lopromedio], radius=1500,
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

        #plug.add_to(archivos[mapa])
        legend_html =   '''
                    <div style="position: fixed;
                                top: 50px; right: 50px; width: 20%; height: 10%;
                                border:2px solid grey; z-index:9999; font-size:14px;
                                ">&nbsp; Datos Generales <br>
                                  &nbsp; Entregados &nbsp; : ''' +str(len(lista_nueva))+''' <i class="fa fa-map-marker fa-2x" style="color:red"></i>
                    </div>
                    '''

        archivos[mapa].get_root().html.add_child(folium.Element(legend_html))

        archivos[mapa].save("rendiciones/"+fechaCarpeta+"/"+nombreSector+".html")

        mapa = mapa + 1

    m = folium.Map(
        location=[lapromedio, lopromedio],
        zoom_start=13,
    )
    from Folium import plugins
    #plugins.Search(states, search_zoom=6, geom_type='Polygon').add_to(m)
    x = crearJson(todos)
    plugins.Search(x, search_zoom=20).add_to(m)
    for i in todos:
        ubicacion = i[0].split(" ")
        latitud = ubicacion[0].replace("S","-")
        longitud = ubicacion[1].replace("W","-")
        rut = i[1]
        folium.Marker([float(latitud),float(longitud)], popup='<div><p>Cliente : '+rut+'</p><p>Latitud : '+latitud+'</p><p>Longitud : '+longitud+'</p><p>Hora : '+hora+'</p></div>',icon =folium.Icon(color='red')).add_to(m)
        #folium.Marker([float(latitud),float(longitud)], popup='<i>'+rut+'</i>').add_to(registros)
        data = [latitud,longitud,rut]


    registro.save("rendiciones/"+fechaCarpeta+"/registros.html")
    plug.add_to(m)
    legend_html =   '''
                <div style="position: fixed;
                            top: 50px; right: 50px; width: 15%; height: 15%;
                            border:2px solid grey; z-index:9999; font-size:14px;
                            ">&nbsp; Datos Generales <br>
                            <div style="color:green">&nbsp; Base &nbsp:''' +str(total)+''' </div>
                              Entregados &nbsp;:''' +str(len(todos))+'''  <i class="fa fa-map-marker fa-2x" style="color:red"></i> <br>
                '''
    faltantes = 0
    for info in errores:
        legend_html +=   '''&nbsp;'''+str(info[0])+''' &nbsp:''' +str(info[1])+''' <br> '''
        faltantes = faltantes + info[1]

    ResultadoTotal = len(todos) + faltantes
    legend_html += '''&nbsp; Resultado Total &nbsp:''' +str(ResultadoTotal)+'''    '''
    legend_html += '''<div style="color:red">&nbsp; Faltantes &nbsp:''' +str(total - ResultadoTotal)+'''  </div>  '''
    legend_html += '''</div> '''
    m.get_root().html.add_child(folium.Element(legend_html))
    m.save("rendiciones/"+fechaCarpeta+"/todos.html")

print ("cantidad total de documentos entregados : "+str(len(todos)) )
############################
lista_ruts = []

for i in ruts:
    if i not in lista_ruts:
        lista_ruts.append(i)
print ("cantidad de ruts "+str(len(lista_ruts)) )
#noEncontrados = []
#print (rutsEncontrados
#for i in lista_ruts:
    #if i not in rutsEncontrados:
#        print (i
#        noEncontrados.append(i)

#print (len(lista_ruts)
#print (len(noEncontrados)
