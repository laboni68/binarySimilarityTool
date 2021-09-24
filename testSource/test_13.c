#include <stdio.h>
int main(){
    int buffer[100];
    int x,y,z;
    	if(y < 40 || y==120)
	{
		return 1;
	}
	else if((y<50 && y>=40) || y==130)
	{
		return 2;
	}
	else if((y<60 && y>=50 ) || y==140)
	{
		return 3;
	}
	return 4;
}

