#include <iostream>
using namespace std;

int euclideanGCD(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int extendedEuclidean(int a, int b, int &x, int &y) {
    int old_r = a, r = b;
    int old_s = 1, s = 0;
    int old_t = 0, t = 1;

    while (r != 0) {
        int quotient = old_r / r;

        int temp = r;
        r = old_r - quotient * r;
        old_r = temp;

        temp = s;
        s = old_s - quotient * s;
        old_s = temp;

        temp = t;
        t = old_t - quotient * t;
        old_t = temp;
    }

    x = old_s;
    y = old_t;
    return old_r; // GCD
}

int modularInverse(int a, int m) {
    int x, y;
    int gcd = extendedEuclidean(a, m, x, y);
    if (gcd != 1) {
        return -1;
    } else {
        return (x % m + m) % m;
    }
}

int main() {
    int a, b;
    cout << "Enter first integer (a): ";
    cin >> a;
    cout << "Enter second integer (b): ";
    cin >> b;

    int gcd_value = euclideanGCD(a, b);
    cout << "GCD of " << a << " and " << b << " (Euclidean Algorithm) = " << gcd_value << endl;

    int x, y;
    int gcd_ext = extendedEuclidean(a, b, x, y);
    cout << "Using Extended Euclidean Algorithm:" << endl;
    cout << "GCD = " << gcd_ext << ", x = " << x << ", y = " << y << endl;
    cout << "Verification: " << a << "*(" << x << ") + " << b << "*(" << y << ") = " << (a * x + b * y) << endl;

    if (gcd_ext == 1) {
        int inverse = modularInverse(a, b);
        cout << "Modular Inverse of " << a << " mod " << b << " = " << inverse << endl;
    } else {
        cout << "Modular Inverse does not exist since GCD != 1" << endl;
    }

    return 0;
}
