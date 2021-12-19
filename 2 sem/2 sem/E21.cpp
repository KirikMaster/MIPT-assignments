#include <iostream>
#include <cmath>

using namespace std;
int main() {
	double N, M;
	cin >> N >> M;
	unsigned int min = ceil(N / M);
	unsigned max = N - M + 1;
	cout << min << " " << max;
}