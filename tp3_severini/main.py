import sys
import csv

PEDIDOS = "pedidos.csv"
CLIENTES = "clientes.csv"
MODO_ADJUNTAR = "a"
DELIMITADOR = ";"
ACCION_PEDIDO  = 1
CANT_PEDIDO = 2
VERDURA_PEDIDO = 3
NOMBRE_PEDIDO = 4
TOMATE = 'T'
BROCOLI = 'B'
ZANAHORIA = 'Z'
LECHUGA = 'L'



def buscar_id(nombre_ingresado):
  id = 1
  se_encontro_id = False
  with open(CLIENTES) as archivo:
    lista_clientes = csv.reader(archivo, delimiter = DELIMITADOR)
    for linea in lista_clientes:
      if linea[1] == nombre_ingresado:
        id = linea[0]
        se_encontro_id = True
      if not se_encontro_id:
        if int(linea[0]) >= id:
          id = (int(linea[0])+1)
  return id , se_encontro_id

def pedido_repetido(id, pedido):
  repetido = False
  with open(PEDIDOS) as archivo:
    lista_pedidos = csv.reader(archivo, delimiter = DELIMITADOR)
    for linea in lista_pedidos:
      if linea[0] == id and linea[1] == pedido:
        repetido = True
  return repetido
        
def frutas_venta(verdura_ingresada):
  return(verdura_ingresada == TOMATE or verdura_ingresada == BROCOLI or
          verdura_ingresada == ZANAHORIA or verdura_ingresada == LECHUGA)

def agregar(pedido):
  id, se_encontro_id = buscar_id(pedido[NOMBRE_PEDIDO])

  if not frutas_venta(pedido[VERDURA_PEDIDO]):
    print("No vendemos su verdura ingresada. La lista de verduras a la venta es:")
    print("("+TOMATE+") Tomate\n("+BROCOLI+") Brocoli\n("+ZANAHORIA+") Zanahoria\n("+LECHUGA+") Lechuga")

  elif pedido_repetido(id, pedido[VERDURA_PEDIDO]):
    print("La verdura que estas intentando agregar, ya fue agregada")
    print("Intena nuevamente con: modificar (id del pedido) (cantidad del pedido) (verdura)")

  else:
    with open(PEDIDOS, MODO_ADJUNTAR) as lista_pedidos, open(CLIENTES, MODO_ADJUNTAR) as lista_clientes: 
      lista_pedidos.write(f"{id}{DELIMITADOR}{pedido[VERDURA_PEDIDO]}{DELIMITADOR}{pedido[CANT_PEDIDO]}\n")
      if not se_encontro_id:
        lista_clientes.write(f"{id}{DELIMITADOR}{pedido[4]}\n")
      print("Se agrego un producto a la lista")

def modificar():
  return 0


def acciones_lista_pedidos(pedido):
  if pedido[ACCION_PEDIDO] == "agregar":
    if len(pedido) == 5:
      agregar(pedido) 
    else:
      print("Parametros para agregar incorrectos. Los correctos son:")
      print("python3 main.py agregar (cantidad de verduras) (tipo de verdura) (nombre)")
  elif pedido[ACCION_PEDIDO] == "modificar":
    if len(pedido) == 5:
      modificar(pedido) 
    else:
      print("Parametros para modificar incorrectos. Los correctos son:")
      print("python3 main.py modificar (id del pedido) (cantidad del pedido) (verdura)")
  else:
    print("Accion enviada incorrecta. Las correctas son:")
    print("agregar\nmodificar\neliminar\nlistar\n")
  
if __name__ == "__main__":
  pedido = sys.argv
 
  acciones_lista_pedidos(pedido)
