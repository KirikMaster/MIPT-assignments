#include <string>
#include <map>
#include <vector>
#include <algorithm>

using ull = unsigned long long;
using namespace std;
class Tracker
{
protected:
    multimap<string, ull> activity;
public:
    // ��� ����� �������� ������������ ���������� ���� �����.
    // ������ ���������:
    // - ����� ������������ �������� �������� (username);
    // - ����� (timestamp - ��� �������� �������� ������� �� ������ �����).
    // ��������: �� �������������, ��� timestamp ����������� ������ ��
    // �����������, � ��� ����� ���� ����� ������.
    void click(const string& username, ull timestamp) {
        pair<string, ull> p(username, timestamp);
        activity.insert(p);
    }

    // �� ����� ������������ ����� �������, ������� ����� ���� ������
    ull getClickCount(const string& username) const {
        return activity.count(username);
    }

    // ����� ��� ������ ����
    ull getFirstClick(const string& username) const {
        if ((getClickCount(username)) > 0) {
            pair <
                multimap<string, ull>::const_iterator,
                multimap<string, ull>::const_iterator
            > range = activity.equal_range(username);
            multimap<string, ull>::const_iterator it;
            vector<ull> v;
            for (it = range.first; it != range.second; ++it) v.push_back(it->second);
            sort(v.begin(), v.end());
            return *v.begin();
        }
        else return 0;
    }

    // ����� ��� ��������� ����
    ull getLastClick(const string& username) const {
        if ((getClickCount(username)) > 0) {
            pair <
                multimap<string, ull>::const_iterator,
                multimap<string, ull>::const_iterator
            > range = activity.equal_range(username);
            multimap<string, ull>::const_iterator it;
            vector<ull> v;
            for (it = range.first; it != range.second; ++it) v.push_back(it->second);
            sort(v.begin(), v.end());
            return *(v.end() - 1);
        }
        else return 0;
    }
};

