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

# class Parse_Modifications_TTX_Mod_in_Prices(Yama_parsing_const):
#
#     def __init__(self,
#                  category,
#                  links_file,
#                  ttx_name=False, # Надо ли считывать TTX Модели
#                  ):

#def main(self,
#           step=10, По сколько моделей вурхнего уровня записывать в файл
#           start=0, С какой строчки начинать
#           num=""):, Номер в имени выходного файла прайсов и прайсов модификаций


#parse = pynd.Parse_Modifications_TTX_Mod_in_Prices('Ноутбук', 'Cсылки Ноутбук Sep-20----2.xlsx', ttx_name=True).main(start=0, num=2)
#parse = pynd.Parse_Modifications_TTX_selenium_fix('Монитор', 'Cсылки Монитор Sep-20----2.xlsx', mod=False, ttx_name=True, ttx_mod=False).main(start=0, num=2)
#parse = pynd.Parse_Modifications_TTX_selenium_fix('Проектор', 'Cсылки Проектор Sep-20----18--14-35.xlsx', mod=False, ttx_name=True, ttx_mod=False).main(start=0, num=1)
parse = pynd.Parse_Modifications_TTX_selenium_fix('ИБП', 'Cсылки ИБП Sep-20----18--14-37.xlsx', mod=False, ttx_name=True, ttx_mod=False).main(start=0, num=1)








