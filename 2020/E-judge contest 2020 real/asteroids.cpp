#include <iostream>
#include <map>
#include <vector>
#include <cmath>
#include <iomanip>

struct station
{
	double x0, y0, z0, R;
};

struct asteroid {
	unsigned long long uuid;
	double x, y, z;
};

using ull = unsigned long long;
using namespace std;
int main() {
	station S;
	double x0, y0, z0, R;
	cin >> x0 >> y0 >> z0 >> R;
	S.x0 = x0;
	S.y0 = y0;
	S.z0 = z0;
	S.R = R;
	unsigned int N;
	cin >> N;
	map<ull, asteroid> data;
	ull uuid, ts;
	double x, y, z;
	asteroid as;
	for (unsigned int i = 0; i < N; i++) {
		cin >> uuid >> ts >> x >> y >> z;
		as.x = x;
		as.y = y;
		as.z = z;
		as.uuid = uuid;
		data[ts] = as;
	}
	vector<ull> pot;
	map<ull, asteroid>::iterator it;
	for (it = data.begin(); it != data.end(); ++it) {
		as = it->second;
		bool alarm = false;
		for (auto c : pot) {
			if (c == as.uuid) {
				alarm = true;
				break;
			}
		}
		if (alarm) continue;
		else {
			double dist;
			dist = sqrt((as.x - S.x0) * (as.x - S.x0) + (as.y - S.y0) * (as.y - S.y0) + (as.z - S.z0) * (as.z - S.z0));
			if (dist < S.R) pot.push_back(as.uuid);
		}
	}
	for (auto c : pot) {
		cout << c << endl;
	}
}