#TODO: Framewor обработки сайтов магазинов по категориям
# обработка unparsed

import pandas as pd
import time
from datetime import datetime
from pprint import pprint
import json
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import re
from urllib.parse import quote, unquote

#общий принцип парсинга - класс parse_common
#Скачиваем json файл Categories
#Для нужной категории выходим на листаж Pagination пока не пошли "кривые данные"

class Parse_Common(object):
    site = ""
    addition_fields = []
    def __init__(self,
                 category, #категория продуктов
                 scraper, # [requests, selenium],
                 ttx=False, #надо ли скачивать характеристики
                 pagination_start=1,
                 pagination_finish=-1,
                 interrupt=5,
                 num_outfile=1 #Дополнительный номер версии выходного файла
                 ):

        self.interrupt = interrupt

        self.bl_ttx = ttx

        self.num_outfile = num_outfile

        self.scraper = scraper

        self.category = category

        self.ttx = ttx
        #скачиваем json
        with open('categories.json', encoding='utf-8') as f:
            self.Categories = json.load(f)

    #   Словарь пар-в для сайта
        self.site_params = self.Categories[self.site]
        #pprint(self.category_site)

    #   Словарь пар-в для категории продукта
        self.category_params = self.site_params["categories"][self.category]
        pprint(self.category_params)

        self.out_columns = [
            'Name',
            'Vendor',
            'Modification_name',
            'Modification_href',
            'Category',
            'Subcategory',
            'Date',
            'Modification_price',
            'Cards_page_num',
            'Site'
        ]

        self.df = pd.DataFrame(columns=self.out_columns + self.addition_fields)

        self.now = datetime.now().strftime('%b-%y')

        self.Folder_Out_Check()

        self.outfile_name = "Prices/" + \
                            self.site + \
                            "/" + \
                            self.site + \
                            "--" + \
                            self.category.title() + \
                            "--" + \
                            self.now + \
                            "--" + \
                            str(self.num_outfile) + \
                            '.xlsx'

        self.warnings = {
            "unknown_host": {"print": "Нет названия хоста {}".format(self.site),
                             "show": True,
                             "raise": False},
            "unknown_category_url": {"print": "Нет URL категории {}:{}".format(self.site, self.category),
                                     "show": True,
                                     "raise": True},
            "no_site_url_suffics": {"print": "Нет Get-добавкий опций страницы для сайта {}".format(self.site),
                                     "show": True,
                                     "raise": False},
            "no_site_viewtype": {"print": "Нет обозначения viewtype для сайта {}".format(self.site),
                                    "show": True,
                                    "raise": False},
            "no_cards_page_params": {"print": "Нет параметров для парсинга страницы выдачи для сайта {}".format(self.site),
                                 "show": True,
                                 "raise": True},
            "no_cookies": {
                "print": "Нет cookies для сайта {}".format(self.site),
                "show": True,
                "raise": False}
        }
        try:
            self.teg_card_params = self.site_params["cards_page_params"]

        except KeyError:
            self.JSON_Content_Warnings_Alarm("no_cards_page_params")

        try:
            self.pg_num = self.site_params["pg_num"]
        except KeyError:
            self.pg_num = "&page="

        try:
            self.host_get_suffics = self.site_params["host_get_suffics"]

        except KeyError:
            self.JSON_Content_Warnings_Alarm("no_site_url_suffics")
            self.host_get_suffics = ""

    def Folder_Out_Check(self):
        import os

        try:
            bl_dir = False
            list_dir_price = os.listdir("Prices/")
            for i in list_dir_price:
                if i == self.site:
                    bl_dir = True
                    break
            if not bl_dir:
                os.makedirs("Prices/" + self.site)

        except FileExistsError:
            print("Что-то с паками под Прайсы")

    def JSON_Content_Warnings_Alarm(self, key):
        if self.warnings[key]["show"]:
            print(self.warnings[key]["print"])
            self.warnings[key]["show"] = False
        if self.warnings[key]["raise"]:
            raise KeyError

    def Find_All_Divs(self, json_div, soup):

        try:
            arguments = self.teg_card_params[json_div]["attributes"]
            if arguments:
                if "class" in arguments:
                    arguments["class_"] = arguments.pop("class")
                #for i in arguments:
                #    arguments[i] = re.compile(arguments[i])
                return soup.find_all(self.teg_card_params[json_div]["teg"], **arguments)
            else:
                return soup.find_all(self.teg_card_params[json_div]["teg"])
        except KeyError:
            print('В JSON нет тега {} для сайта {}'.format(json_div, self.site))
            raise KeyError

    def Find_Div(self, json_div, soup):

        try:
            arguments = self.teg_card_params[json_div]["attributes"]
            if arguments:
                if "class" in arguments:
                    arguments["class_"] = arguments.pop("class")
                #for i in arguments:
                #    arguments[i] = re.compile(arguments[i])
                return soup.find(self.teg_card_params[json_div]["teg"], **arguments)
            else:
                return soup.find(self.teg_card_params[json_div]["teg"])
        except KeyError:
            print('В JSON нет тега {} для сайта {}'.format(json_div, self.site))
            raise KeyError


