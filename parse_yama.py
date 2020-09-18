# парсинг Yandex.Market по категооиям товара
# class Yama_parsing_const - класс с глобальными переменными
#   - dict ya_cookies - cookie market.yandex.ru
#   - def header_(self, referer) - headers market.yandex.ru. referer - динмически формируерумый реферер-пэйдж
# class Parse_links() - класс-наследник Yama_parsing_const
#   def links_to_excel(self, category, folder='Price_link_list/') вызывная функция считывания линков на
#       category из dict self.Categories
# class Parse_models: - класс-наследник Yama_parsing_const
#


import requests
from pprint import pprint
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
from urllib.parse import quote
import re
#from grab import Grab
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Yama_parsing_const(object):
    def header_(self, referer=""):

        header = {
            #'Referer': referer,
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #'Accept-Encoding': 'gzip, deflate, br',
            #'Accept-Language': 'ru,en;q=0.9',
            #'Connection': 'keep-alive',
            #'Cache-Control': 'max-age=0',
            #'Host': 'market.yandex.ru',
            #'Sec-Fetch-Mode': 'navigate',
            #'Sec-Fetch-Site': 'none',
            #'Sec-Fetch-User': '?1',
            #'Upgrade-Insecure-Requests': '1',
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.1.248 Yowser/2.5 Safari/537.36',



            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'yandexuid=7149064641575729573; _ym_uid=1575729574981578479; mda=0; my=YwA=; yuidss=7149064641575729573; ymex=1897042421.yrts.1581682421; gdpr=0; settings-notifications-popup=%7B%22showCount%22%3A3%2C%22showDate%22%3A18335%7D; mOC=1; oMaSefD=1; oMaSpfD=1; oMaRefD=1; oMaPrfD=1; oMaSofD=1; oMaFifD=1; lkOb=1; userAchievements=1; L=aVYCU3BGalJWdHB0TU5IQW1Je1NifFFBIh4kKwU7DjcLFA==.1590424699.14245.371513.b12c4e50cbbe7c513c403938b0780de8; yandex_login=dmschulgin; currentRegionId=213; currentRegionName=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%83; utm_campaign=user_achievements; utm_medium=trigger; utm_source=email; yandex_gid=213; Session_id=3:1592420589.5.0.1590424699783:zTv8bQ:85.1|919128238.0.2|218643.696677.ylsT5_nV4vqg5lSfVN325vu8v5o; sessionid2=3:1592420589.5.0.1590424699783:zTv8bQ:85.1|919128238.0.2|218643.303202.0-6EEDutomK6Y3cKB6XwHuSPdkQ; i=3a1PDCS2PLjIhjqs5B/DVWeEqNbQnK+pffovbMdn9Y5tgdBB1s3+yXPN7r2s9Hk37BLTlP9qhJco/62Xwg1MPcvLeR4=; zm=m-white_bender.webp.css-https%3As3home-static_Go1ex5WQ3bRjxW6Ci7rLgizqklc%3Al; yp=1891690763.multib.1#1902540787.sad.1578091434%3A1587180787%3A9#1607588489.szm.1_5%3A1280x720%3A1218x618#1905784699.udn.cDpEZXBlY2hlNDAz#1592427826.zmblt.1629#1592427826.zmbbr.chrome%3A83_0_4103_97#1595010714.ygu.1#1595100415.csc.2; _ym_d=1592637990; _ym_isad=2; yc=1592897192.zen.cach%3A1592641566; yabs-frequency=/5/100X09-jrbvgsCTU/tVfoS000002yEq7i-N9m00000BmxGGZfFMq00000i3j7uFHoS000002mEqVQz79m00000B0xH-jKi7000000l3iW/; _ym_visorc_10630330=w; uid=AABcEl7txFMG6QB6CiRyAg==; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; spravka=dD0xNTkyNjQwNjI0O2k9MTA5LjI1Mi41OS4yMDU7dT0xNTkyNjQwNjI0NjU5MTE0MDMxO2g9MjQzZWViN2ZlMGI3MTM4ZDBlMDIzZDg1ZDIzOTlhMmE=; skid=9925283531592640624; visits=1579356538-1591128012-1592640624; parent_reqid_seq=23a3d15bae7cb97d45c13dd69bed6269; js=1; dcm=1; _ym_visorc_160656=b; _ym_visorc_45411513=b; first_visit_time=2020-06-20T11%3A10%3A30%2B03%3A00; HISTORY_AUTH_SESSION=a4de0c08; yandexmarket=48; fonts-loaded=1; ugcp=1; oCnCPoS=1; ys=wprid.1592425950904923-80431522882309962600251-production-app-host-sas-web-yp-188#ymrefl.085DDB54FF3551ED; _ym_visorc_11859922=b; cycada=7PVD5wgZSTj/kLF/oQzN6FVNugMpxQqr2hJTlPqWlEk=',
            'Host': 'market.yandex.ru',
            'Referer': referer,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
        }

        return header

    ya_cookies = {
        '_ym_uid': '1575729574981578479',
        'mda': '0',
        'my': 'YwA=',
        'categoryQA': '1',
        'L': 'UWh6d11wUglKWURxVwJKY29/YXNDW2B4IAMqGSkvWi4oDA==.1576330582.14079.396207.a95d6af3485906fe3a5b85ad5e96aae2',
        'yandex_login': 'dmschulgin',
        'yandexuid': '7149064641575729573',
        'yuidss': '7149064641575729573',
        'currentRegionId': '213',
        'currentRegionName': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%83',
        'settings-notifications-popup': '%7B%22showCount%22%3A2%2C%22showDate%22%3A18280%7D',
        'ymex': '1896226411.yrts.1580866411',
        'zm': 'm-white_bender.webp.css-https%3As3home-static_AcrZ-E5XMfrfMIo1gDHPnVN4AdI%3Al',
        'i': 'f84xXe5i+RDS9ZAAcaeRW6dGVcK3pWOh3j9tHolXBj+4D5wJJOYr2Po2Fq9YoOzQbtqNrKdmeuMJECkYhMP95GcEEWM=',
        'yandex_gid': '213',
        'yc': '1581711296.zen.cach%3A1581455687',
        '_ym_d': '1581452810',
        'yabs-frequency': '/4/1W0203IoGLu2415U/ht2mSBWv8L21FcsqEITwyZrje3ad/',
        'skid': '5043396831581538418',
        '_ym_isad': '2',
        'cycada': 'tSzluWir/d0SzOW2g4oBs3aLNKnxzLvG+Evc76owb0I=',
        'Session_id': '3:1581643106.5.0.1576330582444:rTr8bQ:86.1|919128238.0.2|212505.744792.ZdacW_cOsLYLzTuP8fcaSDzt8Zs',
        'sessionid2': '3:1581643106.5.0.1576330582444:rTr8bQ:86.1|919128238.0.2|212505.224397.B1p8konycmHsBJLQ1AWZJJ_Cwkg',
        'yp': '1612402412.cld.2270452#1612402412.brd.6158003823#1896394830.sad.1581034830:1581034830:1#1584922830.hks.0#1597131741.szm.1_5:1280x720:1166x626#1581968565.zmblt.1505#1581968565.zmbbr.yandexbrowser:20_2_1_248#1584044087.ygu.1#1581696462.gpauto.55_713436:37_730183:200:1:1581689262',
        'visits': '1575841847-1579550934-1581689499',
        'uid': 'AABcEl5Gqpsw4AC4BLSWAg==',
        'js': '1',
        'dcm': '1',
        '_ym_visorc_160656': 'b',
        '_ym_visorc_45411513': 'b',
        'first_visit_time': '2020-02-14T17%3A11%3A43%2B03%3A00',
        'yandexmarket': '48',
        'fonts-loaded': '1',
        'ugcp': '1',
        'ys': 'def_bro.0#svt.1#wprid.1581682415557470-933073134786648878600067-vla1-1933#ybzcc.ru',
        'parent_reqid_seq': '4443e96de0ca39b438700c542afbd754%2C9167d730c4966f0d74a8f0e36206d2ac%2C22e8d508c3661ec4b41e9cce6d85bde9',
        'viewtype': 'list'
     }

    ya_cookies2 = { #June 2020
        'fuid01': '5187dbf37aa46e29.1ea1yXg4LdRzObB-t-8Dp5ZUsvvynIX2NMEmQLT2IN-oQI6OGq1Q1nQsrKPOUPER2HtMsOB-p4AP9QnjF1SvJNe86JHPbTw1UraJwGiQHBkyb1gxs7EDw7LMnv5Ylc1s',
        'markethistory': '<h><c>6427101</c><c>432460</c><m>11151827</m><m>10630837</m><m>11142972</m><m>10993382</m><m>12174379</m><m>12174345</m><m>12325200</m><m>11874413</m><m>12393964</m><m>10853777</m><m>12408317</m><m>8293471</m><m>10771048</m><m>10771049</m><m>11851436</m><m>10540949</m><m>12221853</m><m>12174590</m><m>12143640</m><m>12253940</m><m>10541564</m><m>12334353</m><m>12254049</m><m>12253336</m><m>12253311</m><m>12285506</m><m>12285898</m><m>10469466</m><m>11007864</m><m>10469292</m><cm>6427101-11131792</cm><cm>6427101-11547576</cm><cm>6427101-10846379</cm><cm>106905-10467479</cm><cm>432460-11151827</cm><cm>432460-10630837</cm><cm>432460-11142972</cm></h>', 
        'yandexuid': '703207661367760751',
        'deliveryincluded': '1', 
        'in-stock': '1', 
        '_ym_uid': '1471966800285541158', 
        'my': 'YwA=',
        'head-banner-sovetnik-info': '%7B%22closingCounter%22%3A0%2C%22showingCounter%22%3A46%2C%22shownAfterClicked%22%3Afalse%2C%22isClicked%22%3Afalse%7D',
        'head-banner-sovetnik': '%7B%22closingCounter%22%3A0%2C%22showingCounter%22%3A39%2C%22shownAfterClicked%22%3Afalse%2C%22isClicked%22%3Afalse%7D',
        'yandexmarket': '48%2CRUR%2C1%2C%2C%2C%2C2%2C0%2C0%2C213%2C0%2C0%2C12%2C0',
        'head-banner': '%7B%22closingCounter%22%3A0%2C%22showingCounter%22%3A3067%2C%22shownAfterClicked%22%3Afalse%2C%22isClicked%22%3Afalse%7D',
        'onstock': '1',
        '_ym_uid': '1471966800285541158',
        '_ym_d': '1564318515',
        'mda': '0',
        'novelty-badge-filter-payments': '-1',
        'yuidss': '703207661367760751',
        'ymex': '1896274612.yrts.1580914612',
        'gdpr': '0',
        'settings-notifications-popup': '%7B%22showCount%22%3A8%2C%22showDate%22%3A18347%7D',
        'yandex_gid': '213',
        'Session_id': '3:1592317752.5.0.1592317752935:hL7Q1Q:4.1|919128238.0.2|218587.137711.eI201Q3JDCA7S3vObX-pVuCPJrs',
        'sessionid2': '3:1592317752.5.0.1592317752935:hL7Q1Q:4.1|919128238.0.2|218587.7201.eUkY7WWVJAgDa81WAyRWnkPswds',
        'L': 'SVUEeFJIcF1DfXQDXU57e3Z5d0BTV295HTQ5W1ADNTQuNA==.1592317752.14267.358974.04707b2dc1e7cf2f93fce4c6301755d5',
        'yandex_login': 'dmschulgin',
        'yp': '1606498676.dswa.0#1606498676.dsws.17#1606498676.dwbrowsers.14#1889454231.multib.1#1603200819.p_cl.1571664819#1617974648.p_sw.1586438647#1892478330.sad.1558446390%3A1577118330%3A7#1597097547.szm.1:1680x1050:1612x947#1606498676.wzrd_sw.1574962675#1896274612.yrts.1580914612#1594889402.ygu.1#1907677752.udn.cDpEZXBlY2hlNDAz',
        'i': '4Q+gUAiKOpqpQo+9q3Htep8kJLBDcg3p8vG1BkaPw7Gl/nvLmsFQIlp8lr37ANYaXSElkfu9P1sXwZ4V5PZuj97guIc=',
        'zm': 'm-white_bender-more-js.webp.css-https%3As3home-static_Go1ex5WQ3bRjxW6Ci7rLgizqklc%3Al',
        '_ym_isad': '2',
        'yabs-frequency': '/4/1m0w0Rdaw5uuZ7nU/tVfoSBGx8UpvSd2qEo7Wz79mh3idslHoSAmx9_Hoi72qEo1GSB1mj3j03DSlRhGx83dhAswqEo0O8APkj3iWorImSBGx87bAi72qEo07Lh1mj3iWrphqRRGxGBzPi72rEu02xasmSBGx8DPOi72qEq2ouN9mj3j055QmSBGx8BQ5Sd2rEs01rL6mSBGxO07____8LB1mx3LW35ImSEmr81HKi73iDM0CLB3y_ForLB1m-3M0V52mSFWrGBQ4S73uDK01U4YmSEmr81HKi73iDI0NLB1mx3KW622aREmrO07uLB1mx3KW55ImSEmr805_LB1mx3MWmj3WREmrW0DKi73iDO2KIB1mx3KWaKYmSEmr8958i73izJH0xanCi73iD800D82OR-mq03RWN6piDI25rDHi-3LWs3YORFW0/',
        'yc': '1592744080.zen.cach%3A1592330153', 
        'cycada': 'AZpzKKoHFG4jzWncWtHALg/4F3IorNFjwqgm/Ez16Ow=',
        'uid': 'AABixV7rcISEVQB6Bb0hAg==',
        '_ym_visorc_10630330': 'b',
        'SL_GWPT_Show_Hide_tmp': '0',
        'SL_wptGlobTipTmp': '1',
        'spravka': 'dD0xNTkyNDg4MTAxO2k9MjEzLjIwOC4xOTAuMTMyO3U9MTU5MjQ4ODEwMTcwNzIzOTg4NjtoPWFkMzA0NmIyOWRlNjRmNjEwMTUwMTEzNzQ1OTI0MjVi',
        'skid': '8584706041592488101',
        'visits': '1532526818-1585219412-1592488101',
        'js': '1',
        'dcm': '1',
        '_ym_visorc_160656': 'b',
        '_ym_visorc_45411513': 'b',
        'currentRegionId': '213',
        'currentRegionName': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%83',
        'mOC': '1',
        'first_visit_time': '2020-06-18T16%3A48%3A23%2B03%3A00',
        'fonts-loaded': '1',
        'ugcp': '1',
        'oMaSefD': '1',
        'oMaSofD': '1',
        'oMaFifD': '1',
        'lkOb': '1',
        '_ym_visorc_26812653': 'b',
        'parent_reqid_seq': '58e752ba79263232137d658a47cb042c%2Cb3dcea808aa59995b9111e2894d4caf2%2Ccdb0b17cc793ec809ed3ddc37007a4fb',
        '_ym_d': '1592488272',
        #'HISTORY_AUTH_SESSION': '1f384434'

    }

    #host name
    host = 'https://market.yandex.ru'

    #добавка к адресу выдачи списка моделей
    link_tail = '&onstock=1&local-offers-first=0'

    #головная ссылка раздела "Компьютерная техника"
    link_computers = 'https://market.yandex.ru/catalog--kompiuternaia-tekhnika/54425'

    # кнопка "Вперед" на страницах выдачи списков моделей <a> class
    #a_button_eol = 'button button_size_s button_theme_pseudo n-pager__button-next i-bem n-smart-link'
    a_button_eol = '_2prNUdeCKH _3OFYTyXi90'

    # строки таблицы моделей (по 48 на страницу обычно) Div class
    #div_row_models_ls = 'n-snippet-card2 i-bem b-zone b-spy-visible b-spy-events'
    div_row_models_ls = '_1OAvzJPfIW'

    # Название модели на страницы выдачи h3 class
    #h3_model_name = 'n-snippet-card2__title'
    h3_model_name = '_3dCGE8Y9v3 cLo1fZHm2y'

    # Табличка верхняя серая на странице модели ul class
   # ul_table_gray = 'n-product-tabs__list'
    ul_table_gray ="_2CAuvczGU0"

    # Плашка 'цены' в серой табличке на странице модели li class
    #li_offers = 'n-product-tabs__item n-product-tabs__item_name_offers'
    li_offers = "_1OM4gu7kXK _3Kj2EY9ihg"

    # Число на плашке 'цены' (Количество предложений) на странице модели span class
    #span_offers = 'n-product-tabs__count'
    span_offers = "yVmxx3-ZVv"

    # Плашка 'характеристики' в серой табличке на странице модели li class
    #li_spec = 'n-product-tabs__item n-product-tabs__item_name_spec'
    li_spec = "_1OM4gu7kXK _2W_euF-a9B kSWkhB-y4k"

    # Максимальная и минимальная цена в нижнем блоке "средняя цена" на странице модели div class
    div_price_minmax = '_1S8ob0AgBK'

    # Средняя цена в блоке "средняя цена" на странице модели div class
    div_price_avg = '_3TkwCtZtaF'

    # Цена из верхного блока если цена только одна на странце модели  div
    div_price_alone = 'n-product-price-cpa2__price'

    # Таблица с ценами на очередной странице выдачи внутри предложений (модификаций) модели div class
    div_config_prices_table = 'layout layout_type_maya'

    # Таблица характеристик (ТТХ) на странице Харктистик модели
    div_ttx_table = 'layout__col layout__col_size_p75 n-product-spec-wrap'

    #Название характеристики (ТТХ) на странице Харктистик модели
    span_spec_name = 'n-product-spec__name-inner'

    # Значение характеристики (ТТХ) на странице Харктистик модели
    span_spec_value = 'n-product-spec__value-inner'


    Categories = {
        'Ноутбук': {
            'url': 'https://market.yandex.ru/catalog--noutbuki/54544/list?hid=91013',
            'category': ['Ноутбук',
                         'Ноутбук игровой',
                         'Игровой ноутбук',
                         'Ультрабук'],
            'ttx_file': 'Ноутбук--характеристики.xlsx',
            'ttx_mod_file': 'Ноутбук-Мод-характеристики.xlsx'

        },
        'Монитор': {
            'url': 'https://market.yandex.ru/catalog--monitory/54539/list?hid=91052',
            'category': ['Монитор'],
            'ttx_file': 'Монитор--характеристики.xlsx'
        },
        'Проектор': {
            'url': 'https://market.yandex.ru/catalog--multimedia-proektory/60865/list?hid=191219',
            'category': ['Проектор',
                         'Карманный проектор'],
            'ttx_file': 'Проектор--характеристики.xlsx'
        },
        'ИБП': {
            'url': 'https://market.yandex.ru/catalog--istochniki-bespereboinogo-pitaniia/59604/list?hid=91082',
            'category': ['Интерактивный ИБП',
                         'Резервный ИБП',
                         'ИБП с двойным преобразованием'
                         ],
            'ttx_file': 'ИБП--характеристики.xlsx'
        }
    }
    TTX_files_folder = 'TTX_files/'

