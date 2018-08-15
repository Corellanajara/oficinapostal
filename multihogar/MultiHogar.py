import folium
import os
import json
from folium import plugins
import random
total = input("Cantidad total de documentos : ")
x = 1
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
def subirAlServidor(carpeta,archivo):
    import ftplib
    import os

    # Datos FTP
    ftp_servidor = 'ftp.oficinapostalchile.cl'
    ftp_usuario  = 'oficinap'
    ftp_clave    = 'J0Kkap10l9'
    ftp_raiz     = '/public_html/multihogar' # Carpeta del servidor donde queremos subir el fichero

    fichero_origen = '/rendiciones/carpeta/'+archivo+'.html' # Ruta al fichero que vamos a subir
    fichero_destino = archivo+'.html' # Nombre que tendra el fichero en el servidor

    try:
    	s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
    	try:
    		f = open(fichero_origen, 'rb')
    		s.cwd(ftp_raiz)
    		s.storbinary('STOR ' + fichero_destino, f)
    		f.close()
    		s.quit()
    	except:
    		print "No se ha podido encontrar el fichero " + fichero_origen
    except:
    	print "No se ha podido conectar al servidor " + ftp_servidor



def crearJson(datos):
    from easydict import EasyDict as edict
    listaDatos = []
    for data in datos:
        latitud = data[0]
        longitud = data[1]
        cuerpo = '{"type": "Feature", "properties": {"@id": "node/3578353919", "addr:city": "Curico", "addr:country": "Chile","name": "'+str(data[2])+'"}, "geometry": {"type": "Point", "coordinates": ['+str(longitud)+','+str(latitud)+']}}'
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
        data = [hora,minuto,segundo]
        posibilidades.append(data)
    return posibilidades

def buscar(dia,hora,sesgo,file):
    contador = 0
    dias = dia.split("-")
