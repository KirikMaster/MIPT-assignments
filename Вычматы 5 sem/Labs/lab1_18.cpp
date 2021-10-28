#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;
int main() {
	int N;
	cin >> N;
	double y_1, y, y1, arctg1, PI, E, dy;
	arctg1 = atan(1.);
	PI = atan(1) * 4;
	E = exp(1);
	dy = 1e-6;
	y = PI / (arctg1 + 1 - 5 * E) + dy;
	y_1 = y;
	y1 = (PI - y + 5 * E * y_1) / arctg1;
	cout << 0 << " : " << setprecision(32) << y_1 << endl << 1 << " : " << setprecision(32) << y << endl;
	for (int i = 2; i < N + 1; i++) {
		y_1 = y;
		y = y1;
		y1 = (PI - y + 5 * E * y_1) / arctg1;
		cout << i << " : " << setprecision(32) << y1 << endl << endl;
	}
	double c1, c2, lam1, lam2;
	c1 = 0.59259738e-6;
	c2 = 4.07402619e-6;
	lam1 = 3.571753348;
	lam2 = -2.740806333;
	double y_th;
	y_th = c1 * pow(lam1, N) + c2 * pow(lam2, N) + PI / (arctg1 + 1 - 5 * E);
	cout << N << " in theory: " << y_th;
}