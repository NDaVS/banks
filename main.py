from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def get_table_from_CB(url): # Получение таблицы с сайта ЦБ
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read() # Получение страницы ЦБ
    soup = BeautifulSoup(webpage, features="lxml")

    table = soup.find('tbody') # Получение таблицы
    rows = table.find_all('tr') # Получение строк (742)
    true_rows=[] # Нужные строки (376)

    for i in range(len(rows)): # Удаление отозванных
        if not ('ОТЗ' in rows[i].text):
            true_rows.append(rows[i])

    print(f"Успешно получена таблица ({len(true_rows)})")
    with open('parse.txt', 'w') as f:
        stringText = ''
        for i in true_rows:
            stringText += f'https://cbr.ru{i.find("a").get("href")}\n'

        f.write(stringText)
    return true_rows # Супы

#Получение ссылок на сайт компании
def get_data_from_CB_table(bank):

    url = 'https://cbr.ru' + bank.find('a').get('href')

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()  # Получение страницы ЦБ
    soup = BeautifulSoup(webpage, features="lxml")

    try:
        urls = soup.find('div', {'class': 'tabs _links _cols-3'}).find_all('a') # Поиск ссылок

        true_urls = []  # Сюда собируются ссылки на сайт компании
        bad_urls = ['vk', 'twitter', 'google', 'facebook', 'instagram', 'youtube', 't.me']

        for i in urls:
            if not any(x in i.text for x in bad_urls) and ('https' in i.text):
                true_urls.append(i)  # Защищённая и проверенная ссылка
        return true_urls[0].text  # Вывод первой текстовой ссылки
    except:
        urls = 0


        return 0# Вывод первой текстовой ссылки

def get_name (bank):
    url = 'https://cbr.ru' + bank.find('a').get('href')

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()  # Получение страницы ЦБ
    soup = BeautifulSoup(webpage, features="lxml")

    name = soup.find('span', {'class': 'referenceable'}).text
    return name
def get_second_page(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()  # Получение страницы ЦБ
    soup = BeautifulSoup(webpage, features="lxml")

    urls = soup.find_all('a')
    add_url = ''

    for i in urls:
        if 'Реквизиты' in i.text:
            add_url = i.get('href')
            URL = url + add_url
            return URL
# Get company site
def get_company_site(url):

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()  # Получение страницы ЦБ
    soup = BeautifulSoup(webpage, features="lxml")

    urls = soup.find_all('a')
    add_url = ''

    for i in urls:
        if 'Реквизиты' in i.text:
            add_url = i.get('href')
            URL = url + add_url
            return URL
    for i in urls:
        if 'О Банке' in i.text:
            add_url = i.get('href')
            URL = url + add_url
            URL = get_second_page(URL)
            return URL


def get_req(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()  # Получение страницы с реквизитами
    soup = BeautifulSoup(webpage, features="lxml")
    #print(soup.find(text="ИНН").findNextSibling)
    res = []
    nun = soup.text.split('\n')
    inn = 0
    ogrn = 0
    addr = 0
    licence = 0
    for i in nun:
        if i != '':
            res.append(i)
        if 'ИНН' in i:
            if any(str(x) in i for x in range(10)):
                inn = res.index(i)
            else:
                inn = res.index(i) + 1
        if 'ОГРН' in i:
            if any(str(x) in i for x in range(10)):
                ogrn = res.index(i)
            else:
                ogrn = res.index(i) + 1
        if ('Адрес' in i or 'адрес' in i) and not 'электронной' in i:
            if any(str(x) in i for x in range(10)):
                addr = res.index(i)
            else:
                addr = res.index(i) + 1
        if 'Лицензия' in i and licence == '':
            if any(str(x) in i for x in range(10)):
                licence = res.index(i)
            else:
                licence = res.index(i) + 1
    print(f"ИНН {res[inn]}")
    print(f"ОГРН {res[ogrn]}")
    print(f"Адрес {res[addr]}")
    print(f"Лицензия {res[licence]}")

def main():
    #url = input()
    url = 'https://cbr.ru/banking_sector/credit/FullCoList/'
    banks = get_table_from_CB(url)
    # for bank in banks:
    #     get_data_from_CB_table(bank) # debug
    for bank in banks:
        url_on_site = get_data_from_CB_table(bank)
        name = get_name(bank)
        # try:
        #     print(url_on_site)
        #     req = get_company_site(url_on_site)
        #     info = get_req(req)
        # except:
        #     info = 'None'
        if url_on_site != 0:
            with open('main.txt', 'a') as f:
                f.write(f'{name} - {url_on_site}\n')
        else:
            with open('without_url.txt', 'a') as f:
                f.write(f'{name} \n')



if __name__ == '__main__':
    main()