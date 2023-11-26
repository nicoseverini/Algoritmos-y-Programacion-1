import sys
import csv
import os

PEDIDOS = "pedidos.csv"
PEDIDOS_AUX = "pedidos_aux.csv"
CLIENTES = "clientes.csv"
CLIENTES_AUX = "clientes_aux.csv"
MODO_ADJUNTAR = "a"
MODO_ESCRIBIR ="w"
DELIMITADOR = ";"
TOMATE = 'T'
BROCOLI = 'B'
ZANAHORIA = 'Z'
LECHUGA = 'L'
PALABRA_PARA_AGREGAR = "agregar"
PALABRA_PARA_MODIFICAR = "modificar"
PALABRA_PARA_ELIMINAR = "eliminar"
PALABRA_PARA_LISTAR = "listar"

PEDIDOS_ID_CLIENTE = 0
PEDIDOS_VERDURA = 1
PEDIDOS_CANT_VERDURA = 2

CLIENTES_ID_CLIENTE = 0
CLIENTES_NOMBRE_CLIENTE = 1

ACCION_INGRESADA  = 0
CANT_VERDURA_INGRESADA = 1
VERDURA_INGERSADA = 2
NOMBRE_CLIENTE_INGRESADO = 3

ID_CLIENTE = 1
CANT_VERDURA_MODIFICAR = 2
VERDURA_A_MODIFICAR = 3

def inicializar_archivos():
  try:
    archivo_clientes = open(CLIENTES,MODO_ADJUNTAR)
    archivo_pedidos = open(PEDIDOS,MODO_ADJUNTAR)

    archivo_pedidos.close()
    archivo_clientes.close()
  except:
    print("Error al inicializar los archivos")

def buscar_id_por_nombre(nombre_ingresado):
  id = 1
  se_encontro_nombre = False
  try:
    archivo_clientes = open(CLIENTES)
  except:
    print("El archivos de clientes no se abrio correctamente")
    return

  lector_lista_clientes = csv.reader(archivo_clientes, delimiter = DELIMITADOR)
  for linea in lector_lista_clientes:
    if linea[CLIENTES_NOMBRE_CLIENTE] == nombre_ingresado:
      id = linea[CLIENTES_ID_CLIENTE]
      se_encontro_nombre = True
    if not se_encontro_nombre:
      if int(linea[CLIENTES_ID_CLIENTE]) >= id:
        id = (int(linea[CLIENTES_ID_CLIENTE])+1)

  archivo_clientes.close()

  return id , se_encontro_nombre

def buscar_id(id):
  se_encontro_id = False
  try:
    archivo_clientes = open(CLIENTES)
  except:
    print("el archivos de clientes no se abrio correctamente")
    return

  lector_lista_clientes = csv.reader(archivo_clientes, delimiter = DELIMITADOR)
  for linea in lector_lista_clientes:
    if linea[CLIENTES_ID_CLIENTE] == id:
      se_encontro_id = True
  archivo_clientes.close()
 
  return se_encontro_id

def es_pedido_repetido(id, verdura_ingresada):
  repetido = False
  try:
    archivo_pedidos = open(PEDIDOS)
  except:
    print("El arhivo de pedidos no se abrio correctamente")
    return

  lector_lista_pedidos = csv.reader(archivo_pedidos, delimiter = DELIMITADOR)
  for linea in lector_lista_pedidos:
    if linea[PEDIDOS_ID_CLIENTE] == id and linea[PEDIDOS_VERDURA] == verdura_ingresada:
      repetido = True

  archivo_pedidos.close()
  return repetido
        
def es_verdura_disponible(verdura_ingresada):
  return(verdura_ingresada == TOMATE or verdura_ingresada == BROCOLI or
          verdura_ingresada == ZANAHORIA or verdura_ingresada == LECHUGA)

def agregar_verdura_lista(archivo, id_cliente, verdura, cant_verdura):
  archivo.write(f"{id_cliente}{DELIMITADOR}{verdura}{DELIMITADOR}{cant_verdura}\n")

