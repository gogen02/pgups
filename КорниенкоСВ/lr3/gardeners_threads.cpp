#include <windows.h>
#include <iostream>

constexpr auto P = 5;
// using namespace std;

HANDLE threads[P];
CRITICAL_SECTION cs[P];
CRITICAL_SECTION cs1;

int LEFT(int f)
{
    if (f == 0)
        return P - 1;
    else
        return (f - 1) % P;
}

int RIGHT(int f)
{
    if (f == P - 1)
        return 0;
    else
        return (f + 1) % P;
}

void getForks(int f)
{
    EnterCriticalSection(&cs[LEFT(f)]);
    EnterCriticalSection(&cs[RIGHT(f)]);
}

void putDown(int f)
{
    LeaveCriticalSection(&cs[RIGHT(f)]);
    LeaveCriticalSection(&cs[LEFT(f)]);
}

DWORD WINAPI Start(CONST LPVOID philID)
{
    Sleep(rand() % 2000);
    while (1)
    {
        // Сел
        EnterCriticalSection(&cs1);
        std::cout << "Philosopher " << int(philID) + 1 << " seat.\n";
        LeaveCriticalSection(&cs1);
        Sleep(rand() % 2000);

        // Ждёт пока не освободится вилка
        getForks(int(philID));
        Sleep(rand() % 2000);

        // Ест
        EnterCriticalSection(&cs1);
        std::cout << "Philosopher " << int(philID) + 1 << " eating.\n";
        LeaveCriticalSection(&cs1);
        Sleep(rand() % 3000);

        // Кладёт вилки
        putDown(int(philID));
        Sleep(rand() % 2000);

        // Уходит
        EnterCriticalSection(&cs1);
        std::cout << "Philosopher " << int(philID) + 1 << " walking.\n";
        LeaveCriticalSection(&cs1);
        Sleep(rand() % 5000);
    }
}

int main()
{
    for (int i = 0; i < P; i++)
    {
        InitializeCriticalSection(&cs[i]);
    }

    InitializeCriticalSection(&cs1);

    for (int i = 0; i < P; i++)
    {
        threads[i] = CreateThread(NULL, 0, &Start, (LPVOID)i, 0, NULL);
    }

    getchar();

    ExitProcess(0);
}