class Req(object):
    def __init__(self):

        self.text = ''
        self.status_code = 400

        #self.requests(url, headers, cookies)

        # options = webdriver.ChromeOptions()
        # options.add_argument('user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome\\User Data')
        # #driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options)
        # # options.add_argument('--headless')
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("user-data-dir=selenium")
        #
        # # "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
        #
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def requests(self, url, **kwargs):

        response = requests.get(url, **kwargs)

        self.status_code = response.status_code
        self.text = response.text


    def selenium(self, url, **kwargs):

        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument("user-data-dir=selenium")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        try:
            driver.get(url)
            # cook = driver.get_cookies()
            # print(cook)
            if "Ой!" in driver.page_source:
                cap=input()
            self.text = driver.page_source

            #driver.close()
        except Exception:
            #driver.close()
            time.sleep(1)
            self.selenium(url)

        if not self.text:
            time.sleep(3)
            self.selenium(url)
        else:
            self.status_code = 200


    #Скачивание линков на модлеи по категориям
class Parse_links(Yama_parsing_const):


    #скачивание линков на страницы модели по категории
    def parse_links(self, category):

        url = self.Categories[category]['url']
        category_ls = self.Categories[category]['category']


        models_list = list()  # список словарей с моделями с названиеми и ссылками на модели

        response = Req()

        page = 1  # номер страницы выдачи

        pages_full = True  # есть ли целевой контент на очередной странице
        while pages_full:
            if page > 1:
                page_url = url + '&page=' + str(page) + self.link_tail

                if page == 2:
                    referer_ = url + self.link_tail

                else:
                    referer_ = url + '&page=' + str(page - 1) + self.link_tail
            else:
                page_url = url + self.link_tail
                referer_ = self.link_computers

            #response = Req()
            #response.requests(page_url, headers=self.header_(referer_))
            response.selenium(page_url)

            if response.status_code == 200:
            #if gr_.response.code == 200:
                print('поехали ', page_url)
                iter_page_soup = BeautifulSoup(response.text, 'html.parser')
                print(iter_page_soup.title)

                # Пречень блоков моделей (строк таблицы) на очередной странице выдачи
                rows_models = iter_page_soup.find_all('div', class_=self.div_row_models_ls)

                if len(rows_models) != 0:
                    print(page, len(rows_models))

                    for row in rows_models:
                        # И рассовыем их по ключам словаря model_dict
                        model_dict = dict()
                        try:
                            model_link = row.find('h3', class_=self.h3_model_name).find('a')
                            # Отсеиваем редирект на внешние сайты или конкретные конфиги нутбуков и останавливаем работу
                            if ('redir/' in model_link) or \
                                    ((category == 'Ноутбук') and ('/' in model_link.text)):
                                pages_full = False
                                break

                            if model_link:
                                model_dict['Href'] = model_link['href']  # ссылка на страницу модели

                            # Ищем название категории
                            category_len = 0

                            for cat in category_ls:
                                if cat in model_link.text:
                                    category_len = len(cat.split())
                                    try:
                                        old_len = len(model_dict['Category'].split())
                                        if category_len > old_len:
                                            model_dict['Category'] = cat
                                    except Exception:
                                        model_dict['Category'] = cat


                                    #break


                            name = model_link.text.split()

                            # Ищем имя вендора (следующее за категорией)
                            model_dict['Vendor'] = name[category_len]

                            #Формируем название модели вместе с имненм вендора через пробел кроме последнего пробела
                            mod_name = ''
                            for word in name[category_len:]:
                                mod_name += word + ' '
                            model_dict['Name'] = mod_name[:-1]

                        except AttributeError:
                            model_dict['Name'] = ""
                            model_dict['Href'] = ""
                            model_dict['Vendor'] = ""
                            model_dict['Category'] = ""

                        # Пихаем словарь модели в общий список
                        print(model_dict['Name'])
                        models_list.append(model_dict)

                    # Проверяем не последняя ли страница выдачи
                    if iter_page_soup.find('a', class_=self.a_button_eol) is None:
                        pages_full = False

                    page += 1

                else:
                    capcha_quest = iter_page_soup.find('title')

                    if capcha_quest.text == 'Ой!':
                        print(page, 'облом - капча')
                        time.sleep(1)
                    else:
                        print(page, 'фигня какая-то')
                        break

                time.sleep(1)
            else:
                print('облом... ', response.status_code)

        return models_list

    #запихиваем линки на модели в эксель. Вызывная функция парсинга
    def links_to_excel(self, category, folder='Price_link_list/'):

        parsed_links__ls = self.parse_links(category)

        print(len(parsed_links__ls))
        df = pd.DataFrame(parsed_links__ls)
        df.drop_duplicates(subset=['Name'], inplace=True)
        print(len(df))

        now = datetime.now().strftime('%b-%y----%d--%H-%M')
        excel_file_name = folder + 'Cсылки ' + category + ' ' + now + '.xlsx'

        df.to_excel(excel_file_name)

