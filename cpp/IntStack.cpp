// ============================================================
//  整數堆疊（Stack）主控台應用程式
//
//  什麼是堆疊？
//    想像一疊盤子：新盤子只能放在「最上面」，要拿也只能拿「最上面」那個。
//    這種「後進先出」（LIFO, Last In First Out）的容器就叫堆疊。
//
//  本程式用「固定大小的陣列 + 一個 top 索引」來實作，
//  讓你看清楚堆疊內部到底發生了什麼事。
//
//  編譯：g++ -std=c++17 -o IntStack IntStack.cpp
//  執行：./IntStack        （Windows 為 IntStack.exe）
// ============================================================

#include <iostream>
#include <limits>

#ifdef _WIN32
#include <windows.h>   // 讓 Windows 主控台能正確顯示中文（UTF-8）
#endif

// ------------------------------------------------------------
//  IntStack：只能放整數的堆疊
// ------------------------------------------------------------
class IntStack {
private:
    static const int CAPACITY = 10;   // 堆疊最多能放幾個元素（可自行調整）
    int data[CAPACITY];               // 真正存資料的陣列
    int top;                          // 「頂端」在陣列的哪個位置；-1 代表空的

public:
    // 建構子：一開始堆疊是空的，所以 top 設為 -1
    IntStack() : top(-1) {}

    // 是否為空？ top 是 -1 就代表一個元素都沒有
    bool isEmpty() const { return top == -1; }

    // 是否已滿？ top 指到最後一格就代表放不下了
    bool isFull() const { return top == CAPACITY - 1; }

    // 目前有幾個元素
    int size() const { return top + 1; }

    // push（推入）：把一個整數放到頂端
    //   步驟：1. 先確認還有空位  2. top 往上移一格  3. 把值放進去
    bool push(int value) {
        if (isFull()) {
            std::cout << "堆疊已滿（容量 " << CAPACITY << "），無法推入 " << value << "。\n";
            return false;
        }
        ++top;               // 頂端往上移
        data[top] = value;   // 把值放在新的頂端
        std::cout << "已推入: " << value << "（目前大小 " << size() << "）\n";
        return true;
    }

    // pop（彈出）：把頂端的整數拿掉
    //   步驟：1. 先確認不是空的  2. 記下頂端的值  3. top 往下移一格
    //   注意：陣列裡的舊值其實還在，但 top 已經不指向它，就等於「刪掉」了
    bool pop(int& outValue) {
        if (isEmpty()) {
            return false;
        }
        outValue = data[top];   // 記下要拿走的值
        --top;                  // 頂端往下移，等於把它移除
        return true;
    }

    // peek（偷看）：只看頂端的值，不拿走
    bool peek(int& outValue) const {
        if (isEmpty()) {
            return false;
        }
        outValue = data[top];
        return true;
    }

    // 從頂端到底端印出所有元素，並標示 top 的位置
    void display() const {
        if (isEmpty()) {
            std::cout << "堆疊目前是空的。\n";
            return;
        }
        std::cout << "堆疊內容（上面是頂端）：\n";
        for (int i = top; i >= 0; --i) {
            std::cout << "  [" << i << "] " << data[i];
            if (i == top) std::cout << "   <- top";
            std::cout << "\n";
        }
        std::cout << "  ---- 底端 ----\n";
    }

    // 清空堆疊：只要把 top 設回 -1 就好，不必真的去清陣列
    void clear() { top = -1; }
};

// ------------------------------------------------------------
//  以下是「操作介面」的部分：印選單、讀輸入
// ------------------------------------------------------------

void printMenu() {
    std::cout << "\n===== 整數堆疊選單 =====\n"
              << "1. Push（推入一個整數）\n"
              << "2. Pop（彈出頂端）\n"
              << "3. Peek（查看頂端）\n"
              << "4. 顯示全部內容\n"
              << "5. 是否為空 / 是否已滿\n"
              << "6. 目前大小\n"
              << "7. 清空堆疊\n"
              << "0. 結束程式\n"
              << "請選擇: ";
}

// 讀一個整數；讀失敗（例如輸入英文字母）就清掉錯誤狀態並回傳 false
bool readInt(int& value) {
    if (std::cin >> value) {
        return true;
    }
    if (std::cin.eof()) {          // 輸入已經結束（例如 Ctrl+Z / Ctrl+D）
        return false;
    }
    std::cin.clear();              // 清掉錯誤旗標
    std::cin.ignore((std::numeric_limits<std::streamsize>::max)(), '\n');  // 丟掉這一整行
    return false;
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);   // 讓中文在 Windows 主控台正常顯示
#endif

    IntStack stack;
    int choice;

    while (true) {
        printMenu();

        if (!readInt(choice)) {
            if (std::cin.eof()) {
                std::cout << "\n輸入結束，程式離開。\n";
                break;
            }
            std::cout << "輸入無效，請輸入選單上的數字。\n";
            continue;
        }

        if (choice == 0) {
            std::cout << "程式結束，再見！\n";
            break;
        }

        switch (choice) {
            case 1: {
                std::cout << "請輸入要推入的整數: ";
                int value;
                if (readInt(value)) {
                    stack.push(value);
                } else {
                    std::cout << "輸入無效，請輸入整數。\n";
                }
                break;
            }
            case 2: {
                int value;
                if (stack.pop(value)) {
                    std::cout << "已彈出: " << value << "（目前大小 " << stack.size() << "）\n";
                } else {
                    std::cout << "堆疊是空的，沒有東西可以彈出。\n";
                }
                break;
            }
            case 3: {
                int value;
                if (stack.peek(value)) {
                    std::cout << "頂端元素: " << value << "\n";
                } else {
                    std::cout << "堆疊是空的，沒有頂端元素。\n";
                }
                break;
            }
            case 4:
                stack.display();
                break;
            case 5:
                std::cout << (stack.isEmpty() ? "堆疊是空的。" : "堆疊不是空的。") << " "
                          << (stack.isFull()  ? "堆疊已滿。"   : "堆疊還有空位。") << "\n";
                break;
            case 6:
                std::cout << "目前大小: " << stack.size() << "\n";
                break;
            case 7:
                stack.clear();
                std::cout << "堆疊已清空。\n";
                break;
            default:
                std::cout << "沒有這個選項，請重新輸入。\n";
                break;
        }
    }

    return 0;
}
