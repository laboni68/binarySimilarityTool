#include <cmath>
#include <iostream>

double calculation(double numA, double numB, char oper) {
  if (oper == '+') {
    return numA + numB;
  } else if (oper == '-') {
    return numA - numB;
  } else if (oper == '*') {
    return numA * numB;
  } else if (oper == '/') {
    return numA / numB;
  } else if (oper == '^') {
    return pow(numA, numB);
  } else if (oper == 's') {
    return sqrt(numA);
  } else {
    std::cout << "\nYou have put in an invalid operator/number!\n\a";
    return -1.0;
  }
}

int main() {
  double numA, numB, result;
  char oper;
  std::cout
      << "Hello and Welcome to this simple calculator. It was made by: Quincy"
      << std::endl;
  std::cout << "Just simply enter the first number of your problem then the "
               "operator and then the second number of your problem."
            << std::endl;
  std::cout
      << "Operators are: \"+ for adding, - for subtracting, * for "
         "multiplying, / for dividing, ^ for power, s for square root.\"\n"
      << std::endl;
  std::cout << "Enter the first number: ";
  std::cin >> numA;
  std::cout << std::endl;
  std::cout << "Enter the operator: ";
  std::cin >> oper;
  std::cout << std::endl;
  if (oper == 's') {
    std::cin.ignore();
    result = calculation(numA, 0, oper);
  } else {
    std::cout << "Enter the second number: ";
    std::cin >> numB;
    std::cout << std::endl;
    result = calculation(numA, numB, oper);
  }
  std::cout << "Result: " << result << std::endl;
}
