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
#import re
#from grab import Grab

class Yama_parsing_const(object):
    def header_(self, referer=""):

        header = {
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

    #host name
    host = 'https://market.yandex.ru'

    #добавка к адресу выдачи списка моделей
    link_tail = '&onstock=1&local-offers-first=0'

    #головная ссылка раздела "Компьютерная техника"
    link_computers = 'https://market.yandex.ru/catalog--kompiuternaia-tekhnika/54425'

    # кнопка "Вперед" на страницах выдачи списков моделей <a> class
    a_button_eol = 'button button_size_s button_theme_pseudo n-pager__button-next i-bem n-smart-link'

    # строки таблицы моделей (по 48 на страницу обычно) Div class
    div_row_models_ls = 'n-snippet-card2 i-bem b-zone b-spy-visible b-spy-events'

    # Название модели на страницы выдачи h3 class
    h3_model_name = 'n-snippet-card2__title'

    # Табличка верхняя серая на странице модели ul class
    ul_table_gray = 'n-product-tabs__list'

    # Плашка 'цены' в серой табличке на странице модели li class
    li_offers = 'n-product-tabs__item n-product-tabs__item_name_offers'

    # Число на плашке 'цены' (Количество предложений) на странице модели span class
    span_offers = 'n-product-tabs__count'

    # Плашка 'характеристики' в серой табличке на странице модели li class
    li_spec = 'n-product-tabs__item n-product-tabs__item_name_spec'

    # Максимальная и минимальная цена в нижнем блоке "средняя цена" на странице модели div class
    div_price_minmax = '_1S8ob0AgBK'

    # Средняя цена в блоке "средняя цена" на странице модели div class
    div_price_avg = '_3TkwCtZtaF'

    # Цена из верхного блока если цена только одна на странце модели  div
    div_price_alone = 'n-product-price-cpa2__price'

    # Таблица с ценами на очередной странице выдачи внутри предложений (модификаций) модели div class
    div_config_prices_table = 'n-snippet-list n-snippet-list_type_vertical island metrika b-zone b-spy-init b-spy-events i-bem'

    # Таблица характеристик (ТТХ) на странице Харктистик модели
    div_ttx_table = 'layout__col layout__col_size_p75 n-product-spec-wrap'

    #Название характеристики (ТТХ) на странице Харктистик модели
    span_spec_name = 'n-product-spec__name-inner'

    # Значение характеристики (ТТХ) на странице Харктистик модели
    span_spec_value = 'n-product-spec__value-inner'


    Categories = {
        'Ноутбук': {
            'url': 'https://market.yandex.ru/catalog--noutbuki/54544/list?hid=91013',
            'category': ['Ноутбук'],
            'ttx_file': 'Ноутбук--характеристики.xlsx'
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
    TTX_files_folder = 'TTX_files'


#Скачивание линков на модлеи по категориям
class Parse_links(Yama_parsing_const):

    #скачивание линков на страницы модели по категории
    def parse_links(self, category):

        url = self.Categories[category]['url']
        category_ls = self.Categories[category]['category']
        #gr_ = Grab() #объект Grab

        models_list = list()  # список словарей с моделями с названиеми и ссылками на модели

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

            response = requests.get(page_url,
                                    headers=self.header_(referer_),
                                    cookies=self.ya_cookies)

           # gr_.go(page_url,
           #        headers=self.header_(referer_),
           #        cookies=self.ya_cookies)

            if response.status_code == 200:
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
                        model_link = row.find('h3', class_=self.h3_model_name).find('a')
                        # Отсеиваем редирект на внешние сайты или конкретные конфиги нутбуков и останавливаем работу
                        if ('redir/' in model_link) or \
                                ((category == 'Ноутбук') and ('/' in model_link.text)):
                            pages_full = False
                            break

                        model_dict['Href'] = model_link['href']  # ссылка на страницу модели

                        # Ищем название категории
                        category_len = 0

                        for cat in category_ls:
                            if cat in model_link.text:
                                category_len = len(cat.split())
                                model_dict['Category'] = cat
                                break

                        name = model_link.text.split()

                        # Ищем имя вендора (следующее за категорией)
                        model_dict['Vendor'] = name[category_len]

                        #Формируем название модели вместе с имненм вендора через пробел кроме последнего пробела
                        mod_name = ''
                        for word in name[category_len:]:
                            mod_name += word + ' '
                        model_dict['Name'] = mod_name[:-1]

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
                print('облом... ', gr_.doc.code)

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
                    print("status code: ", self.gr_.doc.code)

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
