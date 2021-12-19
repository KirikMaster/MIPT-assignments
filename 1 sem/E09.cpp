#include <cmath>
#include <stdio.h>

struct dot {
	double x, y;
};

double SG(dot* dot1, dot* dot2, dot* dot3) {
	double a = sqrt((dot1->x - dot2->x) * (dot1->x - dot2->x) + (dot1->y - dot2->y) * (dot1->y - dot2->y));
	double b = sqrt((dot2->x - dot3->x) * (dot2->x - dot3->x) + (dot2->y - dot3->y) * (dot2->y - dot3->y));
	double c = sqrt((dot3->x - dot1->x) * (dot3->x - dot1->x) + (dot3->y - dot1->y) * (dot3->y - dot1->y));
	double p = (a + b + c) / 2;
	return  sqrt(p * (p - a) * (p - b) * (p - c));
}

int main() {
	int N;
	scanf("%d", &N);
	dot* dotset1 = new dot[N];
	for (int i = 0; i < N; i++) {
		scanf("%lf%lf", &dotset1->x, &dotset1->y);
		dotset1 += 1;
	}
	dotset1 -= N;
	dot* dotset2; dot* dotset3;
	dotset2 = dotset1 + 1;
	dotset3 = dotset1 + 2;
	double smin;
	smin = SG(dotset1, dotset2, dotset3);
	dotset2 -= 1;
	dotset3 -= 2;
	//int count1, count2, count3 = 0;
	for (int i = 0; i < N; i++) {
		dotset2 = dotset1 + 1;
		for (int j = i+1; j < N; j++) {
			dotset3 = dotset2 + 1;
			for (int k = j+1; k < N; k++) {
				/*if (dotset1 == dotset2 || dotset2 == dotset3 || dotset3 == dotset1) {
					dotset3 += 1;
					continue;
				}*/
				if (SG(dotset1, dotset2, dotset3) < smin) smin = SG(dotset1, dotset2, dotset3);
				dotset3++;
			}
			dotset2++;
		}
		dotset1++;
	}
	dotset1 -= N;
	delete[] dotset1;
	printf("%.4lf", smin);
}