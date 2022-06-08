#include<stdio.h>



int multiplication(int a, int b)
{
	return b * a;
}

int add(int x, int y)
{
	return x + y;
}

int flow(int x, int y, int z)
{
	if(x*x > 9 && y*z < 100)
	{
		return 1;
	}
	else if(y*y < 25 && x*z > 100 )
	{
		return 2;
	}
	else if(z*z < 64 && x*y < 50 )
	{
		return 3;
	}
	else
	{
		return 4;
	}
}

int main(int argc, char** argv)
{
	int a = 7;
	int b = 5;
	int c = 3;
	printf("%d\n", add(a, b));
	printf("%d\n", multiplication(a, b));
	printf("%d\n",flow(a,b,c));
	return 0;
}
