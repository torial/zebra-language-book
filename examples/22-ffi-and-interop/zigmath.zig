// zigmath.zig -- every `pub fn` is callable as zigmath.<name>(...) after `use zigmath`
const std = @import("std");

pub fn gcd(a: i64, b: i64) i64 {
    var x = a;
    var y = b;
    while (y != 0) {
        const t = @mod(x, y);
        x = y;
        y = t;
    }
    return x;
}

pub fn isPrime(n: i64) bool {
    if (n < 2) return false;
    var d: i64 = 2;
    while (d * d <= n) : (d += 1) {
        if (@mod(n, d) == 0) return false;
    }
    return true;
}

// A Zig []const u8 IS a Zebra str, so strings cross with no conversion.
pub fn countOf(haystack: []const u8, needle: []const u8) i64 {
    return @intCast(std.mem.count(u8, haystack, needle));
}
