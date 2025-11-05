#include <bits/stdc++.h>
using namespace std;

// ---------- a. Caesar Cipher ----------
string caesarEncrypt(const string &plaintext, int shift) 
{
    string ciphertext;

    for (char ch : plaintext) 
    {
        if (isalpha(ch)) 
        { 
            char offset = isupper(ch) ? 'A' : 'a';
            ciphertext += char((ch - offset + shift + 26) % 26 + offset);
        } 
        else 
        {
            ciphertext += ch;
        }
    }

    return ciphertext;
}

string caesarDecrypt(const string &ciphertext, int shift) 
{
    return caesarEncrypt(ciphertext, -shift);
}

// ---------- b. Playfair Cipher ----------
string playfairPrepareText(string text) {
    for (char &c : text) {
        c = toupper(c);
        if (c == 'J') c = 'I';
    }
    string prepared;
    for (int i = 0; i < (int)text.size();) {
        char char1 = text[i];
        if (!isalpha(char1)) { i++; continue; }
        if (i + 1 < (int)text.size()) {
            char char2 = text[i + 1];
            if (!isalpha(char2)) { prepared += char1; i++; continue; }
            if (char1 == char2) {
                prepared += char1;
                prepared += 'X';
                i++;
            } else {
                prepared += char1;
                prepared += char2;
                i += 2;
            }
        } else {
            prepared += char1;
            prepared += 'X';
            i++;
        }
    }
    return prepared;
}

vector<vector<char>> playfairGenerateKeyMatrix(string key) {
    for (char &c : key) {
        c = toupper(c);
        if (c == 'J') c = 'I';
    }
    vector<char> matrix;
    set<char> used;
    for (char c : key) {
        if (isalpha(c) && !used.count(c)) {
            matrix.push_back(c);
            used.insert(c);
        }
    }
    for (char c = 'A'; c <= 'Z'; c++) {
        if (c == 'J') continue;
        if (!used.count(c)) {
            matrix.push_back(c);
            used.insert(c);
        }
    }
    vector<vector<char>> mat(5, vector<char>(5));
    for (int i = 0; i < 25; i++) {
        mat[i / 5][i % 5] = matrix[i];
    }
    return mat;
}

pair<int, int> playfairFindPos(const vector<vector<char>> &matrix, char ch) {
    for (int r = 0; r < 5; r++) {
        for (int c = 0; c < 5; c++) {
            if (matrix[r][c] == ch)
                return make_pair(r, c);
        }
    }
    return make_pair(-1, -1);
}

string playfairEncrypt(string plaintext, string key) {
    auto matrix = playfairGenerateKeyMatrix(key);
    string prepared = playfairPrepareText(plaintext);
    string ciphertext;
    for (int i = 0; i < (int)prepared.size(); i += 2) {
        char a = prepared[i], b = prepared[i + 1];
        auto pos1 = playfairFindPos(matrix, a);
        auto pos2 = playfairFindPos(matrix, b);
        int r1 = pos1.first, c1 = pos1.second;
        int r2 = pos2.first, c2 = pos2.second;
        if (r1 == r2) {
            ciphertext += matrix[r1][(c1 + 1) % 5];
            ciphertext += matrix[r2][(c2 + 1) % 5];
        } else if (c1 == c2) {
            ciphertext += matrix[(r1 + 1) % 5][c1];
            ciphertext += matrix[(r2 + 1) % 5][c2];
        } else {
            ciphertext += matrix[r1][c2];
            ciphertext += matrix[r2][c1];
        }
    }
    return ciphertext;
}

string playfairDecrypt(string ciphertext, string key) {
    auto matrix = playfairGenerateKeyMatrix(key);
    string plaintext;
    for (int i = 0; i < (int)ciphertext.size(); i += 2) {
        char a = ciphertext[i], b = ciphertext[i + 1];
        auto pos1 = playfairFindPos(matrix, a);
        auto pos2 = playfairFindPos(matrix, b);
        int r1 = pos1.first, c1 = pos1.second;
        int r2 = pos2.first, c2 = pos2.second;
        if (r1 == r2) {
            plaintext += matrix[r1][(c1 - 1 + 5) % 5];
            plaintext += matrix[r2][(c2 - 1 + 5) % 5];
        } else if (c1 == c2) {
            plaintext += matrix[(r1 - 1 + 5) % 5][c1];
            plaintext += matrix[(r2 - 1 + 5) % 5][c2];
        } else {
            plaintext += matrix[r1][c2];
            plaintext += matrix[r2][c1];
        }
    }
    return plaintext;
}

// ---------- c. Hill Cipher ----------
int modInverse(int a, int m) {
    a %= m;
    for (int x = 1; x < m; x++)
        if ((a * x) % m == 1) return x;
    return -1;
}

vector<vector<int>> matrixModInverse(vector<vector<int>> m, int mod) {
    int n = m.size();
    int det = round(m[0][0] * m[1][1] - m[0][1] * m[1][0]); // 2x2 case
    det = (det % mod + mod) % mod;
    int detInv = modInverse(det, mod);
    if (detInv == -1) throw runtime_error("Matrix not invertible");

    vector<vector<int>> inv(n, vector<int>(n));
    inv[0][0] = m[1][1];
    inv[1][1] = m[0][0];
    inv[0][1] = -m[0][1];
    inv[1][0] = -m[1][0];
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            inv[i][j] = ((inv[i][j] % mod + mod) % mod * detInv) % mod;
    return inv;
}

