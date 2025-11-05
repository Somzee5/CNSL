import java.util.Scanner;

public class ExtendedEuclidean {

    // Euclidean Algorithm for GCD
    public static int euclideanGCD(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    // Extended Euclidean Algorithm
    // returns array: {gcd, x, y}
    public static int[] extendedEuclidean(int a, int b) {
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

        // returns {gcd, x, y}
        return new int[]{old_r, old_s, old_t};
    }

    // Modular Inverse using Extended Euclidean Algorithm
    public static Integer modularInverse(int a, int m) {
        int[] result = extendedEuclidean(a, m);
        int gcd = result[0];
        int x = result[1];

        if (gcd != 1) {
            return null; // Inverse does not exist
        } else {
            return (x % m + m) % m; // Ensure positive result
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter first integer (a): ");
        int a = sc.nextInt();

        System.out.print("Enter second integer (b): ");
        int b = sc.nextInt();

        // GCD using Euclidean Algorithm
        int gcdValue = euclideanGCD(a, b);
        System.out.println("GCD of " + a + " and " + b + " (Euclidean Algorithm) = " + gcdValue);

        // Extended Euclidean Algorithm
        int[] result = extendedEuclidean(a, b);
        int gcd_ext = result[0], x = result[1], y = result[2];

        System.out.println("Using Extended Euclidean Algorithm:");
        System.out.println("GCD = " + gcd_ext + ", x = " + x + ", y = " + y);
        System.out.println("Verification: " + a + "*(" + x + ") + " + b + "*(" + y + ") = " + (a * x + b * y));

        // Modular Inverse
        if (gcd_ext == 1) {
            Integer inverse = modularInverse(a, b);
            System.out.println("Modular Inverse of " + a + " mod " + b + " = " + inverse);
        } else {
            System.out.println("Modular Inverse does not exist since GCD != 1");
        }

        sc.close();
    }
}
