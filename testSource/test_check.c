#include <stdio.h>
int func(int x, int y)
{
	y = x+x;
	return y;
}

int main(){
    int buffer[100];
    printf("Input password: ");
    int x,y;
    func(x,y);
    return 2;
}


