int x, y;

int main(int a, int b) {
  x = 6;
  y = 1;

  while (x > 0) {
    y = y * x;
    x = x - 1;
  }

  puts("El factorial de 6 es : ");
  putw(y);
  puts("\n");
  puts("El valor de x+1 es : ");
  putw(x + 1);

  int v0;
  int v1 = ((2 < 1) == (1 < 2)) || 1;
  int v2 = 3 - 2 * 9 + 11;
}
