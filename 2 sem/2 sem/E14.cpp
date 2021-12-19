#include <stdio.h>
#include <cmath>

int troot(int n) {
	return trunc(sqrt(n));
}
bool whowins(int n, bool player, int* wins) {   //Пусть bool = 0 - первый игрок, bool = 1 - второй
	if (wins[n] != -1 && player == false) return wins[n];
	else if (wins[n] != -1 && player == true) return !wins[n];
	else {
		for (int i = n - 1; i > n - troot(n + 1) - 1; i--) {
			if (whowins(i, !player, wins) == player) return player;    //Проверяем, может ли выиграть этот игрок
		}
		return !player;                                          //Это если не может
	}
}
int main() {
	int n;
	scanf("%d", &n);
	int* wins = new int[n];
	wins[0] = 0;
	for (int i = 1; i < n; i++) wins[i] = -1;
	for (int i = 1; i < n; i++) {
		wins[i] = whowins(i, 0, wins);
	}
	int player = whowins(n - 1, 0, wins) + 1;
	switch (player)
	{
	case 1:
		printf("%s", "First");
		break;
	case 2:
		printf("%s", "Second");
		break;
	}
	delete[] wins;
}