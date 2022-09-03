from parser import parse

src = """
  x = {};
  x.y = 0;
  x.y = x.y + 1;
  x.z = 2;
"""

if __name__ == "__main__":
  i = 0
  for line in src.split('\n'):
    if line != "":
      i += 1
      parse(line)
  

