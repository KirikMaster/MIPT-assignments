#include <vector>

using namespace std;
#pragma once

class Analyzer
{
protected:
    unsigned int numCores;
    vector<unsigned int> Cores;
    const vector<Task>* tasks;
public:
    // ������� ���������� ��� ������� � numCores ����
    Analyzer(unsigned int numCores) : numCores(numCores) {}

    // ���������������� ������� ������
    void analyze(const vector<Task>& tasks) {
        Cores.clear();
        for (unsigned int i = 0; i < numCores; i++) {
            Cores.push_back(0);
        }
        for (auto c : tasks) {
            Cores[c.getCPU()] += c.getSize();
        }
    }

    // �������� ����� �������� �� �������� ����
    int getLoadForCPU(unsigned int cpuNum) {
        return Cores[cpuNum];
    }
};