def agregar_lista_pedidos(id, pedido):
  try:
    archivo_pedidos = open(PEDIDOS)
  except:
    print("No se pudo abrir el archivo de pedidos")
    return

  try:
    archivo_pedidos_aux = open(PEDIDOS_AUX, MODO_ESCRIBIR)
  except:
    archivo_pedidos.close()
    print("No se pudo crear un archivo de pedidos auxiliar")
    return

  lector_lista_pedidos = csv.reader(archivo_pedidos, delimiter = DELIMITADOR)
  escritor_lista_pedidos_aux = csv.writer(archivo_pedidos_aux, delimiter = DELIMITADOR)
  se_agrego = False
  for fila in lector_lista_pedidos:
    if fila[PEDIDOS_ID_CLIENTE] == id and not se_agrego:
      se_agrego = True
      agregar_verdura_lista(archivo_pedidos_aux, id, pedido[VERDURA_INGERSADA], pedido[CANT_VERDURA_INGRESADA])

    escritor_lista_pedidos_aux.writerow(fila)

  if not se_agrego:
    agregar_verdura_lista(archivo_pedidos_aux, id, pedido[VERDURA_INGERSADA], pedido[CANT_VERDURA_INGRESADA])

  archivo_pedidos.close()
  archivo_pedidos_aux.close()

  os.rename(PEDIDOS_AUX, PEDIDOS) 

def agregar_lista_clientes(id, nombre_cliente):
  try:
    archivo_clientes = open(CLIENTES, MODO_ADJUNTAR)
  except:
    print("No se pudo abrir el archivo de clientes")
    return

  archivo_clientes.write(f"{id}{DELIMITADOR}{nombre_cliente}\n")

  archivo_clientes.close()

def agregar(pedido):
  id, se_encontro_nombre = buscar_id_por_nombre(pedido[NOMBRE_CLIENTE_INGRESADO])

  if not es_verdura_disponible(pedido[VERDURA_INGERSADA]):
    print("No vendemos su verdura ingresada. La lista de verduras a la venta es:")
    print("("+TOMATE+") Tomate\n("+BROCOLI+") Brocoli\n("+ZANAHORIA+") Zanahoria\n("+LECHUGA+") Lechuga")

  elif int(pedido[CANT_VERDURA_INGRESADA]) <= 0:
    print("la cantidad de verduras es incorrecta")

  elif es_pedido_repetido(id, pedido[VERDURA_INGERSADA]):
    print("La verdura que estas intentando agregar, ya fue agregada")
    print("Intena nuevamente con: modificar (id del pedido) (cantidad del pedido) (verdura)")

  else:
    agregar_lista_pedidos(id, pedido)
    if not se_encontro_nombre:
      agregar_lista_clientes(id, pedido[NOMBRE_CLIENTE_INGRESADO])

    print("Se agrego un producto a la lista")

def modificar_verdura_lista(archivo_pedidos, archivo_pedidos_aux, pedido):
  lector_lista_pedidos = csv.reader(archivo_pedidos, delimiter = DELIMITADOR)
  escritor_lista_pedidos_aux = csv.writer(archivo_pedidos_aux, delimiter = DELIMITADOR)
  se_modifico = False
  se_agrego = False
  se_encontro_id = False

  for fila in lector_lista_pedidos:
    if fila[PEDIDOS_ID_CLIENTE] == pedido[ID_CLIENTE]:
      se_encontro_id = True
      if fila[PEDIDOS_VERDURA] == pedido[VERDURA_A_MODIFICAR]:
        fila[PEDIDOS_CANT_VERDURA] = fila[PEDIDOS_CANT_VERDURA].replace(fila[PEDIDOS_CANT_VERDURA], pedido[CANT_VERDURA_MODIFICAR])
        se_modifico = True
        print("La modificacion fue exitosa")
    if not se_modifico and not se_agrego and se_encontro_id and fila[PEDIDOS_ID_CLIENTE] != pedido[ID_CLIENTE]:
      se_agrego = True
      agregar_verdura_lista(archivo_pedidos_aux, pedido[ID_CLIENTE], pedido[VERDURA_A_MODIFICAR], pedido[CANT_VERDURA_MODIFICAR])
      print("Se agrego la modificacion correctamente")   
        
    escritor_lista_pedidos_aux.writerow(fila)
  
  if not se_modifico and not se_agrego:
    agregar_verdura_lista(archivo_pedidos_aux, pedido[ID_CLIENTE], pedido[VERDURA_A_MODIFICAR], pedido[CANT_VERDURA_MODIFICAR])

