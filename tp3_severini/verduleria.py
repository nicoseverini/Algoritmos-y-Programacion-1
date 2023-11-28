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

#Pre: -
#Post: Inicializa los archivos para el funcionamiento del programa.
def inicializar_archivos():
  try:
    archivo_clientes = open(CLIENTES,MODO_ADJUNTAR)
    archivo_pedidos = open(PEDIDOS,MODO_ADJUNTAR)

    archivo_pedidos.close()
    archivo_clientes.close()
  except:
    print("Error al inicializar los archivos")

#Pre: -
#Post: Devuelve el ultimo id presente en el archivo de clientes.
def buscar_ultimo_id():
  id = 1
  try:
    archivo_clientes = open(CLIENTES)
  except:
    print("El archivos de clientes no se abrio correctamente")
    return

  lector_lista_clientes = csv.reader(archivo_clientes, delimiter = DELIMITADOR)
  for linea in lector_lista_clientes:
    if int(linea[CLIENTES_ID_CLIENTE]) >= id:
      id = (int(linea[CLIENTES_ID_CLIENTE]))+1

  archivo_clientes.close()

  return id

#Pre: -
#Post: Devuelve True si encuentra el id en el archivo de clientes, False en caso contrario.
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

#Pre: -
#Post: Devuelve True si la verdura ingresada esta disponible, False en caso contrario.
def es_verdura_disponible(verdura_ingresada):
  return(verdura_ingresada == TOMATE or verdura_ingresada == BROCOLI or
          verdura_ingresada == ZANAHORIA or verdura_ingresada == LECHUGA)

#Pre: El archivo debe ser un archivo valido abierto en MODO_ADJUNTAR o MODO_ESCRITURA.
#     El id debe existir
#     verdura_ingresada debe ser una verdura disponible
#     cant_verdura_ingresada debe ser un numero entero y positivo
#Post: Devuelve True si la verdura ingresada esta disponible, False en caso contrario.
def agregar_verdura_lista(archivo, id_cliente, verdura, cant_verdura):
  archivo.write(f"{id_cliente}{DELIMITADOR}{verdura}{DELIMITADOR}{cant_verdura}\n")

#Pre: El id debe existir
#     verdura_ingresada debe ser una verdura disponible
#     cant_verdura_ingresada debe ser un numero entero y positivo
#Post: Agrega el id del cliente(numero del pedido), el tipo de verdura y la cantidad del pedido al archivo de pedidos.
def agregar_lista_pedidos(id, verdura_ingresada, cant_verdura_ingresada):
  try:
    archivo_pedidos = open(PEDIDOS, MODO_ADJUNTAR)
  except:
    print("No se pudo abrir el archivo de pedidos")
    return
  
  agregar_verdura_lista(archivo_pedidos, id, verdura_ingresada, cant_verdura_ingresada)

  archivo_pedidos.close()

#Pre: EL id debe ser un numero entero y positivo
#Post: Agrega el id y el nombre del cliente al archivo de clientes.
def agregar_lista_clientes(id, nombre_cliente):
  try:
    archivo_clientes = open(CLIENTES, MODO_ADJUNTAR)
  except:
    print("No se pudo abrir el archivo de clientes")
    return

  archivo_clientes.write(f"{id}{DELIMITADOR}{nombre_cliente}\n")

  archivo_clientes.close()

#Pre: Pedido debe ser una lista valida con informacion del pedido a agregar.
#Post: Agrega un pedido y un cliente a la lista.
def agregar(pedido):
  if not es_verdura_disponible(pedido[VERDURA_INGERSADA]):
    print("No vendemos su verdura ingresada. La lista de verduras a la venta es:")
    print("("+TOMATE+") Tomate\n("+BROCOLI+") Brocoli\n("+ZANAHORIA+") Zanahoria\n("+LECHUGA+") Lechuga")

  elif not (pedido[CANT_VERDURA_INGRESADA]).isnumeric() or pedido[CANT_VERDURA_INGRESADA] == "0":
    print("La cantidad de verduras tiene que ser un entero positivo")

  else:
    id = buscar_ultimo_id()
    agregar_lista_pedidos(id, pedido[VERDURA_INGERSADA], pedido[CANT_VERDURA_INGRESADA])
    agregar_lista_clientes(id, pedido[NOMBRE_CLIENTE_INGRESADO])

    print("Se agrego un producto a la lista")

#Pre: : archivo_pedidos debe ser un archivo valido abierto en MODO_ESCRITURA.
#       archivo_pedidos_aux debe ser un archivo valido abierto en MODO_ESCRITURA.
#       Pedido debe ser una lista valida con informacion del pedido a modificar.
#Post: Modifica la cantidad de verduras de un pedido en el archivo de pedidos o agrega un nuevo pedido si no existe.
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

#Pre: Pedido debe ser una lista valida con informacion del pedido a modificar.
#Post: Modifica un pedido existente en el archivo de pedidos.
def modificar(pedido):
  if not buscar_id(pedido[ID_CLIENTE]):
    print("El id no fue encontrado")
  elif not es_verdura_disponible(pedido[VERDURA_A_MODIFICAR]):
    print("No vendemos su verdura ingresada. La lista de verduras a la venta es:")
    print("("+TOMATE+") Tomate\n("+BROCOLI+") Brocoli\n("+ZANAHORIA+") Zanahoria\n("+LECHUGA+") Lechuga")
  elif not (pedido[CANT_VERDURA_MODIFICAR]).isnumeric() or pedido[CANT_VERDURA_MODIFICAR] == "0":
    print("La cantidad de verduras tiene que ser un entero positivo")
  else:
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

#Pre: id_pedido debe ser un valor valido para identificar un pedido el la lista.
#Post: Elimina el pedido con el id especificado del archivo de pedidos y actualiza el archivo principal.
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

#Pre:  id_cliente debe ser un valor valido para identificar un cliente en la lista.
#Post: Elimina el cliente con el id especificado del archivo de clientes y actualiza el archivo principal.
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

#Pre: Pedido debe ser una lista valida con informacion del pedido a eliminar.
#Post: Elimina un pedido y cliente de los archivos.
def eliminar(pedido):
  if buscar_id(pedido[ID_CLIENTE]):
    eliminar_pedidos(pedido[ID_CLIENTE])
    eliminar_cliente(pedido[ID_CLIENTE])
    print("Se eliminaron los elementos correctamente")
  else:
    print("La id ingresada en incorrecta")

#Pre: El id tiene que existir.
#Post: Devuelve el nombre del cliente asociado al id.
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

#Pre: inicial_verdura tiene que ser una verdura disponible
#Post: Devuelve el nombre de la verdura segun su inicial.
def nombre_verdura(inicial_verdura):
  if inicial_verdura == TOMATE:
    return "Tomate"
  if inicial_verdura == BROCOLI:
    return "Brocoli" 
  if inicial_verdura == ZANAHORIA:
    return "Zanahoria" 
  if inicial_verdura == LECHUGA:
    return "Lechuga" 

#Pre: Pedido debe ser una lista valida con informacion del pedido a listar.
#Post: Muestra en consola toda la lista de pedidos y clientes si no se ingresa  id, En caso de que ingrese un id lista el pedido y cliente de dicho id.
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

#Pre: pedido debe ser una lista no vacia, con al menos un elemento que represente la accion a realizar.
#Post: Realiza la accion correspondiente segun los parametros del pedido.
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