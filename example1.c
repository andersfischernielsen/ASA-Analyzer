int main()
{
    int x;
    int y;
    int z;
    int o;
    x = 1; 
    while (x > 1) {
        y = x/2;
        if (y > 3) 
            x = x - y;
        z = x - 4;
        if (z > 0) 
            x = x/2;
        z = z-1;
    }
    o = x;
}
