#include <string>
#include <set>

using namespace std;
class ZooKeeper
{
protected:
    multiset<string> animals;
public:
    // ������ ���������� ��������
    ZooKeeper() {}

    // ���������� ��������� ���������� ���������� �����.
    void handleAnimal(const Animal& a) {
        animals.insert(a.getType());
    }

    // ����������, ������� ������ ������ ���� ���� ����������.
    // ���� ����� �� ����, ���������� 0.
    int getAnimalCount(const string& type) const {
        return animals.count(type);
    }
};

