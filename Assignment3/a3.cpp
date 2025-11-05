#include<bits/stdc++.h>
using namespace std;

int euclideanGCD(int a, int b) 
{
    if(a > b)
        swap(a, b);

    if (a == 0)
        return b;
    
    return euclideanGCD(b % a, a);
}

// Bezout's identity --> ax + by = gcd(a, b)
int extendedEuclidean(int a, int b, int &x, int &y) 
{
    if (b == 0) 
    {
        x = 1;
        y = 0;
        return a;
    }

    int x1, y1;
    int gcd = extendedEuclidean(b, a % b, x1, y1);
    x = y1;
    y = x1 - (a / b) * y1;

    return gcd;
}



int modInverse(int a, int m) 
{
    int x, y;
    int g = extendedEuclidean(a, m, x, y);

    if (g != 1)
        return -1; 
    else
        return (x + m) % m;
}

int main() 
{
    int a, b;
    cout << "Enter two integers: ";
    cin >> a >> b;

    int gcd = euclideanGCD(a, b);
    cout << "GCD (Euclidean Algorithm): " << gcd << endl;

    int x, y;
    int gcd_ext = extendedEuclidean(a, b, x, y);

    cout << "GCD (Extended Euclidean Algorithm): " << gcd_ext << endl;
    cout << "Coefficients x and y (Bezout's identity): x = " << x << ", y = " << y << endl;

    cout << "Verification: " << a << "*" << x << " + " << b << "*" << y << " = " << (a*x + b*y) << endl;

    if (gcd_ext == 1) 
    {
        int inv = modInverse(a, b);
        cout << "Modular inverse of " << a << " mod " << b << " is: " << inv << endl;
    } else {
        cout << "Modular inverse does not exist since GCD != 1." << endl;
    }

    return 0;
}