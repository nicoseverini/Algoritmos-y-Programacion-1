#include <stdio.h>
#include "calcular_enanito.h"
/*
  Pre: -
  Post: Mostrar que tipo de enanito serias segun inicial_enanito
*/
void mostrar_respuesta_final(char inicial_enanito){
  switch (inicial_enanito){
    case GRUÑON:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -GRUÑÓN-");
    break;
    case DORMILÓN:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -DORMILÓN-");
    break;
    case SABIO:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -SABIO-");
    break;
    case FELIZ:
      printf("Con las respuestas que brindaste, tu personalidad se alinea con: -FELIZ-");
    break;
  }
}

int main(){
  char inicial_enanito = 0;
  printf("Bienvenido. En este test te diremos a que enanito de la cenicienta te asemejas segun tu personalidad\n");
  printf("Contesta las siguientes preguntas para saber que enanito serias\n");
  
  calcular_enanito(&inicial_enanito);  
  mostrar_respuesta_final(inicial_enanito);

  printf("\n");
  return 0;
}