#   Возврат html-страницы от Selenium
    def Page_Webdriver(self, url_):

        def Err_Webdriver(url_, interrupt):
            driver.close()
            print("Страница не скачивается {}\n повтор...".format(url_))
            time.sleep(interrupt)
            self.Page_Webdriver(url_)

        #try:
        #    options = webdriver.ChromeOptions()
        #    for option in self.site_params["host_options"]:
        #        options.add_argument(option)
        #except Exception:
        #    print("Site Options", Exception)

        driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

        try:
            print(self.driver.current_url)
            self.driver.get(url_)
            print(self.driver.current_url)

            exit_ = self.driver.page_source

            # print(exit_)
            if exit_:
                print("Where is something in {}".format(url_))
            else:
                Err_Webdriver(url_, 1)

            driver.close()
        except Exception:
            Err_Webdriver(url_, 1)

        return exit_

#   Возврат html-страницы on Requests
    def Page_Requests(self, url_):

        cookies = self.site_params["cookies"]

        header = {
            # 'Referer': referer,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en;q=0.9',
            'Connection': 'keep-alive',
            # 'Cache-Control': 'max-age=0',
            # 'Host': 'market.yandex.ru',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.1.248 Yowser/2.5 Safari/537.36',
        }
        time.sleep(self.interrupt)
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.get(url_, headers=header, cookies=cookies)
            #response = requests.get(url_, headers=header, cookies=cookies, retries=retry)
        print(url_, response.status_code)
        if response.status_code == 200:
           return response.text

#   Выбор скрапера Requests или Selenium
    def Page_Scrape(self, url_):

        if self.scraper == 'selenium':

            return self.Page_Webdriver(url_)
        elif self.scraper == 'requests':

            return self.Page_Requests(url_)
        else:
            print("Неведомый скрапер {}".format(self.scraper))
            raise Exception

#   Формирователь url базовый (host+url_)
    def URL_Base_Make(self, url_):

        try:
           exit_url = self.site_params["host"]
        except KeyError:
            self.JSON_Content_Warnings_Alarm("unknown_host")
        finally:
            exit_url += url_

        return exit_url

#   Формирователь url страницы выдачи (host+ categoru-url + page)
    def URL_CardsPage_Make(self, url_="", page=1):

        if url_:
            url_this = url_
        else:
            try:
                url_this = self.category_params["url"]
            except KeyError:
                self.JSON_Content_Warnings_Alarm("unknown_category_url")

        exit_url = self.URL_Base_Make(url_this)

        if page != 1:
            exit_url += self.pg_num + str(page)

        if self.host_get_suffics:
            exit_url += self.host_get_suffics

        print("Make :", exit_url)

        return exit_url

