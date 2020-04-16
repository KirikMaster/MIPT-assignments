#include <string>
#include <set>

using namespace std;
class ZooKeeper
{
protected:
    multiset<string> animals;
public:
    // Создаём смотрителя зоопарка
    ZooKeeper() {}

    // Смотрителя попросили обработать очередного зверя.
    void handleAnimal(const Animal& a) {
        animals.insert(a.getType());
    }

    // Возвращает, сколько зверей такого типа было обработано.
    // Если таких не было, возвращает 0.
    int getAnimalCount(const string& type) const {
        return animals.count(type);
    }
};

