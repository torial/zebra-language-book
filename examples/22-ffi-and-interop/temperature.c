/* temperature.c -- no header, so the Zebra side declares each function */

double celsius_to_fahrenheit(double c) {
    return c * 9.0 / 5.0 + 32.0;
}

int clamp_int(int value, int lo, int hi) {
    if (value < lo) return lo;
    if (value > hi) return hi;
    return value;
}