class Parse_models(Yama_parsing_const):

    # Считывание цен из предложений
    def offers_prices_harvest(self, offers_href, ref_href):

        prices_list = list()

        page_href = offers_href
        #new_ref_href = ref_href

        pages_is_ok = True
        page = 1

        while pages_is_ok == True:
            try:
                response = requests.get(page_href, headers=self.header_(), cookies=self.ya_cookies)
                if response.status_code == 200:
                    offers_page = BeautifulSoup(response.text, 'html.parser')
                    if offers_page.find('a', class_=self.a_button_eol) is None:
                        pages_is_ok = False

                    offers_page_table = offers_page.find('div', class_=self.div_config_prices_table)

                    page_prices = offers_page_table.find_all('div', class_='price')

                    page_price_list = [int(i.text.replace(' ', '').replace('₽', '')) for i in page_prices]
                    #print(page_price_list)

                    prices_list += page_price_list

                else:
                    print("status code: ", response.status_code)

            except Exception as Err:
                print(Err)

            page += 1
            #new_ref_href = page_href
            page_href = offers_href + '&page=' + str(page)

        price_dict = dict()
        price_dict['MinPrice'] = prices_list.min()
        price_dict['MaxPrice'] = prices_list.max()
        price_dict['AvgPrice'] = prices_list.mean()

        return price_dict

    #средняя цена - либо из блока "средняя цена" либо со страницы предложений модели
    def avg_price_harvest(self, page, prices_count_cell, model_href, ID_Name=""):
        price_dict = dict()
        # а есть ли боттом c ценами?
        teg_h2 = page.find_all('h2')
        teg_h2_texts = [i.text for i in teg_h2]

        if 'Средняя цена' in teg_h2_texts:
            # Если блок средней цены на странице модели есть

            margin_prices = page.find('div', class_=self.div_price_minmax).text
            margin_prices = margin_prices.replace(' ', '')
            margin_prices = margin_prices.replace('₽', '')
            defiss = margin_prices.find('—')

            price_dict['MinPrice'] = margin_prices[:defiss]
            price_dict['MaxPrice'] = margin_prices[defiss + 1:]

            avg_price = page.find('div', class_=self.div_price_avg)
            price_dict['AvgPrice'] = int(avg_price.find('span').text.replace(' ', '').replace('₽', ''))
        else:
            # тады лезем внутря в список цен, руками:
            offers_href = self.host + str(prices_count_cell.find('a').get('href'))
            ref_href = self.host + model_href

            offers_price_list = self.offers_prices_harvest(offers_href, ref_href)
            price_dict['MinPrice'] = offers_price_list['MinPrice']
            price_dict['MaxPrice'] = offers_price_list['MaxPrice']
            price_dict['AvgPrice'] = offers_price_list['AvgPrice']


        return price_dict

    #скачивание данных из файла линков по категории
    def links_df_read_excel(self, links_filename):

        links_df = pd.read_excel(links_filename)
        return links_df

    #Основная функция парсинга моделей
    def parse_models_prices(self, links_df):

        df = links_df[['Name', 'Vendor', 'Category']]
        df['Quantaty'] = None

        for i, row_df in links_df.iterrows():

            try:

                response = requests.get(self.host + row_df['Href'], headers=self.header_(), cookies=self.ya_cookies)
                if response.status_code == 200:
                    page = BeautifulSoup(response.text, 'html.parser')

                    title = page.find('title')

                    if 'Маркет' in title.text:

                        # Табличка верхняя серая
                        table_grey = page.find('ul', class_=self.ul_table_gray)

                        # Плашка `Цены`
                        prices_count_cell = table_grey.find('li', class_=self.li_offers)

                        # Количество цен (предложений)
                        if prices_count_cell.find('span', class_=self.span_offers) is not None:
                            df.loc[i, 'Quantaty'] = int(prices_count_cell.find('span', class_=self.span_offers).text)
                        else:
                            df.loc[i, 'Quantaty'] = 0

                        # Цены Средняя, минимум, максимум со страницы модели в боттоме или со страницы предложений

                        if df.loc[i]['Quantaty'] > 2:

                            price_dict = self.avg_price_harvest(page, prices_count_cell, row_df['Href'], row_df['Name'])

                            df.loc[i, 'MinPrice'] = price_dict['MinPrice']
                            df.loc[i, 'MaxPrice'] = price_dict['MaxPrice']
                            df.loc[i, 'AvgPrice'] = price_dict['AvgPrice']

                        else:
                            # если одно предложение (цена) только одна или нет предложений
                            avg_price = page.find('div', class_=self.div_price_alone)
                            if avg_price is not None:
                                df.loc[i, 'AvgPrice'] = int(
                                    avg_price.find('span', class_='price').text.replace(' ', '').replace('₽', ''))
                            else:
                                df.loc[i, 'AvgPrice'] = 'na'

                    elif title.text == 'Ой!':
                        print('Облом: капча. Пропускаем')

                    else:
                        print('Еще чета не так')

            except Exception as Err:
                print(Err)

            print(df.loc[i])

        return df

    #Вызывная функция парсинга
    def prices_to_excel(self, links_filename, links_folder='Price_link_list/', price_folder='Prices/'):
        df = self.parse_models_prices(self.links_df_read_excel(links_folder + links_filename))

        now = datetime.now().strftime('%b-%y----%d--%H-%M')

        category = df.iloc[0]['Category']

        for i in self.Categories:
            if category in self.Categories[i]['category']:
                category_ = i
                break


        exit_filename = price_folder + category_ + '-Цены-от-' + now + '.xlsx'
        df.to_excel(exit_filename)

    #заполнение пустых строк в готовом файле прайсов
    def no_prices_reparse(self, price_filename, links_filename,
                          price_folder='Prices/', links_folder='Price_link_list/'):
        df = pd.read_excel(price_folder + price_filename, index_col=0)
        df_none = df[df['Quantaty'].isna()]
        empty_id = df_none.index

        print(df_none['Name'])

        df_links = pd.read_excel(links_folder + links_filename)
        df_links = df_links.merge(df_none.loc[:, 'Name'], on='Name')

        df_filled = self.parse_models_prices(df_links)

        for i in empty_id:

            id_series = df_filled[df_filled['Name'] == df.loc[i]['Name']]
            for j in id_series.columns:
                df.loc[i, j] = id_series[j].iloc[0]

        now = datetime.now().strftime('%b-%y----%d--%H-%M')
        category = df.iloc[0]['Category']

        exit_filename = price_folder + category + '-Цены-от-' + now + '_empfill.xlsx'
        df.to_excel(exit_filename)

