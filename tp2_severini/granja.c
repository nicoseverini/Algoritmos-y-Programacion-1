#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include "constantes.h"
#include "granja.h"
//-----------------------------------------------inicializar-juego------------------------------------------------------------------------
/*
  pre: -
  post: Devuelve variables_inicializadas
*/
void inicializar_variables(juego_t* juego){
  juego->jugador.cant_monedas = 0;
  juego->movimientos = 0;
  juego->tope_objetos = 0;
  juego->jugador.tope_canasta = 0;
  juego->jugador.tiene_fertilizante = false;
  juego->jugador.cant_insecticidas = INCECTICIDAS_INICIALES;
}
/*
  Pre: Enanito tiene q ser GRUÑOR o DORMILON o SABIO o FELIZ
  Post: Aumenta la cantidad de monedas_iniciales segun el tipo de enanito
*/
void inicializa_monedas(juego_t* juego, char enanito){
  switch (enanito){
    case GRUÑON:
      juego->jugador.cant_monedas += MONEDAS_INICIALES_GRUÑON;
      break;
    case DORMILÓN:
      juego->jugador.cant_monedas += MONEDAS_INICIALES_DORMILON;
      break;
    case SABIO:
      juego->jugador.cant_monedas += MONEDAS_INICIALES_SABIO;
      break;
    case FELIZ:
      juego->jugador.cant_monedas += MONEDAS_INICIALES_FELIZ;
      break;
  }
}
/*
  Pre: -
  Post: Genera una posicion aleatoria entre los limites del terreno
*/
void generar_posicion(coordenada_t* posicion){
  posicion->columna = rand () % MAX_COL_TERRENO; 
  posicion->fila = rand () % MAX_FIL_TERRENO; 
}
/*
  Pre: Huerta_index tiene que ser un valor entre el 0 y menor que MAX_HUERTA
  Post: Genera La posicion del centro de la huerta que estara dentro de los limites del terreo y se encuentra separado de otro centro 
*/
void generar_centro_huerta(juego_t* juego, int huerta_index){
  bool posicion_valida = false;
  while (!posicion_valida){
  generar_posicion(&(juego->huertas[huerta_index].cultivos[0].posicion));
  posicion_valida = true;
  int j = 0;
    while (j < huerta_index && posicion_valida){

      int distancia_cuadrado = (juego->huertas[huerta_index].cultivos[0].posicion.fila - juego->huertas[j].cultivos[0].posicion.fila) * (juego->huertas[huerta_index].cultivos[0].posicion.fila - juego->huertas[j].cultivos[0].posicion.fila) +
      (juego->huertas[huerta_index].cultivos[0].posicion.columna - juego->huertas[j].cultivos[0].posicion.columna) * (juego->huertas[huerta_index].cultivos[0].posicion.columna - juego->huertas[j].cultivos[0].posicion.columna);
      
      if (distancia_cuadrado < MAX_DISTANCIA_CUADRADO){
        posicion_valida = false;  
      }
      j++;
    }
  }
}
/*
  pre: Huerta_index tiene que ser un valor entre el 0 y menor que MAX_HUERTA
  post: 
  - Genera bordes de la huerta, si se encuenrtan dentro del terreno y los marca como posicion_ocupada

*/
void generar_bordes_huerta(juego_t* juego, int huerta_index, bool posicion_ocupada[MAX_COL_TERRENO][MAX_FIL_TERRENO]){
  int fila_centro = juego->huertas[huerta_index].cultivos[0].posicion.fila;
  int columna_centro = juego->huertas[huerta_index].cultivos[0].posicion.columna;
  for (int fila = -1; fila <= 1; fila++){
    for (int columna = -1; columna <= 1; columna++){
      int posicion_fila = fila_centro + fila;
      int posicion_columna = columna_centro + columna;

      if (posicion_fila >= 0 && posicion_fila < MAX_FIL_TERRENO && posicion_columna >= 0 && posicion_columna < MAX_COL_TERRENO){

        posicion_ocupada[posicion_fila][posicion_columna] = true;

        juego->huertas[huerta_index].cultivos[juego->huertas[huerta_index].tope_cultivos].posicion.fila = posicion_fila;
        juego->huertas[huerta_index].cultivos[juego->huertas[huerta_index].tope_cultivos].posicion.columna = posicion_columna;
        juego->huertas[huerta_index].cultivos[juego->huertas[huerta_index].tope_cultivos].tipo = CULTIVO_VACIO;
        juego->huertas[huerta_index].cultivos[juego->huertas[huerta_index].tope_cultivos].ocupado = false;
        juego->huertas[huerta_index].tope_cultivos++;
      }
      
    }
  }
  
}
/*
  Pre:
  - i tiene que ser un valor entre el 0 y menor que TOPE_ESPINAS
  Post: 
  - Genera posicion de TOPE_ESPINAS espinas aleatorias dentro del terreno y no se superponen con ninguna posicion_ocupada
  - Cada posicion fue asignada como posicion_ocupada = true
*/
void generar_espina(juego_t* juego,int i, bool posicion_ocupada[MAX_COL_TERRENO][MAX_FIL_TERRENO]){
  juego->objetos[i].tipo = ESPINAS;
  generar_posicion(&(juego->objetos[i].posicion));
  while(posicion_ocupada[juego->objetos[i].posicion.fila][juego->objetos[i].posicion.columna]){
    generar_posicion(&(juego->objetos[i].posicion));
  }
  posicion_ocupada[juego->objetos[i].posicion.fila][juego->objetos[i].posicion.columna] = true;
}
/*
  Pre: 
  - Los valores (MOVER_ARRIBA, MOVER_ABAJO, MOVER_IZQUIERDA, MOVER_DERECHA) tienen que ser validos
  Post: 
  - Se movio el presonaje en una direccion espesifica segun accion enviada 
  - Si el movimiento se realizo juego->movimientos suma uno
  - Si el movimiento se realizo *accion_realizada = true
*/
void mover_personaje(juego_t* juego, char accion, bool* accion_realizada){
  switch (accion){
    case MOVER_ARRIBA:
      if ((juego->jugador.posicion.fila) != 0 ){
        (juego->jugador.posicion.fila)--;
        (juego->movimientos)++;
        *accion_realizada = true;
      }
      break;
    case MOVER_ABAJO:
      if ((juego->jugador.posicion.fila) != LIMITE_MAPA ){
        (juego->jugador.posicion.fila)++;
        (juego->movimientos)++;
        *accion_realizada = true;
      }
      break;
    case MOVER_IZQUIERDA:
      if ((juego->jugador.posicion.columna) != 0 ){
        (juego->jugador.posicion.columna)--;
        (juego->movimientos)++;
        *accion_realizada = true;
      }
      break;
    case MOVER_DERECHA:
      if ((juego->jugador.posicion.columna) != LIMITE_MAPA ){
        (juego->jugador.posicion.columna)++;
        (juego->movimientos)++;
        *accion_realizada = true;
      }
      break;
  }
}
/*
  Pre: 
  - Los valores de accion (TOMATE, ZANAHORIA, BROCOLI, LECHUGA) tienen que ser validos
  - i es un índice válido para la huerta. 
  - j es un índice válido para los cultivos
  Post: 
  - Sembrar o no, un cultivo espesifico segun la accion enviada
  - Si se sembro se resta el costo del cultivo espesifico y esa posicion pasa a esta ocupada
  - Si se sembro se le suman la duracion de es cultivo a juego->movimientos
*/
void cultivar(juego_t* juego, char accion, int i, int j){
  switch (accion){
    case TOMATE:
      juego->huertas[i].cultivos[j].tipo = TOMATE;
      juego->jugador.cant_monedas -= VALOR_SEMILLA_TOMATE;
      juego->huertas[i].cultivos[j].ocupado = true;
      juego->huertas[i].cultivos[j].movimiento_plantado = (juego->movimientos);
      break;
    case ZANAHORIA:
      juego->huertas[i].cultivos[j].tipo = ZANAHORIA;
      juego->jugador.cant_monedas -= VALOR_SEMILLA_ZANAHORIA;
      juego->huertas[i].cultivos[j].ocupado = true;
      juego->huertas[i].cultivos[j].movimiento_plantado = (juego->movimientos);
      break;
    case BROCOLI:
      juego->huertas[i].cultivos[j].tipo = BROCOLI;
      juego->jugador.cant_monedas -= VALOR_SEMILLA_BROCOLI;
      juego->huertas[i].cultivos[j].ocupado = true;
      juego->huertas[i].cultivos[j].movimiento_plantado = (juego->movimientos);
      break;
    case LECHUGA:
      juego->huertas[i].cultivos[j].tipo = LECHUGA;
      juego->jugador.cant_monedas -= VALOR_SEMILLA_LECHUGA;
      juego->huertas[i].cultivos[j].ocupado = true;
      juego->huertas[i].cultivos[j].movimiento_plantado = (juego->movimientos);
      break;
  }
}
/*
  pre : 
  - i es un índice válido para la huerta. 
  - j es un índice válido para los cultivos
  post : 
  - Devuelve true si la huerta con un cultivo espesifico esta preparada para cosechar
  - Devuelve false si no esta en la huerta y si no esta listo para cosechar
*/
bool planta_crecida(juego_t juego, int i, int j){
  return ( ((juego.huertas[i].cultivos[j].tipo == TOMATE) && (juego.movimientos - juego.huertas[i].cultivos[j].movimiento_plantado) >= MOVIMIENTOS_TOMATE_CRECIDO)||
  ((juego.huertas[i].cultivos[j].tipo == ZANAHORIA) && (juego.movimientos - juego.huertas[i].cultivos[j].movimiento_plantado) >= MOVIMIENTOS_ZANAHORIA_CRECIDO)||
  ((juego.huertas[i].cultivos[j].tipo == BROCOLI) && (juego.movimientos - juego.huertas[i].cultivos[j].movimiento_plantado) >= MOVIMIENTOS_BROCOLI_CRECIDO)||
  ((juego.huertas[i].cultivos[j].tipo == LECHUGA) && (juego.movimientos - juego.huertas[i].cultivos[j].movimiento_plantado) >= MOVIMIENTOS_LECHUGA_CRECIDO) );
}
/*
  pre: 
  -i es un índice válido para la huerta. 
  -j es un índice válido para los cultivos
  post:
  - Devuelve true si el cultivo especifico ya paso su tiempo de vida 
  - Devuelve true si el cultivo especifico ya paso su tiempo de vida 
*/
bool cultivo_esta_podrido(juego_t* juego, int i, int j){
  return ( ((juego->huertas[i].cultivos[j].tipo == TOMATE) && (juego->movimientos - juego->huertas[i].cultivos[j].movimiento_plantado) >= VIDA_TOMATE)||
  ((juego->huertas[i].cultivos[j].tipo == ZANAHORIA) && (juego->movimientos - juego->huertas[i].cultivos[j].movimiento_plantado) >= VIDA_ZANAHORIA)||
  ((juego->huertas[i].cultivos[j].tipo == BROCOLI) && (juego->movimientos - juego->huertas[i].cultivos[j].movimiento_plantado) >= VIDA_BROCOLI)||
  ((juego->huertas[i].cultivos[j].tipo == LECHUGA) && (juego->movimientos - juego->huertas[i].cultivos[j].movimiento_plantado) >= VIDA_LECHUGA) );
}
/*
  pre: -
  post: 
  - Devuelve true si hay una plaga en el vector objetos 
  - Devuelve false si no hay una plaga en el vector objetos
*/
bool tengo_plaga(juego_t* juego){
  bool hay_plaga = false;
  for (int i = TOPE_ESPINAS; i < juego->tope_objetos; i++){
    if (juego->objetos[i].tipo == PLAGAS){
      hay_plaga = true;
    }
  }

  return hay_plaga;
}
/*
  pre : Tiene q haber una plaga en el vector de objetos
  post : Devuelve posicion de plaga en el vector objetos
*/
int posicion_plaga(juego_t* juego){
  int posicion_plaga = 0;
  for (int i = TOPE_ESPINAS; i < juego->tope_objetos; i++){
    if (juego->objetos[i].tipo == PLAGAS){
      posicion_plaga = i;
    }
  }
  return posicion_plaga;
}
/*
  pre: Objeto_index tiene q estar dentro del vector objetos 
  post: Elimina objeto_index del vector objetos
*/
void eliminar_objeto(juego_t* juego, int objeto_index){
  for (int j = objeto_index; j < (juego->tope_objetos)-1; j++) {
    juego->objetos[j] = juego->objetos[j+1];
  }
  juego->tope_objetos--;
}
/*
  Pre: 
  - Los valores (TOMATE, ZANAHORIA, BROCOLI, LECHUGA) tienen que ser validos
  - Huerta_index tiene que ser un valor entre el 0 y menor que MAX_HUERTA
  - juego->jugador.tiene_fertilizante es true
  Post: 
  - Aplicar fertilizante a los cultivos de huerta_index
  - Aquellos cultivos que se encontraban inmaduros pasan a estar maduros y acorta su duracion 
  - Juego->jugador.tiene_fertilizante pasa a ser false 
*/
void aplicar_fertilizante(juego_t* juego, int huerta_index){
  for (int j = 0; j < MAX_PLANTAS; j++){
    if(!(planta_crecida(*juego, huerta_index, j))){
      switch (juego->huertas[huerta_index].cultivos[j].tipo){
        case TOMATE:
          juego->huertas[huerta_index].cultivos[j].movimiento_plantado = (juego->movimientos) - MOVIMIENTOS_TOMATE_CRECIDO;
          break;
        case ZANAHORIA:
          juego->huertas[huerta_index].cultivos[j].movimiento_plantado = (juego->movimientos) - MOVIMIENTOS_ZANAHORIA_CRECIDO;
          break;
        case BROCOLI:
          juego->huertas[huerta_index].cultivos[j].movimiento_plantado = (juego->movimientos) - MOVIMIENTOS_BROCOLI_CRECIDO;
          break;
        case LECHUGA:
          juego->huertas[huerta_index].cultivos[j].movimiento_plantado = (juego->movimientos) - MOVIMIENTOS_LECHUGA_CRECIDO;
          break;
      }
    }
  }
  juego->jugador.tiene_fertilizante = false; 
}
/*
  Pre:
  - Huerta_index tiene que ser un valor entre el 0 y menor que MAX_HUERTA
  - Juego->huertas[huerta_index].plagado tiene que ser true
  - Cantidad de insectidas tiene que ser mayor a 0
  Post: 
  - Juego->huertas[huerta_index].plagado pasa a ser false
  - Se elimina del campo de juego a la plaga 
*/ 
void aplicar_insecticida(juego_t* juego, int huerta_index){
  juego->huertas[huerta_index].plagado = false;
  eliminar_objeto(juego, posicion_plaga(juego));
}
/*
  Pre:
  - Huerta_index tiene que ser un valor entre el 0 y menor que MAX_HUERTA
  - Juego->huertas[huerta_index].plagado tiene que ser true
  Post: 
  - Elimina todos los cultivos de huerta_index y esas posiciones pasan a estar despocupadas
  - Juego->huertas[huerta_index].plagado pasa a ser false

*/
void propagar_plaga(juego_t* juego, int huerta_index){
  for (int j = 0; j < MAX_PLANTAS; j++){
    if (juego->huertas[huerta_index].cultivos[j].tipo != CULTIVO_VACIO){
      juego->huertas[huerta_index].cultivos[j].tipo = CULTIVO_VACIO;
      juego->huertas[huerta_index].cultivos[j].ocupado = false;
      juego->huertas[huerta_index].cultivos[j].movimiento_plantado = juego->movimientos;
    }
  }
  juego->huertas[huerta_index].plagado = false;
}
/*
  Pre: -
  Post: 
  - Devuelve true si las coordenadas posicion1 y posicion2 son iguales en términos de filas y columnas
  - Devuelve false si las coordenadas posicion1 y posicion2 son diferentes en términos de filas o columnas
*/
bool posiciones_iguales(coordenada_t posicion1, coordenada_t posicion2){
  return(posicion1.fila == posicion2.fila && posicion1.columna == posicion2.columna);
}
/*
  Pre: 
  - Posicion de fertilizante
  Post: 
  - Devuelve true si la posicion es igual a una posicion de un objeto del juego 
  - Devuelve false si la posicion es distinta a una posicion de un objeto del juego 
*/
bool posicion_ocupada_fertilizante(coordenada_t posicion, juego_t* juego){
  bool ocupado = false;

  for (int i = 0; i < MAX_HUERTA; i++){
    for (int j = 0; j < juego->huertas[i].tope_cultivos; j++){
      if(posiciones_iguales(posicion, juego->huertas[i].cultivos[j].posicion)){
        ocupado = true;
      }
    }
  }

  for (int i = 0; i < juego->tope_objetos; i++){
    if (posiciones_iguales(posicion, juego->objetos[i].posicion) && juego->objetos[i].tipo != FERTILIZANTE){
      ocupado = true;
    }
  }

  if (posiciones_iguales(posicion, juego->deposito)){
    ocupado = true;
  }
  if (posiciones_iguales(posicion, juego->jugador.posicion)){
    ocupado = true;
  }
    
  return ocupado;
}
/*
  Pre: 
  - Posicion de plaga
  Post: 
  - Devuelve true si la posicion es igual a una posicion de un objeto del juego 
  - Devuelve false si la posicion es distinta a una posicion de un objeto del juego 
*/
bool posicion_ocupada_plaga(coordenada_t posicion, juego_t* juego){
  bool ocupado = false;

  for (int i = 0; i < juego->tope_objetos; i++){
    if (posiciones_iguales(posicion, juego->objetos[i].posicion) && juego->objetos[i].tipo != PLAGAS){
      ocupado = true;
    }
  }
  
  if (posiciones_iguales(posicion, juego->deposito)){
    ocupado = true;
  }
  if (posiciones_iguales(posicion, juego->jugador.posicion)){
    ocupado = true;
  }

  return ocupado;
}
/*
  Pre: accion_realizada tiene q ser verdadero
  Post: Cada diez movimientos contando desde el primero, 
  si en el caso de haber plaga la elimina y genera una nueva plaga con posicion random y aumenta el tope objetos
  si no hay plaga simplemente genera una nueva con posicion random y aumenta el tope objetos
*/
void generar_plagas(juego_t* juego, bool hay_plaga, bool accion_realizada){
  if (juego->movimientos % 10 == 0 && accion_realizada){
    if (hay_plaga){
      eliminar_objeto(juego, posicion_plaga(juego));
    }
    juego->objetos[juego->tope_objetos].tipo = PLAGAS;
    generar_posicion(&(juego->objetos[juego->tope_objetos].posicion));
    while (posicion_ocupada_plaga(juego->objetos[juego->tope_objetos].posicion, juego)){
      generar_posicion(&(juego->objetos[juego->tope_objetos].posicion));
    }
    juego->tope_objetos++;
  }
}
/*
  Pre: accion_realizada tiene q ser verdadero
  Post: Cada quince movimientos genera un fertilizante en una posicion random y aumenta el tope objetos
*/
void generar_fertilizante(juego_t* juego, bool accion_realizada){
  if (juego->movimientos % 15 == 0 && accion_realizada){
    juego->objetos[juego->tope_objetos].tipo = FERTILIZANTE;
    generar_posicion(&(juego->objetos[juego->tope_objetos].posicion));
    while (posicion_ocupada_fertilizante(juego->objetos[juego->tope_objetos].posicion, juego)){
      generar_posicion(&(juego->objetos[juego->tope_objetos].posicion));
    }
    juego->tope_objetos++;
  }
}
/*
 Pre: El jugador tiene q estar encima de un fetilizante y no tiene q tener fertilizante
 Post: Elimina el fertlizante agarrado del vector objetos
*/
void agarrar_fertilizante(juego_t* juego){
  for (int i = TOPE_ESPINAS; i < juego->tope_objetos; i++){
    if (posiciones_iguales(juego->jugador.posicion, juego->objetos[i].posicion) && !(juego->jugador.tiene_fertilizante) && juego->objetos[i].tipo == FERTILIZANTE){
      eliminar_objeto(juego, i);
      juego->jugador.tiene_fertilizante = true;
    }
  }
}
/*
  Pre: Estar a distancia manhattan del deposito
  Post: Devuelve un cantidad de monedas segun el valor de una verdura espesifica 
*/
void vender(juego_t* juego){
  int distancia_manhattan = abs(juego->jugador.posicion.fila - juego->deposito.fila) + abs(juego->jugador.posicion.columna - juego->deposito.columna);
  if (distancia_manhattan <= 2) {
    for (int i = 0; i < juego->jugador.tope_canasta; i++) {
      char verdura = juego->jugador.canasta[i];
      if (verdura != CULTIVO_VACIO) {
        switch (verdura) {
          case TOMATE:
            juego->jugador.cant_monedas += VALOR_TOMATE;
            break;
          case ZANAHORIA:
            juego->jugador.cant_monedas += VALOR_ZANAHORIA;
            break;
          case BROCOLI:
            juego->jugador.cant_monedas += VALOR_BROCOLI;
            break;
          case LECHUGA:
            juego->jugador.cant_monedas += VALOR_LECHUGA;
            break;
        }
        
        juego->jugador.canasta[i] = CULTIVO_VACIO;
      }
    }
    juego->jugador.tope_canasta = 0;
  }
}
/*
  Pre: Planta tiene q estar crecida y la huerta no tiene q estar plagada 
  Post: 
  - Valor en la canasta del cultivo cosechado
  - En la posicion del cultivo cosechado pasa a estar sin cultivo y desocupada
*/
void cosechar(juego_t* juego, int i, int j){
  if(juego->jugador.tope_canasta < TOPE_CANASTA){
    juego->jugador.canasta[juego->jugador.tope_canasta] = juego->huertas[i].cultivos[j].tipo; 
    juego->huertas[i].cultivos[j].tipo = CULTIVO_VACIO; 
    juego->huertas[i].cultivos[j].ocupado = false;
  }
  juego->jugador.tope_canasta++;
}
/*
  Pre: El valor de accion tiene q ser valido 
  Post: 
  - Si la plaga cumplio MOVIMIENTOS_PROPAGAR_PLAGA y se encuentra encima de una huerta q no esta plagada, se propaga la plaga
  - Realiza acciones si en jugador se encuentra encima de la huerta
    - Si el jugador está sobre una huerta y tiene monedas suficientes, cultiva una planta
    - Si el jugador tiene fertilizante y la acción es FERTILIZANTE, aplica fertilizante en la huerta
    - Si el jugador tiene insecticidas y la acción es INSECTICIDA, y la huerta está plagada, aplica insecticida
  - Si la huerta no está plagada, la planta está crecida y no es de tipo vacío, cosecha la planta
  - Si un cultivo está podrido, lo elimina cambiando su tipo a CULTIVO_VACIO y marcando como no ocupado
*/
void realizar_acciones_huerta(juego_t* juego, bool hay_plaga, char accion){
  for (int i = 0; i < MAX_HUERTA; i++){ 
    for (int j = 0; j < juego->huertas[i].tope_cultivos; j++){
      if (hay_plaga && posiciones_iguales(juego->objetos[posicion_plaga(juego)].posicion, juego->huertas[i].cultivos[j].posicion) && !(juego->huertas[i].plagado)){
        juego->huertas[i].plagado = true;
        juego->huertas[i].movimientos_plagado = (juego->movimientos);
      }
      if (((juego->movimientos - juego->huertas[i].movimientos_plagado) == MOVIMIENTOS_PROPAGAR_PLAGA) && juego->huertas[i].plagado){
        propagar_plaga(juego, i);
      }

      if (posiciones_iguales(juego->jugador.posicion, juego->huertas[i].cultivos[j].posicion)){
        if (!(juego->huertas[i].cultivos[j].ocupado) && juego->jugador.cant_monedas > VALOR_SEMILLA_TOMATE && juego->huertas[i].cultivos[j].tipo == CULTIVO_VACIO){
          cultivar(juego, accion, i, j);
        }
        
        if (juego->jugador.tiene_fertilizante && accion == FERTILIZANTE){
          aplicar_fertilizante(juego, i);
        }

        if (juego->jugador.cant_insecticidas > 0 && accion == INSECTICIDA && juego->huertas[i].plagado){
          aplicar_insecticida(juego, i);
        }

        if (!(juego->huertas[i].plagado) && planta_crecida(*juego, i, j) && juego->huertas[i].cultivos[j].tipo != CULTIVO_VACIO && !(cultivo_esta_podrido(juego, i, j))){
          cosechar(juego, i, j);  
        }
      }

      if (cultivo_esta_podrido(juego, i, j) && juego->huertas[i].cultivos[j].tipo != CULTIVO_VACIO){
        juego->huertas[i].cultivos[j].tipo = CULTIVO_VACIO;
        juego->huertas[i].cultivos[j].ocupado = false;
      }
    }
  }
}
/*
  Pre: -
  Post: Mustra en pantalla informacion de personaje en el juego
*/
void mostrar_inventario(juego_t juego){
  printf("Sus monedas son de : %i\n",juego.jugador.cant_monedas);
  printf("Sus insecticidas son : %i\n",juego.jugador.cant_insecticidas);
  printf("Sus movimientos son de : %i\n",juego.movimientos);

  if (!(juego.jugador.tiene_fertilizante)){
    printf("No tiene fertilizante disponible\n");
  }else{
    printf("Tiene fertilizante disponible\n");
  }
}
/*
  Pre: -
  Post: Mostrar en pantalla los contenidos de la canasta
*/
void mostrar_canasta(juego_t juego){
  printf("Canasta : [");
  for (int i = 0; i < TOPE_CANASTA; i++){
    printf(" %c", juego.jugador.canasta[i]);
  }
  printf(" ]\n");
}
/*
  Pre: -
  Post: Inicializa el terreno_juego en 0
*/
void inicializar_terreno_juego(char terreno_juego[MAX_FIL_TERRENO][MAX_COL_TERRENO], int tope_fil_terreno, int tope_col_terreno){
  for (int i = 0; i < tope_fil_terreno; i++) {
  	for (int j = 0; j < tope_col_terreno; j++) {
      terreno_juego[i][j] = 0;
    }
  }
}
/*
  Pre: -
  Post: Carga la informacion del terren_juego
*/
void cargar_terreno_juego(juego_t juego, char terreno_juego[MAX_FIL_TERRENO][MAX_COL_TERRENO]){
  for (int i = 0; i < MAX_HUERTA; i++){
    for (int j = 0; j < juego.huertas[i].tope_cultivos; j++){
      if(juego.huertas[i].cultivos[j].posicion.fila >= 0 && juego.huertas[i].cultivos[j].posicion.fila < MAX_FIL_TERRENO &&
      juego.huertas[i].cultivos[j].posicion.columna >= 0 && juego.huertas[i].cultivos[j].posicion.columna < MAX_COL_TERRENO){
        if (!(planta_crecida(juego, i, j))){
          switch (juego.huertas[i].cultivos[j].tipo){
            case TOMATE:
              juego.huertas[i].cultivos[j].tipo = TOMATE_INMADURO;
              break;
            case ZANAHORIA:
              juego.huertas[i].cultivos[j].tipo = ZANAHORIA_INMADURA;
              break;
            case BROCOLI:
              juego.huertas[i].cultivos[j].tipo = BROCOLI_INMADURO;
              break;
            case LECHUGA:
              juego.huertas[i].cultivos[j].tipo = LECHUGA_INMADURA;
              break;

          }
        }
        terreno_juego[juego.huertas[i].cultivos[j].posicion.fila][juego.huertas[i].cultivos[j].posicion.columna] = juego.huertas[i].cultivos[j].tipo;
      }
    }
  }

  for (int i = 0; i < juego.tope_objetos; i++){
    terreno_juego[juego.objetos[i].posicion.fila][juego.objetos[i].posicion.columna] = juego.objetos[i].tipo;
  }
  
  terreno_juego[juego.deposito.fila][juego.deposito.columna] = DEPOSITO;

  terreno_juego[juego.jugador.posicion.fila][juego.jugador.posicion.columna] = BLANCANIEVES;
}
/*
  Pre: -
  Post: Mustra en pantalla cada posicion del terreno_juego
*/
void imprimir_terreno_juego(char terreno_juego[MAX_FIL_TERRENO][MAX_COL_TERRENO], int tope_fil_terreno, int tope_col_terreno){
	for (int i = 0; i < tope_fil_terreno; i++) {
	  for (int j = 0; j < tope_col_terreno; j++) {
		  printf("[   %c\t]", terreno_juego[i][j]);
	  }
	  printf("\n");
  }
}
/*
  Pre: -
  Post: Mustra informacion de acciones convenientes q puede realizar el pesonaje en una huerta 
*/
void informar_pesonaje_huerta(juego_t juego){
  for (int i = 0; i < MAX_HUERTA; i++){
    for (int j = 0; j < juego.huertas[i].tope_cultivos; j++){
      if (posiciones_iguales(juego.jugador.posicion, juego.huertas[i].cultivos[j].posicion)){ 
        if (!(juego.huertas[i].cultivos[j].ocupado)){
          printf("Plantar: \n(%c) Tomate\n(%c) Zanahoria\n(%c) Brocoli\n(%c) Lechuga\n", TOMATE, ZANAHORIA, BROCOLI, LECHUGA );
          if (juego.jugador.tiene_fertilizante){
            printf("(%c) Fertilizante\n",FERTILIZANTE);
          }
        }else {
          printf("El cultivo esta ocupado\n");
          if (juego.jugador.tiene_fertilizante){
            printf("(%c) Fertilizante\n",FERTILIZANTE);
          }
        }
        if (juego.huertas[i].plagado){
          printf("(%c) Insecticida\n",INSECTICIDA);
        }
      }

    } 
  }
}

