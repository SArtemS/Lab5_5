import unittest


class Currencies:

    def __init__(self, f='favorite_currencies.ini'):
        self._link = 'http://www.cbr.ru/scripts/XML_daily.asp'
        import configparser
        config = configparser.ConfigParser()
        config.read(f)
        self._favorite = config['Favorites']['fav_cur'].split(', ')

    def get_list(self):
        import requests
        from xml.etree import ElementTree as ET
        cur_res_str = requests.get(self._link)
        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")
        return valutes

    def get_all_currencies(self):
        result = []
        for _v in self.get_list():
            result.append(self.get_valute(_v))
        return result

    def get_specific_currency(self, ID):
        for _v in self.get_list():
            if ID == _v.get('ID'):
                return self.get_valute(_v)
        return dict.fromkeys(ID.split(', '))

    def get_favorite_currencies(self):
        result = []
        for _v in self.get_list():
            if _v.get('ID') in self._favorite:
                result.append(self.get_valute(_v))
        return result

    def set_favorite_currencies(self, IDs: list, f='favorite_currencies.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read(f)
        self._favorite.extend(IDs)
        config['Favorites']['fav_cur'] = ", ".join(set(self._favorite))
        with open('favorite_currencies.ini', 'w') as cf:
            config.write(cf)
        print("Отслеживаемые валюты: \n" + config['Favorites']['fav_cur'])

    def remove_favorite_currency(self, f='favorite_currencies.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read(f)
        print(config['Favorites']['fav_cur'] + "\nВведите удаляемый ID:")
        rm_id = str(input())
        if rm_id in self._favorite:
            self._favorite.remove(rm_id)
            config['Favorites']['fav_cur'] = ", ".join(self._favorite)
            with open('favorite_currencies.ini', 'w') as cf:
                config.write(cf)
            return print("ID успешно удален!\n" +
                         config['Favorites']['fav_cur'])
        return print("Такого ID не существует!\n" +
                     config['Favorites']['fav_cur'])

    def get_valute(self, vcount):
        valute = {}
        valute_cur_name, valute_cur_val = vcount.find(
            'Name').text, vcount.find('Value').text
        valute_charcode = vcount.find('CharCode').text
        valute_cur_val = float(valute_cur_val.replace(
            ',', '.'))  # Правильный формат значения валюты
        valute[valute_charcode] = (valute_cur_name,
                                   format(valute_cur_val, '.2f'))
        return valute

    # def __del__(self):
    #     print('Объект уничтожен')

    @property
    def all(self):
        self.__all = []
        for _v in self.get_list():
            self.__all.append(self.get_valute(_v))
        return self.__all

class Currencies_Test(unittest.TestCase):

    def test_wrong_id(self, ID='Wrong ID'):
        self.assertDictEqual(
            Currencies().get_specific_currency(ID), {ID: None},
            'При неправильном ID должен выводиться словарь вида: {ID: None}')

    def test_correct_ID_USD(self, ID = 'R01235'):
        USD = Currencies().get_specific_currency(ID)['USD']
        self.assertEqual(USD[0], ('Доллар США'))
        self.assertGreater(float(USD[1]), 0)
        self.assertLess(float(USD[1]), 200)

    def test_correct_ID_EUR(self, ID = 'R01239'):
        EUR = Currencies().get_specific_currency(ID)['EUR']
        self.assertEqual(EUR[0], ('Евро'))
        self.assertGreater(float(EUR[1]), 0)
        self.assertLess(float(EUR[1]), 200)

    def test_correct_ID_JPY(self, ID = 'R01820'):
        JPY = Currencies().get_specific_currency(ID)['JPY']
        self.assertEqual(JPY[0], ('Японских иен'))
        self.assertGreater(float(JPY[1]), 0)
        self.assertLess(float(JPY[1]), 200)

if __name__ == '__main__':
    # print(*Currencies().get_all_currencies(), sep='\n')
    # print(Currencies().get_specific_currency('R01710A'))
    # print(*Currencies().get_favorite_currencies(), sep='\n')
    # Currencies().set_favorite_currencies(['R01710A', 'R01775'])
    # Currencies().remove_favorite_currency()
    # unittest.main()
    print(*Currencies().all, sep='\n')

    # геттеры, сеттеры, деструктор
