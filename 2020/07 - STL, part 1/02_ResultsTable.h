#include <vector>
#include <algorithm>

using namespace std;
#pragma once
class ResultsTable
{
protected:
    vector<unsigned int> points;
public:
    // Зарегистрировать новый результат, 
    // нас волнуют только баллы, имена пользователей не важны
    void addResult(unsigned int score) {
        points.push_back(score);
    }

    // Получить минимальный балл из всех результатов за всё время
    unsigned int getMinScore() const {
        vector<unsigned int> support = points;
        sort(support.begin(), support.end());
        return *support.begin();
    }

    // Получить, сколько баллов у игрока на заданном месте.
    // Внимание: места нумеруются так, как это принято на турнирах, то есть 
    // лучший результат - 1-ое место, за ним 2-ое место и т.д.
    unsigned int getScoreForPosition(unsigned int positionNumber) const {
        vector<unsigned int> support = points;
        sort(support.begin(), support.end());
        reverse(support.begin(), support.end());
        return support[positionNumber - 1];
    }
};

