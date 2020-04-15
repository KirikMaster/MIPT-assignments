#include <iostream>

#pragma once
template<typename T>
class Vector2D
{
protected:
	T x;
	T y;
public:
	// Конструкторы
	Vector2D() : Vector2D(0, 0) {}
	Vector2D(T x, T y) : x(x), y(y) {}

	// Деструктор
	~Vector2D() {}

	// Получение координат
	T getX() const {
		return this->x;
	}
	T getY() const {
		return this->y;
	}

	// Задание координат
	void setX(T x) {
		this->x = x;
	}
	void setY(T y) {
		this->y = y;
	}

	// Перегруженный оператор - сравнение двух векторов на равенство
	bool operator== (const Vector2D& v2) const {
		return x == v2.x && y == v2.y;
	}

	// Ещё один перегруженный оператор - неравенство векторов
	// Да, это отдельный оператор! Хинт - настоящие джедаи смогут для != использовать уже написанное ==
	bool operator!= (const Vector2D& v2) const {
		return !(*this == v2);
	}

	// Сумма двух векторов, исходные вектора не меняются, возвращается новый вектор
	Vector2D operator+ (const Vector2D& v2) const {
		return Vector2D(x + v2.x, y + v2.y);
	}

	// Вычитание векторов, исходные вектора не меняются, возвращается новый вектор
	Vector2D operator- (const Vector2D& v2) const {
		return Vector2D(x - v2.x, y - v2.y);
	}

	// Оператор умножения вектора на скаляр, исходный вектор не меняется, возвращается новый вектор
	Vector2D operator* (const int a) const {
		return Vector2D(a * x, a * y);
	}
};

template<typename T>
// Оператор умножения скаляра на вектор, исходный вектор не меняется, возвращается новый вектор
// Неожиданно, правда? Умножение скаляра на вектор - это отдельный оператор, причём описанный *вне* класса.
Vector2D<T> operator* (int a, const Vector2D<T>& v) {
	return Vector2D<T>(v.getX() * a, v.getY() * a);
}
template<typename T>
// Вывод вектора, ожидается строго в формате (1; 1)
std::ostream& operator<<(std::ostream& os, const Vector2D<T>& v) {
	os << "(" << v.getX() << "; " << v.getY() << ")";
	return os;
}
template<typename T>
// Чтение вектора, читает просто две координаты без хитросте
std::istream& operator>>(std::istream& is, Vector2D<T>& v) {
	T x, y;
	is >> x >> y;
	v.setX(x);
	v.setY(y);
	return is;
};

