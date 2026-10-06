/* geometry.c -- compiled and linked by `use geometry` */
#include <math.h>
#include "geometry.h"

double hypotenuse(double a, double b) {
    return sqrt(a * a + b * b);
}

long long area_of_rect(long long w, long long h) {
    return w * h;
}
