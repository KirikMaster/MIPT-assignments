#include <string>
#include <set>

using namespace std;
class SessionManager
{
protected:
    set<string> users;
public:
    // ¬ход пользовател€.
    // ќдин пользователь может войти несколько раз подр€д, 
    // считать его при этом нужно один раз.
    void login(const string& username) {
        users.insert(username);
    }

    // ¬ыход пользовател€.
    // ѕользователь может выйти несколько раз подр€д, 
    // падать при этом не нужно.
    void logout(const string& username) {
        if (users.find(username) != users.end()) {
            users.erase(username);
        }
    }

    // —колько сейчас пользователей залогинено.
    int getNumberOfActiveUsers() const {
        return users.size();
    }
};

