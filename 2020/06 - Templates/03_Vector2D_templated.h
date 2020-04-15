#include <iostream>

#pragma once
template<typename T>
class Vector2D
{
protected:
	T x;
	T y;
public:
	// ������������
	Vector2D() : Vector2D(0, 0) {}
	Vector2D(T x, T y) : x(x), y(y) {}

	// ����������
	~Vector2D() {}

	// ��������� ���������
	T getX() const {
		return this->x;
	}
	T getY() const {
		return this->y;
	}

	// ������� ���������
	void setX(T x) {
		this->x = x;
	}
	void setY(T y) {
		this->y = y;
	}

	// ������������� �������� - ��������� ���� �������� �� ���������
	bool operator== (const Vector2D& v2) const {
		return x == v2.x && y == v2.y;
	}

	// ��� ���� ������������� �������� - ����������� ��������
	// ��, ��� ��������� ��������! ���� - ��������� ������ ������ ��� != ������������ ��� ���������� ==
	bool operator!= (const Vector2D& v2) const {
		return !(*this == v2);
	}

	// ����� ���� ��������, �������� ������� �� ��������, ������������ ����� ������
	Vector2D operator+ (const Vector2D& v2) const {
		return Vector2D(x + v2.x, y + v2.y);
	}

	// ��������� ��������, �������� ������� �� ��������, ������������ ����� ������
	Vector2D operator- (const Vector2D& v2) const {
		return Vector2D(x - v2.x, y - v2.y);
	}

	// �������� ��������� ������� �� ������, �������� ������ �� ��������, ������������ ����� ������
	Vector2D operator* (const int a) const {
		return Vector2D(a * x, a * y);
	}
};

template<typename T>
// �������� ��������� ������� �� ������, �������� ������ �� ��������, ������������ ����� ������
// ����������, ������? ��������� ������� �� ������ - ��� ��������� ��������, ������ ��������� *���* ������.
Vector2D<T> operator* (int a, const Vector2D<T>& v) {
	return Vector2D<T>(v.getX() * a, v.getY() * a);
}
template<typename T>
// ����� �������, ��������� ������ � ������� (1; 1)
std::ostream& operator<<(std::ostream& os, const Vector2D<T>& v) {
	os << "(" << v.getX() << "; " << v.getY() << ")";
	return os;
}
template<typename T>
// ������ �������, ������ ������ ��� ���������� ��� ��������
std::istream& operator>>(std::istream& is, Vector2D<T>& v) {
	T x, y;
	is >> x >> y;
	v.setX(x);
	v.setY(y);
	return is;
};

