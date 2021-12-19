#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;
using I = unsigned long long;
int main() {
	int n;
	cin >> n;
	vector <double> A(n);
	for (int i = 0; i < n; i++) {
		cin >> A[i];
	}
	double B, ans = 0;
	for (int i = 0; i < n; i++) {
		cin >> B;
		ans += A[i] * B;
	}
	cout << setprecision(4) << fixed << ans;
}