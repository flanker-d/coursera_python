import sys

digit_string = sys.argv[1]
#digit_string = "160438521039"

res = 0

for num in digit_string:
    res += int(num)

print(res)