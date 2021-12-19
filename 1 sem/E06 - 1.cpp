#include <iostream>
#include <cmath>

using namespace std;
using I = unsigned long long;
I pow(int r, int i) {   //���������� � ������� ��� ��������� ��������
	I temp = 1;
	for (int j = 0; j < i; j++) {
		temp *= r;
	}
	return temp;
}
I palindrom(I n, int digit) { //����������, ������� ����������
	I n1 = 0;
	for (short i = 0; i <= digit; i++) {
		n1 += (n % 10) * pow(10, digit - i - 1);
		n /= 10;
	}
	return n1;
}
int main() {
	I x, y, x1, y1;
	int digitx, digity;
	cin >> x >> y;
	digitx = floor(1 + log(x) / log(10));
	digity = floor(1 + log(y) / log(10));//���������� ��������
	x1 = palindrom(x, digitx);
	y1 = palindrom(y, digity);
	cout << (x1 + y1);
}