//------------------------------------------------------------------------------
void inicializar_juego(juego_t* juego, char enanito){

  inicializar_variables(juego);

  inicializa_monedas(juego, enanito);
  
  bool posicion_ocupada[MAX_FIL_TERRENO][MAX_COL_TERRENO];
  for (int i = 0; i < MAX_FIL_TERRENO; i++){
    for (int j = 0; j < MAX_COL_TERRENO; j++){
      posicion_ocupada[i][j] = false;
    }
  }
  
  for (int i = 0; i < MAX_HUERTA; i++){
    juego->huertas[i].tope_cultivos = 0;
    generar_centro_huerta(juego, i);
    generar_bordes_huerta(juego, i, posicion_ocupada);
    juego->huertas[i].plagado = false;
  }

  for (int i = 0; i < TOPE_ESPINAS; i++){
    generar_espina(juego, i, posicion_ocupada);
    juego->tope_objetos++;
  }

  generar_posicion(&(juego->deposito));
  while (posicion_ocupada[juego->deposito.fila][juego->deposito.columna]){
    generar_posicion(&(juego->deposito));
  }
  posicion_ocupada[juego->deposito.fila][juego->deposito.columna] = true;

  generar_posicion(&(juego->jugador.posicion));
  while (posicion_ocupada[juego->jugador.posicion.fila][juego->jugador.posicion.columna]){
    generar_posicion(&(juego->jugador.posicion));
  }
  posicion_ocupada[juego->jugador.posicion.fila][juego->jugador.posicion.columna] = true;

  for (int i = 0; i < TOPE_CANASTA; i++){
    juego->jugador.canasta[i] = CULTIVO_VACIO;
  }

}

