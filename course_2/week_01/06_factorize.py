import unittest

class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        """
        test_wrong_types_raise_exception - проверяет, что передаваемый в функцию аргумент типа float или str вызывает
        исключение TypeError. Тестовый набор входных данных:  'string',  1.5
        """
        for val in ['string', 1.5]:
            with self.subTest(x=1):
                self.assertRaises(TypeError, factorize, val)

    def test_negative(self):
        """
        test_negative - проверяет, что передача в функцию factorize отрицательного числа вызывает исключение ValueError.
         Тестовый набор входных данных:   -1,  -10,  -100
        """
        for i in (-1, -10, -100):
            with self.subTest(x=2):
                self.assertRaises(ValueError, factorize, i)

    def test_zero_and_one_cases(self):
        """
        test_zero_and_one_cases - проверяет, что при передаче в функцию целых чисел 0 и 1, возвращаются соответственно
         кортежи (0,) и (1,). Набор тестовых данных: 0 → (0, ),  1 → (1, )
        """
        for key, val in [(0, (0,)), (1, (1,))]:
            with self.subTest(x=3):
                self.assertEqual(factorize(key), val)

    def test_simple_numbers(self):
        """
        test_simple_numbers - что для простых чисел возвращается кортеж, содержащий одно данное число. Набор тестовых
        данных: 3 → (3, ),  13 → (13, ),   29 → (29, )
        """
        for i in (3, 13, 29):
            with self.subTest(x=4):
                self.assertEqual(factorize(i), (i,))

    def test_two_simple_multipliers(self):
        """
        test_two_simple_multipliers — проверяет случаи, когда передаются числа для которых функция factorize возвращает
         кортеж с числом элементов равным 2. Набор тестовых данных: 6 → (2, 3),   26 → (2, 13),   121 --> (11, 11)
        """
        for key, val in [(6, (2, 3)), (26, (2, 13)), (121, (11, 11))]:
            with self.subTest(x=5):
                self.assertEqual(factorize(key), val)

    def test_many_multipliers(self):
        """
        test_many_multipliers - проверяет случаи, когда передаются числа для которых функция factorize возвращает кортеж
         с числом элементов больше 2. Набор тестовых данных: 1001 → (7, 11, 13) ,   9699690 → (2, 3, 5, 7, 11, 13, 17, 19)
        """
        for key, val in [(1001, (7, 11, 13)), (9699690, (2, 3, 5, 7, 11, 13, 17, 19))]:
            with self.subTest(x=6):
                self.assertEqual(factorize(key), val)
