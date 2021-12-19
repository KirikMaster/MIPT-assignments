#include <stdio.h>
#include <map>

using namespace std;
int min(int a, int b) {
	return (a > b ? b : a);
}
int main() {
	int len1, len2;
	scanf("%d%d", &len1, &len2);
	map <int, int> includes1;
	map <int, int> includes2;
	int a;
	for (int i = 0; i < len1; i++) {
		scanf("%d", &a);
		includes1[a]++;
	}
	for (int i = 0; i < len2; i++) {
		scanf("%d", &a);
		includes2[a]++;
	}
	//map <int, int>* pos = &includes1;
	int same = 0;
	//map <int, int>* end = pos + len1;
	//for (; pos < end; pos++) {
	//}
	for (auto i : includes1) {
		same += min(i.second, includes2[i.first]);
	}
	//delete[] pos;
	//delete[] end;
	printf("%d", same);
}