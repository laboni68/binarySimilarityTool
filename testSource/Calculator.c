
#include <stdio.h>
#include <stdlib.h>

int doCalculation(int a, int b, int operation) {
  if (operation == 1)
    return a + b;
  else if (operation == 2)
    return a - b;
  else if (operation == 3)
    return a * b;
  else if (operation == 4)
    return a / b;
  else if (operation == 5)
    return a % b;
  else
    return -1;
}

int main(int argc, char *argv[]) {
	int a, b, result, op;
	if (argc == 4) {
		a = atoi(argv[1]);
		b = atoi(argv[2]);
		op = atoi(argv[3]);

    if (op < 1 || op > 5) {
      puts("Invalid operation");
      return -1;
    }

		result = doCalculation(a, b, op);

    printf("Result: %d\n", result);
	}
  else {
    puts("Usage: calculator a b operation");
    puts("Operations:\n1) a+b\n2) a-b\n3) a*b\n4) a/b\n5) a\%b");
    return 0;
  }
}
