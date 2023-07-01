int x, y;

main() {
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
}
