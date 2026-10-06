/* textlib.c -- C functions that take and return C strings (char*) */

/* Count the vowels in a NUL-terminated string. */
int count_vowels(const char *s) {
    int n = 0;
    for (; *s; s++) {
        char c = *s;
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') n++;
    }
    return n;
}

/* Return a pointer to a static, NUL-terminated string. C owns it. */
const char *library_name(void) {
    return "textlib 1.0";
}