def modificar(pedido):
  if buscar_id(pedido[ID_CLIENTE]):
    if es_verdura_disponible(pedido[VERDURA_A_MODIFICAR]):
      if int(pedido[CANT_VERDURA_MODIFICAR]) > 0:
        try:
          archivo_pedidos = open(PEDIDOS)
        except:
          print("No se pudo abrir el archivo de pedidos")
          return

        try:
          archivo_pedidos_aux = open(PEDIDOS_AUX, MODO_ESCRIBIR)
        except:
          archivo_pedidos.close()
          print("No se pudo crear un archivo de pedidos auxiliar")
          return

        modificar_verdura_lista(archivo_pedidos, archivo_pedidos_aux, pedido)   

        archivo_pedidos.close()
        archivo_pedidos_aux.close()

        os.rename(PEDIDOS_AUX, PEDIDOS) 

      else:
        print("la cantidad de verduras es incorrecta")
    else: 
      print("No vendemos su verdura ingresada. La lista de verduras a la venta es:")
      print("("+TOMATE+") Tomate\n("+BROCOLI+") Brocoli\n("+ZANAHORIA+") Zanahoria\n("+LECHUGA+") Lechuga")
  else:
    print("El id no fue encontrado")

def eliminar_pedidos(id_pedido):
  try:
    archivo_pedidos = open(PEDIDOS)
  except:
    print("No se pudo abrir el archivo de pedidos")
    return

  try:
    archivo_pedidos_aux = open(PEDIDOS_AUX, MODO_ESCRIBIR)
  except:
    archivo_pedidos.close()
    print("No se pudo crear un archivo de pedidos auxiliar")
    return
  
  lector_lista_pedidos = csv.reader(archivo_pedidos, delimiter = DELIMITADOR)
  escritor_lista_pedidos_aux = csv.writer(archivo_pedidos_aux, delimiter = DELIMITADOR)

  for fila in lector_lista_pedidos:
    if fila[PEDIDOS_ID_CLIENTE] != id_pedido:
      escritor_lista_pedidos_aux.writerow(fila)

  archivo_pedidos.close()
  archivo_pedidos_aux.close()

  os.rename(PEDIDOS_AUX, PEDIDOS)
   
def eliminar_cliente(id_cliente):
  try:
    archivo_clientes = open(CLIENTES)
  except:
    print("No se pudo abrir el archivo de pedidos")
    return

  try:
    archivo_clientes_aux = open(CLIENTES_AUX, MODO_ESCRIBIR)
  except:
    archivo_clientes.close()
    print("No se pudo crear un archivo de pedidos auxiliar")
    return

  lector_lista_clientes = csv.reader(archivo_clientes, delimiter = DELIMITADOR)
  escritor_lista_clientes_aux = csv.writer(archivo_clientes_aux, delimiter = DELIMITADOR)

  for fila in lector_lista_clientes:
    if fila[CLIENTES_ID_CLIENTE] != id_cliente:
      escritor_lista_clientes_aux.writerow(fila)

  archivo_clientes.close()
  archivo_clientes_aux.close()

  os.rename(CLIENTES_AUX, CLIENTES)

def eliminar(pedido):
  if buscar_id(pedido[ID_CLIENTE]):
    eliminar_pedidos(pedido[ID_CLIENTE])
    eliminar_cliente(pedido[ID_CLIENTE])
    print("Se eliminaron los elementos correctamente")
  else:
    print("La id ingresada en incorrecta")

def buscar_nombre_por_id(id):
  try:
    archivo_clientes = open(CLIENTES)
  except:
    print("el archivos de clientes no se abrio correctamente")
    return

  lector_lista_clientes = csv.reader(archivo_clientes, delimiter = DELIMITADOR)
  for linea in lector_lista_clientes:
    if linea[CLIENTES_ID_CLIENTE] == id:
      return linea[CLIENTES_NOMBRE_CLIENTE]

