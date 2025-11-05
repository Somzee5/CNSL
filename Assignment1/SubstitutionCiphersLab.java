import java.util.*;

public class SubstitutionCiphersLab {

    // --- Caesar Cipher ---
    public static String caesarEncrypt(String text, int shift) {
        StringBuilder result = new StringBuilder();
        shift = shift % 26;
        for (char c : text.toUpperCase().toCharArray()) {
            if (c >= 'A' && c <= 'Z') {
                char ch = (char) ((c - 'A' + shift) % 26 + 'A');
                result.append(ch);
            } else {
                result.append(c);
            }
        }
        return result.toString();
    }

    public static String caesarDecrypt(String cipher, int shift) {
        return caesarEncrypt(cipher, 26 - (shift % 26));
    }

    // --- Playfair Cipher ---
    static char[][] playfairMatrix = new char[5][5];

    public static void generatePlayfairMatrix(String key) {
        key = key.toUpperCase().replaceAll("[^A-Z]", "").replace("J", "I");
        LinkedHashSet<Character> set = new LinkedHashSet<>();
        for (char c : key.toCharArray()) set.add(c);
        for (char c = 'A'; c <= 'Z'; c++) {
            if (c != 'J') set.add(c);
        }
        Iterator<Character> it = set.iterator();
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (it.hasNext()) playfairMatrix[i][j] = it.next();
            }
        }
    }

    public static String playfairEncrypt(String plaintext, String key) {
        generatePlayfairMatrix(key);
        plaintext = plaintext.toUpperCase().replaceAll("[^A-Z]", "").replace("J", "I");
        StringBuilder sb = new StringBuilder();

        // Prepare digraphs
        List<String> digraphs = new ArrayList<>();
        for (int i = 0; i < plaintext.length(); i += 2) {
            char first = plaintext.charAt(i);
            char second = (i + 1) < plaintext.length() ? plaintext.charAt(i + 1) : 'X';
            if (first == second) second = 'X';
            digraphs.add("" + first + second);
            if (first == second) i--;
        }

        for (String pair : digraphs) {
            int[] pos1 = findPosition(pair.charAt(0));
            int[] pos2 = findPosition(pair.charAt(1));

            if (pos1[0] == pos2[0]) {
                // same row
                sb.append(playfairMatrix[pos1[0]][(pos1[1] + 1) % 5]);
                sb.append(playfairMatrix[pos2[0]][(pos2[1] + 1) % 5]);
            } else if (pos1[1] == pos2[1]) {
                // same column
                sb.append(playfairMatrix[(pos1[0] + 1) % 5][pos1[1]]);
                sb.append(playfairMatrix[(pos2[0] + 1) % 5][pos2[1]]);
            } else {
                // rectangle swap columns
                sb.append(playfairMatrix[pos1[0]][pos2[1]]);
                sb.append(playfairMatrix[pos2[0]][pos1[1]]);
            }
        }
        return sb.toString();
    }

    public static String playfairDecrypt(String cipher, String key) {
        generatePlayfairMatrix(key);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < cipher.length(); i += 2) {
            char first = cipher.charAt(i);
            char second = cipher.charAt(i + 1);
            int[] pos1 = findPosition(first);
            int[] pos2 = findPosition(second);

            if (pos1[0] == pos2[0]) {
                sb.append(playfairMatrix[pos1[0]][(pos1[1] + 4) % 5]);
                sb.append(playfairMatrix[pos2[0]][(pos2[1] + 4) % 5]);
            } else if (pos1[1] == pos2[1]) {
                sb.append(playfairMatrix[(pos1[0] + 4) % 5][pos1[1]]);
                sb.append(playfairMatrix[(pos2[0] + 4) % 5][pos2[1]]);
            } else {
                sb.append(playfairMatrix[pos1[0]][pos2[1]]);
                sb.append(playfairMatrix[pos2[0]][pos1[1]]);
            }
        }
        return sb.toString();
    }

    private static int[] findPosition(char c) {
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                if (playfairMatrix[i][j] == c) return new int[]{i, j};
            }
        }
        return null;
    }

    // --- Hill Cipher (2x2) ---
    private static int mod26(int x) {
        x %= 26;
        return x < 0 ? x + 26 : x;
    }

    public static String hillEncrypt(String plaintext, int[][] key) {
        plaintext = plaintext.toUpperCase().replaceAll("[^A-Z]", "");
        if (plaintext.length() % 2 != 0) plaintext += "X";

        StringBuilder cipher = new StringBuilder();
        for (int i = 0; i < plaintext.length(); i += 2) {
            int[] vector = {plaintext.charAt(i) - 'A', plaintext.charAt(i + 1) - 'A'};
            int c1 = mod26(key[0][0] * vector[0] + key[0][1] * vector[1]);
            int c2 = mod26(key[1][0] * vector[0] + key[1][1] * vector[1]);
            cipher.append((char) (c1 + 'A'));
            cipher.append((char) (c2 + 'A'));
        }
        return cipher.toString();
    }

    public static String hillDecrypt(String cipher, int[][] key) {
        // Find inverse of key matrix modulo 26
        int det = mod26(key[0][0] * key[1][1] - key[0][1] * key[1][0]);
        int detInv = modInverse(det, 26);
        if (detInv == -1) return "Inverse doesn't exist, decryption impossible.";

        int[][] invKey = new int[2][2];
        invKey[0][0] = mod26(detInv * key[1][1]);
        invKey[0][1] = mod26(-detInv * key[0][1]);
        invKey[1][0] = mod26(-detInv * key[1][0]);
        invKey[1][1] = mod26(detInv * key[0][0]);

        StringBuilder plaintext = new StringBuilder();
        for (int i = 0; i < cipher.length(); i += 2) {
            int[] vector = {cipher.charAt(i) - 'A', cipher.charAt(i + 1) - 'A'};
            int p1 = mod26(invKey[0][0] * vector[0] + invKey[0][1] * vector[1]);
            int p2 = mod26(invKey[1][0] * vector[0] + invKey[1][1] * vector[1]);
            plaintext.append((char) (p1 + 'A'));
            plaintext.append((char) (p2 + 'A'));
        }
        return plaintext.toString();
    }

    private static int modInverse(int a, int m) {
        a = a % m;
        for (int x = 1; x < m; x++) {
            if ((a * x) % m == 1) return x;
        }
        return -1;
    }

    // --- Vigenere Cipher ---
    public static String vigenereEncrypt(String text, String key) {
        text = text.toUpperCase().replaceAll("[^A-Z]", "");
        key = key.toUpperCase().replaceAll("[^A-Z]", "");
        StringBuilder result = new StringBuilder();
        for (int i = 0, j = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            int shift = key.charAt(j) - 'A';
            char encrypted = (char) ((c - 'A' + shift) % 26 + 'A');
            result.append(encrypted);
            j = (j + 1) % key.length();
        }
        return result.toString();
    }

    public static String vigenereDecrypt(String cipher, String key) {
        cipher = cipher.toUpperCase().replaceAll("[^A-Z]", "");
        key = key.toUpperCase().replaceAll("[^A-Z]", "");
        StringBuilder result = new StringBuilder();
        for (int i = 0, j = 0; i < cipher.length(); i++) {
            char c = cipher.charAt(i);
            int shift = key.charAt(j) - 'A';
            char decrypted = (char) ((c - 'A' - shift + 26) % 26 + 'A');
            result.append(decrypted);
            j = (j + 1) % key.length();
        }
        return result.toString();
    }

    // --- Main method for demonstration ---
    public static void main(String[] args) {
        // Caesar Cipher
        String caesarText = "HELLO WORLD";
        int caesarShift = 3;
        String caesarEncrypted = caesarEncrypt(caesarText, caesarShift);
        String caesarDecrypted = caesarDecrypt(caesarEncrypted, caesarShift);
        System.out.println("Caesar Cipher:");
        System.out.println("Encrypted: " + caesarEncrypted);
        System.out.println("Decrypted: " + caesarDecrypted);
        System.out.println();

        // Playfair Cipher
        String playfairText = "HELLO";
        String playfairKey = "MONARCHY";
        String playfairEncrypted = playfairEncrypt(playfairText, playfairKey);
        String playfairDecrypted = playfairDecrypt(playfairEncrypted, playfairKey);
        System.out.println("Playfair Cipher:");
        System.out.println("Encrypted: " + playfairEncrypted);
        System.out.println("Decrypted: " + playfairDecrypted);
        System.out.println();

        // Hill Cipher
        String hillText = "HELLO";
        int[][] hillKey = { {3, 3}, {2, 5} };
        String hillEncrypted = hillEncrypt(hillText, hillKey);
        String hillDecrypted = hillDecrypt(hillEncrypted, hillKey);
        System.out.println("Hill Cipher:");
        System.out.println("Encrypted: " + hillEncrypted);
        System.out.println("Decrypted: " + hillDecrypted);
        System.out.println();

        // Vigenere Cipher
        String vigenereText = "HELLO";
        String vigenereKey = "KEY";
        String vigenereEncrypted = vigenereEncrypt(vigenereText, vigenereKey);
        String vigenereDecrypted = vigenereDecrypt(vigenereEncrypted, vigenereKey);
        System.out.println("Vigenere Cipher:");
        System.out.println("Encrypted: " + vigenereEncrypted);
        System.out.println("Decrypted: " + vigenereDecrypted);
    }
}
