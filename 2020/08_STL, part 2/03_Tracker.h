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
    // ѕри любом действии пользовател€ вызываетс€ этот метод.
    // ћетоду передаЄтс€:
    // - какой пользователь совершил действие (username);
    // - когда (timestamp - дл€ простоты условные секунды от начала времЄн).
    // ¬нимание: не гарантируетс€, что timestamp расположены строго по
    // возрастанию, в них может быть любой бардак.
    void click(const string& username, ull timestamp) {
        pair<string, ull> p(username, timestamp);
        activity.insert(p);
    }

    // ѕо имени пользовател€ нужно вернуть, сколько всего было кликов
    ull getClickCount(const string& username) const {
        return activity.count(username);
    }

    //  огда был первый клик
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

    //  огда был последний клик
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

