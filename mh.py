import folium
import pandas as pd
df = pd.read_csv("ArchivosGPS/msectorc1_0606gps.txt", sep='\xb0')
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
        data = [hora,minuto,segundo]
        posibilidades.append(data)
    return posibilidades

def buscar(dia,hora,sesgo):
    contador = 0
    dias = dia.split("-")
    dia = int(dias[0])
    mes = int(dias[1])
    year = int(dias[2])

    gps = open("ArchivosGPS/msectorc1_0606gps.txt","r")
    for texto in gps:
        if contador > 9:
            v =  texto.split("\t")
            if len(v) > 8:
                fecha = v[2].split(" ")
                if len(fecha) > 1:
                    Dias = fecha[0].split("-")
                    Dia = int(Dias[0])
                    Mes = int(Dias[1])
                    Year = int(Dias[2])
                    Hora = fecha[1]
                    #print v[1]
                    if(dia == Dia and mes==Mes):
                        lista = convertirHora(hora,sesgo)
                        #print lista
                        for elemento in lista:
                            newHora = str(elemento[0])+":"+str(elemento[1])+":"+str(elemento[2])
                            if newHora == Hora:
                                return v[1]
                        #return v[1]

        else :
            contador = contador + 1

    #obtener el 2  y si encaja
    # se anexa el 1 con el rut
    #print texto
rendicion = []
lector = open("ArchivosLectores/msectorc1_0606lector.txt","r")
ruts = []
sesgo = 22
for texto in lector:

    palabras = texto.split(",")
    c = 0
    for i in range(len(palabras)):
        if  i == 0:
            existe = palabras[i].find("-")

        if existe > 0 and len(palabras[0]) < 12 and len(palabras[0]) > 8:
            #aca los doscumentos son de multihogar
            rut = palabras[0]
            ruts.append(rut)
            #print "rut = "+str(rut)
            hora = palabras[2].split(" ")
            dia = hora[3]
            hora = hora[0]
            dia = dia.replace("/","-")
            dia = dia.replace("\n","")
            #print "dia ="+str(dia)
            #print "hora ="+str(hora)
            #print dia
            gps = buscar(dia,hora,sesgo)
            if gps != None :
                rutsEncontrados.append(rut)
                dato = [gps, rut]
                rendicion.append(dato)


            #print " \n"
            #buscar los que Teniendo el dia [ dia ]
            #esten dentro del sesgo de 6 segundos

        #print i
        c = c + 1
    #print texto
#print len(ruts)

lista_nueva = []
for i in rendicion:
    if i not in lista_nueva:
        lista_nueva.append(i)
#print lista_nueva
#print len(lista_nueva)
multihogar = []
#print lista_nueva


for i in lista_nueva:
    ubicacion = i[0].split(" ")
    latitud = ubicacion[0].replace("S","-")
    longitud = ubicacion[1].replace("W","-")
    rut = i[1]
    data = [latitud,longitud,rut]
    multihogar.append(data)