def nombre_verdura(inicial_verdura):
  if inicial_verdura == TOMATE:
    return "Tomate"
  if inicial_verdura == BROCOLI:
    return "Brocoli" 
  if inicial_verdura == ZANAHORIA:
    return "Zanahoria" 
  if inicial_verdura == LECHUGA:
    return "Lechuga" 

def listar(pedido):
  try:
    archivo_clientes = open(CLIENTES)
  except:
    print("el archivos de clientes no se abrio correctamente")
    return

  try:
    archivo_pedidos = open(PEDIDOS)
  except:
    print("El archivo de pedidos no se abrio correctamente")
    return

  lector_lista_clientes = csv.reader(archivo_clientes, delimiter = DELIMITADOR)
  lector_lista_pedidos = csv.reader(archivo_pedidos, delimiter = DELIMITADOR)

  if len(pedido) == 2:
    if buscar_id(pedido[ID_CLIENTE]):
      print("------------------------------------")
      for linea_cliente in lector_lista_clientes:
        if linea_cliente[CLIENTES_ID_CLIENTE] == pedido[ID_CLIENTE]:
          print(f"{linea_cliente[CLIENTES_NOMBRE_CLIENTE]}, id = ({linea_cliente[CLIENTES_ID_CLIENTE]})")
      for linea_pedido in lector_lista_pedidos:
        if linea_pedido[PEDIDOS_ID_CLIENTE] == pedido[ID_CLIENTE]:
          print(f"  {nombre_verdura(linea_pedido[PEDIDOS_VERDURA])}\t= {linea_pedido[PEDIDOS_CANT_VERDURA]}")
      print("------------------------------------")
    else:
      print("La id ingresada en incorrecta")
  else:
    nombre_actual = 0
    for linea_pedido in lector_lista_pedidos:
      if nombre_actual != linea_pedido[PEDIDOS_ID_CLIENTE]:
        print("------------------------------------")
        print(f"{buscar_nombre_por_id(linea_pedido[PEDIDOS_ID_CLIENTE])}, id = ({linea_pedido[PEDIDOS_ID_CLIENTE]})")
        nombre_actual = linea_pedido[PEDIDOS_ID_CLIENTE]

      print(f"  {nombre_verdura(linea_pedido[PEDIDOS_VERDURA])}\t= {linea_pedido[PEDIDOS_CANT_VERDURA]}")
    print("------------------------------------")

  archivo_clientes.close()
  archivo_pedidos.close()

def acciones_pedido(pedido):
  if pedido[ACCION_INGRESADA] == PALABRA_PARA_AGREGAR:
    if len(pedido) == 4:
      agregar(pedido) 
    else:
      print("Parametros para agregar incorrectos. Los correctos son:")
      print("python3 verduleria.py agregar (cantidad de verduras) (tipo de verdura) (nombre)")
  elif pedido[ACCION_INGRESADA] == PALABRA_PARA_MODIFICAR:
    if len(pedido) == 4:
      modificar(pedido) 
    else:
      print("Parametros para modificar incorrectos. Los correctos son:")
      print("python3 verduleria.py modificar (id del pedido) (cantidad del pedido) (verdura)")
  elif pedido[ACCION_INGRESADA] == PALABRA_PARA_ELIMINAR:
    if len(pedido) == 2:
      eliminar(pedido)
    else:
      print("Parametros para eliminar incorrectos. Los correctos son:")
      print("python3 verduleria.py eliminar (id del pedido)")
  elif pedido[ACCION_INGRESADA] == PALABRA_PARA_LISTAR:
    if len(pedido) <= 2:
      listar(pedido)
    else:
      print("Parametros para listas incorrectos. Los correctos son:")
      print("python3 verduleria.py lista (id del pedido) \nel id es opcional, se usa para ver un pedido en espesifico")
  else:
    print("Accion enviada incorrecta. Las correctas son:")
    print(f"{PALABRA_PARA_AGREGAR}\n{PALABRA_PARA_MODIFICAR}\n{PALABRA_PARA_ELIMINAR}\n{PALABRA_PARA_LISTAR}")
  
if __name__ == "__main__":
  pedido = sys.argv[1::]
  if len(pedido) < 1:
    print("Ingrese una accion")
  else:
    inicializar_archivos()
    acciones_pedido(pedido)