class Parse_models_ttx(Parse_models):

    # Считывание цен из предложений как в паренте

    # Сбор всех ТТХ
    def ttx_harvest(self, ttx_href, ref_href, name):

        ttx_line_df = pd.DataFrame({'Name': [name]})
        #ttx_line_df['Name'] = name

        try:
            response = requests.get(ttx_href,
                                    headers=self.header_(ref_href),
                                    cookies=self.ya_cookies)
            if response.status_code == 200:
                page = BeautifulSoup(response.text, 'html.parser')

            # вся таблица характеристик
            #ttx_table = page.find('div', class_=self.div_ttx_table)
            ttx_table_rows = page.find_all('dl')

            for dl in ttx_table_rows:
                spec_name = dl.find('dt').find('span').text
                comment_find = spec_name.find('?') #Нет ли тут комментария к полю характеристик
                if comment_find != -1:
                    spec_name = spec_name[:comment_find]
                spec_name = spec_name.replace(':', '') #двоеточие и окончательные пробелы
                for i in range(len(spec_name)-1, 0, -1):
                    if spec_name[i] == ' ':
                        spec_name = spec_name[:-1]
                    else:
                        break

                spec_value = dl.find('dd').text
                # Забираем только самые полные характеристики в случае дубляжа ТТХ в таблице
                if spec_name in ttx_line_df.columns:
                    if len(ttx_line_df[spec_name].iloc[0]) < len(spec_value):
                        ttx_line_df.loc[0, spec_name] = spec_value

                else:
                    ttx_line_df[spec_name] = spec_value

        except Exception as Err_response:
            print(Err_response)

        #Прибиваем новую строку
        self.ttx_df__work = pd.concat([self.ttx_df__work, ttx_line_df], ignore_index=True)



    #средняя цена в паренте

    #Основная функция парсинга моделей
    def parse_models_prices(self, links_df):

        df = links_df[['Name', 'Vendor', 'Category']]
        df['Quantaty'] = None

        for i, row_df in links_df.iterrows():

            try:
                response = requests.get(self.host + row_df['Href'], headers=self.header_(), cookies=self.ya_cookies)
                if response.status_code == 200:
                    page = BeautifulSoup(response.text, 'html.parser')

                    title = page.find('title')

                    if 'Маркет' in title.text:

                        # Табличка верхняя серая
                        table_grey = page.find('ul', class_=self.ul_table_gray)

                        # Плашка `Цены`
                        prices_count_cell = table_grey.find('li', class_=self.li_offers)

                        # Количество цен (предложений)
                        if prices_count_cell.find('span', class_=self.span_offers) is not None:
                            df.loc[i, 'Quantaty'] = int(prices_count_cell.find('span', class_=self.span_offers).text)
                        else:
                            df.loc[i, 'Quantaty'] = 0

                        # Цены Средняя, минимум, максимум со страницы модели в боттоме или со страницы предложений

                        if df.loc[i]['Quantaty'] > 2:

                            price_dict = self.avg_price_harvest(page, prices_count_cell, row_df['Href'], row_df['Name'])

                            df.loc[i, 'MinPrice'] = price_dict['MinPrice']
                            df.loc[i, 'MaxPrice'] = price_dict['MaxPrice']
                            df.loc[i, 'AvgPrice'] = price_dict['AvgPrice']

                        else:
                            # если одно предложение (цена) только одна или нет предложений
                            avg_price = page.find('div', class_=self.div_price_alone)
                            if avg_price is not None:
                                df.loc[i, 'AvgPrice'] = int(
                                    avg_price.find('span', class_='price').text.replace(' ', '').replace('₽', ''))
                            else:
                                df.loc[i, 'AvgPrice'] = 'na'


                        # ТТХ Если такой модели до сх пор не было
                        if row_df['Name'] not in self.ttx_names_set:

                            # Плашка `Характеристики`
                            spec_cell = table_grey.find('li', class_=self.li_spec)

                            try:  # на случай если ссылки на характеристики нет
                                ttx_link = str(spec_cell.find('a').get('href'))

                                ttx_href = self.host + ttx_link
                                ref_href = self.host + row_df['Href']

                                self.ttx_harvest(ttx_href, ref_href, row_df['Name'])

                            except AttributeError as Err_ttx:
                                print(Err_ttx)
