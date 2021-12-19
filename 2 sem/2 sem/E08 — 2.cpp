#include <iostream>
#include <map>

using namespace std;
struct dot {
	int location, x1, x2;
};
void sorting(int* A, int* Pos, int N) { //Сортируем массивчик как можем
	for (int i = 0; i < N - 1; i++) {
		for (int j = 0; j < N - 1; j++) {
			if (A[j] > A[j + 1]) {
				A[j] = A[j] ^ A[j + 1];
				A[j + 1] = A[j] ^ A[j + 1];
				A[j] = A[j] ^ A[j + 1];
				Pos[j] = Pos[j] ^ Pos[j + 1];
				Pos[j + 1] = Pos[j] ^ Pos[j + 1];
				Pos[j] = Pos[j] ^ Pos[j + 1];
			}
		}
	}
}
dot seekForShort(int* A, int* Pos, int N) { //Он входит уже отсортированным
	dot x;
	int n2;
	int n1 = A[0];
	x.location = 2000000001;
	for (int i = 1; i < N; i++) {
		n2 = A[i];
		if (n2 - n1 < x.location) {
			x.location = n2 - n1;
			x.x1 = Pos[i - 1] + 1;
			x.x2 = Pos[i] + 1;
		}
		n1 = A[i];
	}
	return x;
}
int main() {
	int N;
	cin >> N;
	//map<int, int>* Ord = new map<int, int>;
	map<int, int> Ord;
	//for (int i = -1000000000; i < 1000000001; i++) Ord[i] = 0;
	int b;
	for (int i = 0; i < N; i++) {
		cin >> b;
		Ord[b] = i;
	}
	int* A = new int[N];
	int* Pos = new int[N];
	int k = 0;
	for (int i = -1000000000; i < 1000000001; i++) {
		if (??????????) {
			A[k] = i;
			Pos[k] = Ord[i];
			k++;
		}
	}

	/*for (int i = 0; i < N; i++) {
		
	}
	for (int i = 0; i < N; i++) cin >> A[i];
	sorting(A, Pos, N);*/
	dot answer;
	answer = seekForShort(A, Pos, N);
	delete[]A;
	delete[]Pos;
	if (answer.x1 > answer.x2) {
		answer.x1 = answer.x1 ^ answer.x2;
		answer.x2 = answer.x1 ^ answer.x2;
		answer.x1 = answer.x1 ^ answer.x2;
	}
	cout << answer.location << endl;
	cout << answer.x1 << " " << answer.x2;
}