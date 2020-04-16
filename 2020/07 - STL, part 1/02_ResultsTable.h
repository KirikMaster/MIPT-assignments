#include <vector>
#include <algorithm>

using namespace std;
#pragma once
class ResultsTable
{
protected:
    vector<unsigned int> points;
public:
    // ���������������� ����� ���������, 
    // ��� ������� ������ �����, ����� ������������� �� �����
    void addResult(unsigned int score) {
        points.push_back(score);
    }

    // �������� ����������� ���� �� ���� ����������� �� �� �����
    unsigned int getMinScore() const {
        vector<unsigned int> support = points;
        sort(support.begin(), support.end());
        return *support.begin();
    }

    // ��������, ������� ������ � ������ �� �������� �����.
    // ��������: ����� ���������� ���, ��� ��� ������� �� ��������, �� ���� 
    // ������ ��������� - 1-�� �����, �� ��� 2-�� ����� � �.�.
    unsigned int getScoreForPosition(unsigned int positionNumber) const {
        vector<unsigned int> support = points;
        sort(support.begin(), support.end());
        reverse(support.begin(), support.end());
        return support[positionNumber - 1];
    }
};

