#include <string>
#include <map>
#include <climits>

using namespace std;
class TelemetryController
{
protected:
    struct data
    {
        unsigned int num = 0;
        long min = LONG_MAX;
        long max = LONG_MIN;
    };
    map<string, data> received;
public:
    // �������� � ���������� �������. ����������� ����������:
    // - device - ������������� ����������, � �������� ������ ��������;
    // - value - ���������� �������� ��������� ��������, ���������� �����������.
    void handleEvent(const string& device, long value) {
        received[device].num++;
        if (value > received[device].max) received[device].max = value;
        if (value < received[device].min) received[device].min = value;
    }

    // �� �������������� ���������� ����������, 
    // ������� ����� �������� �� ���� ������ �� �� �����
    unsigned int getEventsCount(const string& device) const {
        map<string, data>::const_iterator it;
        for (it = received.begin(); it != received.end(); ++it) {
            if (it->first == device) return it->second.num;
        }
        return 0;
    }

    // �� �������������� ���������� ���������� 
    // ����������� �������� �� �� �����, ��������� �� ������� ����������
    long getMinValue(const string& device) const {
        map<string, data>::const_iterator it;
        for (it = received.begin(); it != received.end(); ++it) {
            if (it->first == device) return it->second.min;
        }
        return 0;
    }

    // �� �������������� ���������� ���������� 
    // ������������ �������� �� �� �����, ��������� �� ������� ����������
    long getMaxValue(const string& device) const {
        map<string, data>::const_iterator it;
        for (it = received.begin(); it != received.end(); ++it) {
            if (it->first == device) return it->second.max;
        }
        return 0;
    }
};

