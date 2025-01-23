#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include <windows.h>

#pragma warning(suppress : 6387)

CRITICAL_SECTION cs;
std::vector<std::vector<int>> array(5, std::vector<int>(5, 0));

void print_array(int point, int i, int j) {

    EnterCriticalSection(&cs);
    if (point == 1) {
        if (array[i][j] == 2) {
            LeaveCriticalSection(&cs);
            return;
        }
        array[i][j] = 1;
    }

    if (point == 2) {
        if (array[j][i] == 1) {
            LeaveCriticalSection(&cs);
            return;
    }
        array[j][i] = 2;
    }

    for (const auto& row : array) {
        for (int value : row) {
            std::cout << value << ' ';
        }
        std::cout << '\n';
    }
    std::cout << "*********************\n";
    LeaveCriticalSection(&cs);
    return;
    
}


DWORD WINAPI FirstGardener(LPVOID lpParam) {

    for (int i = 0; i < 5; ++i) {
        for (int j = 0; j < 5; ++j) {

            print_array(1, i, j);
            std::this_thread::sleep_for(std::chrono::milliseconds(500));

        }
    }

    ExitThread(0);

}

DWORD WINAPI SecondGardener(LPVOID lpParam) {

    for (int i = 4; i > -1; --i) {
        for (int j = 4; j > -1; --j) {

            print_array(2, i, j);
            std::this_thread::sleep_for(std::chrono::milliseconds(500));

        }
    }

    ExitThread(0);

}

int main() {

    InitializeCriticalSection(&cs);

    HANDLE gardener1, gardener2;
    
    gardener1 = CreateThread(NULL, 0, FirstGardener, NULL, 0, NULL);
    gardener2 = CreateThread(NULL, 0, SecondGardener, NULL, 0, NULL);

    WaitForSingleObject(gardener1, INFINITE);
    WaitForSingleObject(gardener2, INFINITE);

    DeleteCriticalSection(&cs);

    CloseHandle(gardener1);
    CloseHandle(gardener2);

    return  0;
}
