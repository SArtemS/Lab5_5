import unittest
from main import Currencies

test_currencies = Currencies()


class Currencies_Test(unittest.TestCase):

    def test_wrong_id(self, ID='Wrong ID'):
        test_currencies.specific_currency = ID
        self.assertDictEqual(
            test_currencies.specific_currency, {ID: None},
            'При неправильном ID должен выводиться словарь вида: {ID: None}')

    def test_correct_ID_USD(self, ID='R01235'):
        test_currencies.specific_currency = ID
        USD = test_currencies.specific_currency['USD']
        self.assertEqual(USD[0], ('Доллар США'))
        self.assertGreater(float(USD[1]), 0)
        self.assertLess(float(USD[1]), 200)

    def test_correct_ID_EUR(self, ID='R01239'):
        test_currencies.specific_currency = ID
        EUR = test_currencies.specific_currency['EUR']
        self.assertEqual(EUR[0], ('Евро'))
        self.assertGreater(float(EUR[1]), 0)
        self.assertLess(float(EUR[1]), 200)

    def test_correct_ID_JPY(self, ID='R01820'):
        test_currencies.specific_currency = ID
        JPY = test_currencies.specific_currency['JPY']
        self.assertEqual(JPY[0], ('Японских иен'))
        self.assertGreater(float(JPY[1]), 0)
        self.assertLess(float(JPY[1]), 200)


if __name__ == '__main__':
    unittest.main()