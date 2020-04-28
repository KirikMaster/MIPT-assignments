#include "Point.h"

class Triangle
{
protected:
    Point a, b, c;
public:
    // ������� ����������� �� ��� �����
    Triangle(const Point& a, const Point& b, const Point& c) : a(a), b(b), c(c) {}
    // ��������� � ������� �������� ������������
    double perimeter() const {
        double x, y, z;
        x = (a - b).dist();
        y = (b - c).dist();
        z = (a - c).dist();
        return x + y + z;
    }
};

