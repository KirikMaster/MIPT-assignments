#include <iostream>

using namespace std;
int pow(int x, short n) {
	if (n == 0) return 1;

	if ((n & 1) != 0) {
		return (pow(x, n - 1) * x);
	}
	else {
		auto t = pow(x, n >> 1);
		return (t * t);
	}
}
int main() {
	int N, M, P, num = 0, sumleft = 0, sumright = 0, current;
	cin >> N >> M >> P;
	for (int i = 0; i < pow(M, N >> 1); i++) {
		for (int k = 0; k < N >> 1; k++) {
			current = i % 10;
				sumleft += current;
		}
		for (int j = 0; j < pow(M, N >> 1); j++) {

		}
	}
}