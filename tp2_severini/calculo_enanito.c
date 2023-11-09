#include <stdio.h>
#include <stdbool.h>
#include "calcular_enanito.h"

#define LECHUGA 'A'
#define BROCOLI 'B'
#define ZANAHORIA 'C'
#define TOMATE 'D'
const int PUNTOS_NULO = 0;
const int PUNTOS_BAJOS = 5;
const int PUNTOS_BUENOS = 10;
const int PUNTOS_INCREIBLES = 15;
const char VERANO = 'V';
const char INVIERNO = 'I';
const int MAX_PUNTOS_RESTA = 5;
const int MIN_PUNTOS_RESTA = 0;
const float MIN_TIEMPO_COSECHA = 40.00;
const float MAX_TIEMPO_COSECHA = 120.00;

/*
  Pre: -
  Post: true si cumple las condiciones
*/
bool verdura_valida(char verdura_favorita){
  return ((LECHUGA == verdura_favorita) || (BROCOLI == verdura_favorita) || (TOMATE== verdura_favorita) || (ZANAHORIA == verdura_favorita));
} 
/*
  Pre: -
  Post: Segun su respuesta indica cual es su verdura_fav y dependiendo de esta se le sumaran ciertos puntos a puntos_totales
*/
void preguntar_verduras_fav(int* puntos){
  char verdura_fav = 0;
  printf("¿Cuál es tu verdura favorita?\n(%c) Lechuga\n(%c) Brocoli\n(%c) Zanahoria\n(%c) Tomate\n",LECHUGA ,BROCOLI, ZANAHORIA, TOMATE);
  scanf(" %c",&verdura_fav);
  while (!verdura_valida(verdura_fav)){
    printf("Su opcion ah sido incorrecta vuelve a intentar\n");
    printf("¿Cuál es tu verdura favorita?\n(%c) Lechuga\n(%c) Brocoli\n(%c) Zanahoria\n(%c) Tomate\n",LECHUGA ,BROCOLI, ZANAHORIA, TOMATE);
    scanf(" %c",&verdura_fav);
  }
  switch (verdura_fav){
    case LECHUGA:
      printf("Su verdura favorita es la Lechuga\n");
      *puntos += PUNTOS_NULO;
      printf("Usted a ganado %i puntos\n", PUNTOS_NULO);
    break;
    case BROCOLI:
      printf("Su verdura favorita es el Brocoli\n");
      *puntos += PUNTOS_BAJOS;
      printf("Usted a ganado %i puntos\n",PUNTOS_BAJOS);
    break;
    case ZANAHORIA:
      printf("Su verdura favorita es la Zanahoria\n");
      *puntos += PUNTOS_BUENOS;
      printf("Usted a ganado %i puntos\n",PUNTOS_BUENOS);
    break;
    case TOMATE:
      printf("Su verdura favorita es el Tomate\n");
      *puntos += PUNTOS_INCREIBLES;
      printf("Usted a ganado %i puntos\n",PUNTOS_INCREIBLES);
    break;  
  }
  printf("Sus puntos totales hasta ahora son de: %ipts\n\n",*puntos);
}
/*
  Pre: -
  Post: Segun su respuesta indica team_epoca y dependiendo de esta se le sumaran ciertos puntos a puntos_totales 
*/
void preguntar_epoca(char* epoca,int* puntos){
  printf("¿Sos team verano o team invierno?\n(%c) Invierno\n(%c) Verano\n",INVIERNO ,VERANO);
  scanf(" %c",epoca);
  while (!(*epoca == INVIERNO || *epoca == VERANO)){
    printf("Su opcion ah sido incorrecta vuelve a intentar\n");
    printf("¿Sos team verano o team invierno?\n(%c) Invierno\n(%c) Verano\n",INVIERNO ,VERANO);
    scanf(" %c",epoca);
  }
  if(*epoca == VERANO){
    printf("Elegiste el Verano\n");
    *puntos += PUNTOS_BUENOS;
    printf("Sos de los mios ganaste %i puntos\n",PUNTOS_BUENOS);
  }else{
    printf("Elegiste el Invierno\n");
    printf("Usted no gano puntos(por pecho frio)\n");
  }
  printf("Sus puntos totales hasta ahora son de: %ipts\n\n",*puntos);
}
/*
  Pre: team_epoca tiene que ser VERANO o INVIERNO
  Post: Dependiendo de su respuesta se le restaran ciertos puntos a puntos_totales
*/
void preguntar_cuanto_enoja(char team_epoca, int* puntos){
  int puntos_resta = 0;
  if(team_epoca == VERANO){
    printf("¿Cuánto te enojan los mosquitos? \n");
  }else{
    printf("¿Cuánto te enoja trabajar bajo la lluvia?\n");
  }
  printf("la respuesta debe ser un entero entre el %i y el %i\n",MIN_PUNTOS_RESTA , MAX_PUNTOS_RESTA);
  scanf("%i",&puntos_resta);
  while(!(puntos_resta >= MIN_PUNTOS_RESTA && puntos_resta <= MAX_PUNTOS_RESTA)){
    printf("Su opcion ah sido incorrecta vuelve a intentar\n");
    if(team_epoca == VERANO){
      printf("¿Cuánto te enojan los mosquitos? \n");
    }else{
      printf("¿Cuánto te enoja trabajar bajo la lluvia?\n");
    }
    printf("la respuesta debe ser un entero entre el %i y el %i\n",MIN_PUNTOS_RESTA , MAX_PUNTOS_RESTA);
    scanf("%i",&puntos_resta);
  }
  printf("Su respuesta fue : %i\n", puntos_resta);
  *puntos -= puntos_resta;
  printf("Usted a perdido : %i puntos\n", puntos_resta);
  printf("Sus puntos totales hasta ahora son de: %ipts\n\n",*puntos);
}
/*
  Pre: -
  Post: Dependiendo de su respuesta se le sumaran ciertos puntos a puntos_totales
*/
void preguntar_tiempo_cosechar(int* puntos){
  float tiempo_cosechar = 0;
  printf("¿Cuánto tiempo te llevaría cosechar un cultivo de 10m²?\nResponder en MM.SS entre %.2f y %.2f\n",MIN_TIEMPO_COSECHA, MAX_TIEMPO_COSECHA);
  scanf("%f",&tiempo_cosechar);
  while (!(tiempo_cosechar >= MIN_TIEMPO_COSECHA && tiempo_cosechar <= MAX_TIEMPO_COSECHA)){
    printf("Su opcion ah sido incorrecta vuelve a intentar\n");
    printf("¿Cuánto tiempo te llevaría cosechar un cultivo de 10m²?\nResponder en MM.SS entre %.2f y %.2f\n",MIN_TIEMPO_COSECHA, MAX_TIEMPO_COSECHA);
    scanf("%f",&tiempo_cosechar);
  }
  printf("Su respuesta fue : %.2f\n",tiempo_cosechar);
  float resultado_cosecha =  tiempo_cosechar / 8 ;
  printf("Ustes gano : %i Puntos\n\n",(int)resultado_cosecha);
  *puntos += (int)resultado_cosecha;
  printf("Sus puntos totales son de: %ipts\n\n",*puntos);
}
/*
  Pre: -
  Post: Dependiendo de puntos_totales se le asigna una inicial de un enanito 
*/
void definir_inicial_enanito(char* inicial, int puntos_totales){
  if (puntos_totales < 10){
    *inicial = GRUÑON;
  } else if (puntos_totales >= 10 && puntos_totales <= 19){
    *inicial = DORMILÓN;
  } else if (puntos_totales >= 20 && puntos_totales <= 29){
    *inicial = SABIO;
  } else {
    *inicial = FELIZ;
  }
}

void calcular_enanito(char* inicial_enanito){
  int puntos_totales = 0;
  char team_epoca = 0;
  
  printf("Pregunta n°1 :\n");
  preguntar_verduras_fav(&puntos_totales);
  
  printf("Pregunta n°2 :\n");
  preguntar_epoca(&team_epoca, &puntos_totales);
  
  printf("Pregunta n°3 :\n");
  preguntar_cuanto_enoja(team_epoca, &puntos_totales);
  
  printf("Pregunta n°4 :\n");
  preguntar_tiempo_cosechar(&puntos_totales);

  definir_inicial_enanito(inicial_enanito, puntos_totales);
}