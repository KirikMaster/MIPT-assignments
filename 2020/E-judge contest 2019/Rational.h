#include <ostream>
#include <iostream>

using namespace std;
class Rational {
protected:
    int a;
    int b;
public:
    // ����������� �����, ����� a - ���������, b - �����������
    Rational(int a, int b) : a(a), b(b) {}

    Rational() : Rational(1, 1) {}

    int GetA() const{
        return this->a;
    }

    int GetB() const{
        return this->b;
    }

    // ���������� ���������:
    // - �������� ���� ������
    Rational operator +(Rational& R) const{
        int b = this->b * R.GetB();
        int a = this->b * R.GetA() + R.GetB() * this->a;
        return Rational(a, b);
    }
    // - ��������� ���� ������
    Rational operator -(Rational& R) const{
        int b = this->b * R.GetB();
        int a = -this->b * R.GetA() + R.GetB() * this->a;
        return Rational(a, b);
    }
    // - ��������� ���� ������
    Rational operator *(Rational& R) const{
        return Rational(this->a * R.GetA(), this->b * R.GetB());
    }
    // - ������� ���� ������
    Rational operator /(Rational& R) const{
        return Rational(this->a * R.GetB(), this->b * R.GetA());
    }
    // - ��������� ����� �� ����� ����� (������ �������� ��� ����� ������� ���������)
    Rational operator *(int a) const{
        return Rational(this->a * a, this->b);
    }
};

Rational operator *(int a, const Rational& R) {
    return Rational(R.GetA() * a, R.GetB());
}

ostream& operator <<(ostream& os, const Rational& R) {
    os << R.GetA() << "/" << R.GetB();
    return os;
}