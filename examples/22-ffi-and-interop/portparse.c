/* portparse.c -- C-style error reporting: the return value is the status */

/* Parse a decimal TCP port.
 * Returns the port (1..65535), or a negative error code:
 *   -1  empty or not a number      -2  out of range */
int parse_port(const char *s) {
    if (*s == '\0') return -1;
    long value = 0;
    for (; *s; s++) {
        if (*s < '0' || *s > '9') return -1;
        value = value * 10 + (*s - '0');
        if (value > 65535) return -2;
    }
    if (value == 0) return -2;
    return (int)value;
}
