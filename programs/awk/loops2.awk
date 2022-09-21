x = {}; 
x.a = 1;
x.b = 2;
x.c = 3;
x.d = 3;
while (x.a < 99999999) {
  x.a = x.a + x.b + x.c + x.d + 1;
  x.a = x.b + x.c + x.d + x.a + 2;
  x.a = x.c + x.d + x.a + x.b + 3; 
  x.a = x.d + x.a + x.b + x.c + 4;
}
