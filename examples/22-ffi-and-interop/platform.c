/* platform.c -- the platform difference lives in C, behind one signature */

const char *platform_name(void) {
#if defined(_WIN32)
    return "windows";
#elif defined(__APPLE__)
    return "macos";
#elif defined(__linux__)
    return "linux";
#else
    return "unknown";
#endif
}

const char *path_separator(void) {
#if defined(_WIN32)
    return "\\";
#else
    return "/";
#endif
}