#
                    elif title.text == 'Ой!':
                        print('Облом: капча. Пропускаем')

                    else:
                        print('Еще чета не так')

            except Exception as Err:
                print(Err)

            print(df.loc[i])

        return df

    def TTX_df_read_excel(self, category, ttx_folder='TTX_files/'):


        if 'ttx_file' not in self.Categories[category].keys():
            raise AttributeError('Нет поля ttx_file в словаре Categories')

        ttx_filename = ttx_folder + self.Categories[category]['ttx_file']
        ttx_df__temp = pd.read_excel(ttx_filename, index_col=0)

        #множество имеющихся моделей с TTX
        self.ttx_names_set = frozenset(ttx_df__temp['Name'])

        #Пустой DataFrame для новых ТТХ
        self.ttx_df__work = pd.DataFrame(columns=ttx_df__temp.columns)

    def TTX_df_append(self, category, new_ttx_df, ttx_folder='TTX_files/'):

        ttx_filename = ttx_folder + self.Categories[category]['ttx_file']
        old_ttx_df = pd.read_excel(ttx_filename, index_col=0)
        ttx_df = pd.concat([old_ttx_df, new_ttx_df], ignore_index=True, sort=False)

        ttx_df.to_excel(ttx_filename)

    #Вызывная функция парсинга
    def prices_to_excel(self,
                        category,
                        links_filename,
                        links_folder='Price_link_list/',
                        price_folder='Prices/',
                        ttx_folder='TTX_files/'):

        if category not in self.Categories.keys():
            raise AttributeError('Нет такой категории продукта в Categories')

        # df линков
        df_links = self.links_df_read_excel(links_folder + links_filename)

        # df ttx

        self.TTX_df_read_excel(category, ttx_folder)

        df = self.parse_models_prices(df_links) #вызов парсинга

        now = datetime.now().strftime('%b-%y----%d--%H-%M')

        # выходной файл с ценами

        #category = df.iloc[0]['Category']
        exit_filename = price_folder + category + '-Цены-от-' + now + '.xlsx'
        df.to_excel(exit_filename)

        #выходной файл с TTX
        self.TTX_df_append(category, self.ttx_df__work)


