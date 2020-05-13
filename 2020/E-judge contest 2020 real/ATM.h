#include <vector>
#include <map>

using usi = unsigned short int;
using ui = unsigned int;
using namespace std;
class ATM
{
protected:
    map<ui, map<ui, ui>> curs;
    map<ui, ui> first_cur;
    map<ui, ui> second_cur;
    map<ui, ui> third_cur;
public:
    // �����������, ������ ������ ��������
    ATM() {
        curs[0] = first_cur;
        curs[1] = second_cur;
        curs[2] = third_cur;
    }

    // ����������, ���� �����

    // ������ � ���������� ����� �����
    // - � ������� notes ����������� ����������� �������� ����� (����������, �������� �������)
    // - � ���� currency ������ ��� ������
    void deposit(const std::vector<ui>& notes, unsigned short int currency) {
        for (auto note : notes) {
            curs[currency][note]++;
        }
    }

    // ����� ����� amount � ������ currency, ����� � ����������� �������� ��������
    // - ���� �������� ������ �������, ������ �������� ������ � ��������� � ������� �� � ������������ vector-�
    // - ���� ������� ����������� ����� ������ ����������, �� �������� ������ � ������� ������ vector
    std::vector<ui> withdraw_large(ui amount, unsigned short int currency) {
        vector<ui> withdraw;
        map<ui, ui> now_cur = curs[currency];
        map<ui, ui>::reverse_iterator it;
        for (it = now_cur.rbegin(); it != now_cur.rend(); ++it) {
            if (amount < it->first || it->second == 0) continue;
            else {
                while (it->second != 0 && amount >= it->first) {
                    withdraw.push_back(it->first);
                    amount -= it->first;
                    it->second--;
                }
            }
        }
        if (amount == 0) {
            curs[currency] = now_cur;
            return withdraw;
        }
        else {
            withdraw.clear();
            return withdraw;
        }
    }

    // ����� ����� amount � ������ currency, ����� � ����������� ������� ��������
    // - ���� �������� ������ �������, ������ �������� ������ � ��������� � ������� �� � ������������ vector-�
    // - ���� ������� ����������� ����� ������ ����������, �� �������� ������ � ������� ������ vector
    std::vector<ui> withdraw_small(ui amount, unsigned short int currency) {
        vector<ui> withdraw;
        map<ui, ui> now_cur = curs[currency];
        map<ui, ui>::iterator it;
        for (it = now_cur.begin(); it != now_cur.end(); ++it) {
            if (amount < it->first || it->second == 0) continue;
            else {
                while (it->second != 0 && amount >= it->first) {
                    withdraw.push_back(it->first);
                    amount -= it->first;
                    it->second--;
                }
            }
        }
        if (amount == 0) {
            curs[currency] = now_cur;
            return withdraw;
        }
        else {
            withdraw.clear();
            return withdraw;
        }
    }

    // ������� ������������ �����, ��������� � ������ currency
    ui check_reserve(unsigned short int currency) {
        map<ui, ui> now_cur = curs[currency];
        map<ui, ui>::iterator it;
        ui reserve = 0;
        for (it = now_cur.begin(); it != now_cur.end(); ++it) {
            reserve += it->first * it->second;
        }
        return reserve;
    }
};