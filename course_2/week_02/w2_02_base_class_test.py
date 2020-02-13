import unittest
from inspect import isabstract
from course_2.week_02.w2_02_base_class import Base, A, B, C


class TestBaseClass(unittest.TestCase):

    def test_base_is_abstract(self):
        self.assertEqual(isabstract(Base), True)

    def test_get_answer(self):
        list = [1, 2, 3]
        a = A(list, 0)
        res = a.get_answer()

        for x in [A(list, 0), B(list, 0), C(list, 0)]:
            with self.subTest(x=1):
                self.assertEqual(x.get_answer(), res)


if __name__ == "__main__":
    unittest.main()

