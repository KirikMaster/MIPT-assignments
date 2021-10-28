#include <iostream>
#include <cmath>
#include <iomanip>

double my_function(double x) {
	return exp(1 - x * x) - x * x;
}

double my_function_der(double x) {
	return -exp(1 - x * x) * 2 * x - 2 * x;
}

double my_function_der2(double x) {
	return exp(1 - x * x) * 4 * x * x - 2;
}

int main() {
	double a, b, x0, x, prec, e, error;
	e = exp(1);
	prec = 1e-6;
	a = 0;
	b = 2;
	x0 = 1.2;
	error = 0.8;
	int N;
	std::cin >> N;
	for (int i = 0; i < N; i++) {
		x = x0 - my_function(x0) / my_function_der(x0);
		x0 = x;
		std::cout << std::setprecision(7) << x << '\n';
	}
	std::cout << "N = " << N << ",    x = +-" << std::setprecision(7) << x;
}