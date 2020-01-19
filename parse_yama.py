import requests
from pprint import pprint
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
from urllib.parse import quote

class Yama_parsing_const(object):

    ya_cookies = {
        'yandexuid': '1316442951370867155',
        'fuid01': '4f310da92e0e9ff0.vHkMwDo78qH5TTmHx-stTeCpjL9q0oCG-kHm-t1yw00rSnf7Uxj5eqXaFjpO-Ji3kSQu-TbS-duDcL4tBTDDknJm0Xp2PwtEYgzI74M0t3XEplZr69TXugVdbykMuUYo; yp=1571397397.shlos.0#1600341397.p_sw.1568805397#1572440968.ygu.1#1585616974.szm.1:1680x1050:1614x887',
        '_ym_uid': '1478001885185024594',
        'i': '8k0m5URcQTs/D8+3VhGAv5WDga2dnppzBVV1QJC90LIBHvPMRGJZCfTnVJ0n+Mn0B1Jzd5hn+0ZsECAkAdHOR+LT58Y=',
        'mda': '0',
        'my': 'YwA=',
        'yabs': '-frequency=/4/0000000000000000/XtroS9mt81g-FMsSDoUqLB1md3SW/',
        '_ym_isad': '=2',
        'yandex_gid': '213',
        'font_loaded': 'YSv1',
        '_ym_wasSynced': '%7B%22time%22%3A1569848959698%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D',
        '_ym_d': '1569848960',
        '_ym_visorc_160656': 'b',
        '_ym_visorc_45411513': 'b',
        'markethistory': '<h><cm>6427101-9238862</cm><cm>6427101-8538765</cm><m>106905-10467479</m><m>432460-7691987</m><c>7156311</c></h>',
        'cmp-merge': 'true',
        'reviews-merge': 'true',
        'head-banner-sovetnik': '%7B%22closingCounter%22%3A0%2C%22showingCounter%22%3A1%2C%22shownAfterClicked%22%3Afalse%2C%22isClicked%22%3Afalse%7D; head-banner-sovetnik-info=%7B%22closingCounter%22%3A0%2C%22showingCounter%22%3A1%2C%22shownAfterClicked%22%3Afalse%2C%22isClicked%22%3Afalse%7D',
        'head-banner': '%7B%22closingCounter%22%3A0%2C%22showingCounter%22%3A526%2C%22shownAfterClicked%22%3Afalse%2C%22isClicked%22%3Afalse%7D; currentRegionId=213',
        'currentRegionName': '%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D1%83',
        'pof': '%7B%22clid%22%3A%5B%22505%22%5D%2C%22mclid%22%3Anull%2C%22distr_type%22%3Anull%2C%22vid%22%3Anull%2C%22opp%22%3Anull%7D',
        'cpa': '%7B%22clid%22%3A%5B%22505%22%5D%2C%22mclid%22%3Anull%2C%22distr_type%22%3Anull%2C%22vid%22%3Anull%2C%22opp%22%3Anull%7D; visits=1569848974-1569848974-1569848974; parent_reqid_seq=d42a92a5871ff61374b913eb3f4ccf8f%2Cce5b53e8a009fae941bde9127ffccf95%2C07c761fd008a9de5656c84921bf0aa02; utm_campaign=face_abovesearch',
        'utm_source': 'face_abovesearch',
        'uid': 'AABbhl2R/o6riwEABZ1KAg==',
        'js': '1',
        'first_visit_time': '2019-09-30T16%3A09%3A25%2B03%3A00',
        'HISTORY_UNAUTH_SESSION': 'true',
        'fonts-loaded': '1',
        'ugcp': '1',
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

    # Число на плашке 'цены' (Количество предложений) span class
    span_offers = 'n-product-tabs__count'

    # Плашка 'характеристики' в серой табличке на странице модели li class
    li_spec = 'n-product-tabs__item n-product-tabs__item_name_spec'

    # Максимальная и минимальная цена в блоке "средняя цена" на странице модели div class
    div_price_minmax = '_1S8ob0AgBK'

    # Средняя цена в блоке "средняя цена" на странице модели div class
    div_price_avg = '_3TkwCtZtaF'

    # Цена из верхного блока если цена только одна div
    div_price_alone = 'n-product-price-cpa2__price'

    # Таблица с ценами на очередной странице выдачи внутри предложений модели div class
    div_config_prices_table = 'n-snippet-list n-snippet-list_type_vertical island metrika b-zone b-spy-init b-spy-events i-bem'

    # Таблица характеристик (ТТХ) на странице Харктистик модели
    div_ttx_table = 'layout__col layout__col_size_p75 n-product-spec-wrap'

    #Название характеристики (ТТХ) на странице Харктистик модели
    span_spec_name = 'n-product-spec__name-inner'

    # Значение характеристики (ТТХ) на странице Харктистик модели
    span_spec_value = 'n-product-spec__value-inner'



    def header_(self, referer):
        header = {
            'Referer': referer,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        }

        return header


class Parse(Yama_parsing_const):

    def __init__(self):
        self.Categories = {
            'Ноутбук': {
                'url': 'https://market.yandex.ru/catalog--noutbuki/54544/list?hid=91013',
                'category': ['Ноутбук']
            },
            'Монитор': {
                'url': 'https://market.yandex.ru/catalog--monitory/54539/list?hid=91052',
                'category': ['Монитор']
            },
            'Проектор': {
                'url': 'https://market.yandex.ru/catalog--multimedia-proektory/60865/list?hid=191219',
                'category': ['Проектор']
            },
            'ИБП': {
                'url': 'https://market.yandex.ru/catalog--istochniki-bespereboinogo-pitaniia/59604/list?hid=91082',
                'category': ['Интерактивный ИБП',
                             'Резервный ИБП',
                             'ИБП с двойным преобразованием'
                             ]
            }
        }

    #скачивание линков на страницы модели по категории
    def parse_links(self, category):

        url = self.Categories[category]['url']
        category_ls = self.Categories[category]['category']

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

            response = requests.get(page_url, headers=self.header_(referer_), cookies=self.ya_cookies)

            if response.status_code == 200:
                print('поехали ', page_url)
                iter_page_soup = BeautifulSoup(response.text, 'html.parser')

                # Проверяем не последняя ли страница выдачи
                if iter_page_soup.find('a', class_=self.a_button_eol) is None:
                    pages_full = False

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

                    page += 1

                else:
                    capcha_quest = iter_page_soup.find('title')

                    if capcha_quest.text == 'ÐÐ¹!':
                        print(page, 'облом - капча')
                        time.sleep(1)
                    else:
                        print(page, 'фигня какая-то')
                        break

                time.sleep(2)


            else:
                print('облом... ', response.status_code)


        return models_list

    #запихиваем линки на модели в эксель
    def links_to_excel(self, category, folder='Price_link_list/'):

        parsed_links__ls = self.parse_links(category)
        print(len(parsed_links__ls))
        df = pd.DataFrame(parsed_links__ls)
        df.drop_duplicates(subset=['Name'], inplace=True)
        print(len(df))

        now = datetime.now().strftime('%b-%y----%d--%H-%M')
        excel_file_name = folder + 'Cсылки ' + category + ' ' + now + '.xlsx'

        df.to_excel(excel_file_name)

    # Забор списка цен из предложений
    def offers_prices_harvest(self, offers_href, ref_href):

        prices_list = list()

        page_href = offers_href
        new_ref_href = ref_href

        pages_is_ok = True
        page = 1

        while pages_is_ok == True:
            try:
                offers_response = requests.get(page_href,
                                               headers=self.header_(new_ref_href),
                                               cookies=self.ya_cookies)
                if offers_response.status_code == 200:
                    offers_page = BeautifulSoup(offers_response.text, 'html.parser')
                    if offers_page.find('a', class_=self.a_button_eol) is None:
                        pages_is_ok = False

                    offers_page_table = offers_page.find('div', class_=self.div_config_prices_table)

                    page_prices = offers_page_table.find_all('div', class_='price')

                    page_price_list = [int(i.text.replace(' ', '').replace('₽', '')) for i in page_prices]
                    #print(page_price_list)

                    prices_list += page_price_list

                else:
                    print("status code: ", offers_response.status_code)

            except Exception as Err:
                print(Err)

            page += 1
            new_ref_href = page_href
            page_href = offers_href + '&page=' + str(page)

        return prices_list

    # Сбор всех ТТХ
    def ttx_harvest(self, ttx_href, ref_href):

        ttx_dict = dict()

        try:
            response = requests.get(ttx_href, headers=self.header_(ref_href), cookies=self.ya_cookies)
            if response.status_code - - 200:
                page = BeautifulSoup(response.text, 'html.parser')
            # вся таблица характеристик
            ttx_table = page.find('div', class_=self.div_ttx_table)
            ttx_table_rows = ttx_table.find_all('dl', class_='n-product-spec')

            for dl in ttx_table_rows:
                dl_name = dl.find('span', class_=self.span_spec_name).text
                spec_value = dl.find('span', class_=self.span_spec_value).text
                # Забираем только самые полные характеристики в случае дубляжа ТТХ в таблице
                wth = ttx_dict.setdefault(dl_name, spec_value)
                if wth != spec_value:
                    if len(wth) < len(spec_value):
                        ttx_dict[dl_name] = spec_value

        except Exception as Err_response:
            print(Err_response)

        return ttx_dict

    #скачивание всех данных по моделям из файла линков
    def links_df_read_excel(self, links_filename):

        links_df = pd.read_excel(links_filename)
        return links_df

    #Основная функция парсинга моделей
    def parse_prices_with_all_ttx(self, links_df):

        df = links_df[['Name', 'Vendor', 'Category']]
        df.loc['Quantaty'] = None
        #df_no_ttx_columns = {'Name', 'Vendor', 'Category', 'Quantaty', 'MinPrice', 'MaxPrice', 'AvgPrice'}

        for i, row_df in links_df.iterrows():

            try:
                response = requests.get(self.host + row_df['Href'],
                                        headers=self.header_(self.host +
                                                                   '?text=' +
                                                                   quote(row_df['Name']) +
                                                                   self.link_tail),
                                        cookies=self.ya_cookies)
                if response.status_code == 200:

                    page = BeautifulSoup(response.text, 'html.parser')
                    title = page.find('title')

                    if row_df['Name'] in title.text:

                        # Табличка верхняя серая
                        table_grey = page.find('ul', class_=self.ul_table_gray)

                        # Плашка `Цены`
                        prices_count_cell = table_grey.find('li', class_=self.li_offers)

                        # Плашка `Характеристики`
                        spec_cell = table_grey.find('li', class_=self.li_spec)

                        # Количество цен (предложений)
                        if prices_count_cell.find('span', class_=self.span_offers) is not None:
                            df.loc[i, 'Quantaty'] = int(prices_count_cell.find('span', class_=self.span_offers).text)
                        else:
                            df.loc[i, 'Quantaty'] = 0

                        # Цены Средняя, минимум, максимум со страницы модели в боттоме
                        # Средняя _3TkwCtZtaF Мин/Макс _1S8ob0AgBK

                        if df.loc[i]['Quantaty'] > 2:

                            # а есть ли боттом c ценами?
                            teg_h2 = page.find_all('h2')
                            teg_h2_texts = [i.text for i in teg_h2]

                            if 'Средняя цена' in teg_h2_texts:
                                #Если блок средней цены на странице модели есть

                                margin_prices = page.find('div', class_=self.div_price_minmax).text
                                margin_prices = margin_prices.replace(' ', '')
                                margin_prices = margin_prices.replace('₽', '')
                                defiss = margin_prices.find('—')

                                df.loc[i, 'MinPrice'] = margin_prices[:defiss]
                                df.loc[i, 'MaxPrice'] = margin_prices[defiss + 1:]

                                avg_price = page.find('div', class_=self.div_price_avg)
                                df.loc[i, 'AvgPrice'] = int(avg_price.find('span').text.replace(' ', '').replace('₽', ''))
                            else:
                                # тады лезем внутря в список цен, руками:
                                offers_href = self.host + str(prices_count_cell.find('a').get('href'))
                                ref_href = self.host + row_df['Href']
                                offers_price_list = pd.Series(
                                    self.offers_prices_harvest(offers_href, ref_href))
                                df.loc[i, 'AvgPrice'] = offers_price_list.mean()
                                df.loc[i, 'MinPrice'] = offers_price_list.min()
                                df.loc[i, 'MaxPrice'] = offers_price_list.max()
                        else:
                            # если одно предложение (цена) только одна или нет предложений
                            avg_price = page.find('div', class_=self.div_price_alone)
                            if avg_price is not None:
                                df.loc[i, 'AvgPrice'] = int(
                                    avg_price.find('span', class_='price').text.replace(' ', '').replace('₽', ''))
                            else:
                                df.loc[i, 'AvgPrice'] = 'na'


                        # ТТХ (все)
                        try:  # на случай если ссылки на характеристики нет
                            ttx_link = str(spec_cell.find('a').get('href'))

                            ttx_href = self.host + ttx_link
                            ref_href = self.host + row_df['Href']

                            ttx_dict = self.ttx_harvest(ttx_href, ref_href)

                            new_ttx__set = set(ttx_dict.keys()) - set(df.columns)
                            for new in new_ttx__set:
                                df[new] = None
                            df.loc[i, list(ttx_dict.keys())] = pd.Series(ttx_dict)



                        except AttributeError as Err_ttx:
                            print(Err_ttx)

                    elif title.text == 'ÐÐ¹!':
                        print('Облом: капча. Пропускаем')

                    else:
                        print('Еще чета не так')

            except Exception as Err:
                print(Err)
            print(df.loc[i])
        return df

    #Вызывная функция парсинга
    def prices_to_excel(self, links_filename, links_folder='Price_link_list/', price_folder='Prices/'):
        df = self.parse_prices_with_all_ttx(self.links_df_read_excel(links_folder + links_filename))

        now = datetime.now().strftime('%b-%y----%d--%H-%M')
        category = df.iloc[0]['Category']

        exit_filename = price_folder + category + '-Цены-от-' + now + '.xlsx'
        df.to_excel(exit_filename)

    def no_prices_reparse(self, price_filename, links_filename,
                          price_folder='Prices/', links_folder='Price_link_list/'):
        pass















