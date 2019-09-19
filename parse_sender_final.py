# -*- coding: utf-8 -*-
#@author: Carlos Araujo
import json
import os
import sys
import fileinput

# Reconocemos todos los .pcap del directorio
lista_ficheros = os.listdir(os.path.dirname(os.path.realpath(__file__)))
capturas = []

for campo in lista_ficheros:
    if ".pcap" not in campo:
        continue
    else:
        capturas.append(campo)

# Parse a JSON
for nombre_captura in capturas:
	print ("Parse a json")
	nombre_json = nombre_captura.replace(".pcap", ".json")
	os.system("tshark -r " + nombre_captura + " -T ek > " + nombre_json)

os.system("more titulo.txt")

# Etiquetado
# Envio a ELASTICSEARCH
lista_ficheros_prev = os.listdir(os.path.dirname(os.path.realpath(__file__)))
lista_ficheros_json_prev = []

# Recuperamos los ficheros json del directorio
for campo in lista_ficheros_prev:
    if ".json" not in campo:
        continue
    else:
        lista_ficheros_json_prev.append(campo)
for json_file in lista_ficheros_json_prev:
	print ("En el fichero [" + json_file  + "]")
	opcion_etiquetado = input ("Qué tipo de tráfico se ha generado?:\n\n [1] Normal\n\n [2] Anómalo\n\n [3] Ataque\n\n ----------------\n Opción: ")
	
	if opcion_etiquetado == "1":
		for i, line in enumerate(fileinput.input(json_file, inplace=1)):
			sys.stdout.write(line.replace("}}}", "}},\"traffic_type\": \"normal\"}"))
			#sys.stdout.write(line.replace("}}}}", "}}},\"traffic_type\": \"normal\"}"))
	elif opcion_etiquetado == "2":
		for i, line in enumerate(fileinput.input(json_file, inplace=1)):
			sys.stdout.write(line.replace("}}}", "}},\"traffic_type\": \"anomalous\"}"))
			#sys.stdout.write(line.replace("}}}}", "}}},\"traffic_type\": \"anomalo\"}"))
	elif opcion_etiquetado == 3:
		desc_ataque = raw_input ("Qué tipo de ataque se ha producido?: ")
		comando_desc_ataque =  "}},\"traffic_type\": \"attack -" + desc_ataque + "}"
		for i, line in enumerate(fileinput.input(json_file, inplace=1)):
			print("ajjaj")
			sys.stdout.write(line.replace("}}}", comando_desc_ataque))
			#sys.stdout.write(line.replace("}}}}", "}}},\"traffic_type\": \"attack - " + desc_ataque +"\"}"))

# Envio a ELASTICSEARCH
lista_ficheros = os.listdir(os.path.dirname(os.path.realpath(__file__)))
lista_ficheros_json = []

# Recuperamos los ficheros json del directorio
for campo in lista_ficheros:
    if ".json" not in campo:
        continue
    else:
        lista_ficheros_json.append(campo)

# Split, si es necesario
# Máximo 100mb por fichero
max_size = 100000000

for nombre_fichero in lista_ficheros_json:
	file_size = os.path.getsize(nombre_fichero)
	print(file_size)
	print(max_size)
	if file_size > max_size:
		lista_ficheros_json.remove(nombre_fichero) # lo borramos para no volver a pasar por el
		# Hay que dividir
		cnt = 0 #numero de linea
		cnt_file = 1 #numero de fichero
		with open(nombre_fichero) as fp:
			for linea in fp:
				fichero_resultado = "fichero_resultado_" + str(cnt_file) + ".json"

				file2 = open (fichero_resultado, "a")
				file2.write(linea)
				file2.close()
				cnt += 1
			# Criterios de parada
				if cnt == 1000:
					cnt = 0
					cnt_file += 1
					print ("Fin del fichero número: " + str(cnt_file))
					file2.close()
	# A AQUÍ
# Continuamos con el envio
ip_elastic_server_public = "elk404.ddns.net"
ip_elastic_server_private = "11.0.0.2"

direccion = input ("A qué servidor desea enviarlo?:\n\n [1] Público\n\n [2] Privado\n\n ----------------\n Opción: ")
target_server = ""
if direccion == "1":
    print ("Enviando al servidor ELASTICSEARCH [" + ip_elastic_server_public +   "]")
    target_server = ip_elastic_server_public
else:
    print ("Enviando al servidor ELASTICSEARCH")
    target_server = ip_elastic_server_private

comando_envio = "curl -s -H \"Content-Type: application/x-ndjson\" -XPOST \"" + target_server + ":9200/_bulk\" --data-binary \"@NOMBRE.JSON\""
print (comando_envio)
os.system("more envio.txt")

# Envio a de los json fragmentados
lista_all = os.listdir(os.path.dirname(os.path.realpath(__file__)))
lista_ficheros_json_frag = []
print (lista_all)
for campo in lista_all:
	if "fichero" not in campo:
		continue
	else:
		lista_ficheros_json_frag.append(campo)


comando_envio_aux = "curl -s -H \"Content-Type: application/x-ndjson\" -XPOST \"11.0.0.2:9200/_bulk\" --data-binary \"@NOMBRE.JSON\""

for json_file in lista_ficheros_json_frag:
	print (comando_envio_aux)
	comando_envio_aux = comando_envio_aux.replace("NOMBRE.JSON", json_file)
	os.system(comando_envio_aux)

