#include <ostream>
#include <iostream>

using namespace std;
class Rational {
protected:
    int a;
    int b;
public:
    // Конструктор дроби, здесь a - числитель, b - знаменатель
    Rational(int a, int b) : a(a), b(b) {}

    Rational() : Rational(1, 1) {}

    int GetA() const{
        return this->a;
    }

    int GetB() const{
        return this->b;
    }

    // Реализуйте операторы:
    // - сложения двух дробей
    Rational operator +(Rational& R) const{
        int b = this->b * R.GetB();
        int a = this->b * R.GetA() + R.GetB() * this->a;
        return Rational(a, b);
    }
    // - вычитания двух дробей
    Rational operator -(Rational& R) const{
        int b = this->b * R.GetB();
        int a = -this->b * R.GetA() + R.GetB() * this->a;
        return Rational(a, b);
    }
    // - умножения двух дробей
    Rational operator *(Rational& R) const{
        return Rational(this->a * R.GetA(), this->b * R.GetB());
    }
    // - деления двух дробей
    Rational operator /(Rational& R) const{
        return Rational(this->a * R.GetB(), this->b * R.GetA());
    }
    // - умножения дроби на целое число (должно работать при любом порядке операндов)
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