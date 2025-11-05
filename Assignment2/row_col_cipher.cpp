#include <bits/stdc++.h>
using namespace std;

vector<int> createOrder(const string &key) {
    string sortedKey = key;
    sort(sortedKey.begin(), sortedKey.end());
    vector<int> order;

    for (char k : key) {
        order.push_back(find(sortedKey.begin(), sortedKey.end(), k) - sortedKey.begin() + 1);
    }
    return order;
}

string rowColumnEncrypt(string plaintext, const string &key) {
    int key_len = key.length();
    vector<int> order = createOrder(key);

    plaintext.erase(remove(plaintext.begin(), plaintext.end(), ' '), plaintext.end());

    int rows = plaintext.length() / key_len + (plaintext.length() % key_len != 0);

    vector<vector<char>> matrix(rows, vector<char>(key_len, 'X'));

    int index = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < key_len; c++) {
            if (index < plaintext.length()) {
                matrix[r][c] = plaintext[index++];
            }
        }
    }

    string ciphertext;
    for (int num = 1; num <= key_len; num++) {
        int col = find(order.begin(), order.end(), num) - order.begin();
        for (int r = 0; r < rows; r++) {
            ciphertext.push_back(matrix[r][col]);
        }
    }

    return ciphertext;
}

string rowColumnDecrypt(string ciphertext, const string &key) {
    int key_len = key.length();
    vector<int> order = createOrder(key);

    int rows = ciphertext.length() / key_len;
    vector<vector<char>> matrix(rows, vector<char>(key_len, '\0'));

    int index = 0;
    for (int num = 1; num <= key_len; num++) {
        int col = find(order.begin(), order.end(), num) - order.begin();
        for (int r = 0; r < rows; r++) {
            matrix[r][col] = ciphertext[index++];
        }
    }

    string plaintext;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < key_len; c++) {
            plaintext.push_back(matrix[r][c]);
        }
    }

    while (!plaintext.empty() && plaintext.back() == 'X')
        plaintext.pop_back();

    return plaintext;
}

int main() {
    string key = "SOHAM";
    string plaintext = "WE ARE FROM WALCHAND COLLEGE OF ENGINEERING";

    string encrypted = rowColumnEncrypt(plaintext, key);
    cout << "Encrypted: " << encrypted << endl;

    string decrypted = rowColumnDecrypt(encrypted, key);
    cout << "Decrypted: " << decrypted << endl;

    return 0;
}