#   Последняя версия парсера для yama с учетом модификаций для ноутбуков
class Parse_Modifications_TTX(Yama_parsing_const):
    def __init__(self,
                 category,
                 links_file,
                 mod=True, # Надо ли считывать модификации
                 ttx_name=False, # Надо ли считывать TTX Модели
                 ttx_mod = True # Надо ли считывать TTX Модификаций
                 ):

        link_filename = 'Price_link_list/' + links_file
        self.df_links = pd.read_excel(link_filename, index_col=0)
        print(self.df_links.head(3))

        if category in self.Categories.keys():
            self.category = category
        else:
            raise AttributeError('Нет такой категории продукта в Categories')

        self.df_names = pd.DataFrame(columns=['Name',
                                              'Ya_UN_Name',
                                              'Category',
                                              'Vendor',
                                              'Modification_name',
                                              'Modification_href',
                                              'Modification_price',
                                              'Quantity',
                                              'Subcategory',
                                              'Site',
                                              'Date'])

        self.now = datetime.now().strftime('%b-%y')

        self.mod = mod
        if self.mod:
            self.df_mods = pd.DataFrame(columns=['Name',
                                                'Ya_UN_Name',
                                                  'Vendor',
                                                  'Modification_name',
                                                  'Modification_href',
                                                  'Quantity',
                                                  'Modification_price',
                                                'Category',
                                                 'Subcategory',
                                                 'Site',
                                                 'Date'])
            if ttx_mod:
                self.ttx_mod = ttx_mod
                self.ttx_mod_filename = self.TTX_files_folder + self.Categories[self.category]['ttx_mod_file']
                self.df_ttx_mod = pd.read_excel(self.ttx_mod_filename, index_col=0)

        if ttx_name:
            self.ttx_name = ttx_name
            self.ttx_name_filename = self.TTX_files_folder + self.Categories[self.category]['ttx_file']
            self.df_ttx_name = pd.read_excel(self.ttx_name_filename, index_col=0)


    def main(self, step=10, start=0, num=""):

        self.num = num

        finish_ = len(self.df_links)
        begin_ = start
        end_ = begin_ + step
        while end_ < finish_ - 1:
            end_ = begin_ + step
            if end_ > finish_ - 1:
                end_ = finish_ - 1

            for i, row_df_links in self.df_links.iloc[begin_:end_].iterrows():
                j = len(self.df_names)
                self.df_names.loc[j, 'Site'] = 'yama'
                self.df_names.loc[j, 'Name'] = None
                self.df_names.loc[j, 'Ya_UN_Name'] = row_df_links['Name']
                self.df_names.loc[j, 'Modification_name'] = self.df_names.loc[j, 'Ya_UN_Name']
                self.df_names.loc[j, 'Modification_href'] = self.host + row_df_links['Href']

                self.df_names.loc[j, 'Vendor'] = row_df_links['Vendor']
                self.df_names.loc[j, 'Subcategory'] = row_df_links['Category']
                self.df_names.loc[j, 'Category'] = self.category
                self.df_names.loc[j, 'Date'] = self.now



                url_req = self.URL_Req(row_df_links['Href'])
                if url_req:
                    soup_page = BeautifulSoup(url_req, 'html.parser')
                    soup_table_grey = soup_page.find('ul', class_=self.ul_table_gray)

                    self.df_names.loc[j, ['Quantity', 'Modification_price']] = self.Parse_Model_Page(soup_page,
                                                                                            soup_table_grey)

                    print(self.df_names.iloc[j])
                    if self.mod:
                        if url_req:
                            url_block = soup_table_grey.find('a', {"href": re.compile("mods")})
                            if url_block:
                                url_ = url_block.get('href')
                            else:
                                url_ = None
                            if url_:
                                self.Parse_Modifications(url_,
                                                        row_df_links['Ya_UN_Name'],
                                                        row_df_links['Vendor'],
                                                        row_df_links['Category'])
                if self.ttx_name:
                    ttx_len = len(self.df_ttx_name)
                    self.df_ttx_name = self.TTX_Handler(self.URL_Spec(soup_table_grey),
                                                        self.df_ttx_name,
                                                        self.df_names.loc[j, 'Modification_name'])

            self.DF_to_Excel(self.df_names, num=self.num)
            if self.ttx_name and (len(self.df_ttx_name) > ttx_len):
                self.df_ttx_name.to_excel(self.ttx_name_filename)

            begin_ = end_

    def URL_Req(self, url_, host=True):

        if host:
            url_ = self.host + url_
        try:
            #response = requests.get(url_, headers=self.header_(), cookies=self.ya_cookies, timeout=7)
            response = Req()
            response.selenium(url_)
            if response.status_code == 200:
                return response.text
        except Exception:
            print("не выходит {}".format(url_))
            return None


    def Parse_Model_Page(self, soup_page, soup_table_grey):

        dict_exit = {}

        # Плашка `Цены`
        if soup_table_grey:
            soup_offers_cell = soup_table_grey.find('li', class_=self.li_offers)
            offers_ = soup_offers_cell.find('span', class_=self.span_offers)

            if offers_ is not None:
                dict_exit['Quantity'] = int(offers_.text)
            else:
                dict_exit['Quantity'] = 0

            if dict_exit['Quantity'] > 0:
                dict_exit['Modification_price'] = self.AvgPrice_Handler(soup_page, soup_offers_cell)

            else:
                # если одно предложение (цена) только одна или нет предложений
                avg_price = soup_page.find('div', class_=self.div_price_alone)
                if avg_price is not None:
                    dict_exit['Modification_price'] = int(
                            avg_price.find('span', class_='price').text.replace(' ', '').replace('₽', ''))
                else:
                    dict_exit['Modification_price'] = 'na'
        else:
            dict_exit['Modification_price'] = 'na'
            dict_exit['Quantity'] = None

        return dict_exit

    def Parse_Modifications(self, url_, up_name, up_vendor, up_category):

        page_href = url_
        pages_is_ok = True
        page = 1

        while pages_is_ok:
            print(page, page_href)
            if self.ttx_mod:
                ttx_len = len(self.df_ttx_mod)
            url_req = self.URL_Req(page_href)

            if url_req:
                soup_page = BeautifulSoup(url_req, 'html.parser')

                if soup_page.find('a', class_=self.a_button_eol) is None:
                    pages_is_ok = False
                soup_mods = soup_page.find_all('h3', class_=re.compile("snippet-card"))
                soup_list_mods = [card.find('a') for card in soup_mods]

                for name in soup_list_mods:
                    i = len(self.df_mods)
                    self.df_mods.loc[i, 'Site']
                    self.df_mods.loc[i, 'Ya_UN_Name'] = up_name
                    self.df_mods.loc[i, 'Category'] = self.category
                    self.df_mods.loc[i, 'Subcategory'] = up_category
                    self.df_mods.loc[i, 'Vendor'] = up_vendor
                    self.df_mods.loc[i, 'Modification_name'] = name.text.replace(up_category + " ", "")
                    #TOD Убрать категорию из названия
                    url_mod = name.get('href')
                    self.df_mods.loc[i, 'Modification_href'] = self.host + url_mod
                    url_req = self.URL_Req(url_mod)
                    if url_req:
                        soup_mod_page = BeautifulSoup(url_req, 'html.parser')
                        soup_table_grey = soup_mod_page.find('ul', class_=self.ul_table_gray)
                        dict_ = self.Parse_Model_Page(soup_mod_page, soup_table_grey)
                        self.df_mods.loc[i, 'Quantity'] = dict_['Quantity']
                        self.df_mods.loc[i, 'Modification_price'] = dict_['Modification_price']

                        print(self.df_mods.loc[i, 'Modification_name'])
                        if self.ttx_mod:
                            self.df_ttx_mod = self.TTX_Handler(self.URL_Spec(soup_table_grey),
                                                               self.df_ttx_mod,
                                                               self.df_mods.loc[i, 'Modification_name'])

            self.DF_to_Excel(self.df_mods, num=self.num, level="Modifications")
            if self.ttx_mod and (len(self.df_ttx_mod) > ttx_len):
                self.df_ttx_mod.to_excel(self.ttx_mod_filename)

            page += 1
            page_href = url_ + '&page=' + str(page)


    def TTX_Handler(self, url_, df_ttx, name):

        if name not in df_ttx['Name'].values:
            j = len(df_ttx)
            df_ttx.loc[j, 'Name'] = name
            url_req = self.URL_Req(url_)
            if url_req:
                soup_ttx_page = BeautifulSoup(url_req, 'html.parser')
                soup_ttx_table_rows = soup_ttx_page.find_all('dl')

                for dl in soup_ttx_table_rows:
                    spec_name = dl.find('dt').find('span').text
                    comment_find = spec_name.find('?')  # Нет ли тут комментария к полю характеристик
                    if comment_find != -1:
                        spec_name = spec_name[:comment_find]
                    spec_name = spec_name.replace(':', '')  # двоеточие и окончательные пробелы
                    for i in range(len(spec_name) - 1, 0, -1):
                        if spec_name[i] == ' ':
                            spec_name = spec_name[:-1]
                        else:
                            break

                    spec_value = dl.find('dd').text
                    # Забираем только самые полные характеристики в случае дубляжа ТТХ в таблице
                    if spec_name in df_ttx.columns:

                        if len(str(df_ttx.loc[j, spec_name])) < len(str(spec_value)):
                            df_ttx.loc[j, spec_name] = str(spec_value)
                    else:
                        df_ttx.loc[j, spec_name] = str(spec_value)
            df_ttx.loc[j, 'Date'] = self.now

        return df_ttx


    def URL_Spec(self, soup_table_grey):
        if soup_table_grey:
            return soup_table_grey.find('a', {"href": re.compile("spec")}).get('href')
        else:
            return None



    def AvgPrice_Handler(self, soup_page, soup_offers_cell):

        # а есть ли боттом c ценами?
        teg_h2 = soup_page.find_all('h2')
        teg_h2_texts = [i.text for i in teg_h2]

        if 'Средняя цена' in teg_h2_texts:
                # Если блок средней цены на странице модели есть
            avg_price = soup_page.find('div', class_=self.div_price_avg)
            exit_ = int(avg_price.find('span').text.replace(' ', '').replace('₽', ''))
        else:
                # тады лезем внутря в список цен, руками:
            url_ = str(soup_offers_cell.find('a').get('href'))
            exit_ = self.Offers_Handler(url_)

        return exit_

    def Offers_Handler(self, url_):

            prices_list = list()
            print("OFFERS HANDLER WORK")


            page_href = url_
            # new_ref_href = ref_href
            pages_is_ok = True
            page = 1

            while pages_is_ok == True:
                print(self.host + page_href)
                url_req = self.URL_Req(page_href)
                if url_req:
                    soup_offers_page = BeautifulSoup(url_req, 'html.parser')

                    if soup_offers_page.find('a', class_=self.a_button_eol) is None:
                        pages_is_ok = False

                    # = soup_offers_page.find_all('div', class_=self.div_config_prices_table)

                    list_soup_prices = soup_offers_page.find_all('span', class_='price')

                    page_price_list = [int(i.text.replace(' ', '').replace('₽', '')) for i in list_soup_prices]
                    prices_list += page_price_list

                    page += 1
                    # new_ref_href = page_href
                    page_href = url_ + '&page=' + str(page)
            try:
                exit_ = sum(prices_list)/len(prices_list)
            except ZeroDivisionError:
                exit_ = 'na'

            return exit_


    def DF_to_Excel(self, df_out, num="", level=""):

        filename = "Prices/" + \
                   self.category + \
                   "--" + \
                   level + \
                   "--" + \
                   self.now + \
                   "--" + \
                   str(num) + \
                   ".xlsx"

        df_out.to_excel(filename)

