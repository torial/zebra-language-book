/* stats.c -- an opaque handle: C allocates the object, C frees it */
#include <stdlib.h>

typedef struct {
    long long count;
    double sum;
    double min;
    double max;
} Stats;

Stats *stats_new(void) {
    Stats *s = malloc(sizeof(Stats));
    if (s) { s->count = 0; s->sum = 0.0; s->min = 0.0; s->max = 0.0; }
    return s;
}

void stats_add(Stats *s, double x) {
    if (s->count == 0 || x < s->min) s->min = x;
    if (s->count == 0 || x > s->max) s->max = x;
    s->count++;
    s->sum += x;
}

long long stats_count(const Stats *s) { return s->count; }
double stats_mean(const Stats *s) { return s->count ? s->sum / s->count : 0.0; }
double stats_max(const Stats *s) { return s->max; }

void stats_free(Stats *s) { free(s); }