#   Листание страниц общей выдачи
    def Pagination(self, start=1, finish=-1):

        bl_full_page = True
        counter_page = start

        while bl_full_page:

            url_ = self.URL_CardsPage_Make(page=counter_page)

            self.page_num = counter_page
            #print(url_)

            html_page = self.Page_Scrape(url_)
            if html_page:
                soup_page = BeautifulSoup(html_page, "html.parser")

                df_cards_page = self.Parse_Cards_Page(soup_page)
                #print(self.df)

                if (not df_cards_page.empty) and (not df_cards_page["Modification_price"].isna().all()):
                #if df_cards_page:
                    self.df = pd.concat([self.df, df_cards_page], ignore_index=True)
                    self.df.to_excel(self.outfile_name)
                else:
                    bl_full_page = False


                if finish < 0:
                    counter_page += 1
                else:
                    if counter_page >= finish:
                        bl_full_page = False
                    else:
                        counter_page += 1

#   Обработка очередной страницы выдачи
    def Parse_Cards_Page(self, soup):

        if soup:
            df_ = pd.DataFrame(columns=list(self.df.columns))

        a = soup.find_all("div", class_="sc-1qkffly-6 wqZpL")

        cards = self.Find_All_Divs("card_div", soup)
        #'js--subcategory-product-item subcategory-product-item product_data__gtm-js  product_data__pageevents-js ddl_product'

        #pprint(cards[0])
        if cards:
            for i, card, in enumerate(cards):
                self.Product_Record_Handler(card)
                for col in self.out_columns:
                    df_.loc[i, col] = self.Fld_Fill(col, card)
                for col in self.addition_fields:
                    df_.loc[i, col] = self.Addition_Fld_Fill(col, card)
                if self.bl_ttx:
                    self.TTX_Handler(df_.loc[i, 'Modification_href'])

        print(df_)

        return df_

#   Обработка полей df  со траницы выдачи
    def Fld_Fill(self, fld, card):

        if fld == 'Name':
            return None
        elif fld == 'Vendor':
            return self.Vendor_Handler(card)
        elif fld == 'Modification_name':
            return self.Modification_Name_Handler(card)
        elif fld == 'Modification_href':
            return self.Modification_Href_Handler(card)
        elif fld == 'Category':
            return self.category
        elif fld == 'Subcategory':
            return self.Subcategory_Handler(card)
        elif fld == 'Date':
            return self.now
        elif fld == 'Modification_price':
            return self.Modification_Price_Handler(card)
        elif fld == 'Cards_page_num':
            return self.page_num
        elif fld == 'Site':
            return self.site

    dict_product_record = {}

    def Product_Record_Handler(self, card):

        soup_product = self.Find_Div("product_div", card)
        self.dict_product_record['Modification_href'] = self.URL_Base_Make(soup_product.find("a").get("href"))
        self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_product.find("a").text)

    def Longstring_Handeler(self, longstring):

        #Категория
        if longstring:
            list_word = longstring.split()
            list_found_cat = list()

            for cat in self.category_params["subcategories"]:
                if cat in longstring.lower():
                    list_found_cat.append((cat, len(cat), len(cat.split())))

            list_found_cat.sort(key=lambda x: x[1], reverse=True)

            try:
                self.dict_product_record["Subcategory"] = list_found_cat[0][0]
            except Exception:
                pass
            try:
                self.dict_product_record["Vendor"] = list_word[list_found_cat[0][2]]

                product_name = ""
                for word in list_word[list_found_cat[0][2]:]:
                    product_name += word + " "
                product_name = product_name[:-1]

            except IndexError:
                print("что-то с именем моим:", longstring)

            return product_name

        else:
            return None

    def Addition_Fld_Fill(self, fld, card):
        return None

    def Vendor_Handler(self, card):
        return self.dict_product_record['Vendor']

    def Modification_Name_Handler(self, card):
        return self.dict_product_record['Modification_name']

    def Modification_Href_Handler(self, card):
        return self.dict_product_record['Modification_href']

    def Subcategory_Handler(self, card):
        return self.dict_product_record['Subcategory']

    def Modification_Price_Handler(self, card):

        soup_price = self.Find_Div("price_div", card)
        if soup_price:
            price = soup_price.text
            exit_ = "".join(re.findall(r'\d', price))
        else:
            exit_ = None

        return exit_

    def TTX_Handler(self, url_):
        pass

