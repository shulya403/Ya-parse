import pandas as pd
#import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
                 'ультрабук',
                 'ноутбук для бизнеса',
                 'ноутбук для дизайнеров']
    },
    'Монитор': {
        'url': 'https://www.mvideo.ru/komputernaya-tehnika-4107/monitory-101',
        'type': ['монитор',
                 'монитор игровой',
                 ],
        'nontype':[
            'подставка под монитор',
            'аксессуары',
            'кронштейн для монитора'
        ]



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
    def __init__(self, category_, cat=Categories, pg_num=1):
        self.Categories = cat
        self.pg_num = pg_num

        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument("--window-size=500,1080")
        options.add_argument("--remote-debugging-port=9222")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


        cat_ok = False
        for i in self.Categories:
            if category_.lower() == i.lower():
                print('Категория: {}'.format(i))
                cat_ok = True
                self.category_ = category_
                self.url_category = self.Categories[self.category_]['url']
                self.list_types_category = self.Categories[self.category_]['type']
                if 'nontype' in self.Categories[self.category_]:
                    self.list_nontypes_category = self.Categories[self.category_]['nontype']
                else:
                    self.list_nontypes_category = []
                break
        if not cat_ok:
            print("неверное имя категории: {}".format(category_))
            raise

        self.df = pd.DataFrame(columns=['Name',
                                        'Ya_UN_Name',
                                        'Category',
                                        'Modification_name',
                                        'Modification_href',
                                        'Modification_price',
                                        'Quantity',
                                        'Vendor',
                                        'Subcategory',
                                        'Cards_page_num',
                                        'Date'])

        self.host_url = 'https://www.mvideo.ru'
        self.now = datetime.now().strftime('%b-%y')
        self.exit_filename = self.category_ + '-МВ-Цены-от-' + self.now + "--" + str(self.pg_num) + '.xlsx'

#запрос с использованием Selenium для JavaScript
    def Req_JS(self, url_):

        #options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #options.add_argument("--window-size=500,500")


        #self.driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe", options=options)
            #self.driver.implicitly_wait(3)
        self.driver.get(url_)
        # try:
        #     element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "")))
        # except Exception:
        #     pass
        # finally:
        exit_ = self.driver.page_source

        if not exit_:
            time.sleep(3)
            self.Req_JS(url_)

        return exit_

    #    Получение номера конечной стpаницы
    def Get_EOF_Page(self):

        bs_page = BeautifulSoup(self.Req_JS(self.url_category), 'html.parser')
        bs_pagination = bs_page.find('div', class_='pagination desktop-listing__pagination')
        #print(bs_pagination)
        li_bs_pages_buttons = bs_pagination.find_all('a')
        li_bs_pages_num = [int(i.text.replace(" ", "").replace("\n", "")) for i in li_bs_pages_buttons]

        max_page = max(li_bs_pages_num)

        return max_page

    #вызывная функция парсинга
    def Pagination(self, max_page, begin_page=1):

        for page in range(begin_page, max_page + 1):
            if not page == 1:
                url_ = self.url_category + '?page=' + str(page)
            else:
                url_ = self.url_category

            print(page)
            self.Parse_Pages(url_, page)
            print(page, self.exit_filename)
            self.To_Excel()

    def To_Excel(self):

        self.df.to_excel(self.exit_filename)

    def Pagination_Unparsed(self, filename, new_num, finish):

        self.pg_num = new_num
        self.exit_filename = self.category_ + '-МВ-Цены-от-' + self.now + "--" + str(self.pg_num) + '.xlsx'

        #  НОВЫЙ ФАЙЛ!!!
        df_u = pd.read_excel(filename)
        list_parsed = list(df_u['Cards_page_num'].unique())
        list_unparsed = [i for i in range(1, finish) if i not in list_parsed]
        print(len(list_parsed), len(list_unparsed))
        print(list_unparsed)

        for page in list_unparsed:

            url_ = self.url_category + '?page=' + str(page)
            print(page)
            self.Parse_Pages(url_, page)

            self.To_Excel()

    def Parse_Pages(self, url_, page_):

        bs_page = BeautifulSoup(self.Req_JS(url_), 'html.parser')

        #Карточки продуктов
        li_bs_product_cards = bs_page.find_all('div', class_='product-grid-card')
        if not li_bs_product_cards:
            li_bs_product_cards = bs_page.find_all('div', class_='product-mobile-card')
        #pprint(li_bs_product_cards)
        df_ = pd.DataFrame(columns=self.df.columns)
        Gluk = False  # Ошибка все  99999

        for card in li_bs_product_cards:

            bs_price_block = card.find('div', class_="price-block__price")

            if bs_price_block:
            # Цена если есть, если нет - нафик

                #  Подкатегории
                soup_longstring = card.find('a', class_="product-title product-title--clamp")
                if soup_longstring:
                    longstring = soup_longstring.text

                    list_word = longstring.split()

                    noncat = False
                    if self.list_nontypes_category:
                        for ncat in self.list_nontypes_category:
                            if ncat in longstring.lower():
                                noncat = True
                                break
                    if not noncat:
                        list_found_cat = list()
                        for cat in self.list_types_category:
                            if cat in longstring.lower():
                                list_found_cat.append((cat, len(cat), len(cat.split())))

                        if list_found_cat:
                            list_found_cat.sort(key=lambda x: x[1], reverse=True)
                    # Блок заполнения df row
                            i = len(df_)

                            df_.loc[i, 'Subcategory'] = list_found_cat[0][0]
                            df_.loc[i, 'Modification_price'] = "".join(re.findall(r'\d', bs_price_block.text))
                            df_.loc[i, 'Vendor'] = list_word[list_found_cat[0][2]]
                            df_.loc[i, 'Modification_name'] = " ".join(list_word[list_found_cat[0][2]:])
                            df_.loc[i, 'Modification_href'] = self.host_url + soup_longstring.get('href')

        if len(df_) > 0:
            df_['Cards_page_num'] = page_
            df_['Date'] = self.now
            df_['Quantity'] = None
            df_['Ya_UN_Name'] = None
            df_['Name'] = None
            df_['Site'] = "mvideo"
            df_['Category'] = self.category_

            if df_['Modification_price'].isna().all():
                print("Нет цен на странице, финиш")
                raise

            if (len(df_['Modification_price'].unique()) == 1) and int(df_['Modification_price'].unique()[0]) == 99999:
                Gluk = True

            print(df_[['Modification_name', 'Modification_price']])
            if not Gluk:
                self.df = pd.concat([self.df, df_], ignore_index=True)
        else:
            print("пусто...", page_)

class parse_mvideo_new(parse_mvideo):

    def Click_list_button(self, page):

        def wait_until_all(func, number_):
            while True:
                elements = func()
                if len(elements) == number_:
                    return elements()

        def get_elements(driver):
            wait = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-card--mobile")))

            return wait
                # wait

        button = None
        try:
                button = self.driver.find_element_by_tag_name("mvid-view-switcher")

        except Exception:
                button = self.driver.find_element_by_css_selector(".listing-views")

        if button:
            button.click()
        # time.sleep(10)

            elements_ = self.driver.find_elements_by_css_selector(".product-cards-layout__item.ng-star-inserted")
            elements_num = len(elements_)
            elements = wait_until_all(lambda: get_elements(self.driver), elements_num)

            #element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination desktop-listing__pagination")))

        try:
            self.driver.implicitly_wait(10)
        except Exception:
            pass


        exit_ = self.driver.page_source

        return exit_

    def Req_JS(self, url_):

        def wait_until_all_expected_elements(driver, number_of_elements):
            times = 0
            # while True:
            #         xpath = "//div[@class=\"product-card--mobile\"]"
            #
            #         condition = EC.presence_of_all_elements_located((By.XPATH, xpath))
            #
            #         number_of_cards = len(self.driver.find_elements_by_class_name("product-card--mobile"))
            #
            #         try:
            #             wait = WebDriverWait(driver, 10).until(condition)
            #         except Exception as Err:
            #             print(Err)
            #             wait = list()
            #             pass
            #         print(len(wait))
            #         if len(wait) == number_of_elements:
            #             break
            #         times += 1
            #
            #         if times == 10:
            #             break

        # def get_elements(driver):
        #
        #     xpath = "//div[@class=\"product-card--mobile\"]"
        #     condition = EC.presence_of_all_elements_located((By.XPATH, xpath))
        #
        #     try:
        #         wait = WebDriverWait(driver, 10).until(condition)
        #         return wait
        #     except Exception:
        #         pass
        self.driver.get(url_)
        time.sleep(5)
        product_elements = self.driver.find_elements_by_class_name("product-cards-layout__item")

        number_of_elements = len(product_elements)
        print(number_of_elements)
        for elm in product_elements:
            try:
                elm.location_once_scrolled_into_view
            except Exception:
                pass

        #wait_until_all_expected_elements(self.driver, number_of_elements)

        exit_ = self.driver.page_source

        if not exit_:
            time.sleep(3)
            self.Req_JS(url_)

        return exit_


    def Parse_Pages(self, url_, page_):

        bs_page = BeautifulSoup(self.Req_JS(url_), 'html.parser')

        #Карточки продуктов
        # li_bs_product_cards = bs_page.find_all('div', class_='product-grid-card')
        # if not li_bs_product_cards:
        #     li_bs_product_cards = bs_page.find_all('div', class_='product-mobile-card')
        #pprint(li_bs_product_cards)

        li_bs_product_cards = bs_page.find_all('div', class_='product-card--mobile')

        if li_bs_product_cards:



            df_ = pd.DataFrame(columns=self.df.columns)
            Gluk = False  # Ошибка все  99999

            for card in li_bs_product_cards:

                bs_price_block = card.find('p', class_="price__main-value")
                if not bs_price_block:
                    bs_price_block = card.find('p', class_="price__actual-price")

                if bs_price_block:
                    bs_price_sale_ls = bs_price_block.find_all('span')

                    for i in bs_price_sale_ls:
                        if not i.find('span', class_="currency"):
                                bs_price_block = i
                                break


                    #pprint(card)
                # Цена если есть, если нет - нафик

                    #  Подкатегории
                    soup_longstring = card.find('a', class_="product-title__text")

                    if soup_longstring:
                        longstring = soup_longstring.text

                        list_word = longstring.split()

                        noncat = False
                        if self.list_nontypes_category:
                            for ncat in self.list_nontypes_category:
                                if ncat in longstring.lower():
                                    noncat = True
                                    break
                        if not noncat:
                            list_found_cat = list()
                            for cat in self.list_types_category:
                                if cat in longstring.lower():
                                    list_found_cat.append((cat, len(cat), len(cat.split())))

                            if list_found_cat:
                                list_found_cat.sort(key=lambda x: x[1], reverse=True)
                        # Блок заполнения df row
                                i = len(df_)

                                df_.loc[i, 'Subcategory'] = list_found_cat[0][0]
                                df_.loc[i, 'Modification_price'] = "".join(re.findall(r'\d', bs_price_block.text))
                                df_.loc[i, 'Vendor'] = list_word[list_found_cat[0][2]]
                                df_.loc[i, 'Modification_name'] = " ".join(list_word[list_found_cat[0][2]:])
                                df_.loc[i, 'Modification_href'] = soup_longstring.get('href')
                else:   #price_block
                    pprint(card)

        if len(df_) > 0:
                df_['Cards_page_num'] = page_
                df_['Date'] = self.now
                df_['Quantity'] = None
                df_['Ya_UN_Name'] = None
                df_['Name'] = None
                df_['Site'] = "mvideo"
                df_['Category'] = self.category_

                if df_['Modification_price'].isna().all():
                    print("Нет цен на странице, финиш")
                    raise

                if (len(df_['Modification_price'].unique()) == 1) and int(df_['Modification_price'].unique()[0]) == 99999:
                    Gluk = True

                print(df_[['Modification_name', 'Modification_price']])
                if not Gluk:
                    self.df = pd.concat([self.df, df_], ignore_index=True)
        else:
                print("пусто...", page_)

#   MAIN
# Монитор: 27
# Ноутбук: 91
parse = parse_mvideo_new('Монитор', pg_num=1)
#print(parse.Parse_Pages(url_='https://www.mvideo.ru/noutbuki-planshety-komputery-8/noutbuki-118?page=12'))
#                              https://www.mvideo.ru/komputernaya-tehnika-4107/monitory-101
#parse.Get_EOF_Page()

#   def Pagination(self, max_page, begin_page=1):
# АККУРАТНО С СВЕРХБОЛЬШИМИ ЦЕНАМИ (ЭТО СКИДКА)
parse.Pagination(max_page=32, begin_page=0)

#parse.Pagination_Unparsed('Монитор-МВ-Цены-от-Oct-20--final.xlsx',  new_num=2, finish=44)


