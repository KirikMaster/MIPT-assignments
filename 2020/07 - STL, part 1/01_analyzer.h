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
    // Создать анализатор для системы с numCores ядер
    Analyzer(unsigned int numCores) : numCores(numCores) {}

    // Проанализировать текущие задачи
    void analyze(const vector<Task>& tasks) {
        Cores.clear();
        for (unsigned int i = 0; i < numCores; i++) {
            Cores.push_back(0);
        }
        for (auto c : tasks) {
            Cores[c.getCPU()] += c.getSize();
        }
    }

    // Сообщить общую нагрузку на заданное ядро
    int getLoadForCPU(unsigned int cpuNum) {
        return Cores[cpuNum];
    }
};