class Parse_Modifications_TTX_Mod_in_Prices(Parse_Modifications_TTX):

    def __init__(self,
                 category,
                 links_file,
                 ttx_name=False, # Надо ли считывать TTX Модели
                 #ttx_mod = True # Надо ли считывать TTX Модификаций
                 ):

        link_filename = 'Price_link_list/' + links_file
        self.df_links = pd.read_excel(link_filename, index_col=0)
        print(self.df_links.head(3))

        # WEBDRIVER
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument("user-data-dir=selenium")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        if category in self.Categories.keys():
            self.category = category
        else:
            raise AttributeError('Нет такой категории продукта в Categories')

        self.df_names = pd.DataFrame(columns=['Name',
                                              'Ya_UN_Name',
                                              'Category',
                                              'Vendor',
                                              'Modification_name',
                                              'Modification_href',
                                              'Modification_price',
                                              'Quantity',
                                              'Subcategory',
                                              'Site',
                                              'Date'])

        self.now = datetime.now().strftime('%b-%y')



        self.df_mods = pd.DataFrame(columns=['Name',
                                              'Ya_UN_Name',
                                              'Category',
                                              'Vendor',
                                              'Modification_name',
                                              'Modification_href',
                                              'Modification_price',
                                              'Quantity',
                                              'Subcategory',
                                              'Site',
                                              'Date'])
        # if ttx_mod:
        #         self.ttx_mod = ttx_mod
        #         self.ttx_mod_filename = self.TTX_files_folder + self.Categories[self.category]['ttx_mod_file']
        #         self.df_ttx_mod = pd.read_excel(self.ttx_mod_filename, index_col=0)

        if ttx_name:
            self.ttx_name = ttx_name
            self.ttx_name_filename = self.TTX_files_folder + self.Categories[self.category]['ttx_file']
            self.df_ttx_name = pd.read_excel(self.ttx_name_filename, index_col=0)


    def main(self, step=10, start=0, num=""):

        self.num = num

        finish_ = len(self.df_links)
        begin_ = start
        end_ = begin_ + step
        while end_ < finish_ - 1:
            end_ = begin_ + step
            if end_ > finish_ - 1:
                end_ = finish_ - 1

            for i, row_df_links in self.df_links.iloc[begin_:end_].iterrows():
                j = len(self.df_names)
                self.df_names.loc[j, 'Site'] = 'yama'
                self.df_names.loc[j, 'Name'] = None
                self.df_names.loc[j, 'Ya_UN_Name'] = row_df_links['Name']
                self.df_names.loc[j, 'Modification_name'] = self.df_names.loc[j, 'Ya_UN_Name']
                self.df_names.loc[j, 'Modification_href'] = self.host + row_df_links['Href']

                self.df_names.loc[j, 'Vendor'] = row_df_links['Vendor']
                self.df_names.loc[j, 'Subcategory'] = row_df_links['Category']
                self.df_names.loc[j, 'Category'] = self.category
                self.df_names.loc[j, 'Date'] = self.now



                url_req = self.URL_Req(row_df_links['Href'])
                if url_req:
                    soup_page = BeautifulSoup(url_req, 'html.parser')
                    soup_table_grey = soup_page.find('ul', class_=self.ul_table_gray)

                    self.df_names.loc[j, ['Quantity', 'Modification_price']] = self.Parse_Model_Page(soup_page,
                                                                                            soup_table_grey,
                                                                                            row_df_links['Name'],
                                                                                            row_df_links['Vendor'],
                                                                                            self.category)

                    print(self.df_names.iloc[j])
                    # if self.mod:
                    #     if url_req:
                    #         url_block = soup_table_grey.find('a', {"href": re.compile("mods")})
                    #         if url_block:
                    #             url_ = url_block.get('href')
                    #         else:
                    #             url_ = None
                    #         if url_:
                    #             self.Parse_Modifications(url_,
                    #                                     row_df_links['Ya_UN_Name'],
                    #                                     row_df_links['Vendor'],
                    #                                     row_df_links['Category'])
                if self.ttx_name:
                    ttx_len = len(self.df_ttx_name)
                    self.df_ttx_name = self.TTX_Handler(self.URL_Spec(soup_table_grey),
                                                        self.df_ttx_name,
                                                        self.df_names.loc[j, 'Modification_name'])

            self.DF_to_Excel(self.df_names, num=self.num)
            if self.ttx_name and (len(self.df_ttx_name) > ttx_len):
                self.df_ttx_name.to_excel(self.ttx_name_filename)

            begin_ = end_

    def Parse_Model_Page(self, soup_page, soup_table_grey, Ya_UN_Name, Vendor, Category):

            dict_exit = {}

            # Плашка `Цены`
            if soup_table_grey:
                soup_offers_cell = soup_table_grey.find('li', class_=self.li_offers)
                offers_ = soup_offers_cell.find('span', class_=self.span_offers)

                if offers_ is not None:
                    dict_exit['Quantity'] = int(offers_.text)
                else:
                    dict_exit['Quantity'] = 0

                if dict_exit['Quantity'] > 0:
                    dict_exit['Modification_price'] = self.AvgPrice_Handler(soup_offers_cell,
                                                                            Ya_UN_Name,
                                                                            Vendor,
                                                                            Category)


                else:
                    # если одно предложение (цена) только одна или нет предложений
                    avg_price = soup_page.find('div', class_=self.div_price_alone)
                    if avg_price is not None:
                        dict_exit['Modification_price'] = int(
                            avg_price.find('span', class_='price').text.replace(' ', '').replace('₽', ''))
                    else:
                        dict_exit['Modification_price'] = 'na'
            else:
                dict_exit['Modification_price'] = 'na'
                dict_exit['Quantity'] = None

            return dict_exit
