#include <stdio.h>
#include <cmath>

using T = unsigned long long;
using Y = long double;
Y pow(Y x, T n, T m) {
	if (n == 0) return 1;
	T xd = trunc(x);
	Y xf = x - xd;
	xd %= m;
	x = xd + xf;
	if ((n & 1) != 0) {
		Y a = (pow(x, n - 1, m) * x);
		T b = trunc(a);
		return ((b % m) + (a - b));
	}
	else {
		auto t = pow(x, n >> 1, m);
		Y a = (t * t);
		T b = trunc(a);
		return ((b % m) + (a - b));
	}
}
Y Bine(T n, T m) {
	Y Fidi, AFidi;
	Fidi = ((1 + sqrt(5)) / 2);
	AFidi = ((1 - sqrt(5)) / 2);
	return (((pow(Fidi, n, 10 * m) - pow(AFidi, n, 10 * m)) / sqrt(5)));
}
int main() {
	int N, M;
	scanf_s("%ulld", &N);
	scanf_s("%ulld", &M);
	T ans = round(Bine(N, M));
	printf("%lld", ans % M);
}