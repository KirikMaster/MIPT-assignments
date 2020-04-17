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
    // ������ ��������� ���� ��� ������� (��. �������� ������ ����)
    void setTimeThreshold(usi timeThreshold) {
        this->timeThreshold = timeThreshold;
    }

    // ������ ����������� ���������� ������ ��� ������������ (��. �������� ������ ����)
    void setPortLimit(usi portLimit) {
        this->portLimit = portLimit;
    }

    // ����� ����� ������ ���������� ���������� � ����� �����������.
    void handleConnection(const Connection& c) {
        Connections[c.getSource()].insert({ c.getTimestamp(), c.getPort() });
    }

    // ���������, �������� �� ��������� ����� �����������
    bool isIntruder(const string& source) const {
        if (Connections.find(source) == Connections.end()) return false;                     //�������� �� ����������� �������� �� ������� ������������
        set<usi> Ports;                                                                      //�� ���� �� ��, ��� ��� ���� ���� � Connections
        multimap<ull, usi> Times_Ports = Connections.find(source)->second;                        //����� Times_Ports
        multimap<ull, usi>::const_iterator TP1;
        multimap<ull, usi>::const_iterator TP2;
        for (TP1 = Times_Ports.begin(); TP1 != Times_Ports.end(); ++TP1) {
            for (TP2 = Times_Ports.begin(); TP2 != TP1; ++TP2) {                             //������ � Ports ��� �����, � ������� �� �����, ������� timeThreshold ����������� source
                if ((TP1->first - TP2->first) < timeThreshold) {                             //�� ����, �������� �� �������
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
            Ports.insert(TP1->second);                                                       //������ ����� �������
            if (Ports.size() >= portLimit) return true;                                      //�������� ���������� ������
            Ports.clear();                                                                   //������� ��� � ������� ����� ����� ��������� ��� � ������ �� ��������� ��������
        }
        return false;
    }
};

