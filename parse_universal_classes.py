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
#from requests.packages.urllib3.util.retry import Retry
import re
from urllib.parse import quote, unquote
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import random

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
        if self.scraper == 'selenium':

            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            options.add_argument("--window-size=1920,1080")

            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            #version="108.0.5359.71"
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

        #try:
        #    options = webdriver.ChromeOptions()
        #    for option in self.site_params["host_options"]:
        #        options.add_argument(option)
        #except Exception:
        #    print("Site Options", Exception)


        #driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

        self.driver.get(url_)
        try:
            element = WebDriverWait(self.driver, 5).\
                until(EC.presence_of_element_located((By.CLASS_NAME, "product-min-price__current")))
        except Exception:
            pass
        finally:
            exit_ = self.driver.page_source

        if not exit_:
            time.sleep(3)
            self.Page_webdriver(url_)

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
        #retry = Retry(connect=3, backoff_factor=1)
        #adapter = HTTPAdapter(max_retries=retry)
        #session.mount('http://', adapter)
        #session.mount('https://', adapter)

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

        #a = soup.find_all("div", class_="sc-1qkffly-6 wqZpL")

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
                return longstring

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
            print(exit_)
        else:
            exit_ = None
            print(exit_)

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
    # def Product_Record_Handler(self, card):
    #
    #     soup_product = self.Find_Div("product_div", card)
    #     url_ = soup_product.find("a").get("href")
    #     self.dict_product_record['Modification_href'] = self.URL_Base_Make(url_)
    #     internal_page = self.Page_Scrape(self.URL_Base_Make(url_))
    #     if internal_page:
    #         soup_internal_page = BeautifulSoup(internal_page, 'html.parser')
    #         soup_name = self.Find_Div("internal_page_mod_name", soup_internal_page)
    #         if soup_name:
    #             self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_name.text)
    #     else:
    #         self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_product.find("a").text)
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

# DNS
class Parse_DNS(Parse_Common):

    site = "dns"

    def Page_Webdriver(self, url_):

        #try:
        #    options = webdriver.ChromeOptions()
        #    for option in self.site_params["host_options"]:
        #        options.add_argument(option)
        #except Exception:
        #    print("Site Options", Exception)


        #driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

        self.driver.get(url_)
        # try:
        #     element = WebDriverWait(self.driver, 5).\
        #         until(EC.presence_of_element_located((By.CLASS_NAME, "product-min-price__current")))
        # except Exception:
        #     pass
        # finally:
        time.sleep(self.interrupt)
        exit_ = self.driver.page_source

        if not exit_:
            time.sleep(3)
            self.Page_webdriver(url_)

        return exit_

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
        #retry = Retry(connect=3, backoff_factor=1)
        #adapter = HTTPAdapter(max_retries=retry)
        #session.mount('http://', adapter)
        #session.mount('https://', adapter)

        #print(url_)
        response = session.get(url_, headers=header)
        #response = requests.get(url_, headers=header)
        response.encoding = 'UTF-8'
        print(url_, response.status_code)
        if response.status_code == 200:
           #session.close()
           return response.text

    def Product_Record_Handler(self, card):

        soup_product = self.Find_Div("product_div", card)
        self.dict_product_record['Modification_href'] = self.URL_Base_Make(soup_product.get("href"))
        self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_product.find("span").text)

    def Modification_Price_Handler(self, card):

        # url_ = self.Modification_Href_Handler(card)
        # page_internal = self.Page_Scrape(url_)
        # if page_internal:
        #     soup_page_internal = BeautifulSoup(page_internal, "html.parser")
        #     soup_price = soup_page_internal.find('span', class_="product-card-price__current product-card-price__current_active")
        #     if soup_price:
        #         price_ = soup_price.text
        #         exit_ = "".join(re.findall(r'\d', price_))
        #
        #     return exit_

        soup_price = self.Find_Div("price_div", card)
        if soup_price:
            # try:
            #     action_price = soup_price.find('div', class_="product-min-price__min")
            #     price_ = action_price.find('mark', class_="product-min-price__min-price").text
            # except Exception:
            price_prev = None
            try:
                price_prev = soup_price.find('span', class_="product-buy__prev").text
            except Exception:
                pass
            price_ = soup_price.text
            if price_prev:
                price_ = price_.replace(price_prev, "")

            exit_ = "".join(re.findall(r'\d', price_))

        else:
            exit_ = None

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

