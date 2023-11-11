#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>
#include "constantes.h"
#include "calcular_enanito.h"
#include "granja.h"

/*
  Pre: -
  Post: Mostrar que tipo de enanito serias segun inicial_enanito
*/
void mostrar_respuesta_final(char inicial_enanito){
  switch (inicial_enanito){
    case GRUÑON:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -GRUÑÓN-\n");
    break;
    case DORMILÓN:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -DORMILÓN-\n");
    break;
    case SABIO:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -SABIO-\n");
    break;
    case FELIZ:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -FELIZ-\n");
    break;
  }
}
/*
  Pre: -
  Post: 
  - Devuelve true si la accion es igual a una valor especifico
  - Devuelve false si la accion es distinta a una valor especifico
*/
bool accion_valida(char accion){
  return(accion == MOVER_ARRIBA || accion == MOVER_IZQUIERDA || accion == MOVER_ABAJO || accion == MOVER_DERECHA || accion == FERTILIZANTE || accion == INSECTICIDA || accion == TOMATE || accion == BROCOLI || accion == ZANAHORIA || accion == LECHUGA);
} 
/*
  Pre: -
  Post: Despendiendo del estado_juego termina, empieza o sigue el juego
*/
void verificar_estado(int estado, juego_t* juego){
  while (estado == 0) {
    char accion;
  
    imprimir_terreno(*juego);

    printf("Ingrese una acción: ");
    scanf(" %c", &accion);
    while (!(accion_valida(accion))){
      printf("Su accion fue invalida vuelva a intentrlo\n");
      printf("Ingrese una acción: ");
      scanf(" %c", &accion);
    }
    
    realizar_jugada(juego, accion);

    estado = estado_juego(*juego);
  }
  if (estado == 1) {
    printf("¡Has ganado el juego!\n");
  } else if (estado == -1) {
    printf("¡Has perdido el juego!\n");
  }
}

int main(){
  srand (( unsigned)time(NULL));
  char inicial_enanito; 
  juego_t juego;
  char respuesta;

  printf("Bienvenido. En este test te diremos a que enanito de la cenicienta te asemejas segun tu personalidad\n");
  printf("Contesta las siguientes preguntas para saber que enanito serias\n");
  calcular_enanito(&inicial_enanito);  

  mostrar_respuesta_final(inicial_enanito);
  
  printf("Si desea continuar con el juego presione S de lo contrario presione cualquier letra\n");
  scanf(" %c",&respuesta);
  if (respuesta == 'S'){
    inicializar_juego(&juego, inicial_enanito);

    int estado = estado_juego(juego);
    verificar_estado(estado,&juego);
  }
  printf("\n");
  return 0;
}
 