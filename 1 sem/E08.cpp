#include <iostream>

using namespace std;
struct dot {
	int location, x1, x2;
};
void sorting(int* A, int* Pos, int N) { //��������� ��������� ��� �����
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
dot seekForShort(int* A, int* Pos, int N) { //�� ������ ��� ���������������
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
	int* A = new int[N];
	int* Pos = new int[N];
	for (int i = 0; i < N; i++) Pos[i] = i;
	for (int i = 0; i < N; i++) cin >> A[i];
	sorting(A, Pos, N);
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