# Citilink - качается нормально, но нужно ставить большую задержку.
class Parse_CL(Parse_Common):
    site = "citilink"

    def Product_Record_Handler(self, card):

        soup_product = self.Find_Div("product_div", card)
        #self.dict_product_record['Modification_href'] = soup_product.find("a").get("href")
        #self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_product.find("a").text)
        self.dict_product_record['Modification_href'] = self.URL_Base_Make(soup_product.find("a").get("href"))
        self.dict_product_record['Modification_name'] = self.Longstring_Handeler(soup_product.find("a").get('title'))


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

class Parse_Ya(Parse_Common):
    site = "yama"

    def __init__(self,
                 category, #категория продуктов
                 scraper, # [requests, selenium],
                 ttx=False, #надо ли скачивать характеристики
                 pagination_start=1,
                 pagination_finish=-1,
                 interrupt=5,
                 num_outfile=1, #Дополнительный номер версии выходного файла
                 user_id=0,
                 user_id_rewrite=False
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

        self.user_id = user_id

        if self.scraper == 'selenium':

            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            if self.user_id == 0:
                pass
            else:
                options.add_argument("--window-size=1820,1080")
                #options_dict = self.Make_user(user_id_rewrite)
                try:
                    #str_user_agent = '--user-agent="' + options_dict['user_agent'] + '"'
                    #options.add_argument(str_user_agent)
                    options.add_argument(r"--user_data_dir=C:\Users\shulya403\AppData\Local\Google\Chrome\User Data")
                    options.add_argument(r"--profile-directory=Default")
                except Exception:
                    pass
                # try:
                #     #print(options_dict['cookies'])
                #     #cookies = pickle.load(open(options_dict['cookies'], "rb"))
                #     #for cookie in cookies:
                #         #print(cookie)
                #         #self.driver.add_cookie(cookie)
                #
                # except Exception:
                #     pass

            #options.add_argument('--user-agent="Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.99 Safari/533.4 ChromePlus/1.4.1.0alpha1"')
            #options.add_argument('--user-agent="Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Chrome/5.0.336.0 Safari/533.1 ChromePlus/1.3.8.1"')
            #options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.30 (KHTML, like Gecko) Comodo_Dragon/12.1.0.0 Chrome/12.0.742.91 Safari/534.30"')

            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def Make_user(self, user_id_rewrite):


        if self.user_id == 0:
            pass
        else:
            users_df = pd.read_excel('Users_id/users_id.xlsx', index_col='ID')
            if self.user_id in users_df.index:

                user_agent = users_df.loc[self.user_id]['User_agent']

                print(user_agent)
            else:
                user_agent = self.Get_user_agent_file()
                new_row = pd.Series({'User_agent': user_agent}, name=self.user_id)
                print(new_row)
                users_df = users_df.append(new_row, ignore_index=False)
                print(users_df)
                #users_df.loc[self.user_id]['User_agent'] = user_agent
                users_df.to_excel('Users_id/users_id.xlsx')
                input()

            #cookie = self.Make_cookie_file(id=self.user_id, ua=user_agent, rewrite=user_id_rewrite)

        return {
            'user_agent': user_agent,
            'cookies': None
        }
    def Get_user_agent_file(self):
        df_ = pd.read_excel('Users_id/user_agents.xlsx')
        df_chrome = df_[(df_['Ok'] == 1) & (df_['User-Agents'].str.contains('Chrome', regex=False))]

        random.seed()

        return df_chrome.iloc[random.randint(0, len(df_chrome)-1)]['User-Agents']


    def Make_cookie_file(self, id, ua, rewrite):

        str_filename = 'Users_id/cookies_' + str(id) + '.pkl'

        if rewrite:
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get('https://yandex.ru')
            str_user_agent = '--user-agent="' + ua + '"'
            options.add_argument(str_user_agent)
            print('>>>')
            input()
            pickle.dump(driver.get_cookies(), open(str_filename, "wb"))

        return str_filename


    def Page_Webdriver(self, url_):

        #try:
        #    options = webdriver.ChromeOptions()
        #    for option in self.site_params["host_options"]:
        #        options.add_argument(option)
        #except Exception:
        #    print("Site Options", Exception)


        #driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

        self.driver.get(url_)
        exit_ = self.driver.page_source
        if not exit_:
            time.sleep(3)
            self.Page_webdriver(url_)
        try:
            elem_title = self.driver.find_element_by_tag_name("title")
            if "Ой!" in elem_title._parent.title:
                input()
                exit_ = self.driver.page_source
        except Exception:
            pass
        return exit_

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

    def Pagination(self, start=1, finish=-1, vendors=[]):
#TODO: vendors_list
        if vendors:
            dict_vendors = dict()
            for ven_ in vendors:
                dict_vendors[ven_] = self.category_params["url"][ven_]
        else:
            dict_vendors = self.category_params["url"]
        for ven in dict_vendors:
            self.this_vendor = str(ven)
            print(str(ven))
            self.this_url = dict_vendors[str(ven)]

            counter_page = start

            bl_full_page = True

            while bl_full_page:


                url_ = self.URL_CardsPage_Make(url_=self.this_url, page=counter_page)

                self.page_num = self.this_vendor + "_" + str(counter_page)
                #print(url_)

                html_page = self.Page_Scrape(url_)
                self.Page_Into_View_Run()
                html_page = self.driver.page_source

                if html_page:
                    soup_page = BeautifulSoup(html_page, "html.parser")
                    elem_button_forward = soup_page.find("span", class_="_3e9Bd")
                    if not elem_button_forward:
                        bl_full_page = False

                    df_cards_page = self.Parse_Cards_Page(soup_page)
                    #print(self.df)

                    if (not df_cards_page.empty) and (not df_cards_page["Modification_price"].isna().all()):
                    #if df_cards_page:
                        self.df = pd.concat([self.df, df_cards_page], ignore_index=True)
                        xl_writer = pd.ExcelWriter(self.outfile_name, engine='xlsxwriter', options={'strings_to_urls': False})
                        self.df.to_excel(xl_writer)
                        xl_writer.close()

                    else:
                        bl_full_page = False

                    if finish < 0:
                        counter_page += 1
                    else:
                        if counter_page >= finish:
                            bl_full_page = False
                        else:
                            counter_page += 1
                    if not bl_full_page:
                        print("финиш ", self.this_vendor)

    def Page_Into_View_Run(self):

        count_divs = 0
        while True:
            #count_divs < 48:
            elem_card = self.driver.find_elements_by_tag_name("article")
            if count_divs == len(elem_card):
                break
            count_divs = len(elem_card)
            elem_card[count_divs - 1].location_once_scrolled_into_view
            print(count_divs)
            time.sleep(5)

    def URL_CardsPage_Make(self, url_="", page=1):

        if url_:
            exit_url = url_
        else:
            return None
        # else:
        #     try:
        #         url_this = self.category_params["url"]
        #     except KeyError:
        #         self.JSON_Content_Warnings_Alarm("unknown_category_url")
        if page != 1:
            exit_url += self.pg_num + str(page)

        if self.host_get_suffics:
            exit_url += self.host_get_suffics

        print("Make :", exit_url)

        return exit_url
    def Longstring_Handeler(self, longstring):

        #Категория
        self.dict_product_record["Vendor"] = self.this_vendor
        self.dict_product_record["Subcategory"] = ""
        if longstring:

            return longstring
        else:
            return None

        #   Обработка очередной страницы выдачи

    def Parse_Cards_Page(self, soup):

            if soup:
                df_ = pd.DataFrame(columns=list(self.df.columns))

            # a = soup.find_all("div", class_="sc-1qkffly-6 wqZpL")
            #time.sleep(5)

            cards = self.Find_All_Divs("card_div", soup)
            # 'js--subcategory-product-item subcategory-product-item product_data__gtm-js  product_data__pageevents-js ddl_product'
            print("len cards -> ", len(cards))
            # pprint(cards[0])
            if cards:
                #elem_card = self.driver.find_elements_by_tag_name("article")
                #print(len(elem_card))
                for i, card in enumerate(cards):
                    #elem_card[i].location_once_scrolled_into_view
                    #time.sleep(1)
                    self.Product_Record_Handler(card)
                    for col in self.out_columns:
                        df_.loc[i, col] = self.Fld_Fill(col, card)
                    if self.bl_ttx:
                        self.TTX_Handler(df_.loc[i, 'Modification_href'])

            print(df_)

            return df_