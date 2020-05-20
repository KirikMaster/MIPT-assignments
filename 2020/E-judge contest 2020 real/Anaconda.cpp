#include <string>
#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <iterator>
#include <cassert>

using usi = unsigned short int;
using namespace std;
int main() {
	string zoo, pyp;
	cin >> zoo >> pyp;
	map<string, vector<usi>> animals;
	vector<usi> python;
	ifstream input;
	input.open(zoo);
	string str, title;
	bool name = true;
	while (!input.eof()) {
		getline(input, str);
		if (name) {
			title = str;
			name = false;
		}
		else if (str == ""){
			name = true;
		}
		else {
			animals[title].push_back(str.size());
		}
	}
	input.close();
	input.open(pyp);
	while (input >> str) {
		python.push_back(str.size());
	}
	input.close();
	map<string, usi> missing;
	for (auto anim : animals) {   //Взяли животное
		vector<usi>::iterator it, fixed, an, fu;
		string kat = anim.first;          //Название животного
		vector<usi> anima = anim.second;  //Профиль животного
		for (it = python.begin(); it != python.end(); ++it) { //Пошли строчка за строчкой по питону
			fixed = it;
			bool alarm = false;
			for (an = anima.begin(); an != anima.end(); ++an) {  //Перебрали все строчки животного
				if (*it != *an) {
					alarm = true;
					it = fixed;
					break;
				}
				fu = it;
				++fu;
				if (fu == python.end()) {
					alarm = true;
					break;
				}
				fu = an;
				++fu;
				if (fu == anima.end()) break;
				else ++it;
			}
			if (!alarm) {             //alarm не было, значит животное сошлось по контуру
				missing[kat]++;
			}
		
		}
	}
	map<string, usi>::iterator mis;
	for (mis = missing.begin(); mis != missing.end(); ++mis) {
		cout << mis->first << " " << mis->second << endl;
	}
}