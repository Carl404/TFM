# -*- coding: utf-8 -*-

import json
import os
import sys
import fileinput

# Reconocemos todos los .pcap del directorio
lista_ficheros = os.listdir()
capturas = []

for campo in lista_ficheros:
    if "captura" not in campo:
        continue
    else:
        capturas.append(campo)

# Parse a JSON
for nombre_captura in capturas:
    nombre_json = nombre_captura.replace(".pcap", ".json")
    os.system("tshark -r " + nombre_captura + " -T ek > " + nombre_json)

os.system("more titulo.txt")

# Etiquetado
# Envio a ELASTICSEARCH
lista_ficheros_prev = os.listdir()
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
			sys.stdout.write(line.replace("}}}}", "}}},\"traffic_type\": \"normal\"}"))
	elif opcion_etiquetado == "2":
		for i, line in enumerate(fileinput.input(json_file, inplace=1)):
			sys.stdout.write(line.replace("}}}", "}},\"traffic_type\": \"anomalo\"}"))
			sys.stdout.write(line.replace("}}}}", "}}},\"traffic_type\": \"anomalo\"}"))
	elif opcion_etiquetado == "3":
		desc_ataque = input ("Qué tipo de ataque se ha producido?: ")
		for i, line in enumerate(fileinput.input(json_file, inplace=1)):
			sys.stdout.write(line.replace("}}}", "}},\"traffic_type\": \"attack - " + desc_ataque + "\"}"))
			sys.stdout.write(line.replace("}}}}", "}}},\"traffic_type\": \"attack - " + desc_ataque +"\"}"))

# Envio a ELASTICSEARCH
lista_ficheros = os.listdir()
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
	json_size = os.path.getsize(nombre_fichero)
	print(json_size)
	if json_size > max_size: # json_size > max_size
		lista_ficheros_json.remove(nombre_fichero)
		# Hay que dividir
		with open(nombre_fichero) as fp:
			line = fp.readline()
			cnt = 0
			cnt_file = 1
			for line in fp:
				#print (line)
				fichero_resultado = "fichero_resultado[" + str(cnt_file) + "].json"
				file2 = open (fichero_resultado, "w")
				line2 = fp.readline()
				file2.write(line2)
				file2.write(line)
				cnt += 1
				# Criterios de parada
				# "pcap_file"}
				# }}}}
				if cnt == 2:
					cnt = 0
					cnt_file += 1
					#print ("Fin fichero")
					#file2.close()

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

os.system("more envio.txt")

# Envio a ELASTICSEARCH
#for json_file in lista_ficheros_json:
#	comando_envio = comando_envio.replace("NOMBRE.JSON", json_file)
#	print(comando_envio)
	#os.system(comando_envio)

# Envio a de los json fragmentados
os.system("rm *.swp")

lista_all = os.listdir()
lista_ficheros_json_frag = []

for campo in lista_all:
	if "].json" not in campo:
		continue
	else:
		lista_ficheros_json_frag.append(campo)


comando_envio_aux = "curl -s -H \"Content-Type: application/x-ndjson\" -XPOST \"11.0.0.2:9200/_bulk\" --data-binary \"@NOMBRE.JSON\""

for json_file in lista_ficheros_json_frag:
	#json_file_formatted = json_file.replace("[", "\[")
	#json_file_formatted = json_file.replace("]", "\]")
	comando_envio_aux = comando_envio_aux.replace("NOMBRE.JSON", json_file)
	os.system(comando_envio_aux)