#

    def AvgPrice_Handler(self, soup_offers_cell, Ya_UN_Name, Vendor, Category):

            # а есть ли боттом c ценами?
            # teg_h2 = soup_page.find_all('h2')
            # teg_h2_texts = [i.text for i in teg_h2]

            # if 'Средняя цена' in teg_h2_texts:
            #     # Если блок средней цены на странице модели есть
            #     avg_price = soup_page.find('div', class_=self.div_price_avg)
            #     exit_ = int(avg_price.find('span').text.replace(' ', '').replace('₽', ''))
      #лезем внутря в список цен, руками:
           url_ = str(soup_offers_cell.find('a').get('href'))
           exit_ = self.Offers_Handler(url_, Ya_UN_Name, Vendor, Category)

           return exit_

    def Offers_Handler(self, url_, Ya_UN_Name, Vendor, Category):

            prices_list = list()
            print("OFFERS HANDLER WORK")

            page_href = url_
            # new_ref_href = ref_href
            pages_is_ok = True
            page = 1
            df_pointer = len(self.df_mods)

            while pages_is_ok:
                print(self.host + page_href)
                url_req = self.URL_Req(page_href)
                if url_req:
                    soup_offers_page = BeautifulSoup(url_req, 'html.parser')

                    if soup_offers_page.find('a', class_=self.a_button_eol) is None:
                        pages_is_ok = False

                    #Остальные _1vFSS76Axn

                    list_cards = soup_offers_page.find_all('div', class_="_1vFSS76Axn") #карточка модели
                    #first_card = soup_offers_page.find('div', class_="_2REMycE4YO")
                    if list_cards:
                        #if first_card:
                            #list_cards.append(first_card)

                        for crd in list_cards:
                            self.df_mods.loc[df_pointer, 'Ya_UN_Name'] = Ya_UN_Name
                            self.df_mods.loc[df_pointer, 'Vendor'] = Vendor
                            self.df_mods.loc[df_pointer, 'Category'] = Category
                            self.df_mods.loc[df_pointer, 'Site'] = 'yama'
                            self.df_mods.loc[df_pointer, 'Date'] = self.now
                            try:
                                name_source_href = crd.find('h3').find('a')

                                self.df_mods.loc[df_pointer, 'Modification_href'] = name_source_href.get('href')
                                name_ = name_source_href.find('span').text
                                if Vendor.lower() in name_.lower():
                                    name_ = name_.replace(Vendor + " ", "").replace(Vendor.title() + " ", "")
                                self.df_mods.loc[df_pointer, 'Subcategory'] = ""
                                for cat in self.Categories[Category]['category']:
                                    if cat.lower() in name_.lower():
                                        if len(cat) > len(self.df_mods.loc[df_pointer, 'Subcategory']):
                                            self.df_mods.loc[df_pointer, 'Subcategory'] = cat

                                if self.df_mods.loc[df_pointer, 'Subcategory']:
                                    name_ = name_.replace(self.df_mods.loc[df_pointer, 'Subcategory'] + " ", "")

                                self.df_mods.loc[df_pointer, 'Modification_name'] = name_

                            except Exception:
                                self.df_mods.loc[df_pointer, 'Modification_href'] = None
                                self.df_mods.loc[df_pointer, 'Modification_name'] = None
                                self.df_mods.loc[df_pointer, 'Subcategory'] = None

                            price_spans = crd.find('div', {"data-zone-name": 'price'}).find('span').find_all('span')
                            for spn in price_spans:
                                dgt = re.compile(r'\d')
                                if re.search(dgt, spn.text):
                                    #price_ = spn.text.replace(" ", "")
                                    price_ = "".join(re.findall(dgt, spn.text))
                                    self.df_mods.loc[df_pointer, 'Modification_price'] = price_
                                    prices_list.append(int(price_))

                            df_pointer += 1

                self.DF_to_Excel(self.df_mods, num=self.num, level="Modifications")

                page += 1
                page_href = url_ + '&page=' + str(page)


            try:
                prices_list_cl = [x for x in prices_list if x is not None]
                exit_ = int(sum(prices_list_cl) / len(prices_list_cl))
            except ZeroDivisionError:
                exit_ = 'na'

            return exit_

    def URL_Req(self, url_, host=True):

        if host:
            url_ = self.host + url_
        try:
            self.driver.get(url_)
            if self.driver.page_source:
                if not "Ой" in self.driver.page_source:
                    return self.driver.page_source
        except Exception:
            print("не выходит {}".format(url_))
            return None

class Parse_Modifications_TTX_selenium_fix(Parse_Modifications_TTX):

    def __init__(self,
                 category,
                 links_file,
                 mod=True,  # Надо ли считывать модификации
                 ttx_name=False,  # Надо ли считывать TTX Модели
                 ttx_mod=True  # Надо ли считывать TTX Модификаций
                 ):

        link_filename = 'Price_link_list/' + links_file
        self.df_links = pd.read_excel(link_filename, index_col=0)
        print(self.df_links.head(3))

        # WEBDRIVER
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument("user-data-dir=selenium")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

        if category in self.Categories.keys():
            self.category = category
        else:
            raise AttributeError('Нет такой категории продукта в Categories')

        self.df_names = pd.DataFrame(columns=['Name',
                                              'Ya_UN_Name',
                                              'Category',
                                              'Vendor',
                                              'Modification_name',
                                              'Modification_href',
                                              'Modification_price',
                                              'Quantity',
                                              'Subcategory',
                                              'Site',
                                              'Date'])

        self.now = datetime.now().strftime('%b-%y')

        self.mod = mod
        if self.mod:
            self.df_mods = pd.DataFrame(columns=['Name',
                                                 'Ya_UN_Name',
                                                 'Vendor',
                                                 'Modification_name',
                                                 'Modification_href',
                                                 'Quantity',
                                                 'Modification_price',
                                                 'Category',
                                                 'Subcategory',
                                                 'Site',
                                                 'Date'])
            if ttx_mod:
                self.ttx_mod = ttx_mod
                self.ttx_mod_filename = self.TTX_files_folder + self.Categories[self.category]['ttx_mod_file']
                self.df_ttx_mod = pd.read_excel(self.ttx_mod_filename, index_col=0)

        if ttx_name:
            self.ttx_name = ttx_name
            self.ttx_name_filename = self.TTX_files_folder + self.Categories[self.category]['ttx_file']
            self.df_ttx_name = pd.read_excel(self.ttx_name_filename, index_col=0)

    def URL_Req(self, url_, host=True):

        if host:
            url_ = self.host + url_
        try:
            self.driver.get(url_)
            if self.driver.page_source:
                if not "Ой" in self.driver.page_source:
                    return self.driver.page_source
        except Exception:
            print("не выходит {}".format(url_))
            return None

    def Offers_Handler(self, url_):

            prices_list = list()
            print("OFFERS HANDLER WORK")


            page_href = url_
            # new_ref_href = ref_href
            pages_is_ok = True
            page = 1

            while pages_is_ok == True:
                print(self.host + page_href)
                url_req = self.URL_Req(page_href)
                if url_req:
                    soup_offers_page = BeautifulSoup(url_req, 'html.parser')

                    if soup_offers_page.find('a', class_=self.a_button_eol) is None:
                        pages_is_ok = False

                    #list_soup_prices = soup_offers_page.find_all('span', class_='price')

                    price_spans = soup_offers_page.find_all('div', {"data-zone-name": 'price'})
                    if price_spans:
                        for pri in price_spans:
                            price_spn = pri.find('span').find_all('span')
                        for spn in price_spn:
                            dgt = re.compile(r'\d')
                            if re.search(dgt, spn.text):

                                price_ = "".join(re.findall(dgt, spn.text))
                                if price_:
                                    prices_list.append(int(price_))

                    page += 1

                    page_href = url_ + '&page=' + str(page)
            try:
                exit_ = int(sum(prices_list)/len(prices_list))
            except ZeroDivisionError:
                exit_ = 'na'

            return exit_

