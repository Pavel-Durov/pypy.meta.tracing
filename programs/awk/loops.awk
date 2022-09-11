x = {}; 
x.a = 0;
x.b = 4;

while (x.a < 99999) {
  x.a = x.a + x.b;
}

x.b = 9;
y = {};
y.a = x.b;

while (x.b < 1000) {
  x.b = x.b + 1;
}

y.z = x.b;