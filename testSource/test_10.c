#include <stdio.h>
int main(){
    int buffer[100];
    printf("Input password: ");
    int x;
    	if(x >=60)
	{
		return 4;
	}
	else if(x>=50 )
	{
		return 3;
	}
	else if(x>=40)
	{
		return 2;
	}
	else{
		return 1;
	}

	return 0;
}