# На Request Session и c визможностью find через re.compile
class Parse_Common_by_Request(Parse_Common):

    # Request only
    def Page_Scrape(self, url_):
        return self.Page_Requests(url_)


    # с re
    def Find_All_Divs(self, json_div, soup):

        try:
            arguments = self.teg_card_params[json_div]["attributes"]
            if arguments:
                if "class" in arguments:
                    arguments["class_"] = arguments.pop("class")
                if "re" in self.teg_card_params[json_div]:
                    for i in arguments:
                        arguments[i] = re.compile(arguments[i])
                return soup.find_all(self.teg_card_params[json_div]["teg"], **arguments)
            else:
                return soup.find_all(self.teg_card_params[json_div]["teg"])
        except KeyError:
            print('В JSON нет тега {} для сайта {}'.format(json_div, self.site))
            raise KeyError

    # с re
    def Find_Div(self, json_div, soup):

        try:
            arguments = self.teg_card_params[json_div]["attributes"]
            if arguments:
                if "class" in arguments:
                    arguments["class_"] = arguments.pop("class")
                if "re" in self.teg_card_params[json_div]:
                    for i in arguments:
                        arguments[i] = re.compile(arguments[i])
                return soup.find(self.teg_card_params[json_div]["teg"], **arguments)
            else:
                return soup.find(self.teg_card_params[json_div]["teg"])
        except KeyError:
            print('В JSON нет тега {} для сайта {}'.format(json_div, self.site))
            raise KeyError


class Parse_El(Parse_Common):
    site = "eldorado"

    # Берет название модели с внутренней страницы: там артикул
    def Product_Record_Handler(self, card):

        soup_product = self.Find_Div("product_div", card)
        url_ = soup_product.find("a").get("href")
        self.dict_product_record['Modification_href'] = self.URL_Base_Make(url_)
        internal_page = self.Page_Scrape(self.URL_Base_Make(url_))
        if internal_page:
            soup_internal_page = BeautifulSoup(internal_page, 'html.parser')
            soup_name = self.Find_Div("internal_page_mod_name", soup_internal_page)
            if soup_name:
                self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_name.text)
        else:
            self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_product.find("a").text)

# DNS берет цены со втрой страницы выдачи. Оч медленный но работает
class Parse_DNS(Parse_Common):

    site = "dns"

    def Page_Requests(self, url_):

        cookies = self.site_params["cookies"]

        header = {
            #'Referer': 'https://www.dns-shop.ru/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en;q=0.9',
            'Connection': 'keep-alive',
            # 'Cache-Control': 'max-age=0',
            # 'Host': 'market.yandex.ru',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.1.248 Yowser/2.5 Safari/537.36',
        }
        time.sleep(self.interrupt)
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        #print(url_)
        response = session.get(url_, headers=header)
        #response = requests.get(url_, headers=header)
        response.encoding = 'UTF-8'
        print(url_, response.status_code)
        if response.status_code == 200:
           #session.close()
           return response.text


    def Modification_Price_Handler(self, card):

        url_ = self.Modification_Href_Handler(card)
        page_internal = self.Page_Scrape(url_)
        if page_internal:
            soup_page_internal = BeautifulSoup(page_internal, "html.parser")
            soup_price = self.Find_Div("internal_page_price", soup_page_internal)
            if soup_price:
                price_ = soup_price.get("content")
                exit_ = "".join(re.findall(r'\d', price_))

            return exit_

    def URL_CardsPage_Make(self, url_="", page=1):

        if url_:
            url_this = url_
        else:
            try:
                url_this = self.category_params["url"]
            except KeyError:
                self.JSON_Content_Warnings_Alarm("unknown_category_url")

        exit_url = self.URL_Base_Make(url_this)

        if page != 1:
            exit_url += self.pg_num + unquote(str(page))

        print("Make :", exit_url)

        return exit_url

    def Longstring_Handeler(self, longstring):

        #Категория
        if longstring:
            list_word = longstring.split()
            list_found_cat = list()

            for cat in self.category_params["subcategories"]:
                if cat in longstring.lower():
                    list_found_cat.append((cat, len(cat), len(cat.split())))

            list_found_cat.sort(key=lambda x: x[1], reverse=True)

            try:
                self.dict_product_record["Subcategory"] = list_found_cat[0][0]
            except Exception:
                pass
            try:
                self.dict_product_record["Vendor"] = list_word[list_found_cat[0][2]+1]

                product_name = ""
                for word in list_word[list_found_cat[0][2]+1:]:
                    product_name += word + " "

                product_name += list_word[0]

            except IndexError:
                print("что-то с именем моим:", longstring)

            return product_name

        else:
            return None

