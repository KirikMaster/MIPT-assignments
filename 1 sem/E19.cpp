#include <string>
#include <stdio.h>
#include <map>
#include <iostream>

using namespace std;
int main() {
	string stroka;
	cin >> stroka;
	map <char, int> letters;
	for (char c = 'A'; c <= 'Z'; c++) {
		int count = 0;
		for (auto i : stroka) {
			if (i == c) count++;
		}
		letters[c] = count;
	}
	while (true) {
		int max = 0;
		char sym;
		for (char c = 'A'; c <= 'Z'; c++) {
			if (letters[c] > max) {
				max = letters[c];
				sym = c;
			}
		}
		letters[sym] = 0;
		if (!max) break;
		else printf("%c% d\n", sym, max);
	}
	//scanf_s("%10s", &stroka);
	//printf("%10s", stroka);
}