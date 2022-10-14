#include <stdio.h>
int func(int x, int y){
    	if(x < 100)
	{
		return 1;
	}
	else if(y < 25)
	{
		return 2;
	}
	else if(y > 50 )
	{
		return 3;
	}
	else{
		return 5;
	}

	return 0;
}
int main(){
    int x,y;
    scanf("%d", &x);
scanf("%d", &y);
func(x,y);
}


