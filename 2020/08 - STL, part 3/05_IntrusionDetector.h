#include <string>
#include "Connection.h"
#include <map>
#include <vector>
#include <set>

using namespace std;
using usi = unsigned short int;
using ull = unsigned long long;
class IntrusionDetector
{
protected:
    usi timeThreshold;
    usi portLimit;
    map<string, multimap<ull, usi>> Connections;
public:
    // Задать временное окно для анализа (см. описание логики выше)
    void setTimeThreshold(usi timeThreshold) {
        this->timeThreshold = timeThreshold;
    }

    // Задать минимальное количество портов для срабатывания (см. описание логики выше)
    void setPortLimit(usi portLimit) {
        this->portLimit = portLimit;
    }

    // Вызов этого метода уведомляет анализатор о новом подключении.
    void handleConnection(const Connection& c) {
        Connections[c.getSource()].insert({ c.getTimestamp(), c.getPort() });
    }

    // Проверить, является ли указанный адрес нарушителем
    bool isIntruder(const string& source) const {
        if (Connections.find(source) == Connections.end()) return false;                     //Проверка на присутствие действий со стороны пользователя
        set<usi> Ports;                                                                      //То есть на то, что его ключ есть в Connections
        multimap<ull, usi> Times_Ports = Connections.find(source)->second;                        //Чисто Times_Ports
        multimap<ull, usi>::const_iterator TP1;
        multimap<ull, usi>::const_iterator TP2;
        for (TP1 = Times_Ports.begin(); TP1 != Times_Ports.end(); ++TP1) {
            for (TP2 = Times_Ports.begin(); TP2 != TP1; ++TP2) {                             //Вносим в Ports все порты, к которым за время, меньшее timeThreshold подключался source
                if ((TP1->first - TP2->first) < timeThreshold) {                             //То есть, проверка по времени
                    pair <
                        multimap<ull, usi>::const_iterator,
                        multimap<ull, usi>::const_iterator
                    > range = Times_Ports.equal_range(TP2->first);
                    multimap<ull, usi>::const_iterator it;
                    for (it = range.first; it != range.second; ++it) {
                        Ports.insert(it->second);
                    }
                }
            }
            Ports.insert(TP1->second);                                                       //Вносим также текущий
            if (Ports.size() >= portLimit) return true;                                      //Проверка количества портов
            Ports.clear();                                                                   //Очищаем сет с портами чтобы потом заполнить его с начала на следующей итерации
        }
        return false;
    }
};

