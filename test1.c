int x, y;

int z = 99, f;

int main(int a, int b) {
  x = 6;
  y = 1;
  z = x + y;

  while (x > 0) {
    y = y * x;
    x = x - 1;
  }

  puts("El factorial de 6 es : ");
  putw(y);
  puts("...\n");
  puts("El valor de x+1 es : ");
  putw(x + 1);

  if (a == 99 + 1 || b == 10 - 1) {
    puts("Hello");
  } else {
    puts("Bye");
  }

  int v0;
  int v1 = ((2 < 1) == (1 < 2)) || 1;
  int v2 = 3 - 2 * 9 + 11;
  int v3 = !v0;
}
