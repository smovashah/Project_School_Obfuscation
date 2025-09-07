// #include <stdio.h>

int square(int n) {
    // محاسبه توان دوم
    return n * n;
}

int main() {
    int x = 5;
    int y = square(x);
    printf("x=%d, y=%d\n", x, y);
    return 0;
}
