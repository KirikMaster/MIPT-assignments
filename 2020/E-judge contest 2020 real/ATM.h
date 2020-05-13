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
    // Конструктор, создаёт пустой банкомат
    ATM() {
        curs[0] = first_cur;
        curs[1] = second_cur;
        curs[2] = third_cur;
    }

    // Деструктор, если нужен

    // Вносит в устройство набор купюр
    // - в векторе notes перечислены достоинства вносимых купюр (разумеется, возможны повторы)
    // - в поле currency указан код валюты
    void deposit(const std::vector<ui>& notes, unsigned short int currency) {
        for (auto note : notes) {
            curs[currency][note]++;
        }
    }

    // Снять сумму amount в валюте currency, выдав её максимально крупными купюрами
    // - если операция прошла успешно, учесть выданные купюры в банкомате и вернуть их в возвращаемом vector-е
    // - если целиком запрошенную сумму выдать невозможно, не выдавать ничего и вернуть пустой vector
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

    // Снять сумму amount в валюте currency, выдав её максимально мелкими купюрами
    // - если операция прошла успешно, учесть выданные купюры в банкомате и вернуть их в возвращаемом vector-е
    // - если целиком запрошенную сумму выдать невозможно, не выдавать ничего и вернуть пустой vector
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

    // Вернуть максимальную сумму, доступную в валюте currency
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