def gcd(a, b):
  assert isinstance(a, int) and isinstance(b, int) and int(a) > 0 and int(b) > 0
  while b != 0:
    r = a % b
    b = a
    a = r
  return a

if __name__ == "__main__":
    a = gcd("1","2")