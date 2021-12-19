#include <iostream>

using namespace std;
using I = unsigned long int;
I fib(int N) {
	if (N == 0) return 0;
	else if (N == 1) return 1;
	else return fib(N - 1) + fib(N - 2);
}

int main() {
	int N;
	cin >> N;
	I fib1 = 0, fib2 = 1, temp;
	for (int i = 0; i < N - 1; i++) {
		temp = fib2;
		fib2 += fib1;
		fib1 = temp;
	}
	cout << fib2 * 2;
}
