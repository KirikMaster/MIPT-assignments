#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;
int main() {
	int N;
	cin >> N;
	double y_1, y, y1, arctg1, PI, E;
	arctg1 = atan(1.);
	PI = atan(1) * 4;
	E = exp(1);
	y_1 = PI / (arctg1 + 1 - 5 * E);
	y = y_1;
	y1 = (PI - y + 5 * E * y_1) / arctg1;
	cout << 0 << " : " << setprecision(32) << y_1 << endl << 1 << " : " << setprecision(32) << y << endl;
	for (int i = 2; i < N + 1; i++) {
		y_1 = y;
		y = y1;
		y1 = (PI - y + 5 * E * y_1) / arctg1;
		cout << i << " : " << setprecision(32) << y1 << endl;
	}
}