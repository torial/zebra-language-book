/* checksum.c -- a small C library: CRC-32 (the zlib/PNG polynomial) */

/* The checksum of `len` bytes at `data`. The bytes need no terminator. */
unsigned int crc32_bytes(const unsigned char *data, long long len) {
    unsigned int crc = 0xFFFFFFFFu;
    for (long long i = 0; i < len; i++) {
        crc ^= data[i];
        for (int k = 0; k < 8; k++)
            crc = (crc >> 1) ^ (0xEDB88320u & (0u - (crc & 1u)));
    }
    return ~crc;
}