string hillEncrypt(string plaintext, vector<vector<int>> key) {
    int n = key.size();
    for (char &c : plaintext) c = toupper(c);
    plaintext.erase(remove(plaintext.begin(), plaintext.end(), ' '), plaintext.end());

    while (plaintext.size() % n != 0) 
        plaintext += 'X';

    string ciphertext;

    for (int i = 0; i < (int)plaintext.size(); i += n) {
        vector<int> vec(n);

        for (int j = 0; j < n; j++) 
            vec[j] = plaintext[i + j] - 'A';

        vector<int> res(n, 0);

        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
                res[r] += key[r][c] * vec[c];

        for (int r = 0; r < n; r++)
            ciphertext += char((res[r] % 26 + 26) % 26 + 'A');
    }
    return ciphertext;
}

string hillDecrypt(string ciphertext, vector<vector<int>> key) {
    int n = key.size();
    auto invKey = matrixModInverse(key, 26);
    string plaintext;
    for (int i = 0; i < (int)ciphertext.size(); i += n) {
        vector<int> vec(n);
        for (int j = 0; j < n; j++) vec[j] = ciphertext[i + j] - 'A';
        vector<int> res(n, 0);
        for (int r = 0; r < n; r++)
            for (int c = 0; c < n; c++)
                res[r] += invKey[r][c] * vec[c];
        for (int r = 0; r < n; r++)
            plaintext += char((res[r] % 26 + 26) % 26 + 'A');
    }
    return plaintext;
}

// ---------- d. Vigenere Cipher ----------
string vigenereEncrypt(const string &plaintext, string key) {
    for (char &c : key) c = toupper(c);
    string ciphertext;
    int keyLen = key.size();
    for (int i = 0; i < (int)plaintext.size(); i++) {
        char ch = plaintext[i];
        if (isalpha(ch)) {
            char offset = isupper(ch) ? 'A' : 'a';
            int keyVal = key[i % keyLen] - 'A';
            ciphertext += char((ch - offset + keyVal) % 26 + offset);
        } else {
            ciphertext += ch;
        }
    }
    return ciphertext;
}

string vigenereDecrypt(const string &ciphertext, string key) {
    for (char &c : key) c = toupper(c);
    string plaintext;
    int keyLen = key.size();
    for (int i = 0; i < (int)ciphertext.size(); i++) {
        char ch = ciphertext[i];
        if (isalpha(ch)) {
            char offset = isupper(ch) ? 'A' : 'a';
            int keyVal = key[i % keyLen] - 'A';
            plaintext += char((ch - offset - keyVal + 26) % 26 + offset);
        } else {
            plaintext += ch;
        }
    }
    return plaintext;
}

// ---------- Wrapper Functions ----------
void caesarCipher() {
    string text;
    int shift, choice;
    cout << "\n1. Encrypt\n2. Decrypt\nChoice: ";
    cin >> choice;
    cin.ignore();
    cout << "Enter text: ";
    getline(cin, text);
    cout << "Enter shift: ";
    cin >> shift;
    if (choice == 1)
        cout << "Ciphertext: " << caesarEncrypt(text, shift) << endl;
    else
        cout << "Plaintext: " << caesarDecrypt(text, shift) << endl;
}

void playfairCipher() {
    string text, key;
    int choice;
    cout << "\n1. Encrypt\n2. Decrypt\nChoice: ";
    cin >> choice;
    cin.ignore();
    cout << "Enter text: ";
    getline(cin, text);
    cout << "Enter key: ";
    getline(cin, key);
    if (choice == 1)
        cout << "Ciphertext: " << playfairEncrypt(text, key) << endl;
    else
        cout << "Plaintext: " << playfairDecrypt(text, key) << endl;
}

void hillCipher() {
    string text;
    int choice;
    cout << "\n1. Encrypt\n2. Decrypt\nChoice: ";
    cin >> choice;
    cin.ignore();
    cout << "Enter text (A-Z only): ";
    getline(cin, text);
    vector<vector<int>> key = {{3, 3}, {2, 5}}; // Example 2x2 key
    if (choice == 1)
        cout << "Ciphertext: " << hillEncrypt(text, key) << endl;
    else
        cout << "Plaintext: " << hillDecrypt(text, key) << endl;
}

void vigenereCipher() {
    string text, key;
    int choice;
    cout << "\n1. Encrypt\n2. Decrypt\nChoice: ";
    cin >> choice;
    cin.ignore();
    cout << "Enter text: ";
    getline(cin, text);
    cout << "Enter key: ";
    getline(cin, key);
    if (choice == 1)
        cout << "Ciphertext: " << vigenereEncrypt(text, key) << endl;
    else
        cout << "Plaintext: " << vigenereDecrypt(text, key) << endl;
}

// ---------- Main ----------
int main() {
    int choice;
    while (true) {
        cout << "\n=== Classical Substitution Ciphers ===\n";
        cout << "1. Caesar Cipher\n";
        cout << "2. Playfair Cipher\n";
        cout << "3. Hill Cipher\n";
        cout << "4. Vigenere Cipher\n";
        cout << "5. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1: caesarCipher(); break;
            case 2: playfairCipher(); break;
            case 3: hillCipher(); break;
            case 4: vigenereCipher(); break;
            case 5: cout << "Exiting program...\n"; return 0;
            default: cout << "Invalid choice! Try again.\n";
        }
    }
}