# Citilink - качается нормально, но нужно ставить большую задержку. Периодически кидает 479 отлуп
class Parse_CL(Parse_Common):
    site = "citilink"

    def Find_All_Divs(self, json_div, soup):

        try:
            arguments = self.teg_card_params[json_div]["attributes"]
            if arguments:
                if "class" in arguments:
                    arguments["class_"] = arguments.pop("class")
                if "re" in self.teg_card_params[json_div]:
                    for i in arguments:
                        arguments[i] = re.compile(arguments[i])
                return soup.find_all(self.teg_card_params[json_div]["teg"], **arguments)
            else:
                return soup.find_all(self.teg_card_params[json_div]["teg"])
        except KeyError:
            print('В JSON нет тега {} для сайта {}'.format(json_div, self.site))
            raise KeyError

    def Find_Div(self, json_div, soup):

        try:
            arguments = self.teg_card_params[json_div]["attributes"]
            if arguments:
                if "class" in arguments:
                    arguments["class_"] = arguments.pop("class")
                if "re" in self.teg_card_params[json_div]:
                    for i in arguments:
                        arguments[i] = re.compile(arguments[i])
                return soup.find(self.teg_card_params[json_div]["teg"], **arguments)
            else:
                return soup.find(self.teg_card_params[json_div]["teg"])
        except KeyError:
            print('В JSON нет тега {} для сайта {}'.format(json_div, self.site))
            raise KeyError

    def URL_CardsPage_Make(self, url_="", page=1):

        if url_:
            url_this = url_
        else:
            try:
                url_this = self.category_params["url"]
            except KeyError:
                self.JSON_Content_Warnings_Alarm("unknown_category_url")

        exit_url = self.URL_Base_Make(url_this)

        exit_url += self.site_params["host_get_suffics"]

        if page != 1:
            exit_url += self.pg_num + str(page)

        print("Make :", exit_url)

        return exit_url

    def Longstring_Handeler(self, longstring):

        #Категория
        if longstring:
            list_word = longstring.split()
            list_found_cat = list()

            for cat in self.category_params["subcategories"]:
                if cat in longstring.lower():
                    list_found_cat.append((cat, len(cat), len(cat.split())))

            list_found_cat.sort(key=lambda x: x[1], reverse=True)

            try:
                self.dict_product_record["Subcategory"] = list_found_cat[0][0]
            except Exception:
                pass
            try:
                self.dict_product_record["Vendor"] = list_word[list_found_cat[0][2]].title()
                if self.dict_product_record["Vendor"] in ['Hp', 'MSI']:
                    self.dict_product_record["Vendor"] = self.dict_product_record["Vendor"].upper()

                product_name = ""
                for word in list_word[list_found_cat[0][2]:]:
                    product_name += word + " "
                product_name = product_name[:-1]

            except IndexError:
                print("что-то с именем моим:", longstring)

            return product_name

        else:
            return None

# Мвидео Глючит Selenium - то работает то нет. Вместо этого юзать parse_mvideo
class Parse_MV(Parse_Common):
    site = "mvideo"
    addition_fields = [
        'Customer_rate'
    ]
    def URL_Base_Make(self, url_):
        return url_

    def Addition_Fld_Fill(self, fld, card):
        return self.Customer_Rate_Handler(fld, card)

    def Customer_Rate_Handler(self, fld, card):
        soup_rate = self.Find_Div("customer_rate_div", card)
        if soup_rate:
            exit_ = float("".join(re.findall(r'\d', soup_rate.get("style"))))/100
            return exit_
        else:
            return None

    def Product_Record_Handler(self, card):

        soup_product = self.Find_Div("product_div", card)
        self.dict_product_record['Modification_href'] = soup_product.get("href")
        self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_product.text)
        #pprint(self.dict_product_record)

