#include <iostream>
#include <vector>

using namespace std;
using I = unsigned long long;
bool invert(bool x) {
	if (x == true) return false;
	else return true;
}
int main() {
	int n;
	cin >> n;
	vector <I> A(n);
	for (int i = 0; i < n; i++) cin >> A[i];
	I b, sum = 0;
	bool odd = true, alarm = false;
	int index = 0;
	for (int i = 0; i < n + 1; i++) {
		cin >> b;
		for (int j = index; j < n; j++) {
			if (b < A[j]) {
				if (odd) {
					sum += b;
					sum = sum % 1000000000;
				}
				odd = invert(odd);
				break;
			}
			else {
				index++;
				if (odd) {
					sum += A[j];
					sum = sum % 1000000000;
				}
				odd = invert(odd);
				if (index == n) alarm = true;
			}
		}
		if (alarm) {
			if (odd) sum += b;
			odd = invert(odd);
		}
	}
	cout << (sum % 1000000000);
}