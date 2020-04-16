#include <string>
#include <istream>
#include <ostream>

using namespace std;
#pragma once
class Person
{
protected:
    string surname;
    string name;
    string middlename;
public:
    // Создать человека с ФИО
    Person(string surname, string name, string middleName) : surname(surname), name(name), middlename(middleName) {}
    Person() : Person("", "", "") {}
    ~Person() {}

    string getName() const{
        return name;
    }
    string getSurname() const{
        return surname;
    }
    string getMiddlename() const{
        return middlename;
    }

    void setName(string name) {
        this->name = name;
    }
    void setSurname(string surname) {
        this->surname = surname;
    }
    void SetMiddlename(string middlename) {
        this->middlename = middlename;
    }

    bool operator <(Person& p) {
        if (this->surname == p.getSurname()) {
            if (this->name == p.getName()) {
                if (this->middlename > p.getMiddlename()) return 0;
                else return 1;
            }
            else if (this->name < p.getName()) return 1;
            else return 0;
        }
        else if (this->surname < p.getSurname()) return 1;
        else return 0;
    }
};

istream& operator >>(istream& is, Person& p) {
    string surname, name, middlename;
    is >> surname >> name >> middlename;
    p.SetMiddlename(middlename);
    p.setName(name);
    p.setSurname(surname);
    return is;
}

ostream& operator <<(ostream& os, const Person& p) {
    os << p.getSurname() << " " << p.getName() << " " << p.getMiddlename();
    return os;
}