#Не работает да и не надо, видимо
class Parse_YaMa(Parse_Common):
    site = "yama"
    addition_fields = [
        'Name_offers',
        'Modification_offers'
    ]

    level = True

    def Modification_Price_Handler(self, card):

        href_ = self.dict_product_record['Modification_href']
        if 'redir/' not in href_:
            url_ = self.URL_Base_Make(self.dict_product_record['Modification_href'])
            html_page = self.Page_Scrape(url_)
            soup_up_model_page = BeautifulSoup(html_page, "html.parser")

            # Табличка верхня
            soup_table_grey = soup_up_model_page.find('ul', class_="_2CAuvczGU0")
            soup_button_offers = soup_table_grey.find('li', class_="_1OM4gu7kXK _3Kj2EY9ihg")

            soup_offers = soup_button_offers.find('span', class_="yVmxx3-ZVv")

            if self.level:
                self.level = False

                if soup_offers is not None:
                    self.dict_addition_fld['Name_offers'] = soup_offers.text

                else:
                    self.dict_addition_fld['Name_offers'] = 0
                    return 'na'

                url_modifications = soup_table_grey.find('a', {"href": re.compile("mods")}).get('href')
                self.Pagination(self.URL_CardsPage_Make(url_modifications))
                self.level = True

            else:
                url_offers = soup_button_offers.find('a').get('href')
                exit_ = self.Get_Price(soup_up_model_page, url_offers)
                if self.ttx:
                    soup_button_specs = soup_table_grey.find('li', class_="_1OM4gu7kXK _2W_euF-a9B kSWkhB-y4k")
                    url_specs = soup_button_specs.find('a').get('href')
                    self.Get_TTX(url_specs)
                self.dict_addition_fld['Modification_offers'] = soup_offers.text
                return exit_

        else: return None

    def Get_Price(self, soup_page, url_):

        def offers_prices_harvest(offers_href):

            prices_list = list()
            pages_is_ok = True
            page = 1

            url_ = self.URL_Base_Make(offers_href)

            while pages_is_ok == True:

                try:

                    html_page = self.Page_Scrape(url_)
                    offers_page = BeautifulSoup(html_page, 'html.parser')
                    if offers_page.find('a',
                                        class_='button button_size_s button_theme_pseudo n-pager__button-next i-bem n-smart-link') is None:
                        pages_is_ok = False

                    offers_page_table = offers_page.find('div',
                                class_="n-snippet-list n-snippet-list_type_vertical island metrika b-zone b-spy-init b-spy-events i-bem")
                    page_prices = offers_page_table.find_all('div', class_='price')
                    page_price_list = [int(i.text.replace(' ', '').replace('₽', '')) for i in page_prices]
                    prices_list += page_price_list

                except Exception as Err:
                    print(Err)

                page += 1
                url_ = self.URL_Base_Make(offers_href + '&page=' + str(page))

            AvgPrice = prices_list.mean()

            return AvgPrice

        # средняя цена - либо из блока "средняя цена" либо со страницы предложений модели
        def avg_price_harvest(page):

            price_dict = dict()
            # а есть ли боттом c ценами?
            teg_h2 = page.find_all('h2')
            teg_h2_texts = [i.text for i in teg_h2]

            if 'Средняя цена' in teg_h2_texts:
                # Если блок средней цены на странице модели есть
                soup_avg_price = page.find('div', class_="_3TkwCtZtaF")
                avg_price = int(soup_avg_price.find('span').text.replace(' ', '').replace('₽', ''))
            else:
                # тады лезем внутря в список цен, руками:
                avg_price = offers_prices_harvest(url_)
            return avg_price


        return avg_price_harvest(soup_page)

    def Get_TTX(self, url_):
        pass
