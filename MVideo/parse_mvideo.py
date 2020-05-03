import pandas as pd
#import requests
from bs4 import BeautifulSoup
#from requests_html import HTMLSession, HTML
from selenium import webdriver
from pprint import pprint
import re
from datetime import datetime
import time


Categories = {
    'Ноутбук': {
        'url': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118',
        'type': ['ноутбук',
                 'ноутбук игровой',
                 'ноутбук-трансформер',
                 'ультрабук']
    }
}

header_ = {
            #'Referer': referer,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en;q=0.9',
            'Connection': 'keep-alive',
            #'Cache-Control': 'max-age=0',
            #'Host': 'market.yandex.ru',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.1.248 Yowser/2.5 Safari/537.36',

        }

class parse_mvideo(object):
    def __init__(self, category_, cat=Categories):
        self.Categories = cat
        cat_ok = False
        for i in self.Categories:
            if category_.lower() == i.lower():
                print('Категория: {}'.format(i))
                cat_ok = True
                self.category_ = category_
                self.url_category = self.Categories[self.category_]['url']
                self.list_types_category = self.Categories[self.category_]['type']
                break
        if not cat_ok:
            print("неверное имя категории: {}".format(category_))
            raise

        self.df = pd.DataFrame(columns=['Name',
                                        'Modification_name',
                                        'Vendor',
                                        'Href',
                                        'Subcategory',
                                        'Price',
                                        'Page'])
        self.host_url = 'https://www.mvideo.ru'
        self.now = datetime.now().strftime('%b-%y')

#запрос с использованием Selenium для JavaScript
    def Req_JS(self, url_):

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe", options=options)
        try:
            driver.get(url_)
            exit_ = driver.page_source
        #print(exit_)
            driver.close()
        except Exception:
            driver.close()
            time.sleep(10)
            self.Req_JS(url_)

        if not exit_:
            time.sleep(10)
            self.Req_JS(url_)

        return exit_

    #    Получение номера конечной стpраницы
    def Get_EOF_Page(self):

        bs_page = BeautifulSoup(self.Req_JS(self.url_category), 'html.parser')
        bs_pagination = bs_page.find('div', class_='pagination desktop-listing__pagination')
        #print(bs_pagination)
        li_bs_pages_buttons = bs_pagination.find_all('a')
        li_bs_pages_num = [int(i.text.replace(" ", "").replace("\n", "")) for i in li_bs_pages_buttons]

        max_page = max(li_bs_pages_num)

        return max_page

    #вызывная функция парсинга
    def Pagination(self, max_page):

        self.Parse_Pages(self.url_category, 1)

        for page in range(2, max_page + 1):
            url_ = self.url_category + '?page=' + str(page)
            print(page)
            self.Parse_Pages(url_, page)

            self.To_Excel()

    def To_Excel(self):

        #now = datetime.now().strftime('%b-%y')
        exit_filename = self.category_ + '3-МВ-Цены-от-' + self.now + '.xlsx'
        self.df.to_excel(exit_filename)

    def Pagination_Unparsed(self):

        #  НОВЫЙ ФАЙЛ!!!
        df_u = pd.read_excel('Ноутбук1-МВ-Цены-от-Apr-20.xlsx')
        list_parsed = list(df_u['Page'].unique())
        list_unparsed = [i for i in range(1, 69) if i not in list_parsed]
        print(len(list_parsed), len(list_unparsed))
        print(list_unparsed)

        for page in list_unparsed:
            if page < 69:
                url_ = self.url_category + '?page=' + str(page)
                print(page)
                self.Parse_Pages(url_, page)

                self.To_Excel()

    def Parse_Pages(self, url_, page_):

        bs_page = BeautifulSoup(self.Req_JS(url_), 'html.parser')

        #Карточки продуктов
        li_bs_product_cards = bs_page.find_all('div', class_='product-grid-card')
        #pprint(li_bs_product_cards)

        for card in li_bs_product_cards:
            df_ = pd.DataFrame(columns=self.df.columns)

        #Цена если есть, если нет - нафик

            bs_price_block = card.find('div', class_="price-block__price")
            if bs_price_block:
                df_.loc[0, 'Price'] = re.sub(r'\s+|¤|\\\n', "", bs_price_block.text) #.replace(" ", "").replace("¤", "").replace("\n", "")
                #Поле для категории верхнего уровня
                df_.loc[0, 'Name'] = None

                full_prod_name = card.find('a', class_="product-title product-title--clamp")
                list_prod_name = full_prod_name.text.split()

                # Подкатегория из Categories.type
                subcategory = str()
                subcategory_num = 0
                for token in list_prod_name:
                    if re.match(r'[а-я|\-]+', token.lower()):
                        subcategory += token.lower() + ' '
                        subcategory_num += 1
                    else:
                        subcategory = subcategory[:-1]
                        break

                for type_ in self.list_types_category:
                    if type_ == subcategory:
                        df_.loc[0, 'Subcategory'] = type_
                        break
                if not df_.loc[0, 'Subcategory']:
                    df_.loc[0, 'Subcategory'] = '? ' + subcategory

                # Имя вендора
                df_['Vendor'] = list_prod_name[subcategory_num]

                # Полное название вендор + продукт
                df_['Modification_name'] = full_prod_name.text.replace('\n', "")[len(subcategory)+3:]

                #Ссыль на страницу продукта
                df_['Href'] = self.host_url + full_prod_name.get('href')

                df_['Page'] = page_

                print(df_)

                self.df = pd.concat([self.df, df_], ignore_index=True)



#   MAIN
parse = parse_mvideo('Ноутбук')
#print(parse.Parse_Pages(url_='https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118?page=12'))
#parse.Get_EOF_Page()
#parse.Pagination(parse.Get_EOF_Page())
parse.Pagination_Unparsed()


