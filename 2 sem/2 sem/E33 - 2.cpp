#include <stdio.h>

using T = unsigned long long;
int main() {
	int N, M;
	scanf("%ulld", &N);
	scanf("%ulld", &M);
	T C = 1;
	T C1 = 1;
	T C2 = 2;
	for (int i = 4; i < N + 1; i++) {
		C = C1;
		C1 = C2;
		C2 = (C + C1) % M;
	}
	printf("%lld", C2);
}