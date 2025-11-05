#include <bits/stdc++.h>
using namespace std;

string railFenceEncrypt(string text, int key) {
    vector<vector<char>> rail(key, vector<char>(text.length(), '\n'));
    bool dir_down = false;
    int row = 0, col = 0;

    for (char ch : text) {
        if (row == 0 || row == key - 1)
            dir_down = !dir_down;

        rail[row][col++] = ch;

        row += dir_down ? 1 : -1;
    }

    string result;
    for (int i = 0; i < key; i++) {
        for (int j = 0; j < (int)text.length(); j++) {
            if (rail[i][j] != '\n')
                result.push_back(rail[i][j]);
        }
    }
    return result;
}

string railFenceDecrypt(string cipher, int key) {
    vector<vector<char>> rail(key, vector<char>(cipher.length(), '\n'));

    bool dir_down = false;
    int row = 0, col = 0;

    for (int i = 0; i < (int)cipher.length(); i++) {
        if (row == 0) dir_down = true;
        if (row == key - 1) dir_down = false;

        rail[row][col++] = '*';
        row += dir_down ? 1 : -1;
    }

    int index = 0;
    for (int i = 0; i < key; i++) {
        for (int j = 0; j < (int)cipher.length(); j++) {
            if (rail[i][j] == '*' && index < (int)cipher.length())
                rail[i][j] = cipher[index++];
        }
    }

    string result;
    row = 0; col = 0;
    for (int i = 0; i < (int)cipher.length(); i++) {
        if (row == 0) dir_down = true;
        if (row == key - 1) dir_down = false;

        if (rail[row][col] != '*')
            result.push_back(rail[row][col++]);

        row += dir_down ? 1 : -1;
    }

    return result;
}

int main() 
{
    string text = "SOHAM_PATIL";
    int key = 3;

    string encrypted = railFenceEncrypt(text, key);
    cout << "Encrypted: " << encrypted << endl;

    string decrypted = railFenceDecrypt(encrypted, key);
    cout << "Decrypted: " << decrypted << endl;

    return 0;
}
