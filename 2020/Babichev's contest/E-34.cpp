#include <iostream>
#include <string>
#include <set>

using T = long long;
using namespace std;

class point {          //Ôèçè÷åñêàÿ òî÷êà ñ öåëî÷èñëåííûìè êîîðäèíàòàìè
private:
    T x;
    T y;
    T z;
public:
    point(T& x, T& y, T& z) : x(x), y(y), z(z) {
    }

    point() {
        this->x = this->y = this->z = 0;
    }

    ~point() {}

    T getX() const { return this->x; };
    T getY() const { return this->y; };
    T getZ() const { return this->z; };

    bool operator==(const point& p) const {
        if (this->x == p.getX() && this->y == p.getY() && this->z == p.getZ()) return 1;
        else return 0;
    }

    bool operator!=(const point& p) const {
        return !(*this == p);
    }

    bool operator<(const point& p) const {                   //Ñðàâíèâàåì ïî x, åñëè ðàâíû - òî ïî y, åñëè ðàâíû - òî ïî z
        if (this->x == p.getX()) {
            if (this->y == p.getY()) {
                if (this->z < p.getZ()) return 1;
                else return 0;
            }
            else if (this->y < p.getY()) return 1;
            else return 0;
        }
        else if (this->x < p.getX()) return 1;
        else return 0;
    }

    bool operator>(const point& p) const {
        if (this->x == p.getX()) {
            if (this->y == p.getY()) {
                if (this->z > p.getZ()) return 1;
                else return 0;
            }
            else if (this->y > p.getY()) return 1;
            else return 0;
        }
        else if (this->x > p.getX()) return 1;
        else return 0;
    }
    
    point operator+(const point& p) const {
        point q = point();
        q.x = (this->x + p.getX());
        q.y = (this->y + p.getY());
        q.z = (this->z + p.getZ());
        return q;
    }
};

int main() {
    multiset<point> points;
    int n;                        //Êîëè÷åñòâî ýëåìåíòîâ
    cin >> n;
    T x, y, z;
    for (int i = 0; i < n; i++) {         //Êëàä¸ì òî÷êè â ìóëüòèñåò
        cin >> x >> y >> z;
        points.insert(point(x, y, z));
    }
    multiset<point>::iterator front;
    multiset<point>::reverse_iterator back;
    front = points.begin();
    back = points.rbegin();
    point center = *front + *back;
    int m = n - (n % 2);            //Íàèáîëüøåå ÷¸òíîå êîëè÷åñòâî ýëåìåíòîâ
    bool alarm = 0;
    for (int i = 0; i < (m / 2); i++) {
        if ((*front + *back) != center) alarm = 1;
        ++front;
        ++back;
        if (alarm) break;
    }
    if (n != m) {
        if (*front != center) alarm = 1;
    }
    cout << (alarm ? "No" : "Yes");
}
