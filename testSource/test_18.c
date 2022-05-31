#include <stdio.h>
int main(){
    int buffer[100];
    printf("Input password: ");
    int x,y;
    if(x <= 99)return 1;
    else if(y > 51 )return 3;
    else if(y <= 24)return 2;
    else return 5;
    return 0;
}
