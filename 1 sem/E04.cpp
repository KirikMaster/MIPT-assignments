#include <iostream>
#include <string>

using namespace std;
using I = unsigned long long;
I pow(int r, int i) {   //¬озведение в степень дл€ небольших степеней
	I temp = 1;
	for (int j = 0; j < i; j++) {
		temp *= r;
	}
	return temp;
}
int convert(char c) {
	if (c >= '0' && c <= '9') return (int)(c - '0');
	else if (c >= 'a' && c <= 'z') return (int)(c - 'a' + 10);
	else if (c >= 'A' && c <= 'Z') return (int)(c - 'A' + 10);
	return 0;
}
int main() {
	I ans = 0;
	string x;
	int r;
	cin >> r >> x;
	int index = x.size();
	for (auto c : x) {
		ans += pow(r, index - 1) * convert(c);
		index--;
	}
	cout << ans;
}