#import parse_yama_esport as pynd
import parse_yama as pynd

# Сначала скачиваются линки для категории. Class Parce_links
# Затем качаются прайсы и обновления TTX. Class Parse_models_ttx()
# Если есть дырки в файле прасов то вызывается перепроход функцией no_prices_reparse


#parse_link = pynd.Parse_links()
#parse_link.links_to_excel('Ноутбук')
#parse_link.links_to_excel('Монитор')
#parse_link.links_to_excel('Проектор')
#parse_link.links_to_excel('ИБП')


# Херачит отдельно по вендорам
# Убрать из xls - /offer/, //Market-clik
# 'vendors': ['Acer', 'Alienware','Apple', 'Asus', 'Dell', 'Honor', 'HP','Lenovo', 'MSI', 'Huawei']
# 'vendors': ['Acer','AOC','Asus','BenQ','Dell','HP', 'Iiyama', 'LG', 'Philips', 'Samsung', 'Viewsonic', 'Lenovo', 'MSI','NEC', 'Xiaomi','Gigabyte']
# 'vendors': ['Acer','BenQ','Epson','Infocus','LG','NEC','Optoma','Sony','Viewsonic','Xiaomi','Barco','Canon','Casio','Christie','Hiper ','Hitachi','JVC','Panasonic',
#             'Ricoh','Smart','Vivitek']
# 'vendors': ['APC','Eaton','Ippon','Delta','Cyberpower','Powercom','Vertiv','SI','Huawei','Powerman','Impuls','Eltena-Inelt','Legrand','Socomec','Riello','Maklesan',
#             'GE','DKC','Tripp Lite','AEG','Irbis','Sven','Hiper']

# parse_link.links_to_excel('Ноутбук', vendors_list=[])

#parse_link = pynd.Parse_links_v3(page_max=20)
#parse_link.links_to_excel('Ноутбук', vendors_list=[])
#parse_link.links_to_excel('Монитор', vendors_list=['BenQ'])
#parse_link.links_to_excel('Проектор', vendors_list=['Infocus', 'NEC', 'Canon','Casio','Christie','Hiper ','Hitachi','JVC','Panasonic', 'Ricoh','Smart','Vivitek'])
#parse_link.links_to_excel('ИБП', vendors_list=['Ippon', 'Huawei', 'Legrand'])


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

#Прерывание (пустые данные). Надо докачивать с позици номер строки последнего по Excel -1
parse = pynd.Parse_Modifications_TTX_selenium_fix('Ноутбук', 'Cсылки Ноутбук Apr-22----04--17-12.xlsx', mod=False, ttx_name=False, ttx_mod=False, capcha_loc=True).\
    main(start=3230, num=6, step=500)
# parse = pynd.Parse_Modifications_TTX_selenium_fix('Монитор', 'Cсылки Монитор Mar-22----11--final.xlsx', mod=False, ttx_name=False, ttx_mod=False, capcha_loc=True).\
#        main(start=464, num=1 , step=500)
# parse = pynd.Parse_Modifications_TTX_selenium_fix('Проектор', 'Cсылки Проектор Mar-22----16--final.xlsx', mod=False, ttx_name=False, ttx_mod=False, capcha_loc=True).\
#      main(start=0, num=0, step=500)
# parse = pynd.Parse_Modifications_TTX_selenium_fix('ИБП', 'Cсылки ИБП Feb-22----final.xlsx', mod=False, ttx_name=False, ttx_mod=False, capcha_loc=True).\
#    main(start=0, num=0, step=500)

#parse = pynd.Parse_Modifications_TTX_selenium_fix('Электросамока т', '', mod=False, ttx_name=True, ttx_mod=False).\
#     main(start=0, num=1, step=500)









