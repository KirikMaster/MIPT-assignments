#include <vector>
#include <istream>
#include <algorithm>
#include "cell.h"
#include <string>

using usi = unsigned short int;
using namespace std;
// Ѕазовый класс шахматной фигуры
class Piece {
protected:
    cell positiont;
public:
    //  онструктор и деструктор, а также иные методы, если они нужны

    virtual ~Piece() {}

    virtual void check(const cell& q) const {
        if (q.v < 'A' || q.v > 'H' || q.h < 1 || q.h > 8) throw runtime_error("Invalid cell");
    }

    virtual void setPosition(char v, usi h) {
        check(cell(v, h));
        this->positiont = cell(v, h);
    }
    // ¬ернуть текущую позицию фигуры
    virtual cell position() const {
        return this->positiont;
    }
    // ѕолучить множество всех достижимых полей
    virtual vector<cell> moves() const = 0;

    // ѕроверка, может ли данна€ фигура ходить на данное поле
    virtual bool available(const cell& q) const = 0;
};

istream& operator >>(istream& is, Piece& P) {
    string inp;
    is >> inp;
    char v = inp[0];
    usi h = (usi)inp[1]-48;
    if (v < 'A' || v > 'H' || h < 1 || h > 8) throw runtime_error("Invalid cell");
    P.setPosition(v, h);
    return is;
}

//  ороль, ходит на 1 клетку в любом направлении
class King : public Piece {
public:
    King() {}

    void setPosition(char v, usi h) {
        Piece::check(cell(v, h));
        this->positiont = cell(v, h);
    }

    cell position() const {
        return this->positiont;
    }

    bool available(const cell& q) const {
        Piece::check(q);
        if (this->positiont.v == q.v + 1 || this->positiont.v == q.v - 1) {
            if (this->positiont.h == q.h + 1 || this->positiont.h == q.h || this->positiont.h == q.h - 1) {
                return true;
            }
            else return false;
        }
        else if (this->positiont.v == q.v) {
            if (this->positiont.h == q.h + 1 || this->positiont.h == q.h - 1) return true;
            else return false;
        }
        else return false;
    }

    vector<cell> moves() const {
        vector<cell> moves;
        for (usi i = 1; i < 9; i++) {
            for (char j = 'A'; j < 'H' + 1; j++) {
                if (available(cell(j, i))) {
                    moves.push_back(cell(j, i));
                }
            }
        }
        return moves;
    }
};

// —лон, ходит только по диагонали в любом направлении на любое количество клеток
class Bishop : public virtual Piece {
public:
    Bishop() {}

    void setPosition(char v, usi h) {
        Piece::check(cell(v, h));
        this->positiont = cell(v, h);
    }

    cell position() const {
        return this->positiont;
    }

    virtual bool available(const cell& q) const {
        Piece::check(q);
        if (this->positiont.h == q.h) return false;
        else if (this->positiont.h - q.h == this->positiont.v - q.v || this->positiont.h - q.h == -this->positiont.v + q.v) return true;
        else return false;
    }

    vector<cell> moves() const {
        vector<cell> moves;
        for (usi i = 1; i < 9; i++) {
            for (char j = 'A'; j < 'H' + 1; j++) {
                if (available(cell(j, i))) {
                    moves.push_back(cell(j, i));
                }
            }
        }
        return moves;
    }
};

// Ћадь€, ходит только по вертикали и горизонтали в любом направлении на любое количество клеток
class Rook : public virtual Piece {
public:
    Rook() {}

    void setPosition(char v, usi h) {
        Piece::check(cell(v, h));
        this->positiont = cell(v, h);
    }

    cell position() const {
        return this->positiont;
    }

    virtual bool available(const cell& q) const {
        Piece::check(q);
        if ((this->positiont.h - q.h != 0 && this->positiont.v - q.v == 0) || (this->positiont.v - q.v != 0 && this->positiont.h - q.h == 0)) return true;
        else return false;
    }

    vector<cell> moves() const {
        vector<cell> moves;
        for (usi i = 1; i < 9; i++) {
            for (char j = 'A'; j < 'H' + 1; j++) {
                if (available(cell(j, i))) {
                    moves.push_back(cell(j, i));
                }
            }
        }
        return moves;
    }
};

// ‘ерзь, ходит по диагонали, вертикали и горизонтали в любом направлении на любое количество клеток
// (наследуетс€ от слона и ладьи, это не единственный возможный подход, но в данной задаче это так)
class Queen : public Bishop, public Rook {
public:
    Queen() {}

    void setPosition(char v, usi h) {
        Piece::check(cell(v, h));
        this->positiont = cell(v, h);
    }

    cell position() const {
        return this->positiont;
    }

    bool available(const cell& q) const {
        Piece::check(q);
        if (Bishop::available(q) || Rook::available(q)) return true;
        else return false;
    }

    vector<cell> moves() const {
        vector<cell> moves;
        for (usi i = 1; i < 9; i++) {
            for (char j = 'A'; j < 'H' + 1; j++) {
                if (available(cell(j, i))) {
                    moves.push_back(cell(j, i));
                }
            }
        }
        return moves;
    }
};