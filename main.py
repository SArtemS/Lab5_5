class Currencies:

    def __init__(self, f='favorite_currencies.ini'):
        self._link = 'http://www.cbr.ru/scripts/XML_daily.asp'
        import configparser
        config = configparser.ConfigParser()
        config.read(f)
        self._specific_ID = 'R01010'
        self._favorites = config['Favorites']['fav_cur'].split(', ')

    def get_list(self):
        import requests
        from xml.etree import ElementTree as ET
        cur_res_str = requests.get(self._link)
        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")
        return valutes

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

    @property
    def all_currencies(self):
        print("\nПолучение всех валют:")
        self._all_currencies = []
        for _v in self.get_list():
            self._all_currencies.append(self.get_valute(_v))
        return self._all_currencies

    @property
    def specific_currency(self):
        print("\nПолучение определенной валюты:")
        for _v in self.get_list():
            if self._specific_ID == _v.get('ID'):
                self._specific_currency = self.get_valute(_v)
                return self._specific_currency
        self._specific_currency = dict.fromkeys(self._specific_ID.split(', '))
        return self._specific_currency

    @specific_currency.setter
    def specific_currency(self, new_specific_ID: str):
        print("\nСмена ID определнной валюты на " + new_specific_ID)
        self._specific_ID = new_specific_ID

    @property
    def favorite_currencies(self):
        print("\nОтслеживаемые валюты:")
        self._favorite_currencies = []
        if self._favorites:
            for _v in self.get_list():
                if _v.get('ID') in self._favorites:
                    self._favorite_currencies.append(self.get_valute(_v))
        return self._favorite_currencies

    @favorite_currencies.setter
    def favorite_currencies(self, IDs: list, f='favorite_currencies.ini'):
        import configparser
        config = configparser.ConfigParser()
        config.read(f)
        if config['Favorites']['fav_cur'] == "": self._favorites = IDs
        else: self._favorites.extend(IDs)
        config['Favorites']['fav_cur'] = ", ".join(set(self._favorites))
        with open('favorite_currencies.ini', 'w') as cf:
            config.write(cf)
        print("\nID отслеживаемых валют: \n" + config['Favorites']['fav_cur'])

    @favorite_currencies.deleter
    def favorite_currencies(self, f='favorite_currencies.ini'):
        print("\nУдаление ID отслеживаемых валют:")
        import configparser
        config = configparser.ConfigParser()
        config.read(f)
        self._favorites = None
        config['Favorites']['fav_cur'] = ""
        with open('favorite_currencies.ini', 'w') as cf:
            config.write(cf)
        print("ID отслеживаемых валют удалены")
        

if __name__ == '__main__':
    Current_Currencies = Currencies()
    del Current_Currencies.favorite_currencies
    print(*Current_Currencies.all_currencies, sep='\n')
    print(Current_Currencies.specific_currency)
    Current_Currencies.specific_currency = 'R01775'
    print(Current_Currencies.specific_currency)
    print(Current_Currencies.favorite_currencies, sep='\n')
    Current_Currencies.favorite_currencies = ['R01710A', 'R01775']
    print(Current_Currencies.favorite_currencies, sep='\n')
