int main()
{
    int x;
    int a;
    int b;
    int c;
    x = input();
    a = x-1;
    b = x-2;
    while (x > 0) {
      c = a*b - x;
      x = x - 1;
    }
    c = a*b;
}
