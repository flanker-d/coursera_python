class FileReader:

    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        try:
            with open(self.file_name, 'r') as f:
                result = f.read()
                return result
        except FileNotFoundError as err:
            return ""


def _main():
    reader = FileReader('not_exist_file.txt')
    text = reader.read()
    print(text)

    with open('some_file.txt', 'w') as file:
        file.write('some text')

    reader = FileReader('some_file.txt')
    text = reader.read()
    print(text)

if __name__ == "__main__":
    _main()