#include <iostream>
#include <cmath>

using namespace std;
using I = unsigned long long;
I pow(int r, int i) {   //Возведение в степень для небольших степеней
	I temp = 1;
	for (int j = 0; j < i; j++) {
		temp *= r;
	}
	return temp;
}
void output(int num) {
	if (num < 10)	cout << num;
	else if (num < 21)
	{
		if (num == 10) cout << 'A';
		else if (num == 11) cout << 'B';
		else if (num == 12) cout << 'C';
		else if (num == 13) cout << 'D';
		else if (num == 14) cout << 'E';
		else if (num == 15) cout << 'F';
		else if (num == 16) cout << 'G';
		else if (num == 17) cout << 'H';
		else if (num == 18) cout << 'I';
		else if (num == 19) cout << 'J';
		else if (num == 20) cout << 'K';
	}
	else {
		if (num == 21) cout << 'L';
		else if (num == 22) cout << 'M';
		else if (num == 23) cout << 'N';
		else if (num == 24) cout << 'O';
		else if (num == 25) cout << 'P';
		else if (num == 26) cout << 'Q';
		else if (num == 27) cout << 'R';
		else if (num == 28) cout << 'S';
		else if (num == 29) cout << 'T';
		else if (num == 30) cout << 'U';
		else if (num == 31) cout << 'V';
		else if (num == 32) cout << 'W';
		else if (num == 33) cout << 'X';
		else if (num == 34) cout << 'Y';
		else if (num == 35) cout << 'Z';
	}
}
int main() {
	int r, digit;
	unsigned long long x;
	cin >> x >> r;
	digit = floor(1 + log(x) / log(r)); //Оценка количества разрядов
	int num;
	for (int i = digit - 1; i > -1; i--) {
		num = x / pow(r, i);
		output(num);
		x %= pow(r, i);
	}
}