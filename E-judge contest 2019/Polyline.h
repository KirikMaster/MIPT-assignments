#include <cmath>

class Polyline
{
protected:
    struct Point
    {
        double x;
        double y;
        Point* next;
    };
    Point* first;
    Point* last;
    unsigned int num = 0;
public:
    // ����������� � ����������, ���� ����������
    Polyline() {
        first = new Point;
        last = first;
    }
    virtual ~Polyline() {
        Point* next = first->next;
        delete first;
        while (next != nullptr) {
            first = next;
            next = next->next;
            delete first;
        }
    }
    // �������� ��������� ����� � �������
    void addPoint(double x, double y) {
        last->x = x;
        last->y = y;
        last->next = new Point;
        last = last->next;
        last->next = nullptr;
        num++;
    }

    // �������� ��������� ����� � ������� � ������ ������
    unsigned int getNumberOfPoints() const {
        return num;
    }

    // �������� ����� ������� � ������ ������
    double getLength() const {
        Point* cur;
        double Length = 0;
        for (cur = first; cur->next->next != nullptr; cur = cur->next) {
            Length += sqrt((cur->x - cur->next->x) * (cur->x - cur->next->x) + (cur->y - cur->next->y) * (cur->y - cur->next->y));
        }
        return Length;
    }

    // �������� x-���������� i-�� ����� �������, ����� ���������� � ������� ����������
    // (�������������, ��� ����� i ������ ������, ��� ��, ������� ���� getNumberOfPoints())
    double getX(unsigned int i) const {
        Point* cur;
        unsigned int count = 0;
        for (cur = first; cur != nullptr; cur = cur->next) {
            if (i == count) return cur->x;
            count++;
        }
        return 0;
    }

    // �������� y-���������� i-�� ����� �������, ����� ���������� � ������� ����������
    // (�������������, ��� ����� i ������ ������, ��� ��, ������� ���� getNumberOfPoints())
    double getY(unsigned int i) const {
        Point* cur;
        unsigned int count = 0;
        for (cur = first; cur != nullptr; cur = cur->next) {
            if (i == count) return cur->y;
            count++;
        }
        return 0;
    }
};

