import os.path
import tempfile
import uuid

class File:

    def __init__(self, path_to_file):
        self.path_to_file = os.path.abspath(path_to_file)
        self.current_line = 0

        if not os.path.exists(path_to_file):
            with open(path_to_file, 'w'):
                pass

    def __add__(self, other):
        name = str(uuid.uuid1())
        name = name.strip('-')
        file_obj = File(os.path.join(tempfile.gettempdir(), name))
        buf = self.read()
        buf += other.read()
        file_obj.write(buf)
        return  file_obj

    def __str__(self):
        return self.path_to_file

    def __iter__(self):
        return self

    def __next__(self):
        buf = self.read_line(self.current_line)
        if buf == '':
            raise StopIteration
        self.current_line += 1
        return buf

    def read(self):
        with open(self.path_to_file, 'r') as f:
            return f.read()

    def read_line(self, line_number):
        with open(self.path_to_file) as fp:
            for i, line in enumerate(fp):
                if i == line_number:
                    return line
            return ''

    def write(self, data):
        with open(self.path_to_file, 'w') as f:
            return f.write(data)

def _main():
    path_to_file = 'some_filename'

    if os.path.exists(path_to_file):
        os.remove(path_to_file)
    if os.path.exists(path_to_file + '_1'):
        os.remove(path_to_file + '_1')
    if os.path.exists(path_to_file + '_2'):
        os.remove(path_to_file + '_2')
    if os.path.exists('new_file'):
        os.remove('new_file')

    assert os.path.exists(path_to_file) == False

    file_obj = File(path_to_file)
    assert os.path.exists(path_to_file) == True

    assert file_obj.read() == ''
    assert file_obj.write('some text') == 9
    assert file_obj.read() == 'some text'
    assert file_obj.write('other text') == 10
    assert file_obj.read() == 'other text'

    file_obj_1 = File(path_to_file + '_1')
    file_obj_2 = File(path_to_file + '_2')
    assert file_obj_1.write('line 1\n') == 7
    assert file_obj_2.write('line 2\n') == 7

    new_file_obj = file_obj_1 + file_obj_2
    assert isinstance(new_file_obj, File) == True

    print(new_file_obj.read())
    print(new_file_obj)
    # #C:\Users\Media\AppData\Local\Temp\71b9e7b695f64d85a7488f07f2bc051c
    for line in new_file_obj:
        print(ascii(line))
    # #'line 1\n'
    # #'line 2\n'

if __name__ == "__main__":
    _main()
