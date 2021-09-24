#include <stdio.h>
int main(){
    int buffer[100];
    printf("Input password: ");
    int x;
    	if(x < 40)
	{
		return 1;
	}
	else if(x <50)
	{
		return 2;
	}
	else if(x< 60)
	{
		return 3;
	}
	else{
		return 4;
	}

	return 0;
}