void realizar_jugada(juego_t* juego, char accion){

  bool accion_realizada = false;
  mover_personaje(juego, accion, &accion_realizada);

  for (int i = 0; i < TOPE_ESPINAS; i++){
    if (posiciones_iguales(juego->jugador.posicion, juego->objetos[i].posicion)){
      juego->jugador.cant_monedas -= MONEDAS_PINCHASO;
    }
  }

  generar_plagas(juego, tengo_plaga(juego), accion_realizada);

  generar_fertilizante(juego, accion_realizada);

  agarrar_fertilizante(juego);

  realizar_acciones_huerta(juego, tengo_plaga(juego), accion);

  vender(juego);
  
  if (juego->jugador.cant_insecticidas > 0 && accion == INSECTICIDA){
    juego->jugador.cant_insecticidas--;
  }
  if (juego->jugador.tiene_fertilizante && accion == FERTILIZANTE){
    juego->jugador.tiene_fertilizante = false;
  }
}

void imprimir_terreno(juego_t juego){ 
  system("clear");
  char terreno_juego[MAX_FIL_TERRENO][MAX_COL_TERRENO];
  int tope_fil_terreno = 20;
  int tope_col_terreno = 20;

  mostrar_inventario(juego);

  mostrar_canasta(juego);

  inicializar_terreno_juego(terreno_juego, tope_fil_terreno, tope_col_terreno);
  
  cargar_terreno_juego(juego, terreno_juego);

  imprimir_terreno_juego(terreno_juego, tope_fil_terreno, tope_col_terreno);
  
  informar_pesonaje_huerta(juego);
}

int estado_juego(juego_t juego){
  int valor_estado = 0;
  if (juego.jugador.cant_monedas <= 0){
    valor_estado = -1;
  }else if (juego.jugador.cant_monedas >= MAXIMO_MONEDAS){
    valor_estado = 1;
  }
  return valor_estado;
}