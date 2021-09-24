#include <stdio.h>
int main(){
    int buffer[100];
    printf("Input password: ");
    int x,y,z;
    	if(y < 40)
	{
		return 1;
	}
	else if(y>=50 && y<60 )
	{
		return 3;
	}
	else if(y>=40 && y <50)
	{
		return 2;
	}
	else{
		return 4;
	}
}
