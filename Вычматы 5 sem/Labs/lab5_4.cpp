#include <iostream>
#include <cmath>
#include <vector>
#include <iomanip>

using namespace std;

double f(double x) {
	return sin(100 * x) / (1 + x * x);
}

int main() {
	double h, PI;
	h = 2.77e-6;
	PI = 4 * atan(1);
	vector <double> x(round(PI / 2 / h));
	for (int i = 0; i < x.size(); i++) {
		x[i] = i * h;
	}
	double integral = 0;
	for (auto i : x) {
		integral += f(i);
	}
	integral -= (f(x[0]) + f(x[x.size() - 1])) / 2;
	integral *= PI / 2 / (x.size());
	cout << "Newton-Kotex method: " << setprecision(4) << integral << endl;

	double integral2;
	double c1, c2, x1, x2;
	x1 = PI / 4 * (1 - sqrt(PI * PI - 0.0006));
	x2 = PI / 4 * (1 + sqrt(PI * PI - 0.0006));
	c1 = PI / (100 * sqrt(PI * PI - 0.0006));
	c2 = -PI / (100 * sqrt(PI * PI - 0.0006));
	integral2 = (c1 * f(x1) + c2 * f(x2)) * PI / 4;
	cout << "Gauss method: " << setprecision(4) << integral2;
}