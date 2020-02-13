import sys

number = int(sys.argv[1])

for i in range(number):
    result_string = " " * (number - i - 1) + "#" * (i + 1)
    print(result_string)
