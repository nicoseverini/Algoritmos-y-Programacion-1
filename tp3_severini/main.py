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
ACCION_PEDIDO  = 0
CANT_VERDURA_PEDIDO = 1
VERDURA_PEDIDO = 2
NOMBRE_PEDIDO = 3
TOMATE = 'T'
BROCOLI = 'B'
ZANAHORIA = 'Z'
LECHUGA = 'L'

NUMERO_PEDIDO = 1
CANT_VERDURA_MODIFICAR = 2
VERDURA_MODIFICAR = 3

def buscar_nombre(nombre_ingresado):
  id = 1
  se_encontro_nombre = False
  try:
    archivo = open(CLIENTES)
  except:
    print("el archivos de clientes no se abrio correctamente")

  lista_clientes = csv.reader(archivo, delimiter = DELIMITADOR)
  for linea in lista_clientes:
    if linea[1] == nombre_ingresado:
      id = linea[0]
      se_encontro_nombre = True
    if not se_encontro_nombre:
      if int(linea[0]) >= id:
        id = (int(linea[0])+1)

  archivo.close()

  return id , se_encontro_nombre

def buscar_id(id):
  se_encontro_id = False
  try:
    archivo = open(CLIENTES)
  except:
    print("el archivos de clientes no se abrio correctamente")

  lista_clientes = csv.reader(archivo, delimiter = DELIMITADOR)
  for linea in lista_clientes:
    if linea[0] == id:
      se_encontro_id = True
  archivo.close()

  return se_encontro_id

def pedido_repetido(id, pedido):
  repetido = False
  with open(PEDIDOS) as archivo:
    lector_lista_pedidos = csv.reader(archivo, delimiter = DELIMITADOR)
    for linea in lector_lista_pedidos:
      if linea[0] == id and linea[1] == pedido:
        repetido = True
  return repetido
        
def verduras_venta(verdura_ingresada):
  return(verdura_ingresada == TOMATE or verdura_ingresada == BROCOLI or
          verdura_ingresada == ZANAHORIA or verdura_ingresada == LECHUGA)

def agregar_verdura_lista(lista_pedidos, lista_clientes, pedido):
  id, se_encontro_nombre = buscar_nombre(pedido[NOMBRE_PEDIDO])

  if not verduras_venta(pedido[VERDURA_PEDIDO]):
    print("No vendemos su verdura ingresada. La lista de verduras a la venta es:")
    print("("+TOMATE+") Tomate\n("+BROCOLI+") Brocoli\n("+ZANAHORIA+") Zanahoria\n("+LECHUGA+") Lechuga")

  elif int(pedido[CANT_VERDURA_PEDIDO]) <= 0:
    print("la cantidad de verduras es incorrecta")

  elif pedido_repetido(id, pedido[VERDURA_PEDIDO]):
    print("La verdura que estas intentando agregar, ya fue agregada")
    print("Intena nuevamente con: modificar (id del pedido) (cantidad del pedido) (verdura)")

  else:
      lista_pedidos.write(f"{id}{DELIMITADOR}{pedido[VERDURA_PEDIDO]}{DELIMITADOR}{pedido[CANT_VERDURA_PEDIDO]}\n")
      if not se_encontro_nombre:
        lista_clientes.write(f"{id}{DELIMITADOR}{pedido[NOMBRE_PEDIDO]}\n")
      print("Se agrego un producto a la lista")

def agregar(pedido):
  try:
    lista_pedidos = open(PEDIDOS, MODO_ADJUNTAR)
  except:
    print("No se pudo abrir el archivo de pedidos")
    return
  
  try:
    lista_clientes = open(CLIENTES, MODO_ADJUNTAR)
  except:
    lista_pedidos.close()
    print("No se pudo abrir el archivo de clientes")
    return
  
  agregar_verdura_lista(lista_pedidos, lista_clientes, pedido)

  lista_pedidos.close()
  lista_clientes.close()

def modificar_verdura_lista(archivo_pedidos, archivo_pedidos_aux, pedido):
  lector_lista_pedidos = csv.reader(archivo_pedidos, delimiter = DELIMITADOR)
  escritor_lista_pedidos_aux = csv.writer(archivo_pedidos_aux, delimiter = DELIMITADOR)
  id_encontrado = False

  for fila in lector_lista_pedidos:
    if fila[0] == pedido[NUMERO_PEDIDO]:
      id_encontrado = True
      if verduras_venta(pedido[VERDURA_MODIFICAR]):
        if fila[1] == pedido[VERDURA_MODIFICAR]:
          if int(pedido[CANT_VERDURA_MODIFICAR]) > 0:
            fila[2] = fila[2].replace(fila[2], pedido[CANT_VERDURA_MODIFICAR])
            print("La modificacion fue exitosa")
          else:
            print("la cantidad de verduras es incorrecta")
    
    escritor_lista_pedidos_aux.writerow(fila)
  
  if not id_encontrado:
    print("El id no fue encontrado")
  if not verduras_venta(pedido[VERDURA_MODIFICAR]):
    print("No vendemos su verdura ingresada. La lista de verduras a la venta es:")
    print("("+TOMATE+") Tomate\n("+BROCOLI+") Brocoli\n("+ZANAHORIA+") Zanahoria\n("+LECHUGA+") Lechuga")

def modificar(pedido):
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

def eliminar_pedidos(pedido):
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
    if fila[0] != pedido[1]:
      escritor_lista_pedidos_aux.writerow(fila)



  archivo_pedidos.close()
  archivo_pedidos_aux.close()

  os.rename(PEDIDOS_AUX, PEDIDOS)
   
def eliminar_cliente(pedido):
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
    if fila[0] != pedido[1]:
      escritor_lista_clientes_aux.writerow(fila)

  archivo_clientes.close()
  archivo_clientes_aux.close()

  os.rename(CLIENTES_AUX, CLIENTES)

def eliminar(pedido):
  if buscar_id(pedido[1]):
    eliminar_pedidos(pedido)
    eliminar_cliente(pedido)
    print("Se eliminaron los elementos correctamente")
  else:
    print("La id ingresada en incorrecta")

def listar(pedido):
  return 0


def acciones_lista_pedidos(pedido):
  if pedido[ACCION_PEDIDO] == "agregar":
    if len(pedido) == 4:
      agregar(pedido) 
    else:
      print("Parametros para agregar incorrectos. Los correctos son:")
      print("python3 main.py agregar (cantidad de verduras) (tipo de verdura) (nombre)")
  elif pedido[ACCION_PEDIDO] == "modificar":
    if len(pedido) == 4:
      modificar(pedido) 
    else:
      print("Parametros para modificar incorrectos. Los correctos son:")
      print("python3 main.py modificar (id del pedido) (cantidad del pedido) (verdura)")
  elif pedido[ACCION_PEDIDO] == "eliminar":
    if len(pedido) == 2:
      eliminar(pedido)
    else:
      print("Parametros para modificar incorrectos. Los correctos son:")
      print("python3 main.py eliminar (id del pedido)")
  elif pedido[ACCION_PEDIDO] == "listar":
    if len(pedido) >= 2:
      listar(pedido)
  else:
    print("Accion enviada incorrecta. Las correctas son:")
    print("agregar\nmodificar\neliminar\nlistar\n")
  
if __name__ == "__main__":
  pedido = sys.argv[1::]

  acciones_lista_pedidos(pedido)