#    print (dias
    dia = int(dias[0])
    mes = int(dias[1])
    year = int(dias[2])

    gps = open("gps/"+str(file),"r")
    for texto in gps:
        if str(texto[:10]) == "Trackpoint" :
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
lista_ruts = []
todos = []
todosNoEncontrados = []
location = "lector/"
coordenadas = []
archivos = []
rutas = []
ruts = []
sectores = []
mapa = 0
ultimaLatitud = " "
ultimaLongitud = " "
rut_lista = []
for file in os.listdir(location):
    rendicion = []
    noEncontrados = []

    lector = open("lector/"+file,"r")
    nombreSector = file.split("_")
    fechaCarpeta = nombreSector[1][0:2]
    if not os.path.exists("rendiciones/"+fechaCarpeta):
        os.makedirs("rendiciones/"+fechaCarpeta)
    nombreSector = nombreSector[0]
    nombreSector = nombreSector[1:]
    if nombreSector == "molina1" or nombreSector == "molina2":
        archivos.append(folium.Map(
            location=[-35.11534,-71.27811],
            zoom_start=13
        ))
    else :
        archivos.append(folium.Map(
            location=[-34.9926116,-71.2527959],
            zoom_start=13
        ))

    archivo = file.replace("lector","gps")
    print (file)
    print (archivo)
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
                gps = buscar(dia,hora,sesgo,archivo)
                if gps != None :
                    ubicacion = gps.split(" ")
                    latitud = ubicacion[0].replace("S","-")
                    longitud = ubicacion[1].replace("W","-")
                    rutsEncontrados.append(rut)
                    dato = [latitud , longitud , rut, hora]
                    rendicion.append(dato)
                    ultimaLatitud = latitud
                    ultimaLongitud = longitud
                else :
                    dato = [str(float(ultimaLatitud)+random.uniform(0.00003,0.0005)) , str(float(ultimaLongitud)+random.uniform(0.00003,0.0005)) , rut, hora]
                    rendicion.append(dato)
                    noEncontrados.append(rut)
                    print "no lo encontre "
            c = c + 1

    lista_nueva = []

    no_encontrados = []
    for i in rendicion:
        if i[2] not in rut_lista:
            lista_nueva.append(i)
            todos.append(i)
            rut_lista.append(i[2])
    for i in noEncontrados:
        if i not in no_encontrados:
            no_encontrados.append(i)
        if i not in todosNoEncontrados:
            todosNoEncontrados.append(i)
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
        latitud = i[0]
        longitud = i[1]
        rut = i[2]
        hora = i[3]
        print latitud
        print longitud
        print hora
        print rut
        print i
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
        #for i in no_encontrados:
         #   latitud = float(lapromedio) + random.uniform(0.0003,0.005)
          #  longitud = float(lopromedio) + random.uniform(0.0003,0.005)
           # folium.Marker([float(latitud),float(longitud)],icon =folium.Icon(color='red'), popup='<div><p>Cliente : '+i+'</p><p>Latitud : '+str(latitud)+'</p><p>Longitud : '+str(longitud)+'</p><p>Hora : '+hora+'</p></div>').add_to(archivos[mapa])
        folium.features.Circle(location=[lapromedio, lopromedio], radius=1500,
                        color='black',
                        fill=True,
                        fill_color='#07131d'
                        ).add_to(archivos[mapa])

        plug = plugins.TimestampedGeoJson({
            'type': 'FeatureCollection',
        }, period='PT1M', add_last_point=True)

        #plug.add_to(archivos[mapa])
        legend_html =   '''

                   <div style="position: fixed;
                            bottom: 50px; right: 40px;z-index:9999;
                            "><img src="http://oficinapostalchile.cl/datos/oficinapostal.png" alt="oficinapostal logo" height="90px" width="110px" ></div>
                    <div style="position: fixed;
                                top: 10px; left: 50px; width: 190px; height: 100px;
                                border:2px solid grey; z-index:9999; font-size:14px;
                                "><br>&nbsp; Datos Generales <br>
                                  &nbsp; Entregados &nbsp; : ''' +str(len(lista_nueva) )+''' <i class="fa fa-map-marker fa-2x" style="color:red"></i>
                    </div>
                    '''

        archivos[mapa].get_root().html.add_child(folium.Element(legend_html))

        archivos[mapa].save("rendiciones/"+fechaCarpeta+"/"+nombreSector+".html")
        subirAlServidor(fechaCarpeta,nombreSector);
        mapa = mapa + 1

    m = folium.Map(
        location=[lapromedio, lopromedio],
        zoom_start=13,
    )
    n = folium.Map(
        location=[lapromedio, lopromedio],
        zoom_start=13,
    )
    from Folium import plugins
    #plugins.Search(states, search_zoom=6, geom_type='Polygon').add_to(m)
    x = crearJson(todos)
    plugins.Search(x, search_zoom=20).add_to(n)
    for i in todos:
        latitud = i[0]
        longitud = i[1]
        rut = i[2]
        folium.Marker([float(latitud),float(longitud)], popup='<div><p>Cliente : '+rut+'</p><p>Latitud : '+latitud+'</p><p>Longitud : '+longitud+'</p><p>Hora : '+hora+'</p></div>',icon =folium.Icon(color='red')).add_to(m)
        #folium.Marker([float(latitud),float(longitud)], popup='<i>'+rut+'</i>').add_to(registros)
        data = [latitud,longitud,rut]

    registro.save("rendiciones/"+fechaCarpeta+"/registros.html")

    plug.add_to(m)

    for i in ruts:
        if i not in lista_ruts:
            lista_ruts.append(i)
    problemas = len(lista_ruts) - len(todos)
    legend_html =   '''

                <div style="position: fixed;
                            bottom: 50px; right: 40px;z-index:9999;
                            "><img src="http://oficinapostalchile.cl/datos/oficinapostal.png" alt="oficinapostal logo" height="90px" width="110px" ></div>
                <div style="position: fixed;
                            top: 10px; left: 50px; width: 200px; height: 200px;
                            border:2px solid grey; z-index:9999; font-size:14px;
                            "><br>&nbsp; Datos Generales <br>
                            <div style="color:green">&nbsp; Base &nbsp:''' +str(total)+''' </div>
                                &nbsp;  Entregados &nbsp;:''' +str(len(todos)+problemas)+'''  <i class="fa fa-map-marker fa-2x" style="color:red"></i> <br>


                '''
    faltantes = 0
    for info in errores:
        legend_html +=   '''&nbsp;&nbsp;'''+str(info[0])+''' &nbsp:''' +str(info[1])+''' <br> '''
        faltantes = faltantes + info[1]

    ResultadoTotal = len(todos) + faltantes + problemas
    legend_html += '''&nbsp; Resultado Total &nbsp:''' +str(ResultadoTotal)+'''    '''
    legend_html += '''<div style="color:red">&nbsp; Faltantes &nbsp:''' +str(total - ResultadoTotal)+'''  </div>  '''
    legend_html += '''</div> '''
    m.get_root().html.add_child(folium.Element(legend_html))
    m.save("rendiciones/"+fechaCarpeta+"/todos.html")
    n.get_root().html.add_child(folium.Element(legend_html))
    n.save("rendiciones/"+fechaCarpeta+"/buscarClientes.html")

print ("cantidad total de documentos entregados : "+str(len(todos)) )
############################
print ("cantidad de ruts "+str(len(lista_ruts)) )
