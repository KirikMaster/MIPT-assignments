#include "Point.h"

class Triangle
{
protected:
    Point a, b, c;
public:
    // Создать треугольник из трёх точек
    Triangle(const Point& a, const Point& b, const Point& c) : a(a), b(b), c(c) {}
    // Посчитать и вернуть периметр треугольника
    double perimeter() const {
        double x, y, z;
        x = (a - b).dist();
        y = (b - c).dist();
        z = (a - c).dist();
        return x + y + z;
    }
};

