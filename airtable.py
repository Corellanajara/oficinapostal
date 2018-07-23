#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import MySQLdb
db = MySQLdb.connect("192.99.150.93","oficinap_corellana","oficinapostal2018*","oficinap_oficinaPostal" )
#db = MySQLdb.connect("localhost","root","789123","oficinaPostal" )
query = db.cursor()

url = "https://api.airtable.com/v0/appPVvurYaZbgh3qt/Carga%20Carteros"
headers={"Authorization":"Bearer keyrVS4U5PcmP2ADt"}
resp = requests.get(url,headers=headers)
contenido = json.loads(resp.content)
#print contenido
for dato in contenido['records']:
    print dato
    id = dato['id']
    creado = dato['createdTime']
    sector = dato['fields']['sector']
    cartero = dato['fields']['Cartero']
    fecha = dato['fields']['Fecha']
    cantidad = dato['fields']['Cantidad']
    if 'Fecha Descarga' in dato['fields']:
        fechaDescarga = dato['fields']['Fecha Descarga']
        print "FECHA = "+str(fechaDescarga)
    print "id = "+str(id)
    print "creado = "+str(creado)
    print "fecha = "+str(fecha)
    print "cartero = "+str(cartero)
    print "sector = "+str(sector)
    sql = "REPLACE into carga values ('"+str(id)+"','"+str(creado)+"','"+str(fecha)+"','"+str(cartero)+"','"+sector+"',"+str(cantidad)+")"
    query.execute(sql)
    db.commit()
    print "\n"
