#include <string>
#include <set>

using namespace std;
class SessionManager
{
protected:
    set<string> users;
public:
    // ���� ������������.
    // ���� ������������ ����� ����� ��������� ��� ������, 
    // ������� ��� ��� ���� ����� ���� ���.
    void login(const string& username) {
        users.insert(username);
    }

    // ����� ������������.
    // ������������ ����� ����� ��������� ��� ������, 
    // ������ ��� ���� �� �����.
    void logout(const string& username) {
        if (users.find(username) != users.end()) {
            users.erase(username);
        }
    }

    // ������� ������ ������������� ����������.
    int getNumberOfActiveUsers() const {
        return users.size();
    }
};

