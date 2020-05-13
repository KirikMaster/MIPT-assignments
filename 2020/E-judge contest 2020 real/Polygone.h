#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;
class Polygone
{
protected:
    vector<Point2D> points;
public:
    // Конструктор, создаёт полигон из набора точек.
    // Точки передаются в порядке обхода полигона по контуру.
    Polygone(const std::vector<Point2D>& points) : points(points) {}

    // Деструктор, если нужен
    ~Polygone() {}

    double Geron(Point2D& x, Point2D& y, Point2D& z) const {
        double a = sqrt((x.x() - y.x()) * (x.x() - y.x()) + (x.y() - y.y()) * (x.y() - y.y()));
        double b = sqrt((x.x() - z.x()) * (x.x() - z.x()) + (x.y() - z.y()) * (x.y() - z.y()));
        double c = sqrt((z.x() - y.x()) * (z.x() - y.x()) + (z.y() - y.y()) * (z.y() - y.y()));
        double p = (a + b + c) / 2;
        return sqrt(p * (p - a) * (p - b) * (p - c));
    }
    // Возвращает площадь полигона
    double area() const {
        vector<Point2D> p = points; //Тупо копия. Да. А что ещё делать
        //vector<Point2D>::const_iterator start;
        //start = points.begin();
        //vector<Point2D>::const_iterator it1;
        //vector<Point2D>::const_iterator it2;
        //it1 = points.begin() + 1;
        //it2 = it1++;
        double ar = 0;
        for (unsigned int i = 1; i < this->size() - 1; i++) {
            ar += Geron(p[0], p[i], p[i+1]);
        }
        return ar;
    }

    // Возвращает количество вершин полигона
    unsigned int size() const {
        vector<Point2D>::const_iterator it;
        unsigned int count = 0;
        for (it = points.begin(); it != points.end(); ++it) {
            count++;
        }
        return count;
    }

    // Возвращает N-ую вершину полигона
    // (вершины нумеруются в том же порядке, в котором были переданы)
    Point2D vertex(unsigned int N) const {
        vector<Point2D> p = points;
        return p[N];
        //vector<Point2D>::const_iterator it;
        //it += N;
        //return *it;
    }
};
