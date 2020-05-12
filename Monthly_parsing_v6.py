import parse_yama as pynd

# Сначала скачиваются линки для категории. Class Parce_links
# Затем качаются прайсы и обновления TTX. Class Parse_models_ttx()
# Если есть дырки в файле прасов то вызывается перепроход функцией no_prices_reparse


#parse_link = pynd.Parse_links()
#parse_link.links_to_excel('Ноутбук')
#parse_link.links_to_excel('Монитор')
#parse_link.links_to_excel('Проектор')
#parse_link.links_to_excel('ИБП')

#parse_category = pynd.Parse_models()

#parse_category.prices_to_excel('Cсылки Монитор Feb-20----16--18-37.xlsx')
#parse_category.prices_to_excel('Cсылки ИБП Feb-20----16--19-02.xlsx')
#parse_category.prices_to_excel('Cсылки Проектор Feb-20----16--18-41.xlsx')




#parse.prices_to_excel('Монитор', 'Cсылки Монитор Apr-20----16--15-00.xlsx')
#parse.prices_to_excel('Проектор', 'Cсылки Проектор Apr-20----16--15-02.xlsx')
#parse.prices_to_excel('ИБП', 'Cсылки ИБП Apr-20----16--15-05.xlsx')

#parse_category = pynd.Parse_models()
#parse_category.no_prices_reparse('Ноутбук-Цены-от-Mar-20----17--13-06.xlsx', 'Cсылки Ноутбук Mar-20----16--19-08.xlsx')

#class Parse_Modifications_TTX(Yama_parsing_const):
#    def __init__(self,
#                 category,
#                 links_file,
#                 mod=True, # Надо ли считывать модификации
#                 ttx_name=False, # Надо ли считывать TTX Модели
#                 ttx_mod = True # Надо ли считывать TTX Модификаций
#                 ):

#def main(self,
#           step=100, По сколько моделей вурхнего уровня записывать в файл
#           num=""):, Номер в имени выходного файла прайсов и прайсов модификаций


parse = pynd.Parse_Modifications_TTX('Ноутбук',
                                     'Cсылки Ноутбук May-20--restrict-1.xlsx',
                                     ).main(num=6)









